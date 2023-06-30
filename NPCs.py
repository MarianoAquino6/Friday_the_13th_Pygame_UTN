import pygame
from config import *
from auxiliar import get_surface_list_from_sprite_images_and_scale_them

class Cop:
    def __init__(self, starting_x, starting_y, movement_amount, movements_speed, animation_speed, boss, subfolder, alien=False, gang_member=False):
        #CHARACTER STATUS
        self.walk_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\WALKING", False, boss=boss, alien=alien, gang_member=gang_member)
        self.walk_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\WALKING", True, boss=boss, alien=alien, gang_member=gang_member)  
        self.shoot_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\SHOOTING", False, boss=boss, alien=alien, gang_member=gang_member)  
        self.shoot_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\SHOOTING", True, boss=boss, alien=alien, gang_member=gang_member)   
        self.dead_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\DEAD", False, dead_victim = True, boss=boss, alien=alien, gang_member=gang_member)  
        self.dead_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\DEAD", True, dead_victim = True, boss=boss, alien=alien, gang_member=gang_member)

        #CHARACTER ANIMATION
        self.frame = 0
        self.current_animation = self.walk_left
        self.current_animation_image = self.current_animation[self.frame]

        #CHARACTER RECT
        self.rect = self.current_animation_image.get_rect()
        self.rect.x = starting_x     
        self.rect.y = starting_y
        self.starting_y = starting_y

        if boss:
            self.gun_rect = pygame.Rect(self.rect.centerx+60, self.rect.y+80, 20, 20)
        elif alien:
            self.gun_rect = pygame.Rect(self.rect.centerx-60, self.rect.centery-40, 20, 20)
        else:
            self.gun_rect = pygame.Rect(self.rect.centerx-40, self.rect.centery, 20, 20)
        
        # self.gun_rect = pygame.Rect(self.rect.centerx-40, self.rect.centery, 20, 20) if not boss else pygame.Rect(self.rect.x, self.rect.y+80, 20, 20)

        #CONTROLLING CHARACTER
        self.movement_amount = movement_amount
        self.movements_speed = movements_speed
        self.animation_speed = animation_speed
        self.x = 0
        self.y = 0
        self.time_since_last_frame = 0
        self.time_since_last_movement = 0

        #CHARACTER FEATURES
        self.shooting = False
        self.direction = "LEFT"
        self.alive = True
        self.life = 100 if not boss else 500
        self.boss = boss
        self.alien = alien
        self.gang_member = gang_member

        self.sound_playing = True
        self.shooting_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Cop Gun Shot.mp3")
        self.alien_shooting_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Alien Gun Shot.mp3")

    def walk(self, direction):
        self.shooting = False

        #CHOOSING CURRENT ANIMATION ACCORDING TO CURRENT DIRECTION
        if direction == "RIGHT":
            self.current_animation = self.walk_right
            self.x = self.movement_amount
            self.direction = "RIGHT"
        else:
            self.current_animation = self.walk_left
            self.x = -self.movement_amount
            self.direction = "LEFT"

    def shoot(self, direction):
        self.shooting = True
        
        #IF CHARACTER WASN'T ALREADY SHOOTING
        if self.current_animation != self.shoot_right and self.current_animation != self.shoot_left:
            self.frame = 0 #RESETTING FRAME
        
        #CHOOSING CURRENT ANIMATION ACCORDING TO CURRENT DIRECTION
        if direction == "RIGHT":
            self.current_animation = self.shoot_right
            self.x = 0
            if not self.boss: #BOSS HAS A DIFFERENT GUN RECT LOCATION
                self.gun_rect.x = self.rect.centerx + 25
            else:
                self.gun_rect.x = self.rect.centerx + 75
            self.direction = "RIGHT"
        else:
            self.current_animation = self.shoot_left
            self.x = 0
            if not self.boss: #BOSS HAS A DIFFERENT GUN RECT LOCATION
                self.gun_rect.x = self.rect.centerx - 40
            else:
                self.gun_rect.x = self.rect.centerx - 75
            self.direction = "LEFT"

    def update_character(self, ms, jason_voorhees_rect, jason_attacks, invisible_rects):
        self.auto_control_enemy(jason_voorhees_rect, invisible_rects)
        self.collides_with_jason(jason_voorhees_rect, jason_attacks)
        self.animate_character(ms)
        self.move_character(ms)
        self.play_sound("SHOOT")
        
    def auto_control_enemy(self, jason_voorhees_rect, invisible_rects):
        if self.alive == True:
            if self.rect.x > jason_voorhees_rect.x and self.rect.x - jason_voorhees_rect.x < SCREEN_WIDTH/4 and self.rect.y - jason_voorhees_rect.y < jason_voorhees_rect.height:
                self.shoot(direction="LEFT")
            elif self.rect.x < jason_voorhees_rect.x and jason_voorhees_rect.x - self.rect.x < SCREEN_WIDTH/4 and self.rect.y - jason_voorhees_rect.y < jason_voorhees_rect.height:
                self.shoot(direction="RIGHT")
            else:
                if self.direction == "RIGHT" and self.collides_with_any(invisible_rects):
                    self.walk(direction="LEFT")
                    self.rect.x -=30
                    self.gun_rect.x -= 30
                    # print("Colisiona y cambia a la izquierda")
                elif self.direction == "LEFT" and self.collides_with_any(invisible_rects):
                    self.walk(direction="RIGHT")
                    self.rect.x +=30
                    self.gun_rect.x += 30
                    # print("Colisiona y cambia a la derecha")
                elif self.direction == "RIGHT" and not self.collides_with_any(invisible_rects):
                    self.walk(direction="RIGHT")
                    # print("No colisiona y se mueve a la derecha")
                elif self.direction == "LEFT" and not self.collides_with_any(invisible_rects):
                    self.walk(direction="LEFT")
                    # print("No colisiona y se mueve a la izquierda")

    def collides_with_any(self, invisible_rects):
        for rect in invisible_rects:
            if self.rect.colliderect(rect):
                return True
        return False
    
    def collides_with_jason(self, jason_voorhees_rect, jason_attacks):
        if jason_attacks and not self.boss:
            if self.rect.colliderect(jason_voorhees_rect):
                self.x = 0
                if self.alien:
                    self.rect.y = self.starting_y + 98
                elif self.gang_member:
                    self.rect.y = self.starting_y + 120
                else:
                    self.rect.y = self.starting_y + 82
                self.frame = 0
                self.rect.width = 160
                self.rect.height = 70
                if self.direction == "RIGHT":
                    self.current_animation = self.dead_right
                    self.shooting = False
                else:
                    self.current_animation = self.dead_left
                    self.shooting = False
                self.alive = False
        elif jason_attacks and self.boss:
            if self.rect.colliderect(jason_voorhees_rect) and self.life > 0:
                self.life -= 1
            if self.rect.colliderect(jason_voorhees_rect) and self.life == 0:
                self.x = 0
                self.rect.y = self.starting_y + 140
                self.frame = 0
                self.rect.width = 160
                self.rect.height = 70
                if self.direction == "RIGHT":
                    self.current_animation = self.dead_right
                    self.shooting = False
                else:
                    self.current_animation = self.dead_left
                    self.shooting = False
                self.alive = False

    def play_sound(self, mode):
        if not self.alien and mode == "SHOOT":
            if self.shooting and not self.sound_playing:
                self.shooting_sound_effect.set_volume(0.2)
                self.shooting_sound_effect.play(-1)
                self.sound_playing = True
            elif not self.shooting and self.sound_playing:
                self.shooting_sound_effect.stop()
                self.sound_playing = False
        elif self.alien and mode =="SHOOT":
            if self.shooting and not self.sound_playing:
                self.alien_shooting_sound_effect.set_volume(0.2)
                self.alien_shooting_sound_effect.play(-1)
                self.sound_playing = True
            elif not self.shooting and self.sound_playing:
                self.alien_shooting_sound_effect.stop()
                self.sound_playing = False

    def animate_character(self, ms):
        self.time_since_last_frame += ms
        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0

            if (not self.boss) or (self.boss and self.alive):
                if(self.frame < len(self.current_animation) - 1):
                    self.frame += 1
                else: 
                    self.frame = 0
            else:
                if self.frame < len(self.current_animation) - 1:
                    self.frame += 1
                else:
                    self.frame = 4
                
    def move_character(self, ms):
        self.time_since_last_movement += ms
        if self.time_since_last_movement > self.movements_speed:
            self.time_since_last_movement = 0
            self.rect.x += self.x
            self.gun_rect.x += self.x

    def draw_character(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(255,0,0),self.rect)
            pygame.draw.rect(SCREEN,(0,0,255),self.gun_rect)
        self.current_animation_image = self.current_animation[self.frame]
        SCREEN.blit(self.current_animation_image, self.rect)

