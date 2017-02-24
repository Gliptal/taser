from xml.dom.minidom import parseString as parse_string

from dicttoxml import dicttoxml as dict_to_xml

import args
import data
import calc


def generate():
    template = data.load("data/template.yaml")

    target_altitude = calc.ft_to_m(args.TARGET["altitude"])
    if args.ATTACK_HDG is None:
        attack_heading = calc.reverse_heading(calc.thdg_to_mhdg(args.TARGET["heading"]))
    else:
        attack_heading = calc.reverse_heading(args.ATTACK_HDG)

    wire_length = calc.hypotenuse_from_catheti(args.BASE_DIST, args.BASE_ALT-target_altitude)
    wire_angle = calc.angle_from_catheti(args.BASE_ALT, args.BASE_DIST)
    wire_entry_width = calc.sin_cathetus_from_angle(wire_length, args.LEEWAY_HDG)

    floor_lat, floor_lon = calc.shift_coords(args.TARGET["position"], args.BASE_DIST*0.3, -attack_heading)
    abort_lat, abort_lon = floor_lat, floor_lon
    release_lat, release_lon = calc.shift_coords(args.TARGET["position"], calc.cos_cathetus_from_angle(args.RELEASE_ALT-target_altitude, wire_angle), -attack_heading)
    track_lat, track_lon = calc.shift_coords(args.TARGET["position"], calc.cos_cathetus_from_angle(args.TRACK_ALT-target_altitude, wire_angle), -attack_heading)

    floor_altitude = args.FLOOR_ALT/2
    abort_altitude = args.FLOOR_ALT+((args.ABORT_ALT-args.FLOOR_ALT)/2)
    release_altitude = args.RELEASE_ALT
    track_altitude = args.TRACK_ALT

    floor_width = wire_entry_width/2
    abort_width = floor_width
    release_width = wire_entry_width/1.5
    track_width = release_width

    floor_length = args.BASE_DIST
    abort_length = floor_length
    release_length = args.BASE_DIST*0.5
    track_length = release_length

    template[0]["Position"]["Latitude"] = args.TARGET["position"]["latitude"]
    template[0]["Position"]["Longitude"] = args.TARGET["position"]["longitude"]
    template[0]["Position"]["Altitude"] = target_altitude
    template[0]["Orientation"]["Pitch"] = wire_angle
    template[0]["Orientation"]["Yaw"] = attack_heading
    template[0]["Size"]["Width"] = wire_entry_width
    template[0]["Size"]["Length"] = wire_length
    template[0]["Size"]["Height"] = args.LEEWAY_ALT*2

    template[1]["Position"]["Latitude"] = floor_lat
    template[1]["Position"]["Longitude"] = floor_lon
    template[1]["Position"]["Altitude"] = floor_altitude
    template[1]["Orientation"]["Yaw"] = attack_heading
    template[1]["Size"]["Width"] = floor_width
    template[1]["Size"]["Length"] = floor_length
    template[1]["Size"]["Height"] = args.FLOOR_ALT

    template[2]["Position"]["Latitude"] = abort_lat
    template[2]["Position"]["Longitude"] = abort_lon
    template[2]["Position"]["Altitude"] = abort_altitude
    template[2]["Orientation"]["Yaw"] = attack_heading
    template[2]["Size"]["Width"] = abort_width
    template[2]["Size"]["Length"] = abort_length
    template[2]["Size"]["Height"] = args.ABORT_ALT-args.FLOOR_ALT

    template[3]["Position"]["Latitude"] = release_lat
    template[3]["Position"]["Longitude"] = release_lon
    template[3]["Position"]["Altitude"] = release_altitude
    template[3]["Orientation"]["Yaw"] = attack_heading
    template[3]["Size"]["Width"] = release_width
    template[3]["Size"]["Length"] = release_length
    template[3]["Size"]["Height"] = args.LEEWAY_ALT*2

    template[4]["Position"]["Latitude"] = track_lat
    template[4]["Position"]["Longitude"] = track_lon
    template[4]["Position"]["Altitude"] = track_altitude
    template[4]["Orientation"]["Yaw"] = attack_heading
    template[4]["Size"]["Width"] = track_width
    template[4]["Size"]["Length"] = track_length
    template[4]["Size"]["Height"] = args.LEEWAY_ALT*2

    _dict_to_file(template)

def _dict_to_file(tree):
    xml_string = dict_to_xml(tree, attr_type=False, custom_root="Objects", item_func=lambda p: "Object")
    xml_dom = parse_string(xml_string)

    output_file = open(args.FILE+".xml", "w+")
    output_file.write(xml_dom.toprettyxml())
    output_file.close()
