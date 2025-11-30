import pygame
from sprites.collectible import Collectible
from sprites.enemy import Enemy
from sprites.stalactite import Stalactite
from level.tile import Tile, TILE_SIZE
from level.tileset_loader import load_tileset
from level.world_loader import load_map

class Level:
    def __init__(self, planet_name):
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.stalactites = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        self.player_spawn = (0, 0)
        self.enemy_spawns = []
        self.stalactite_spawns = []
        self.collectible_spawns = []

        # Carga mapa y tiles según planeta
        self.planet = planet_name
        self.load_background()
        self.load_tileset()
        self.load_map()

        # Después de leer el mapa, instanciamos objetos
        self.spawn_enemies()
        self.spawn_stalactites()
        self.spawn_collectibles()

        if self.planet == "glacius":
            self.ice_sound = pygame.mixer.Sound("assets/music/cold_wind.mp3")
            self.ice_sound.set_volume(0.4)
            self.ice_sound.play()

    # ------------------------------
    # Sección de carga de assets
    # ------------------------------
    def load_background(self):
        bg_path = f"assets/images/bg_{self.planet}.png"
        self.background = pygame.image.load(bg_path).convert()


    def load_tileset(self):
        ts_path = f"assets/images/tilesets/{self.planet}.png"
        self.tileset = load_tileset(ts_path)


    # ------------------------------
    # Mapa
    # ------------------------------
    def load_map(self):
        layout = load_map(self.planet)

        tile_sheet = {
            "ice_top": self.tileset[0],
            "ice_center": self.tileset[1],
            "ice_edge": self.tileset[2],
            "rock_top": self.tileset[3],
            "rock_center": self.tileset[4],
            "rock_edge": self.tileset[5],
        }

        for row_idx, row in enumerate(layout):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE

                # Tiles
                if cell in ("R", "1", "#"):
                    self.tiles.add(Tile(x, y, tile_sheet["rock_top"], "solid"))

                elif cell == "r":
                    self.tiles.add(Tile(x, y, tile_sheet["rock_center"], "solid"))

                elif cell == "i": 
                    self.tiles.add(Tile(x, y, tile_sheet["ice_center"], "ice"))

                elif cell == "e":
                    self.tiles.add(Tile(x, y, tile_sheet["ice_edge"], "solid"))

                # Spawns
                #player
                elif cell == "P":
                    self.player_spawn = (x, y)
                #enemigo
                elif cell == "E":
                    self.enemy_spawns.append((x, y + 18,))
                #stalactita
                elif cell == "S":
                    self.stalactite_spawns.append((x, y))
                # collectibles
                #fragmento
                elif cell == "F":
                    self.collectible_spawns.append((x, y+ 50, "fragment"))
                #heal
                elif cell == "H":
                    self.collectible_spawns.append((x, y+ 50, "heal"))

    # ------------------------------
    # Instanciadores
    # ------------------------------
    def spawn_enemies(self):
        for x, y in self.enemy_spawns:
            self.enemies.add(Enemy(x, y, 120))

    def spawn_stalactites(self):
        stal_img = pygame.image.load("assets/images/stalactite.png").convert_alpha()
        stal_img = pygame.transform.scale(stal_img, (16, 32))
        for x, y in self.stalactite_spawns:
            self.stalactites.add(Stalactite(x, y, stal_img))

    def spawn_collectibles(self):
        fragment_img = pygame.image.load("assets/images/alfa.png").convert_alpha()
        fragment_img = pygame.transform.scale(fragment_img, (60, 55))

        heal_img = pygame.image.load("assets/images/item.png").convert_alpha()
        heal_img = pygame.transform.scale(heal_img, (60, 60))

        for x, y, type_ in self.collectible_spawns:
            if type_ == "fragment":
                self.collectibles.add(Collectible(x, y, fragment_img, type="fragment"))
            elif type_ == "heal":
                self.collectibles.add(Collectible(x, y, heal_img, type="heal"))

    # ------------------------------
    # Dibujo
    # ------------------------------
    def draw(self, surface):
        self.tiles.draw(surface)
        self.collectibles.draw(surface)
        self.stalactites.draw(surface)
        self.enemies.draw(surface)