class Chopper:
    def __init__(self, starting_x, starting_y, movement_amount, folder):
        self.animation = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", folder, False, chopper=True)  
        
        self.frame = 0
        self.current_animation_image = self.animation[self.frame]

        self.rect = self.current_animation_image.get_rect()
        self.starting_y = starting_y
        self.rect.x = starting_x     
        self.rect.y = starting_y

        self.movement_amount = movement_amount
        self.time_since_last_movement = 0

        self.gun_rect = pygame.Rect(self.rect.centerx+85, self.rect.centery+92, 20, 20)
        self.starting_gun_rect_y = self.gun_rect.y
        self.shooting = False
    
    def bounce_helicopter(self, ms):
        self.time_since_last_movement += ms
        if self.time_since_last_movement < 1000:
            self.rect.y -= self.movement_amount
            self.gun_rect.y -= self.movement_amount
            self.frame = 1
            self.shooting = True
        elif self.time_since_last_movement > 1000 and self.time_since_last_movement < 2000:
            self.rect.y += self.movement_amount
            self.gun_rect.y += self.movement_amount
            self.frame = 0
            self.shooting = False
        elif self.time_since_last_movement > 2000:
            self.rect.y = self.starting_y
            self.gun_rect.y = self.starting_gun_rect_y
            self.time_since_last_movement = 0
    
    def draw(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(255,0,0),self.rect)
        self.current_animation_image = self.animation[self.frame]
        SCREEN.blit(self.current_animation_image, self.rect)
        if DEBUG:
            pygame.draw.rect(SCREEN,(0,0,255),self.gun_rect)

