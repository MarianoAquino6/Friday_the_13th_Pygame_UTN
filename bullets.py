import pygame
from config import *
from auxiliar import get_surface_list_from_sprite_images_and_scale_them
from items import AnimatedItem
from NPCs import Cop, Chopper, Drone, UFO

class Bullet:
    def __init__(self, source_rect, direction, speed, max_distance, folder):
        self.horizontal_bullet = get_surface_list_from_sprite_images_and_scale_them("ITEMS", f"{folder}/BULLET", False, bullet=True)
        self.right_diagonal_bullet = get_surface_list_from_sprite_images_and_scale_them("ITEMS", f"{folder}/BULLET", False, diagonal=True, bullet=True)
        self.left_diagonal_bullet = get_surface_list_from_sprite_images_and_scale_them("ITEMS", f"{folder}/BULLET", True, diagonal=True, bullet=True)
        
        self.image = self.horizontal_bullet[0]
        self.rect = self.image.get_rect()
        self.rect.center = source_rect.center
        self.direction = direction
        self.speed = speed

        self.max_distance = max_distance
        self.distance_travelled = 0

    def update(self):
        if self.direction == "LEFT":
            self.image = self.horizontal_bullet[0]
            self.rect.centerx -= self.speed

        elif self.direction == "RIGHT":
            self.image = self.horizontal_bullet[0]
            self.rect.centerx += self.speed 

        elif self.direction == "LEFT_DIAGONAL":
            self.image = self.left_diagonal_bullet[0]
            self.rect.centerx -= self.speed 
            self.rect.centery += self.speed 
        elif self.direction == "RIGHT_DIAGONAL":
            self.image = self.right_diagonal_bullet[0]
            self.rect.centerx += self.speed 
            self.rect.centery += self.speed
           
        self.distance_travelled += self.speed
    
        if self.distance_travelled >= self.max_distance:
            self.dissapear()

    def dissapear(self):
        self.rect.y = -9000

    def draw(self):
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 255, 0), self.rect)
        SCREEN.blit(self.image, self.rect)

def shoot_bullet(enemy_list, item_list, bullet_list, folder):
    for enemy in enemy_list:
        if type(enemy) != UFO:
            if enemy.shooting:
                if type(enemy) == Cop:
                    bullet = Bullet(enemy.gun_rect, enemy.direction, 10, 500, folder)
                    bullet_list.append(bullet)
                if type(enemy) == Chopper:
                    bullet = Bullet(enemy.gun_rect, "RIGHT_DIAGONAL", 10, 500, folder)
                    bullet_list.append(bullet)
                if type(enemy) == Drone:
                    bullet = Bullet(enemy.gun_rect, "LEFT_DIAGONAL", 10, 500, folder)
                    bullet_list.append(bullet)
    for item in item_list:
        if type(item) == AnimatedItem:
            if item.shooting:
                bullet_1 = Bullet(item.gun_rect_1, "RIGHT_DIAGONAL", 10, 500, folder)
                bullet_2 = Bullet(item.gun_rect_2, "RIGHT_DIAGONAL", 10, 500, folder)
                bullet_list.append(bullet_1)
                bullet_list.append(bullet_2)
