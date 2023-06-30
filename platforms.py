import pygame
import os
from config import *

class Platform:
    def __init__(self, image, x, y, movement_speed=0, moving=False, has_top_rect=False, has_left_rect=False, has_right_rect=False, damaging=False):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x     
        self.rect.y = y

        #DIFFERENT TYPES OF RECTS
        self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height / 8) if has_top_rect else None
        self.left_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height / 4, self.rect.width / 8, self.rect.height) if has_left_rect else None
        self.right_rect = pygame.Rect(self.rect.right - self.rect.width / 8, self.rect.y + self.rect.height / 4, self.rect.width / 8, self.rect.height) if has_right_rect else None

        #MOVING PLATFORMS
        self.moving = moving
        self.movement_speed = movement_speed
        self.starting_x = x
        self.direction = "RIGHT"

        #DAMAGING PLATFORMS
        self.damaging = damaging

    def update_and_draw_platform(self, side_platform_rects):
        #IF PLATFORM MOVES
        if self.moving:
            self.move_platform(side_platform_rects)
        self.draw()

    def move_platform(self, side_platform_rects):
    #IF DIRECTION IS RIGHT
        if self.direction == "RIGHT":
            if self.collides_with_any(side_platform_rects):
                self.rect.x -= self.movement_speed
                self.top_rect.x -= self.movement_speed
                self.direction = "LEFT"
            else:
                self.rect.x += self.movement_speed
                self.top_rect.x += self.movement_speed
        #IF DIRECTION IS LEFT
        else:
            if self.collides_with_any(side_platform_rects):
                self.rect.x += self.movement_speed
                self.top_rect.x += self.movement_speed
                self.direction = "RIGHT"
            else:
                self.rect.x -= self.movement_speed
                self.top_rect.x -= self.movement_speed
    
    def collides_with_any(self, side_platform_rects):
        for rect in side_platform_rects:
            if self.rect.colliderect(rect):
                return True
        return False

    def draw(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(255,0,0),self.rect)
        SCREEN.blit(self.image, self.rect)
        if DEBUG:
            if self.top_rect != None:
                pygame.draw.rect(SCREEN,(0,0,255),self.top_rect)
            if self.left_rect != None:
                pygame.draw.rect(SCREEN,(0,0,255),self.left_rect)
            if self.right_rect != None:
                pygame.draw.rect(SCREEN,(0,0,255),self.right_rect)

def get_tower(folder, starting_x, starting_y, width, height):
    tower = []
    platform_width = PLATFORM_WIDTH
    platform_height = PLATFORM_HEIGHT 
    num_vertical_repeats = height

    starting_x = starting_x
    starting_y = starting_y

    base_path = "PLATFORMS"

    #UNDERGROUND FRAGMENT--------------------------------------------------------------------------------------------
    for i in range(num_vertical_repeats):
        #LEFT BORDER
        platform_image_left_path = os.path.join(base_path, f"{folder}/SIDE BORDERS", "0.png")
        platform_image_left = pygame.image.load(platform_image_left_path).convert_alpha()
        platform_image_left_scaled = pygame.transform.scale(platform_image_left, (platform_width, platform_height))
        platform_image_left_flipped = pygame.transform.flip(platform_image_left_scaled, True, False)

        x = starting_x
        y = starting_y - (platform_height * i)

        platform_fragment = Platform(image=platform_image_left_flipped, x=x, y=y, has_top_rect=False, has_left_rect=True, has_right_rect=False, damaging=False)
        tower.append(platform_fragment)

        #CENTER
        for j in range(width):
            platform_image_center_path = os.path.join(base_path, f"{folder}/UNDERGROUND CENTER", "0.png")
            platform_image_center = pygame.image.load(platform_image_center_path).convert_alpha()
            platform_image_center_scaled = pygame.transform.scale(platform_image_center, (platform_width, platform_height))

            x = starting_x + platform_width * (j + 1)
            y = starting_y - (platform_height * i)

            platform_fragment = Platform(image=platform_image_center_scaled, x=x, y=y, has_top_rect=False, has_left_rect=False, has_right_rect=False, damaging=False)
            tower.append(platform_fragment)

        #RIGHT BORDER
        platform_image_right_path = os.path.join(base_path, f"{folder}/SIDE BORDERS", "0.png")
        platform_image_right = pygame.image.load(platform_image_right_path).convert_alpha()
        platform_image_right_scaled = pygame.transform.scale(platform_image_right, (platform_width, platform_height))

        x = starting_x + platform_width * (width + 1)
        y = starting_y - (platform_height * i)

        platform_fragment = Platform(image=platform_image_right_scaled, x=x, y=y, has_top_rect=False, has_left_rect=False, has_right_rect=True, damaging=False)
        tower.append(platform_fragment)

    #TOP FRAGMENT---------------------------------------------------------------------------------------------------
    #LEFT BORDER
    platform_image_left_path = os.path.join(base_path, f"{folder}/TOP BORDERS", "0.png")
    platform_image_left = pygame.image.load(platform_image_left_path).convert_alpha()
    platform_image_left_scaled = pygame.transform.scale(platform_image_left, (platform_width, platform_height))
    platform_image_left_flipped = pygame.transform.flip(platform_image_left_scaled, True, False)

    x = starting_x
    y = starting_y - (platform_height * num_vertical_repeats)

    platform_fragment = Platform(image=platform_image_left_flipped, x=x, y=y, has_top_rect=True, has_left_rect=True, has_right_rect=False, damaging=False)
    tower.append(platform_fragment)

    #CENTER
    for i in range(width):
        platform_image_center_path = os.path.join(base_path, f"{folder}/TOP CENTER", "0.png")
        platform_image_center = pygame.image.load(platform_image_center_path).convert_alpha()
        platform_image_center_scaled = pygame.transform.scale(platform_image_center, (platform_width, platform_height))
        
        x = starting_x + platform_width * (i + 1)
        y = starting_y - (platform_height * num_vertical_repeats)

        platform_fragment = Platform(image=platform_image_center_scaled, x=x, y=y, has_top_rect=True, has_left_rect=False, has_right_rect=False, damaging=False)
        tower.append(platform_fragment)

    #RIGHT BORDER
    platform_image_right_path = os.path.join(base_path, f"{folder}/TOP BORDERS", "0.png")
    platform_image_right = pygame.image.load(platform_image_right_path).convert_alpha()
    platform_image_right_scaled = pygame.transform.scale(platform_image_right, (platform_width, platform_height))

    x = starting_x + platform_width * (width + 1)
    y = starting_y - (platform_height * num_vertical_repeats)

    platform_fragment = Platform(image=platform_image_right_scaled, x=x, y=y, has_top_rect=True, has_left_rect=False, has_right_rect=True, damaging=False)
    tower.append(platform_fragment)
    return tower