class Drone:
    def __init__(self, starting_x, starting_y, movement_amount, animation_speed, folder):
        self.flying = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{folder}/FLYING", False, drone=True)
        self.dying = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{folder}/DESTROYED", False, drone=True)
        
        self.frame = 0
        self.animation = self.flying
        self.current_animation_image = self.animation[self.frame]

        self.rect = self.current_animation_image.get_rect()
        self.starting_y = starting_y
        self.rect.x = starting_x     
        self.rect.y = starting_y

        self.movement_amount = movement_amount
        self.animation_speed = animation_speed
        self.time_since_last_frame = 0
        self.time_since_last_movement = 0

        self.gun_rect = pygame.Rect(self.rect.centerx-20, self.rect.centery+20, 20, 20)
        self.starting_gun_rect_y = self.gun_rect.y
        self.alive = True
        self.shooting = False

        self.exploding_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Drone Exploding.mp3")
    
    def update_and_draw_drone(self, ms, jason_voorhees):
        if self.alive:
            self.bounce_drone(ms)
        self.animate_character(ms, jason_voorhees)
        self.draw()

    def bounce_drone(self, ms):
        self.time_since_last_movement += ms
        if self.time_since_last_movement < 1000:
            self.rect.y -= self.movement_amount
            self.gun_rect.y -= self.movement_amount
            self.shooting = True
        elif self.time_since_last_movement > 1000 and self.time_since_last_movement < 2000:
            self.rect.y += self.movement_amount
            self.gun_rect.y += self.movement_amount
            self.shooting = False
        elif self.time_since_last_movement >= 2000:
            self.rect.y = self.starting_y
            self.gun_rect.y = self.starting_gun_rect_y
            self.time_since_last_movement = 0
    
    def animate_character(self, ms, jason_voorhees):
        self.time_since_last_frame += ms
        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0

            if self.gets_wrecked(jason_voorhees) or not self.alive:
                self.animation = self.dying
                self.alive = False

                if self.frame < len(self.animation) - 1:
                    self.frame += 1
                else:
                    self.rect.y = 5000
                    self.gun_rect.y = 5000
            else:
                if self.frame < len(self.animation) - 1:
                    self.frame += 1
                else:
                    self.frame = 0

    def gets_wrecked(self, jason_voorhees):
        if self.rect.colliderect(jason_voorhees.rect) and jason_voorhees.attacking:
            self.exploding_sound_effect.set_volume(0.2)
            self.exploding_sound_effect.play()
            return True
        else:
            return False

    def draw(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(255,0,0),self.rect)
            pygame.draw.rect(SCREEN,(0,255,255),self.gun_rect)
        self.current_animation_image = self.animation[self.frame]
        SCREEN.blit(self.current_animation_image, self.rect)

