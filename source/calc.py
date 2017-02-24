import geopy
from geopy.distance import distance, VincentyDistance
import math
import re

def ft_to_m(ft):
    return ft*0.3048

def thdg_to_mhdg(thdg):
    return thdg

def reverse_heading(hdg):
    return (hdg+180) % 360

def hypotenuse_from_catheti(h, l):
    return math.sqrt((l**2)+(h**2))

def angle_from_catheti(h, l):
    return math.degrees(math.atan(h/l))

def sin_cathetus_from_angle(l, a):
    return l*math.tan(math.radians(a))

def cos_cathetus_from_angle(h, a):
    return h/math.tan(math.radians(a))

def shift_coords(coords, dist, hdg):
    lat = _dms_to_dd(coords["latitude"])
    lon = _dms_to_dd(coords["longitude"])

    origin = geopy.Point(lat, lon)
    destination = geopy.distance.VincentyDistance(kilometers=dist/1000).destination(origin, hdg)

    return _dd_to_dms(destination.latitude)+"N", _dd_to_dms(destination.longitude)+"W"

def _dms_to_dd(dms):
    parts = re.split('[°\'"]+', dms.replace("Â", ""))
    dd = float(parts[0])+float(parts[1])/60+float(parts[2])/(60*60)

    return dd

def _dd_to_dms(dd):
    mnt, sec = divmod(dd*60*60, 60)
    deg, mnt = divmod(mnt, 60)
    dms = str(int(deg))+"Â°"+str(int(mnt))+"'"+str(int(sec))+"\""

    return dms
