import math
from xml.dom.minidom import parseString as parse_string

from dicttoxml import dicttoxml as dict_to_xml

import args
import fileio


def generate():
    ranges = fileio.load_data("data/ranges.yaml")
    template = fileio.load_data("data/template.yaml")

    target = None
    for rng in ranges:
        if args.RANGE == rng["name"]:
            for tgt in rng["targets"]:
                if args.TARGET == tgt["name"]:
                    target = tgt

    template[0]["Position"]["Latitude"] = target["position"]["latitude"]
    template[0]["Position"]["Longitude"] = target["position"]["longitude"]
    template[0]["Position"]["Altitude"] = target["altitude"]*0.3048
    template[0]["Orientation"]["Pitch"] = math.degrees(math.atan(args.ROLL/args.BASE))
    template[0]["Orientation"]["Yaw"] = (target["heading"]+180) % 360
    template[0]["Size"]["Width"] = 926
    template[0]["Size"]["Length"] = math.sqrt((args.BASE**2)+((args.ROLL-target["altitude"]*0.3048)**2))
    template[0]["Size"]["Height"] = 413

    template[1]["Position"]["Latitude"] = target["position"]["latitude"]
    template[1]["Position"]["Longitude"] = target["position"]["longitude"]
    template[1]["Position"]["Altitude"] = 0+(args.FLOOR/2)
    template[1]["Orientation"]["Yaw"] = (target["heading"]+180) % 360
    template[1]["Size"]["Width"] = 1852
    template[1]["Size"]["Length"] = args.BASE*1.5
    template[1]["Size"]["Height"] = args.FLOOR

    template[2]["Position"]["Latitude"] = target["position"]["latitude"]
    template[2]["Position"]["Longitude"] = target["position"]["longitude"]
    template[2]["Position"]["Altitude"] = args.FLOOR+((args.ABORT-args.FLOOR)/2)
    template[2]["Orientation"]["Yaw"] = (target["heading"]+180) % 360
    template[2]["Size"]["Width"] = 1852
    template[2]["Size"]["Length"] = args.BASE*1.5
    template[2]["Size"]["Height"] = args.ABORT-args.FLOOR

    template[3]["Position"]["Latitude"] = target["position"]["latitude"]
    template[3]["Position"]["Longitude"] = target["position"]["longitude"]
    template[3]["Position"]["Altitude"] = args.PICKLE
    template[3]["Orientation"]["Yaw"] = (target["heading"]+180) % 360
    template[3]["Size"]["Width"] = 1852
    template[3]["Size"]["Length"] = args.BASE*1.5
    template[3]["Size"]["Height"] = args.LEEWAY*2

    template[4]["Position"]["Latitude"] = target["position"]["latitude"]
    template[4]["Position"]["Longitude"] = target["position"]["longitude"]
    template[4]["Position"]["Altitude"] = args.TRACK
    template[4]["Orientation"]["Yaw"] = (target["heading"]+180) % 360
    template[4]["Size"]["Width"] = 1852
    template[4]["Size"]["Length"] = args.BASE*1.5
    template[4]["Size"]["Height"] = args.LEEWAY*2

    xml_string = dict_to_xml(template, attr_type=False, custom_root="Objects", item_func=_itemize)
    xml_dom = parse_string(xml_string)

    output_file = open(args.FILE+".xml", "w+")
    output_file.write(xml_dom.toprettyxml())

def _itemize(parent):
    return "Object"