class Stink:
    def __init__(self, starting_x, starting_y, movement_amount, movements_speed, animation_speed):
        self.running_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", "STINK\WALKING", False)  
        self.running_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", "STINK\WALKING", True)
        self.dead_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", "STINK\DEAD", False, dead_victim = True)  
        self.dead_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", "STINK\DEAD", True, dead_victim = True)

        self.frame = 0
        self.current_animation = self.running_right
        self.current_animation_image = self.current_animation[self.frame]

        self.rect = self.current_animation_image.get_rect()
        self.rect.x = starting_x     
        self.rect.y = starting_y

        self.movement_amount = movement_amount
        self.movements_speed = movements_speed
        self.animation_speed = animation_speed
        self.x = 0
        self.y = 0
        self.time_since_last_frame = 0
        self.time_since_last_movement = 0

        self.shooting = False
        self.direction = "RIGHT"
        self.alive = True

    def run(self, direction):
        if direction == "RIGHT":
            self.current_animation = self.running_right
            self.direction = "RIGHT"
            self.x = self.movement_amount

        else:
            self.current_animation = self.running_left
            self.direction = "LEFT"
            self.x = -self.movement_amount

    def update_character(self, ms, jason_voorhees_rect, jason_attacks, invisible_rects):
        self.auto_control_enemy(invisible_rects)
        self.collides_with_jason(jason_voorhees_rect, jason_attacks)
        self.animate_character(ms)
        self.move_character(ms)
        
    def auto_control_enemy(self, invisible_rects):
        if self.alive == True:
            if self.direction == "RIGHT" and self.collides_with_any(invisible_rects):
                self.run(direction="LEFT")
                self.rect.x -= 30
            elif self.direction == "LEFT" and self.collides_with_any(invisible_rects):
                self.run(direction="RIGHT")
                self.rect.x += 30
            elif self.direction == "RIGHT" and not self.collides_with_any(invisible_rects):
                self.run(direction="RIGHT")
                # print("No colisiona y se mueve a la derecha")
            elif self.direction == "LEFT" and not self.collides_with_any(invisible_rects):
                self.run(direction="LEFT")
                # print("No colisiona y se mueve a la izquierda")

    def collides_with_any(self, invisible_rects):
        for rect in invisible_rects:
            if self.rect.colliderect(rect):
                return True
        return False

    def collides_with_jason(self, jason_voorhees_rect, jason_attacks):
        if jason_attacks:
            if self.rect.colliderect(jason_voorhees_rect):
                self.x = 0
                self.rect.y = 600
                self.frame = 0
                self.rect.width = 160
                self.rect.height = 70
                if self.direction == "RIGHT":
                    self.current_animation = self.dead_right
                else:
                    self.current_animation = self.dead_left
                self.alive = False

    def animate_character(self, ms):
        self.time_since_last_frame += ms
        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0

            if(self.frame < len(self.current_animation) - 1):
                self.frame += 1
            else: 
                self.frame = 0

    def move_character(self, ms):
        self.time_since_last_movement += ms
        if self.time_since_last_movement > self.movements_speed:
            self.time_since_last_movement = 0
            self.rect.x += self.x

    def draw_character(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(255,0,0),self.rect)
        self.current_animation_image = self.current_animation[self.frame]
        SCREEN.blit(self.current_animation_image, self.rect)

