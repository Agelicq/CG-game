import pygame
from sprites.collectible import Collectible
from level.tile import Tile, TILE_SIZE
from level.tileset_loader import load_tileset
from level.world_loader import load_map

class Level:
    def __init__(self, planet_name):
        self.tiles = pygame.sprite.Group()
        self.player_spawn = (0, 0)  # si no hay P en el mapa, aparece en (0, 0)
        self.enemy_spawns = []
        self.stalactite_spawns = []
        self.collectibles = pygame.sprite.Group()
        self.fragments = pygame.sprite.Group()

        self.fragment_img = pygame.image.load("assets/images/alfa.png").convert_alpha()
        self.fragment_img = pygame.transform.scale(self.fragment_img, (60, 55))
        self.heal_img = pygame.image.load("assets/images/item.png").convert_alpha()
        self.heal_img = pygame.transform.scale(self.heal_img, (60, 60))


        self.load_level(planet_name)

    def load_level(self, planet_name):
        layout = load_map(planet_name)

        tiles = load_tileset("assets/images/ice.png")

        tile_sheet = {
            "ice_top": tiles[0],
            "ice_center": tiles[1],
            "ice_edge": tiles[2],
            "rock_top": tiles[3],
            "rock_center": tiles[4],
            "rock_edge": tiles[5],
        }

        for row_idx, row in enumerate(layout):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE

                #bloques
                if cell == "R" or cell == "1" or cell == "#":      # piso rocoso superior
                    tile = Tile(x, y, tile_sheet["rock_top"], "solid")
                    self.tiles.add(tile)

                elif cell == "r":    # roca interna
                    tile = Tile(x, y, tile_sheet["rock_center"], "solid")
                    self.tiles.add(tile)

                elif cell == "i":    # hielo interior
                    tile = Tile(x, y, tile_sheet["ice_center"], "ice")
                    self.tiles.add(tile)

                elif cell == "e":  #roca
                    tile = Tile(x, y, tile_sheet["ice_edge"], "solid")
                    self.tiles.add(tile)

                #player/enemigos/obstaculos
                elif cell == "P":
                    self.player_spawn = (x, y)
                
                elif cell == "E":
                    self.enemy_spawns.append((x, y))

                elif cell == "S":
                    self.stalactite_spawns.append((x, y))

                #objetos
                elif cell == "H":
                    self.collectibles.add(Collectible(x, y + 50, self.heal_img, type="heal"))

                elif cell == "F":
                    self.collectibles.add(Collectible(x, y + 50, self.fragment_img, type="fragment"))

    def draw(self, surface):
        self.tiles.draw(surface)
