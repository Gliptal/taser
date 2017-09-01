from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

import args
import utils


def generate():
    template = utils.data.load("data/template.yaml")

    if args.MAIN.MODE == "range":
        target_altitude = utils.calc.ft_to_m(args.TARGET.TARGET["altitude"])
    elif args.MAIN.MODE == "coords":
        target_altitude = utils.calc.ft_to_m(args.TARGET.ALTITUDE)
    base_altitude   = args.SLED.BASE_ALT-target_altitude
    if args.WIRE.ATTACK_HDG is not None:
        attack_heading = utils.calc.hdg_to_ohdg(args.WIRE.ATTACK_HDG)
    else:
        if args.MAIN.MODE == "range":
            attack_heading = utils.calc.hdg_to_ohdg(utils.calc.thdg_to_mhdg(args.TARGET.TARGET["heading"]))
        elif args.MAIN.MODE == "coords":
            attack_heading = utils.calc.hdg_to_ohdg(utils.calc.thdg_to_mhdg(0))

    wire_length = utils.calc.hl_to_w(args.SLED.BASE_DIST, base_altitude)
    wire_angle  = utils.calc.hl_to_a(base_altitude, args.SLED.BASE_DIST)
    wire_width  = utils.calc.la_to_h(wire_length, args.WIRE.LEEWAY_HDG)
    wire_height = args.WIRE.LEEWAY_ALT*2

    if args.MAIN.MODE == "range":
        aimdist_lat, aimdist_lon = utils.calc.shift_coords(args.TARGET.TARGET["position"]["latitude"], args.TARGET.TARGET["position"]["longitude"], args.SLED.AIM_DIST, -utils.calc.hdg_to_ohdg(attack_heading))
    elif args.MAIN.MODE == "coords":
        aimdist_lat, aimdist_lon = utils.calc.shift_coords(args.TARGET.COORD_LAT, args.TARGET.COORD_LON, args.SLED.AIM_DIST, -utils.calc.hdg_to_ohdg(attack_heading))
    min_lat,     min_lon     = utils.calc.shift_coords(aimdist_lat, aimdist_lon, args.SLED.BASE_DIST*0.3, -attack_heading)
    abort_lat,   abort_lon   = min_lat, min_lon
    release_lat, release_lon = utils.calc.shift_coords(aimdist_lat, aimdist_lon, utils.calc.ha_to_l(args.SLED.RELEASE_ALT-target_altitude, wire_angle), -attack_heading)
    track_lat,   track_lon   = utils.calc.shift_coords(aimdist_lat, aimdist_lon, utils.calc.ha_to_l(args.SLED.TRACK_ALT-target_altitude, wire_angle),   -attack_heading)

    if args.MAIN.DECLUTTER:
        min_altitude   = args.SLED.MIN_ALT
        abort_altitude = args.SLED.ABORT_ALT
    else:
        min_altitude   = args.SLED.MIN_ALT/2
        abort_altitude = args.SLED.MIN_ALT+((args.SLED.ABORT_ALT-args.SLED.MIN_ALT)/2)
    release_altitude = args.SLED.RELEASE_ALT
    track_altitude   = args.SLED.TRACK_ALT

    min_width     = wire_width
    abort_width   = wire_width
    release_width = wire_width
    track_width   = wire_width

    min_length     = args.SLED.BASE_DIST
    abort_length   = min_length
    release_length = args.SLED.BASE_DIST*0.5
    track_length   = release_length

    if args.MAIN.DECLUTTER:
        min_height   = 1
        abort_height = 1
    else:
        min_height   = args.SLED.MIN_ALT
        abort_height = args.SLED.ABORT_ALT-args.SLED.MIN_ALT
    release_height = args.WIRE.LEEWAY_ALT*2
    track_height   = args.WIRE.LEEWAY_ALT*2

    template[0]["Position"]["Latitude"]  = aimdist_lat
    template[0]["Position"]["Longitude"] = aimdist_lon
    template[0]["Position"]["Altitude"]  = target_altitude
    template[0]["Orientation"]["Pitch"]  = wire_angle
    template[0]["Orientation"]["Yaw"]    = attack_heading
    template[0]["Size"]["Width"]         = wire_width
    template[0]["Size"]["Length"]        = wire_length
    template[0]["Size"]["Height"]        = wire_height

    template[1]["Position"]["Latitude"]  = min_lat
    template[1]["Position"]["Longitude"] = min_lon
    template[1]["Position"]["Altitude"]  = min_altitude
    template[1]["Orientation"]["Yaw"]    = attack_heading
    template[1]["Size"]["Width"]         = min_width
    template[1]["Size"]["Length"]        = min_length
    template[1]["Size"]["Height"]        = min_height

    template[2]["Position"]["Latitude"]  = abort_lat
    template[2]["Position"]["Longitude"] = abort_lon
    template[2]["Position"]["Altitude"]  = abort_altitude
    template[2]["Orientation"]["Yaw"]    = attack_heading
    template[2]["Size"]["Width"]         = abort_width
    template[2]["Size"]["Length"]        = abort_length
    template[2]["Size"]["Height"]        = abort_height

    template[3]["Position"]["Latitude"]  = release_lat
    template[3]["Position"]["Longitude"] = release_lon
    template[3]["Position"]["Altitude"]  = release_altitude
    template[3]["Orientation"]["Yaw"]    = attack_heading
    template[3]["Size"]["Width"]         = release_width
    template[3]["Size"]["Length"]        = release_length
    template[3]["Size"]["Height"]        = release_height

    template[4]["Position"]["Latitude"]  = track_lat
    template[4]["Position"]["Longitude"] = track_lon
    template[4]["Position"]["Altitude"]  = track_altitude
    template[4]["Orientation"]["Yaw"]    = attack_heading
    template[4]["Size"]["Width"]         = track_width
    template[4]["Size"]["Length"]        = track_length
    template[4]["Size"]["Height"]        = track_height

    _dict_to_file(template)


def _dict_to_file(tree):
    xml_string = dicttoxml(tree, attr_type=False, custom_root="Objects", item_func=lambda p: "Object")
    xml_dom = parseString(xml_string)

    utils.data.save(args.MAIN.FILENAME, xml_dom.toprettyxml())
