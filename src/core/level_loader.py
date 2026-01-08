import pygame
import pytmx
from src import config


def load_level(filename):
    # 1. Load the TMX file data
    tmx_data = pytmx.util_pygame.load_pygame(filename)

    walls = []
    visuals = []
    hazards = []
    spawn_point = (0, 0)
    slime_spawns = []
    frog_spawns = []


    # 2. Iterate through "Terrain" layer to create Walls
    # We look for the layer named 'Terrain'
    layer = tmx_data.get_layer_by_name("Terrain")

    if layer:
        # Iterate over x, y coordinates and the image (gid)
        for x, y, gid in layer:
            # If gid is not 0 (0 means empty air)
            if gid != 0:
                # Calculate pixel position
                pixel_x = x * config.TILE_SIZE
                pixel_y = y * config.TILE_SIZE

                # Create a physical rectangle for physics
                rect = pygame.Rect(pixel_x, pixel_y, config.TILE_SIZE, config.TILE_SIZE)
                walls.append(rect)
                image = tmx_data.get_tile_image_by_gid(gid)
                visuals.append((image, rect))

    # 3. Iterate through "Spawns" object layer

    objects = tmx_data.get_layer_by_name("Spawners")
    for obj in objects:
        if obj.name == "PlayerStart":
            spawn_point = (obj.x, obj.y - 64)

        elif obj.name == "SlimeStart":
            slime_spawns.append((obj.x, obj.y- 32))

        elif obj.name == "FrogStart":
            frog_spawns.append((obj.x, obj.y -32))


    # Return the image of the map (visuals) and the physics (walls/spawn)
    return tmx_data, walls,hazards, visuals, spawn_point, slime_spawns, frog_spawns