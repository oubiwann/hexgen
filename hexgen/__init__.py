import random

from hexgen.mapgen import MapGen
from hexgen.hex import HexFeature
from hexgen.constants import *
from hexgen.enums import GeoformType
from hexgen.draw import HexGridDraw

# @exec_time
def draw_grid(hex_grid):
    def color_heightmap(h):
        alt = int(h.altitude)
        return (alt, alt, alt)

    # make terrain map
    def color_terrain(h):
        return h.color_terrain

    def color_rivers(h):
        return h.color_rivers

    def color_temperature_end_year(h):
        return h.color_temperature[0]

    def color_temperature_mid_year(h):
        return h.color_temperature[1]

    def temperature_end_year(h):
        return h.temperature[0]

    def temperature_mid_year(h):
        return h.temperature[1]

    def color_biome(h):
        return h.color_biome

    def color_territories(h):
        return h.color_territories

    def color_satellite(h):
        return h.color_satellite

    def color_features(h):
        if h.has_feature(HexFeature.lava_flow):
            return (200, 100, 0)
        if h.has_feature(HexFeature.volcano):
            return (255, 0, 0)
        if h.has_feature(HexFeature.crater):
            return (255, 255, 0)
        return (200, 200, 200)

    def color_resources(h):
        if h.resource is not None:
            return h.resource.get('type').color
        return (100, 100, 100)

    def color_zone(h):
        return h.zone.color

    def key_zone(h):
        return h.zone.map_key

    def hex_latitude(h):
        return h.latitude

    def color_pressure_end_year(h):
        return h.color_pressure[0]

    def color_pressure_mid_year(h):
        return h.color_pressure[1]

    def pressure_number_end_year(h):
        return h.pressure[0]

    def pressure_number_mid_year(h):
        return h.pressure[1]

    def color_wind_end_year(h):
        return h.color_pressure[0]

    def color_wind_mid_year(h):
        return h.color_pressure[1]

    def wind_display_end_year(h):
        wind = h.wind[0].get('direction')
        if wind:
            return wind.arrow
        return "-"

    def wind_display_mid_year(h):
        wind = h.wind[1].get('direction')
        if wind:
            return wind.arrow
        return "-"

    def color_hex_type(h):
        if h.is_land:
            return (0, 255, 0)
        return (0, 0, 255)

    def color_geoforms(h):
        for g in GeoformType.list():
            if h.geoform.type is g:
                return g.color
        return (0, 0, 255)

    HexGridDraw(hex_grid, color_features, "../output/map_features.png", show_coasts=True, rivers=False)
    HexGridDraw(hex_grid, color_heightmap, "../output/map_height.png",   rivers=False, show_coasts=True)
    HexGridDraw(hex_grid, color_terrain, "../output/map_terrain.png",    rivers=True, show_coasts=True)
    HexGridDraw(hex_grid, color_hex_type, "../output/map_hex_types.png", rivers=True, show_coasts=True)
    HexGridDraw(hex_grid, color_geoforms, "../output/map_geoforms.png", rivers=False, show_coasts=True)
    HexGridDraw(hex_grid, color_rivers, "../output/map_rivers.png", rivers=True, show_coasts=True)
    HexGridDraw(hex_grid, color_temperature_end_year, "../output/map_temp_end_year.png", rivers=False, show_coasts=True)
    HexGridDraw(hex_grid, color_temperature_mid_year, "../output/map_temp_mid_year.png", rivers=False, show_coasts=True)
    HexGridDraw(hex_grid, color_biome, "../output/map_biome.png", rivers=False)
    HexGridDraw(hex_grid, color_territories, "../output/map_territories.png", rivers=False, show_coasts=True, borders=True)
    HexGridDraw(hex_grid, color_satellite, "../output/map_satellite.png")
    HexGridDraw(hex_grid, color_resources, "../output/map_resources.png")
    HexGridDraw(hex_grid, color_zone, "../output/map_zone.png", text_func=key_zone, rivers=False, show_coasts=False)
    HexGridDraw(hex_grid, color_zone, "../output/map_latitude.png", text_func=hex_latitude, rivers=False, show_coasts=False)
    HexGridDraw(hex_grid, color_pressure_end_year, "../output/map_pressure_end_year.png", rivers=False, show_coasts=True)
    HexGridDraw(hex_grid, color_pressure_mid_year, "../output/map_pressure_mid_year.png", rivers=False, show_coasts=True)
    HexGridDraw(hex_grid, color_wind_end_year, "../output/map_wind_end_year.png", text_func=wind_display_end_year, rivers=False, show_coasts=True)
    HexGridDraw(hex_grid, color_wind_mid_year, "../output/map_wind_mid_year.png", text_func=wind_display_mid_year, rivers=False, show_coasts=True)

    # report on territories
    for t in hex_grid.territories:
        print("Territory {}:\n"
              "\tSize: {}\n"
              "\tColor: {}\n"
              "\tLandlocked: {}\n"
              "\tAverage Temperature: {}\n"
              "\tAverage Moisture: {}\n"
              "\tNeighbors: {}"
              .format(t.id, t.size, t.color, t.landlocked, t.avg_temp, t.avg_moisture,
                      t.neighbors))
        print("\tBiomes:")
        for b in t.biomes:
            print("\t - {}: {} - {}%".format(b.get('biome').title,
                                             b.get('count'),
                                             round((b.get('count') / t.size) * 100, 2)))
        print("\tGroups: {}".format(len(t.groups)))
        for g in t.groups:
            print("\t\tHexes: {}, X: {}, Y: {}".format(g.get('size'), g.get('x'), g.get('y')))