class AlienQueen:
    def __init__(self, starting_x, starting_y, movement_amount, movements_speed, animation_speed, subfolder, alien_queen=False, michael_myers=False):
        #CHARACTER STATUS
        self.walk_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\WALKING", False, alien_queen=alien_queen, michael_myers=michael_myers)
        self.walk_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\WALKING", True, alien_queen=alien_queen, michael_myers=michael_myers)  
        self.attack_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\ATTACKING", False, alien_queen=alien_queen, michael_myers=michael_myers)  
        self.attack_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\ATTACKING", True, alien_queen=alien_queen, michael_myers=michael_myers)   
        self.dead_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\DEAD", False, dead_victim = True, alien_queen=alien_queen, michael_myers=michael_myers)  
        self.dead_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", f"{subfolder}\DEAD", True, dead_victim = True, alien_queen=alien_queen, michael_myers=michael_myers)

        #CHARACTER ANIMATION
        self.frame = 0
        self.current_animation = self.walk_left
        self.current_animation_image = self.current_animation[self.frame]

        #CHARACTER RECT
        self.rect = self.current_animation_image.get_rect()
        self.rect.x = starting_x     
        self.rect.y = starting_y
        self.starting_y = starting_y

        #CONTROLLING CHARACTER
        self.movement_amount = movement_amount
        self.movements_speed = movements_speed
        self.animation_speed = animation_speed
        self.x = 0
        self.y = 0
        self.time_since_last_frame = 0
        self.time_since_last_movement = 0

        #CHARACTER FEATURES
        self.attacking = False
        self.shooting = False
        self.direction = "LEFT"
        self.alive = True
        self.life = 500
        self.michael_myers = michael_myers

        self.attacking_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Alien Queen Attack.mp3")
        self.sound_playing = True

    def walk(self, direction):
        self.attacking = False

        #CHOOSING CURRENT ANIMATION ACCORDING TO CURRENT DIRECTION
        if direction == "RIGHT":
            self.current_animation = self.walk_right
            self.x = self.movement_amount
            self.direction = "RIGHT"
        else:
            self.current_animation = self.walk_left
            self.x = -self.movement_amount
            self.direction = "LEFT"

    def attack(self, direction):
        self.attacking = True
        
        #IF CHARACTER WASN'T ALREADY ATTACKING
        if self.current_animation != self.attack_right and self.current_animation != self.attack_left:
            self.frame = 0 #RESETTING FRAME
        
        #CHOOSING CURRENT ANIMATION ACCORDING TO CURRENT DIRECTION
        if direction == "RIGHT":
            self.current_animation = self.attack_right
            self.x = 0
            self.direction = "RIGHT"
        else:
            self.current_animation = self.attack_left
            self.x = 0
            self.direction = "LEFT"

    def update_character(self, ms, jason_voorhees_rect, jason_attacks, invisible_rects):
        self.auto_control_enemy(jason_voorhees_rect, invisible_rects)
        self.collides_with_jason(jason_voorhees_rect, jason_attacks)
        self.animate_character(ms)
        self.move_character(ms)
        self.play_sound()
        
    def auto_control_enemy(self, jason_voorhees_rect, invisible_rects):
        if self.alive == True:
            if self.rect.x > jason_voorhees_rect.x and self.rect.x - jason_voorhees_rect.x < SCREEN_WIDTH/8 and self.rect.y - jason_voorhees_rect.y < jason_voorhees_rect.height:
                self.attack(direction="LEFT")
            elif self.rect.x < jason_voorhees_rect.x and jason_voorhees_rect.x - self.rect.x < SCREEN_WIDTH/8 and self.rect.y - jason_voorhees_rect.y < jason_voorhees_rect.height:
                self.attack(direction="RIGHT")
            else:
                if self.direction == "RIGHT" and self.collides_with_any(invisible_rects):
                    self.walk(direction="LEFT")
                    self.rect.x -=30
                elif self.direction == "LEFT" and self.collides_with_any(invisible_rects):
                    self.walk(direction="RIGHT")
                    self.rect.x +=30
                elif self.direction == "RIGHT" and not self.collides_with_any(invisible_rects):
                    self.walk(direction="RIGHT")
                elif self.direction == "LEFT" and not self.collides_with_any(invisible_rects):
                    self.walk(direction="LEFT")

    def collides_with_any(self, invisible_rects):
        for rect in invisible_rects:
            if self.rect.colliderect(rect):
                return True
        return False
    
    def collides_with_jason(self, jason_voorhees_rect, jason_attacks):
        if jason_attacks:
            if self.rect.colliderect(jason_voorhees_rect) and self.life > 0:
                self.life -= 1
            if self.rect.colliderect(jason_voorhees_rect) and self.life == 0:
                self.x = 0
                if not self.michael_myers:
                    self.rect.y = self.starting_y + 180
                else:
                    self.rect.y = self.starting_y + 140
                self.frame = 0
                self.rect.width = 160
                self.rect.height = 70
                if self.direction == "RIGHT":
                    self.current_animation = self.dead_right
                    self.shooting = False
                else:
                    self.current_animation = self.dead_left
                    self.shooting = False
                self.alive = False
                self.attacking = False

    def animate_character(self, ms):
        self.time_since_last_frame += ms
        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0

            if self.alive:
                if(self.frame < len(self.current_animation) - 1):
                    self.frame += 1
                else: 
                    self.frame = 0
            else:
                self.frame = 0
                
    def play_sound(self):
        if self.alive:
            if self.attacking and not self.sound_playing:
                self.attacking_sound_effect.set_volume(0.2)
                self.attacking_sound_effect.play(-1)
                self.sound_playing = True
            elif not self.attacking and self.sound_playing:
                self.attacking_sound_effect.stop()
                self.sound_playing = False
        else:
            self.attacking_sound_effect.stop()
             
    def move_character(self, ms):
        self.time_since_last_movement += ms
        if self.time_since_last_movement > self.movements_speed:
            self.time_since_last_movement = 0
            self.rect.x += self.x

    def draw_character(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(255,0,0),self.rect)
        self.current_animation_image = self.current_animation[self.frame]
        SCREEN.blit(self.current_animation_image, self.rect)

