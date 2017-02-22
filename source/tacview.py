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

    template["Object"]["Position"]["Latitude"] = target["position"]["latitude"]
    template["Object"]["Position"]["Longitude"] = target["position"]["longitude"]
    template["Object"]["Position"]["Altitude"] = target["altitude"]*0.3048
    template["Object"]["Orientation"]["Pitch"] = math.degrees(math.atan(args.ROLL/args.BASE))
    template["Object"]["Orientation"]["Yaw"] = (target["heading"]+180) % 360
    template["Object"]["Size"]["Width"] = 463
    template["Object"]["Size"]["Length"] = math.sqrt((args.BASE**2)+(args.ROLL**2))
    template["Object"]["Size"]["Height"] = args.LEEWAY*2

    xml_string = dict_to_xml(template, attr_type=False, custom_root="Objects")
    xml_dom = parse_string(xml_string)

    output_file = open(args.OUT+".xml", "w+")
    output_file.write(xml_dom.toprettyxml())
