import math
from xml.dom.minidom import parseString as parse_string

from dicttoxml import dicttoxml as dict_to_xml

import args
import data
import calc


def generate():
    template = data.load("data/template.yaml")

    target_altitude = calc.ft_to_m(args.TARGET["altitude"])
    attack_heading = calc.reverse_heading(args.TARGET["heading"])
    wire_length = calc.hypotenuse_from_catheti(args.BASE, args.ROLL-target_altitude)
    wire_entry_width = calc.cathetus_from_angle(wire_length, args.ENTRY)
    shifted_lat = calc.shift_coords(args.TARGET["position"], args.BASE*0.3, attack_heading)[0]+"N"
    shifted_lon = calc.shift_coords(args.TARGET["position"], args.BASE*0.3, attack_heading)[1]+"W"
    altitude_block_length = args.BASE*1.5

    template[0]["Position"]["Latitude"] = args.TARGET["position"]["latitude"]
    template[0]["Position"]["Longitude"] = args.TARGET["position"]["longitude"]
    template[0]["Position"]["Altitude"] = target_altitude
    template[0]["Orientation"]["Pitch"] = calc.angle_from_catheti(args.ROLL, args.BASE)
    template[0]["Orientation"]["Yaw"] = attack_heading
    template[0]["Size"]["Width"] = wire_entry_width
    template[0]["Size"]["Length"] = wire_length
    template[0]["Size"]["Height"] = args.LEEWAY*2

    template[1]["Position"]["Latitude"] = shifted_lat
    template[1]["Position"]["Longitude"] = shifted_lon
    template[1]["Position"]["Altitude"] = (args.FLOOR/2)
    template[1]["Orientation"]["Yaw"] = attack_heading
    template[1]["Size"]["Width"] = wire_entry_width/2
    template[1]["Size"]["Length"] = altitude_block_length
    template[1]["Size"]["Height"] = args.FLOOR

    template[2]["Position"]["Latitude"] = shifted_lat
    template[2]["Position"]["Longitude"] = shifted_lon
    template[2]["Position"]["Altitude"] = args.FLOOR+((args.ABORT-args.FLOOR)/2)
    template[2]["Orientation"]["Yaw"] = attack_heading
    template[2]["Size"]["Width"] = wire_entry_width/2
    template[2]["Size"]["Length"] = altitude_block_length
    template[2]["Size"]["Height"] = args.ABORT-args.FLOOR

    template[3]["Position"]["Latitude"] = shifted_lat
    template[3]["Position"]["Longitude"] = shifted_lon
    template[3]["Position"]["Altitude"] = args.PICKLE
    template[3]["Orientation"]["Yaw"] = attack_heading
    template[3]["Size"]["Width"] = wire_entry_width/2
    template[3]["Size"]["Length"] = altitude_block_length
    template[3]["Size"]["Height"] = args.LEEWAY*2

    template[4]["Position"]["Latitude"] = shifted_lat
    template[4]["Position"]["Longitude"] = shifted_lon
    template[4]["Position"]["Altitude"] = args.TRACK
    template[4]["Orientation"]["Yaw"] = attack_heading
    template[4]["Size"]["Width"] = wire_entry_width/2
    template[4]["Size"]["Length"] = altitude_block_length
    template[4]["Size"]["Height"] = args.LEEWAY*2

    _dict_to_file(template)

def _dict_to_file(tree):
    xml_string = dict_to_xml(tree, attr_type=False, custom_root="Objects", item_func=lambda p: "Object")
    xml_dom = parse_string(xml_string)

    output_file = open(args.FILE+".xml", "w+")
    output_file.write(xml_dom.toprettyxml())
    output_file.close()