# @exec_time
# def save_grid(colony, hex_grid, debug=False):
#     """
#     Saves a hex_grid to the database
#     :param colony: Colony instance
#     :param hex_grid: HexGrid instance
#     :return: True or False on success
#     """
#     # cleans up
#     if len(colony.provinces) is not None:
#         print("Removing previous territories and hexes") if debug else False
#         colony.provinces = []
#         colony.hexes = []
#         colony.save()
#
#     print("Saving world map data to colony") if debug else False
#     colony.world_map_config = dict(sea_level=hex_grid.sealevel,
#                                    max_height=hex_grid.top_height)
#     colony.save()
#
#     print("Saving provinces") if debug else False
#     provinces = []
#
#     # first pass, make instances
#     for t in hex_grid.territories:
#         gen_name = Namegen('states').generate_name()
#         p = Province(name=gen_name,
#                      avg_temp=t.avg_temp,
#                      avg_rainfall=t.avg_moisture,
#                      landlocked=t.landlocked)
#         p.color = t.color
#         p.colony = colony
#         p._groups = ';'.join([str(i.get('size'))+','+str(i.get('x'))+','+str(i.get('y')) for i in t.groups])
#         t.db_instance = p
#         session.add(p)
#
#     # make neighbors
#     print("Saving neighboring province lists") if debug else False
#     for t in hex_grid.territories:
#         t.db_instance.neighbors = [tn.db_instance for tn in t.neighbors]
#
#     # generate hex instances
#     print("Saving hexagons (will take a while)") if debug else False
#     for y, row in enumerate(hex_grid.hex_grid.grid):
#         for x, col in enumerate(row):
#             hex_inst = hex_grid.hex_grid.find_hex(x, y)
#
#             n_hex = Hex(x=x, y=y, altitude=hex_inst.altitude,
#                         rainfall=hex_inst.moisture,
#                         temperature=hex_inst.temperature,
#                         biome=hex_inst.biome,
#                         color_terrain=hex_inst.color_terrain,
#                         color_rainfall=hex_inst.color_rivers,
#                         color_temperature=hex_inst.color_temperature,
#                         color_biome=hex_inst.color_biome,
#                         color_satellite=hex_inst.color_satellite)
#
#             if hex_inst.resource is not None:
#                 hex_inst.resource_rating = hex_inst.resource.get('rating')
#                 hex_inst.resource_type = hex_inst.resource.get('type')
#
#             # is this a coastal hex?
#             for e in hex_inst.edges:
#                 edge_t = set()
#                 edge_t.add(0)
#                 if hex_inst.is_land and e.two.is_water:
#                     edge_t.add(2)
#                 if e.one.is_owned and e.two.is_owned and e.one.territory.id != e.two.territory.id:
#                     edge_t.add(4)
#                 setattr(n_hex, 'edge_'+e.side.name, tuple(edge_t))
#
#             segments = hex_grid.find_river(x, y)
#             for s in segments:
#                 edge_t = set(getattr(n_hex, 'edge_'+s.name))
#                 edge_t.add(1)
#                 setattr(n_hex, 'edge_'+s.name, tuple(edge_t))
#
#
#
#             if hex_inst.is_owned:
#                 n_hex.province = hex_inst.territory.db_instance
#             n_hex.colony = colony
#             session.add(n_hex)
#
#     session.commit()


def generate(params, debug=True, image=True):
    """
    Given a colony, creates a world map
    :param params: generator parameters
    :return: True or False on success
    """
    hex_grid = MapGen(params=params, debug=debug)

    if image:
        draw_grid(hex_grid)

    return hex_grid
