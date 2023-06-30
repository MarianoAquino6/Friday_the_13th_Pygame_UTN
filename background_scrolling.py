import pygame
from config import *
from items import AnimatedItem
from NPCs import Cop, Chopper, Drone

# LOADING BACKGROUND IMAGES
def create_background_images(level, image_amount):
    background_images = []
    for i in range(0, image_amount):
        background_image = pygame.image.load(f"BACKGROUND IMAGES/LEVEL {level}/{i}.png").convert_alpha()
        background_image_scaled = pygame.transform.scale(background_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
        background_images.append(background_image_scaled)
    return background_images

#SCROLLING BACKGROUND IMAGES
scrolling_x = 0
def draw_bg(background_images, scrolling_x):
    #NUMERO DE VECES QUE IMPRIMO EL FONDO UNO TRAS OTRO
    for x in range(12):
        speed = 1 #VARIABLE DE VELOCIDAD. ES 1 EN CADA ITERACION DEL 'FOR X IN RANGE()'
        #RECORRO LOS FONDOS
        for i in background_images:
            #BLITEO EL FONDO ITERADO USANDO EL X ITERADO MULTIPLICADO POR EL ANCHO DE LA PANTALLA
            #DE ESTA FORMA LA PRIMERA ES 0*1280 (0), LA SEGUNDA ES 1*1280 (AL FINAL DE LA PANTALLA), ETC
            #EL X EN DONDE BLITEAMOS DEPENDE TAMBIEN DE SI ESTAMOS SCROLLEANDO LA PANTALLA Y DE LA VELOCIDAD DEL LAYER
            SCREEN.blit(i, (((x * SCREEN_WIDTH) - scrolling_x * speed), 0))
            speed += 2 #LA PRIMERA VEZ SPEED ES 2, LA SEGUNDA ES 4, ETC. PARA SETTEAR LA VELOCIDAD CON LA CUAL CADA ELEMENTO SE MUEVE

def scroll_items_and_platforms(mode, platform_list, item_list, enemy_list, invisible_rect, bullet_list):
    if mode == "SCROLL LEFT":
        for platform in platform_list:
                platform.rect.x -= 10
                if platform.top_rect != None:
                    platform.top_rect.x -= 10
                if platform.left_rect != None:
                    platform.left_rect.x -= 10
                if platform.right_rect != None:
                    platform.right_rect.x -= 10
        for item in item_list:
            item.rect.x -= 10
            if type(item) == AnimatedItem:
                if item.gun_rect_1 != None:
                    item.gun_rect_1.x -= 10
                    item.gun_rect_2.x -= 10
        for enemy in enemy_list:
            enemy.rect.x -= 10
            if type(enemy) == Cop or type(enemy) == Chopper or type(enemy) == Drone:
                enemy.gun_rect.x -= 10
        for rect in invisible_rect:
            rect.x -= 10
        for bullet in bullet_list:
           bullet.rect.x -= 10

    elif mode == "SCROLL RIGHT":
        for platform in platform_list:
                platform.rect.x += 10
                if platform.top_rect != None:
                    platform.top_rect.x += 10
                if platform.left_rect != None:
                    platform.left_rect.x += 10
                if platform.right_rect != None:
                    platform.right_rect.x += 10
        for item in item_list:
            item.rect.x += 10
            if type(item) == AnimatedItem:
                if item.gun_rect_1 != None:
                    item.gun_rect_1.x += 10
                    item.gun_rect_2.x += 10
        for enemy in enemy_list:
            enemy.rect.x += 10
            if type(enemy) == Cop or type(enemy) == Chopper or type(enemy) == Drone:
                enemy.gun_rect.x += 10
        for rect in invisible_rect:
            rect.x += 10
        for bullet in bullet_list:
            bullet.rect.x += 10
    else:
        for platform in platform_list:
            if not platform.moving:
                platform.rect.x += 0
                if platform.top_rect != None:
                    platform.top_rect.x += 0
                if platform.left_rect != None:
                    platform.left_rect.x += 0
                if platform.right_rect != None:
                    platform.right_rect.x += 0
        for item in item_list:
            item.rect.x += 0

            if type(item) == AnimatedItem:
                if item.gun_rect_1 != None:
                    item.gun_rect_1.x += 0
                    item.gun_rect_2.x += 0
        for enemy in enemy_list:
            enemy.rect.x += 0
            if type(enemy) == Cop or type(enemy) == Chopper or type(enemy) == Drone:
                enemy.gun_rect.x += 0
        for rect in invisible_rect:
            rect.x += 0
        for bullet in bullet_list:
            bullet.rect.x += 0