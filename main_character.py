import pygame
from config import *
from auxiliar import get_surface_list_from_sprite_images_and_scale_them
from items import AnimatedItem
from NPCs import AlienQueen, Taxi, Chopper

class JasonVoorhees:
    def __init__(self, starting_x, starting_y, movement_amount, movements_speed, animation_speed, jump_power, jump_height):
        #CHARACTER STATUS
        self.stand_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS", "JASON\STANDING", False)  
        self.stand_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS","JASON\STANDING", True)
        self.walk_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS","JASON\WALKING", False)  
        self.walk_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS","JASON\WALKING", True)  
        self.jump_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS","JASON\JUMPING", False)  
        self.jump_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS","JASON\JUMPING", True)     
        self.attacking_right = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS","JASON\ATTACKING", False, jason_attacking=True)
        self.attacking_left = get_surface_list_from_sprite_images_and_scale_them("CHARACTERS","JASON\ATTACKING", True, jason_attacking=True)

        #CHARACTER ANIMATION
        self.frame = 0
        self.current_animation = self.stand_right
        self.current_animation_image = self.current_animation[self.frame]
        self.animation_speed = animation_speed

        #CHARACTER RECT
        self.rect = self.current_animation_image.get_rect()
        self.rect.x = starting_x     
        self.rect.y = starting_y
        self.foot_rect = pygame.Rect(self.rect.x+5, self.rect.y + self.rect.height-self.rect.height/8, self.rect.width-20, self.rect.height/8)

        #CONTROLLING CHARACTER
        self.movement_amount = movement_amount
        self.movements_speed = movements_speed
        self.x = 0
        self.y = 0
        self.time_since_last_frame = 0
        self.time_since_last_movement = 0
        self.jump_power = jump_power
        self.starting_jumping_point = 0
        self.jump_height = jump_height
        self.gravity = 10
        
        #CHARACTER FEATURES
        self.direction = "RIGHT"
        self.is_jumping = True
        self.attacking = True
        self.life = 100
        self.score = 0
        self.abducted = False

        #SOUNDS
        self.sound_playing = True
        self.machete_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Machete.mp3")
        self.increase_life_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Increase Life.mp3")
        self.increase_score_sound_effect = pygame.mixer.Sound("SOUNDTRACK/SPECIAL FX/Increase Score.mp3")

    #CONTROLLING CHARACTER----------------------------------------------------------------------------------------
    def check_events_and_set_parameters(self, pressed_keys):
        if pressed_keys[pygame.K_a] and not pressed_keys[pygame.K_d] and not pressed_keys[pygame.K_SPACE] and not pressed_keys[pygame.K_j]:
            self.walk("LEFT")
        elif not pressed_keys[pygame.K_a] and pressed_keys[pygame.K_d] and not pressed_keys[pygame.K_SPACE] and not pressed_keys[pygame.K_j]:
            self.walk("RIGHT")
        elif pressed_keys[pygame.K_SPACE]:
            #WHEN SPACEBAR IS GETTING PRESSED IT ENABLES JUMPING
            self.jump(True)
        elif (pressed_keys[pygame.K_j] or (pressed_keys[pygame.K_j] and (pressed_keys[pygame.K_a] or pressed_keys[pygame.K_d]))):
            self.attack()
        else:
            self.stand()

    def jump(self, available):
        #IF I ENABLED JUMPING AND THE CHARACTER IS NOT ALREADY JUMPING
        if available == True and self.is_jumping == False:
            #SAVING STARTING JUMPING POINT
            self.starting_jumping_point = self.rect.y

            #CHOOSING CURRENT ANIMATION ACCORDING TO CURRENT DIRECTION
            if self.direction == "RIGHT":
                self.current_animation = self.jump_right
            else:
                self.current_animation = self.jump_left
            
            #RESETTING FRAME, ENABLING VERTICAL MOVEMENT THEN CHANGING JUMPING FLAG
            self.frame = 0
            self.y = -self.jump_power
            self.is_jumping = True
        
        #IF I DISABLED JUMPING
        elif available == False:
            self.is_jumping = False #CHANGING JUMPING FLAG
            self.stand() #MAKING CHARACTER STAND
            
    def stand(self):
        self.attacking = False

        #IF THE CHARACTER WASN'T ALREADY JUMPING
        if(self.current_animation != self.stand_right and self.current_animation != self.stand_left):
            self.frame = 0 #RESETTING FRAME
            
            #STOPPING MOVEMENT
            self.x = 0
            self.y = 0 

            #CHOOSING CURRENT ANIMATION ACCORDING TO CURRENT DIRECTION
            if self.direction == "RIGHT":
                self.current_animation = self.stand_right
            else:
                self.current_animation = self.stand_left
                
    def walk(self, direction):
        self.attacking = False

        #IF CHARACTER WASN'T ALREADY WALKING, OR IT CHANGES DIRECTION
        if (self.direction != direction) or (self.current_animation != self.walk_right and self.current_animation != self.walk_left):
            self.frame = 0 #RESETTING FRAME

            #CHOOSING CURRENT ANIMATION ACCORDING TO CURRENT DIRECTION, THEN CHANGING DIRECTION
            if direction == "RIGHT":
                self.direction = "RIGHT"
                self.current_animation = self.walk_right
                self.x = self.movement_amount
            else:
                self.direction = "LEFT"
                self.current_animation = self.walk_left
                self.x = -self.movement_amount

    def attack(self):
        self.x = 0 #STOPPING CHARACTER FROM MOVING

        #IF CHARACTER WASN'T ALREADY ATTACKING
        if(self.current_animation != self.attacking_right and self.current_animation != self.attacking_left):
            #RESETTING FRAME AND CHANGING ATTACKING FLAG
            self.frame = 0
            self.attacking = True 

            #CHOOSING CURRENT ANIMATION ACCORDING TO CURRENT DIRECTION
            if self.direction == "RIGHT":
                self.current_animation = self.attacking_right
            else:
                self.current_animation = self.attacking_left

    #UPDATING AND DRAWING CHARACTER------------------------------------------------------------------------------------------
    def update_and_draw_character(self, ms, platform_list, item_list, npc_list, bullet_list, ufo=None):
        self.animate_character(ms, ufo)
        self.move_character(ms, platform_list, ufo)
        self.collides_with_something(platform_list, item_list, bullet_list, npc_list)
        self.draw_character()
        self.play_sound("ATTACK")
        
    def animate_character(self, ms, ufo):
        if not ufo:
            self.time_since_last_frame += ms #ACCUMULATING TIME

            #IF ACCUMULATED TIME IS GREATER THAN 'ANIMATION SPEED'
            if self.time_since_last_frame > self.animation_speed:
                self.time_since_last_frame = 0 #RESETTING 'TIME SINCE LAST FRAME'

                #CHANGING CURRENT FRAME
                if(self.frame < len(self.current_animation) - 1):
                    self.frame += 1 
                else: 
                    self.frame = 0

    def move_character(self, ms, platform_list, ufo=None):
        self.time_since_last_movement += ms #ACCUMULATING TIME

        #IF ACCUMULATED TIME IS GREATER THAN 'MOVEMENTS SPEED'
        if self.time_since_last_movement > self.movements_speed:
            if not ufo:
                self.time_since_last_movement = 0 #RESETTING 'TIME SINCE LAST MOVEMENT'

                #CONTROLLING JUMPING FEATURE: IF 'Y MOVEMENT' IS GREATER THAN ACTUAL 'JUMP HEIGHT' AND THE CHARACTER IS JUMPING
                if(self.starting_jumping_point - self.rect.y > self.jump_height and self.is_jumping):
                    self.y = 0 #DISABLING FURTHER VERTICAL MOVEMENT

                #ACTUALLY MOVING CHARACTER'S RECT:
                #MOVING 'X COORDINATE':
                if self.x < 0:                       #IF STATEMENTS TO NOT LET CHARACTER GET OUT OF SCREEN
                    if self.rect.x - self.x < 0:
                        self.rect.x = 0
                        self.foot_rect.x = 0
                    else:
                        self.rect.x += self.x
                        self.foot_rect.x += self.x
                elif self.x > 0:
                    if self.rect.x + self.rect.width + self.x > SCREEN_WIDTH:
                        self.rect.x = SCREEN_WIDTH - self.rect.width
                        self.foot_rect.x = SCREEN_WIDTH - self.rect.width
                    else:
                        self.rect.x += self.x
                        self.foot_rect.x += self.x

                #MOVING 'Y COORDINATE':
                self.rect.y += self.y
                if self.is_jumping:
                    self.foot_rect.y += self.y

                #IF RECT IS NOT ON A PLATFORM (IT'S ON AIR)
                if not self.on_platform(platform_list):
                    #USING GRAVITY TO MOVE INCREASE 'Y COORDINATE'
                    self.rect.y += self.gravity
                    self.foot_rect.y += self.gravity 
                #IF RECT IS ON A PLATFORM (IT' NOT ON AIR) AND WAS JUMPING
                elif self.is_jumping:
                    #DISABLE JUMPING
                    self.jump(False)
            else:
                if not ufo.abduct:
                    self.attacking = False
                    self.current_animation = self.stand_right
                    self.x = 0
                    self.y = 0
                else:
                    self.x = 0
                    self.rect.y -= 3
    
    def on_platform(self, platform_list):
        #IF IT'S ON A EQUAL OR GREATER 'Y COORDINATE' THAN GROUND LEVEL
        if self.rect.y >= GROUND_LEVEL:
            return True #IS ON A PLATFORM
        else:
            for platform in platform_list:
                #IF PLATFORM HAS A TOP_RECT:
                #CHECKING IF CHARACTER IS STANDING ON IT
                if platform.top_rect != None:
                    if self.foot_rect.colliderect(platform.top_rect):
                        return True
            return False

    def collides_with_something(self, platform_list, item_list, bullet_list, npc_list):
        #PLATFORMS----------------------------------------------
        for platform in platform_list:
            # IF PLATFORM HAS A LEFT RECT
            if platform.left_rect != None:
                if self.direction == "RIGHT" and self.rect.colliderect(platform.left_rect):
                    self.x = 0 #STOP MOVEMENT
            # IF PLATFORM HAS A RIGH RECT
            if platform.right_rect != None:
                if self.direction == "LEFT" and self.rect.colliderect(platform.right_rect):
                    self.x = 0 #STOP MOVEMENT
            # IF PLATFORM IS DAMAGING
            if platform.damaging:
                if self.foot_rect.colliderect(platform.rect):
                    self.life -= 500 
        
        #ITEMS---------------------------------------------------
        for item in item_list:
            #IF ITEM IS NOT ANIMATED
            if type(item) != AnimatedItem:
                #IF ITEM INCREASES LIFE
                if item.increase_life:
                    if self.rect.colliderect(item.rect):
                        self.life += 500
                        item.rect.x += 15000
                        self.play_sound("LIFE")
                #IF ITEM INCREASES SCORE
                elif item.increase_score:
                    if self.rect.colliderect(item.rect):
                        self.score += 2
                        item.rect.x += 15000
                        self.play_sound("COIN")
            #IF ITEM IS ANIMATED
            else:
                if item.damaging:
                    if not item.force_field:
                        if self.rect.colliderect(item.rect):
                            self.life -= 1
                    else:
                        if self.rect.colliderect(item.rect):
                            self.life -= 1000
        
        #BULLETS----------------------------------------------------
        for bullet in bullet_list:
            if self.rect.colliderect(bullet.rect):
                    self.life -= 0.01
        
        #NPCs--------------------------------------------------------
        for npc in npc_list:
            if type(npc) == AlienQueen:
                if self.rect.colliderect(npc.rect) and npc.attacking:
                    self.life -= 0.1
            if type(npc) == Taxi:
                if self.rect.colliderect(npc.rect) and npc.driving:
                    self.life -= 1
        
        if self.attacking:
            for npc in npc_list:
                if self.rect.colliderect(npc.rect) and type(npc) != Chopper and npc.alive :
                    self.score += 1

    def play_sound(self, mode):
        if mode == "ATTACK":
            if self.attacking and not self.sound_playing:
                self.machete_sound_effect.set_volume(0.2)
                self.machete_sound_effect.play(-1)
                self.sound_playing = True
            elif not self.attacking and self.sound_playing:
                self.machete_sound_effect.stop()
                self.sound_playing = False
        
        if mode == "LIFE":
            self.increase_life_sound_effect.set_volume(0.2)
            self.increase_life_sound_effect.play()
        
        if mode == "COIN":
            self.increase_score_sound_effect.set_volume(0.2)
            self.increase_score_sound_effect.play()

    def draw_character(self):
        if DEBUG:
            pygame.draw.rect(SCREEN,(255,0,0),self.rect)
            pygame.draw.rect(SCREEN,(0,0,255),self.foot_rect)
        self.current_animation_image = self.current_animation[self.frame]
        SCREEN.blit(self.current_animation_image, self.rect)
