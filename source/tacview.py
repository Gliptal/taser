from xml.dom.minidom import parseString as parse_string

from dicttoxml import dicttoxml as dict_to_xml

import args
import data
import calc


def generate():
    template = data.load("data/template.yaml")

    target_altitude = calc.ft_to_m(args.TARGET["altitude"])
    base_altitude = args.BASE_ALT-target_altitude
    if args.ATTACK_HDG is None:
        attack_heading = calc.reverse_heading(calc.thdg_to_mhdg(args.TARGET["heading"]))
    else:
        attack_heading = calc.reverse_heading(args.ATTACK_HDG)
    aimdist_lat, aimdist_lon = calc.shift_coords(args.TARGET["position"]["latitude"], args.TARGET["position"]["longitude"], args.AIM_DIST, -calc.reverse_heading(attack_heading))

    wire_length = calc.hypotenuse_from_catheti(args.BASE_DIST, base_altitude)
    wire_angle = calc.angle_from_catheti(base_altitude, args.BASE_DIST)
    wire_entry_width = calc.sin_cathetus_from_angle(wire_length, args.LEEWAY_HDG)
    wire_height = args.LEEWAY_ALT*2

    min_lat, min_lon = calc.shift_coords(aimdist_lat, aimdist_lon, args.BASE_DIST*0.3, -attack_heading)
    abort_lat, abort_lon = min_lat, min_lon
    release_lat, release_lon = calc.shift_coords(aimdist_lat, aimdist_lon, calc.cos_cathetus_from_angle(args.RELEASE_ALT-target_altitude, wire_angle), -attack_heading)
    track_lat, track_lon = calc.shift_coords(aimdist_lat, aimdist_lon, calc.cos_cathetus_from_angle(args.TRACK_ALT-target_altitude, wire_angle), -attack_heading)

    if args.DECLUTTER:
        min_altitude = args.MIN_ALT
        abort_altitude = args.ABORT_ALT
    else:
        min_altitude = args.MIN_ALT/2
        abort_altitude = args.MIN_ALT+((args.ABORT_ALT-args.MIN_ALT)/2)
    release_altitude = args.RELEASE_ALT
    track_altitude = args.TRACK_ALT

    min_width = wire_entry_width
    abort_width = min_width
    release_width = wire_entry_width
    track_width = release_width

    min_length = args.BASE_DIST
    abort_length = min_length
    release_length = args.BASE_DIST*0.5
    track_length = release_length

    if args.DECLUTTER:
        min_height = 1
        abort_height = 1
    else:
        min_height = args.MIN_ALT
        abort_height = args.ABORT_ALT-args.MIN_ALT
    release_height = args.LEEWAY_ALT*2
    track_height = args.LEEWAY_ALT*2

    template[0]["Position"]["Latitude"] = aimdist_lat
    template[0]["Position"]["Longitude"] = aimdist_lon
    template[0]["Position"]["Altitude"] = target_altitude
    template[0]["Orientation"]["Pitch"] = wire_angle
    template[0]["Orientation"]["Yaw"] = attack_heading
    template[0]["Size"]["Width"] = wire_entry_width
    template[0]["Size"]["Length"] = wire_length
    template[0]["Size"]["Height"] = wire_height

    template[1]["Position"]["Latitude"] = min_lat
    template[1]["Position"]["Longitude"] = min_lon
    template[1]["Position"]["Altitude"] = min_altitude
    template[1]["Orientation"]["Yaw"] = attack_heading
    template[1]["Size"]["Width"] = min_width
    template[1]["Size"]["Length"] = min_length
    template[1]["Size"]["Height"] = min_height

    template[2]["Position"]["Latitude"] = abort_lat
    template[2]["Position"]["Longitude"] = abort_lon
    template[2]["Position"]["Altitude"] = abort_altitude
    template[2]["Orientation"]["Yaw"] = attack_heading
    template[2]["Size"]["Width"] = abort_width
    template[2]["Size"]["Length"] = abort_length
    template[2]["Size"]["Height"] = abort_height

    template[3]["Position"]["Latitude"] = release_lat
    template[3]["Position"]["Longitude"] = release_lon
    template[3]["Position"]["Altitude"] = release_altitude
    template[3]["Orientation"]["Yaw"] = attack_heading
    template[3]["Size"]["Width"] = release_width
    template[3]["Size"]["Length"] = release_length
    template[3]["Size"]["Height"] = release_height

    template[4]["Position"]["Latitude"] = track_lat
    template[4]["Position"]["Longitude"] = track_lon
    template[4]["Position"]["Altitude"] = track_altitude
    template[4]["Orientation"]["Yaw"] = attack_heading
    template[4]["Size"]["Width"] = track_width
    template[4]["Size"]["Length"] = track_length
    template[4]["Size"]["Height"] = track_height

    _dict_to_file(template)

def _dict_to_file(tree):
    xml_string = dict_to_xml(tree, attr_type=False, custom_root="Objects", item_func=lambda p: "Object")
    xml_dom = parse_string(xml_string)

    output_file = open(args.FILE+".xml", "w+")
    output_file.write(xml_dom.toprettyxml())
    output_file.close()
