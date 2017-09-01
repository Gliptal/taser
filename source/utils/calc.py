import geopy
import geopy.distance
import math
import re


def ft_to_m(ft):
    return ft*0.3048


def thdg_to_mhdg(thdg):
    return thdg+11


def hdg_to_ohdg(hdg):
    return (hdg+180) % 360


def hl_to_w(h, l):
    return math.hypot(h, l)


def hl_to_a(h, l):
    return math.degrees(math.atan(h/l))


def la_to_h(l, a):
    return l*math.tan(math.radians(a))


def ha_to_l(h, a):
    return h/math.tan(math.radians(a))


def shift_coords(lat, lon, dist, hdg):
    lat = _dms_to_dd(lat)
    lon = _dms_to_dd(lon)

    origin = geopy.Point(lat, lon)
    shifted = geopy.distance.VincentyDistance(kilometers=dist/1000).destination(origin, hdg)

    return _dd_to_dms(shifted.latitude)+"N", _dd_to_dms(shifted.longitude)+"W"


def _dms_to_dd(dms):
    parts = re.split('[.°\'"]+', dms.replace("Â", ""))
    dd = float(parts[0]) + float(parts[1])/60 + float(parts[2])/(60*60)

    return dd


def _dd_to_dms(dd):
    mnt, sec = divmod(dd*60*60, 60)
    deg, mnt = divmod(mnt, 60)
    dms = str(int(deg)) + "Â°" + str(int(mnt)) + "'" + str(int(sec)) + "\""

    return dms
