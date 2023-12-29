import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstical_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstical_sprites = obstical_sprites
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else: 
            self.direction.x = 0
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')

        # self.rect.center += self.direction * speed

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstical_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # Moving right
                        self.rect.right = sprite.rect.left # move the player back 
                    if self.direction.x < 0: 
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstical_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # Moving Up
                        self.rect.bottom = sprite.rect.top # move the player back 
                    if self.direction.y < 0: # Movind down
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)