import random
import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from ui import UI
from utilities import import_csv_layout, import_folder
from weapon import Weapon
from enemy import Enemy

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_LargeObjects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        
        graphics = {
            'grass':  import_folder('graphics/Grass'),
            'objects': import_folder('graphics/Objects')
        }
     
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row): 
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random.choice(graphics['grass']))

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '394':
                               self.player = Player(
                                    (x,y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_weapon, self.create_magic
                                )
                            else:
                                monster_names = {
                                    '390': 'bamboo',
                                    '391': 'spirit',
                                    '392': 'raccoon',
                                }   
                                monster_name = monster_names.get(col, 'squid')
                                Enemy(monster_name, (x,y), [self.visible_sprites], self.obstacle_sprites) 

        

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])
    
    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        # Update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        # General Setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(0,0)

        # Creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # getting the offset
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset)


        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites: 
            sprite.enemy_update(player)
    
