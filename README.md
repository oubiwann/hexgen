# Hexgen

![Satellite Map](http://i.imgur.com/ekkaWgkl.png)

## What is this?

It's a world map generator written in Python. It generates a random world map
represented in a hexagon grid. The parameters for the generator allow for any
kind of planet surface to be generated. It also can segment the surface into
randomly sized globs called territories.

## Why?

I'm using this as a board for a browser-based game I am working on. It can be
used for anything from DnD campaigns to open-source games or even just for fun.


## Dependencies

* GNU Make
* Docker

## Setup

```
$ make docker
```

## Usage

Quick help:

```
$ ./bin/docker-hexgen -h
```
```
usage: hexgen [-h] [--map-type MAP_TYPE] [--ocean-type OCEAN_TYPE]
              [--surface-pressure SURFACE_PRESSURE] [--axial-tilt AXIAL_TILT]
              [--size SIZE] [--roughness ROUGHNESS] [--base-temp BASE_TEMP]
              [--avg-temp AVG_TEMP] [--sea-percent SEA_PERCENT]
              [--hydrosphere] [--image] [--num-rivers NUM_RIVERS]
              [--make-lakes] [--make-territories]
              [--num-territories NUM_TERRITORIES] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --map-type MAP_TYPE
  --ocean-type OCEAN_TYPE
  --surface-pressure SURFACE_PRESSURE
  --axial-tilt AXIAL_TILT
  --size SIZE
  --roughness ROUGHNESS
  --base-temp BASE_TEMP
  --avg-temp AVG_TEMP
  --sea-percent SEA_PERCENT
  --hydrosphere
  --image
  --num-rivers NUM_RIVERS
  --make-lakes
  --make-territories
  --num-territories NUM_TERRITORIES
  --debug
```

An actual run might look something like this:
```
$ ./bin/docker-hexgen --axial-tilt=26 --base-temp=-20 --avg-temp=10 \
                      --size=108 --roughness=10 --make-lakes
```


### Output

All output is saved to the `./output` directory. This includes a series of
world map images of different types as well as all the generated world data in
JSON format.

### Hexagon types:

- land: defined as a solid surface
- water: define as a liquid surface

### Hexagon properties
- altitude (int, 0 - 255)
- temperature (celsius)
- moisture (int): water content
- fertility: soil fertility
- feature
    - lake
    - crater
    - volcano


### Parameters
- Required parameters
    - size (int): World map size in hexagons. This defines the width and height of the hexagon grid.
    - avg_temp (celsius): average surface temperature of this planet
- General parameters (required):
    - roughness (int, 0 - 10): used by the diamond-square algorithm to determine the roughness of the terrain.
    - axial_tilt (int, -90 - 90): This world's axial tilt. Has a huge impact on temperature variations.
    - land_percent (int, 0 - 100): Percent of surface that is land
    - hydrosphere (bool): whether the world has surface hydrosphere
    - ocean_type (OceanType): composition of the ocean. Can be water, hydrocarbons, magma

- Surface features (optional):
    - aquifer_max (int): maximum number of aquifers to place underground
    - river_max (int): maximum number of rivers to place on the map
    - crater_max (int): maximum number of craters to place on the surface
    - volcano_max (int): maximum number of volanoes to place on the surface
    - make_lakes (bool): Put lakes on hexes with 4 or more river segments

- Territories (optional):
    - make_territories (bool): whether to generate territories
    - land_only (bool): if True, territories will only exist on land
    - separate_zones (bool): if True, territories will never leave their zones
    - merge_islands (bool): if True, unclaimed islands will be given to the nearest territory
    - merge_small (bool): if True, small territories will be merged with their neighbors

- Exporting:
    - export_type (string, one of "png", "json")
    - png export:
        - draw_borders: (bool): Draw borders between territories and on coastlines