def get_floating_platform(folder, starting_x, starting_y, small, moving, movement_speed=0):
    floating_platform = []
    platform_width = PLATFORM_WIDTH
    platform_height = PLATFORM_HEIGHT  

    starting_x = starting_x
    starting_y = starting_y

    base_path = "PLATFORMS"

    #SMALL PLATFORM
    if small:
            platform_image_path = os.path.join(base_path, f"{folder}/FLOATING", "small.png")
            platform_image = pygame.image.load(platform_image_path).convert_alpha()
            platform_image_scaled = pygame.transform.scale(platform_image, (platform_width, platform_height))

            x = starting_x
            y = starting_y

            if moving:
                platform_fragment = Platform(image=platform_image_scaled, x=x, y=y, movement_speed=movement_speed, moving=True, has_top_rect=True, has_left_rect=False, has_right_rect=False, damaging=False)
            else:
                platform_fragment = Platform(image=platform_image_scaled, x=x, y=y, has_top_rect=True, has_left_rect=False, has_right_rect=False, damaging=False)
            floating_platform.append(platform_fragment)
    #LARGE PLATFORM
    else:
            platform_image_path = os.path.join(base_path, f"{folder}/FLOATING", f"entire.png")
            platform_image = pygame.image.load(platform_image_path).convert_alpha()
            platform_image_scaled = pygame.transform.scale(platform_image, (platform_width*3, platform_height))

            x = starting_x 
            y = starting_y

            if moving:
                platform_fragment = Platform(image=platform_image_scaled, x=x, y=y, movement_speed=movement_speed, moving=True, has_top_rect=True, has_left_rect=False, has_right_rect=False, damaging=False)
            else:
                platform_fragment = Platform(image=platform_image_scaled, x=x, y=y, has_top_rect=True, has_left_rect=False, has_right_rect=False, damaging=False)
            floating_platform.append(platform_fragment)
    return floating_platform

def get_lava_floor_spikes_or_street(folder, mode, starting_x, starting_y, width):
    lava_spikes_or_street_floor = []
    platform_width = PLATFORM_WIDTH
    platform_height = PLATFORM_HEIGHT 

    starting_x = starting_x
    starting_y = starting_y

    base_path = "PLATFORMS"

    for i in range(width):
        #LAVA/ACID
        if mode == "LAVA":
            platform_image_path = os.path.join(base_path, f"{folder}/LAVA.png")
        #SPIKES
        elif mode == "SPIKES":
            platform_image_path = os.path.join(base_path, f"{folder}/SPIKES.png")
        else:
            platform_image_path = os.path.join(base_path, f"{folder}/STREET.png")


        platform_image = pygame.image.load(platform_image_path).convert_alpha()
        platform_image_scaled = pygame.transform.scale(platform_image, (platform_width, platform_height))
        
        x = starting_x + platform_width * i 
        y = starting_y

        if mode == "LAVA" or mode == "SPIKES":
            platform_fragment = Platform(image=platform_image_scaled, x=x, y=y, has_top_rect=True, has_left_rect=False, has_right_rect=False, damaging=True)
        else:
            platform_fragment = Platform(image=platform_image_scaled, x=x, y=y, has_top_rect=False, has_left_rect=False, has_right_rect=False, damaging=False)
        lava_spikes_or_street_floor.append(platform_fragment)
    return lava_spikes_or_street_floor

def get_side_platform_rects(platform_objects_list):
    side_platform_rects = []

    for platform in platform_objects_list:
        if platform.right_rect:
            side_platform_rects.append(platform.right_rect)
        elif platform.left_rect:
            side_platform_rects.append(platform.left_rect)
    return side_platform_rects