import math
import re

def ft_to_m(ft):
    return ft*0.3048

def hypotenuse_from_catheti(h, l):
    return math.sqrt((l**2)+(h**2))

def angle_from_catheti(h, l):
    return math.degrees(math.atan(h/l))

def cathetus_from_angle(l, a):
    return l*math.tan(math.radians(a))

def reverse_heading(hdg):
    return (hdg+180) % 360

def shift_coords(coords, dist, hdg):
    lat = _dms_to_dd(coords["latitude"])
    lon = _dms_to_dd(coords["longitude"])

    x = dist*math.cos(math.radians(hdg))
    y = dist*math.sin(math.radians(hdg))

    Dlat = x/6378137
    Dlon = y/(6378137*math.cos(math.radians(lat)))

    lat0 = lat+math.degrees(Dlat)
    lon0 = lon+math.degrees(Dlon)

    return _dd_to_dms(lat0), _dd_to_dms(lon0)

def _dms_to_dd(dms):
    parts = re.split('[°\'"]+', dms.replace("Â", ""))
    dd = float(parts[0])+float(parts[1])/60+float(parts[2])/(60*60)

    return dd

def _dd_to_dms(dd):
    mnt, sec = divmod(dd*60*60, 60)
    deg, mnt = divmod(mnt, 60)
    dms = str(int(deg))+"Â°"+str(int(mnt))+"'"+str(int(sec))+"\""

    return dms
