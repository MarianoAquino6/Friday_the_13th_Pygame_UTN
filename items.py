import pygame
import os
from config import *
import auxiliar

class AnimatedItem:
    def __init__(self, starting_x, starting_y, folder, lightning, spinning_saw, turret, animation_speed, button, force_field, traffic_light, damaging=False):
        self.frame = 0
        self.animation = auxiliar.get_surface_list_from_sprite_images_and_scale_them("ITEMS", folder, False, lightning=lightning, spinning_saw=spinning_saw, turret=turret, button=button, force_field=force_field, traffic_light=traffic_light)  
        self.current_animation_image = self.animation[self.frame]

        self.rect = self.current_animation_image.get_rect()
        self.rect.x = starting_x     
        self.rect.y = starting_y

        self.time_since_last_frame = 0
        self.animation_speed = animation_speed

        self.button = button
        self.force_field = force_field
        self.lightning = lightning
        self.traffic_light = traffic_light
        self.red = False if traffic_light else None
        self.damaging = damaging

        self.gun_rect_1 = pygame.Rect(self.rect.centerx+55, self.rect.centery+40, 20, 20) if turret else None
        self.gun_rect_2 = pygame.Rect(self.rect.centerx+65, self.rect.centery+20, 20, 20) if turret else None
        self.shooting = False if turret else None

        self.button_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Button.mp3")

    def animate_and_draw_item(self, ms, jason_voorhees, pressed_key, force_field_button=None):
        if self.button:
            if self.rect.colliderect(jason_voorhees.rect) and pressed_key[pygame.K_e]:
                self.frame = 1
                self.button_sound_effect.set_volume(0.2)
                self.button_sound_effect.play()
        elif self.force_field:
            if force_field_button.frame == 0:
                self.frame = 0
                self.damaging = True
            else:
                self.frame = 1
                self.damaging = False    
        else:
            self.time_since_last_frame += ms
            if self.time_since_last_frame > self.animation_speed:
                self.time_since_last_frame = 0

                if(self.frame < len(self.animation) - 1):
                    self.frame += 1
                    if self.shooting != None:
                        self.shooting = True
                else: 
                    self.frame = 0
                    if self.shooting != None:
                        self.shooting = False
                
                if self.lightning: 
                    if self.frame > 3 and self.frame < 9:
                        self.damaging = True
                    else:
                        self.damaging = False
            
            if self.traffic_light:
                if self.frame == 2:
                    self.red = True
                else:
                    self.red = False

        if DEBUG:
            pygame.draw.rect(SCREEN,(0,255,0),self.rect)
            if self.gun_rect_1:
                pygame.draw.rect(SCREEN,(0,0,255),self.gun_rect_1)
                pygame.draw.rect(SCREEN,(0,0,255),self.gun_rect_2)
        self.current_animation_image = self.animation[self.frame]
        SCREEN.blit(self.current_animation_image, self.rect)

class Item:
    def __init__(self, image, x, y, increase_life=False, increase_score=False):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x     
        self.rect.y = y
        self.increase_life = increase_life
        self.increase_score = increase_score

    def draw_item(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(0,255,0),self.rect)
        SCREEN.blit(self.image, self.rect)

def get_coin(path, x, y):
    base_path = "ITEMS"
    item_image_path = os.path.join(base_path, f"{path}.png")
    item_image = pygame.image.load(item_image_path).convert_alpha()
    item_image_scaled = pygame.transform.scale(item_image,(40,40))
    coin = Item(image=item_image_scaled,x=x,y=y, increase_life=False, increase_score=True)
    return coin

def get_beer(folder, x, y):
    base_path = "ITEMS"
    item_image_path = os.path.join(base_path, f"{folder}/BEER.png")
    item_image = pygame.image.load(item_image_path).convert_alpha()
    item_image_scaled = pygame.transform.scale(item_image,(150,60))
    beer = Item(image=item_image_scaled,x=x,y=y, increase_life=True, increase_score=False)
    return beer

def get_lightning(x, y):
    lightning = AnimatedItem(starting_x=x, starting_y=y, folder="LEVEL 1/LIGHTNING", lightning=True, spinning_saw=False, turret=False, button=False, force_field=False, traffic_light=False, animation_speed=150, damaging=False)
    return lightning

def get_spinning_saw(folder, x, y):
    spinning_saw = AnimatedItem(starting_x=x, starting_y=y, folder=folder, spinning_saw=True, lightning=False,turret=False, button=False, force_field=False, traffic_light=False, animation_speed=50, damaging=True)
    return spinning_saw

def get_turret(x, y):
    turret = AnimatedItem(starting_x=x, starting_y=y, folder="LEVEL 1/TURRET", spinning_saw=False, lightning=False, turret=True, button=False, force_field=False, traffic_light=False, animation_speed=1000, damaging=False)
    return turret

def get_button(x, y):
    button = AnimatedItem(starting_x=x, starting_y=y, folder="LEVEL 2/BUTTON", spinning_saw=False, lightning=False, turret=False, button=True, force_field=False, traffic_light=False, animation_speed=0, damaging=False)
    return button

def get_force_field(x, y):
    force_field = AnimatedItem(starting_x=x, starting_y=y, folder="LEVEL 2/FORCE FIELD", spinning_saw=False, lightning=False, turret=False, button=False, force_field=True, traffic_light=False, animation_speed=0, damaging=True)
    return force_field

def get_traffic_light(x,y):
    traffic_light = AnimatedItem(starting_x=x, starting_y=y, folder="LEVEL 3/TRAFFIC LIGHT", spinning_saw=False, lightning=False, turret=False, button=False, force_field=False, traffic_light=True, animation_speed=3000, damaging=False)
    return traffic_light