class Taxi:
    def __init__(self, starting_x, starting_y, movement_amount, movements_speed, animation_speed):
        #CHARACTER STATUS
        self.drive_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", "TAXI", True, taxi=True)
        self.drive_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", "TAXI", False, taxi=True)  

        #CHARACTER ANIMATION
        self.frame = 0
        self.current_animation = self.drive_right
        self.current_animation_image = self.current_animation[self.frame]

        #CHARACTER RECT
        self.rect = self.current_animation_image.get_rect()
        self.rect.x = starting_x     
        self.rect.y = starting_y

        #CONTROLLING CHARACTER
        self.movement_amount = movement_amount
        self.movements_speed = movements_speed
        self.animation_speed = animation_speed
        self.x = 0
        self.y = 0
        self.time_since_last_frame = 0
        self.time_since_last_movement = 0

        #CHARACTER FEATURES
        self.direction = "LEFT"
        self.shooting = False
        self.driving= True

        self.sound_playing = True
        self.boss = False
        self.taxi_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Taxi.mp3")

    def drive(self, direction):
        #CHOOSING CURRENT ANIMATION ACCORDING TO CURRENT DIRECTION
        if direction == "RIGHT":
            self.current_animation = self.drive_right
            self.x = self.movement_amount
            self.direction = "RIGHT"
        else:
            self.current_animation = self.drive_left
            self.x = -self.movement_amount
            self.direction = "LEFT"

    def update_character(self, ms, invisible_rects, traffic_light):
        self.auto_control_enemy(invisible_rects)
        self.animate_character(ms, traffic_light)
        self.move_character(ms, traffic_light)
        self.play_sound()
        
    def auto_control_enemy(self, invisible_rects):
        if self.direction == "RIGHT" and self.collides_with_any(invisible_rects):
            self.drive(direction="LEFT")
            self.rect.x -=30
        elif self.direction == "LEFT" and self.collides_with_any(invisible_rects):
            self.drive(direction="RIGHT")
            self.rect.x +=30
        elif self.direction == "RIGHT" and not self.collides_with_any(invisible_rects):
            self.drive(direction="RIGHT")
        elif self.direction == "LEFT" and not self.collides_with_any(invisible_rects):
            self.drive(direction="LEFT")

    def collides_with_any(self, invisible_rects):
        for rect in invisible_rects:
            if self.rect.colliderect(rect):
                return True
        return False

    def play_sound(self):
        if not self.driving and not self.sound_playing and not self.boss:
            self.taxi_sound_effect.set_volume(0.03)
            self.taxi_sound_effect.play(-1)
            self.sound_playing = True
        elif self.driving and self.sound_playing:
            self.taxi_sound_effect.stop()
            self.sound_playing = False

    def animate_character(self, ms, traffic_light):
        self.time_since_last_frame += ms
        if self.time_since_last_frame > self.animation_speed and not traffic_light.red:
            self.time_since_last_frame = 0
            if(self.frame < len(self.current_animation) - 1):
                self.frame += 1
            else: 
                self.frame = 0

    def move_character(self, ms, traffic_light):
        self.driving = False
        self.time_since_last_movement += ms
        if self.time_since_last_movement > self.movements_speed and not traffic_light.red:
            self.time_since_last_movement = 0
            self.rect.x += self.x
            self.driving = True

    def draw_character(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(255,0,0),self.rect)
        self.current_animation_image = self.current_animation[self.frame]
        SCREEN.blit(self.current_animation_image, self.rect)

class UFO:
    def __init__(self, starting_x, starting_y, movement_amount, movements_speed):
        self.flying = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", "UFO/FLYING", False, ufo=True)
        self.abducting = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", "UFO/ABDUCTING", False, ufo=True)

        #CHARACTER ANIMATION
        self.current_animation = self.flying[0]
        self.current_animation_image = self.current_animation

        #CHARACTER RECT
        self.rect = self.current_animation_image.get_rect()
        self.rect.x = starting_x     
        self.rect.y = starting_y
        self.space_ship_rect = pygame.Rect(self.rect.centerx, self.rect.y+50, 70, 70)

        #CONTROLLING CHARACTER
        self.movement_amount = movement_amount
        self.movements_speed = movements_speed
        self.y = 0
        self.time_since_last_movement = 0

        #CHARACTER FEATURES
        self.abduct = False
        self.sound_playing = True
        self.abduction_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Abduction.mp3")

    def update_and_draw_character(self, ms):
        self.auto_control_enemy()
        self.move_character(ms)
        self.draw_character()
        
    def auto_control_enemy(self):
        if self.rect.y < 100:
            self.y = self.movement_amount
            self.abduct = False
        else:
            self.y = 0
            self.abduct = True
            self.current_animation = self.abducting[0]
            self.abduction_sound_effect.set_volume(0.2)
            self.abduction_sound_effect.play()

    def move_character(self, ms):
        self.time_since_last_movement += ms
        if self.time_since_last_movement > self.movements_speed:
            self.time_since_last_movement = 0
            self.rect.y += self.y
            self.space_ship_rect.y += self.y

    def draw_character(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(255,0,0),self.rect)
            pygame.draw.rect(SCREEN,(0,0,255),self.space_ship_rect)
        self.current_animation_image = self.current_animation
        SCREEN.blit(self.current_animation_image, self.rect)