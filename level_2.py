import pygame
import sys
from music import play_music
from creating_level import *
from background_scrolling import *
from main_character import *
from auxiliar import *
import graphic_user_interface
from final_battle import *
from bullets import *
import items


def level_2(player_name, score=None):
    #---------------------------------------------READING AND CREATING LEVEL--------------------------------------------------------
    #READING LEVEL
    level = read_json(level="level_2")

    #CREATING LEVEL FROM JSON FILE
    play_music(level=level["level"], boss=False)
    background_images = create_background_images(level=level["level"],image_amount=level["background_image"]["image_amount"])

    platform_objects_list = []
    item_object_list = []
    npc_list = []
    bullet_list = []

    jason_voorhees = JasonVoorhees(starting_x=level["jason_voorhees"]["starting_x"], starting_y=level["jason_voorhees"]["starting_y"], 
                                movement_amount=level["jason_voorhees"]["movement_amount"], movements_speed=level["jason_voorhees"]["movements_speed"], 
                                animation_speed=level["jason_voorhees"]["animation_speed"], jump_power=level["jason_voorhees"]["jump_power"], 
                                jump_height = level["jason_voorhees"]["jump_height"])

    create_npc(drones=level["enemies"]["drone"], aliens=level["enemies"]["alien"], npc_list=npc_list)
    create_items(beers= level["items"]["beer"], coins=level["items"]["coin"],spinning_saws=level["items"]["orb"] ,buttons=level["items"]["button"], force_fields=level["items"]["force_field"], item_object_list=item_object_list)
    create_platforms(lava_or_spikes=level["platforms"]["lava_or_spikes"], 
                        towers=level["platforms"]["tower"], floatings=level["platforms"]["floating_platform"], platform_objects_list=platform_objects_list)
    
    #OTHER:
    fps = level["fps"]
    side_platform_rects = get_side_platform_rects(platform_objects_list)
    invisible_rects = create_invisible_rect_for_npcs_collision(invisible_rects=level["other"]["invisible_rects"])
    force_field_button = None

    #---------------------------------------------------------------GAME LOOP----------------------------------------------------------------
    #TIMER
    event_1000ms = pygame.USEREVENT
    pygame.time.set_timer(event_1000ms, 1000)
    remaining_time = 90

    enemy_death_time = None
    time_since_death = 0

    #MAIN FLAGS
    scroll = True
    paused = False

    scrolling_x = 0
    jason_voorhees.score = score

    while True:
        #-----------------------------------------------------EVENTS----------------------------------------------------
        time = CLOCK.tick(fps)
        minutes = remaining_time // 60
        seconds = remaining_time % 60

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == event_1000ms:
                if not paused:
                    remaining_time -= 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if graphic_user_interface.pause_button.is_clicked(event.pos):
                    paused = True
                if graphic_user_interface.resume_button.is_clicked(event.pos):
                    paused = False
                if graphic_user_interface.back_to_menu.is_clicked(event.pos):
                    pygame.mixer.music.stop()
                    paused = False
                    graphic_user_interface.draw_menu()

        #CHECKING IF GAME IS PAUSED
        if paused:
            graphic_user_interface.show_pause_screen()
        else:
            pressed_keys = pygame.key.get_pressed()
            
            #----------------------------------------------------SCROLLING-------------------------------------------------
            if jason_voorhees.rect.x < SCREEN_WIDTH-120 and scroll:
                #SI ME ESTOY MOVIENDO HACIA LA DERECHA Y SCROLEE MENOS DE 250:
                if jason_voorhees.x > 0 and scrolling_x < MAP_LENGHT: #EN ESTE CASO SE PUEDE CONSIDERAR A 250 COMO LA LONGITUD DEL MAPA
                    scrolling_x += 1.5 #MUEVO EL FONDO PARA LA IZQUIERDA
                    scroll_items_and_platforms(mode="SCROLL LEFT", platform_list=platform_objects_list, item_list=item_object_list, enemy_list=npc_list, invisible_rect = invisible_rects, bullet_list=bullet_list)
                #SI ME ESTOY MOVIENDO HACIA LA DERECHA Y SCROLEE MENOS DE 250:
                if (jason_voorhees.x < 0 and (jason_voorhees.rect.x > 5)) and scrolling_x > 0:
                    scrolling_x -= 1.5
                    scroll_items_and_platforms(mode="SCROLL RIGHT", platform_list=platform_objects_list, item_list=item_object_list, enemy_list=npc_list, invisible_rect = invisible_rects, bullet_list=bullet_list)
                if jason_voorhees.x == 0:
                    scrolling_x += 0
                    scroll_items_and_platforms(mode="DON'T SCROLL", platform_list=platform_objects_list, item_list=item_object_list, enemy_list=npc_list, invisible_rect = invisible_rects, bullet_list=bullet_list)
            elif scroll:
                scrolling_x = 0
                scroll = False
                set_final_battle(jason_voorhees, level, invisible_rects, npc_list)

            #--------------------------------------------UPDATING AND BLITING----------------------------------------------------------
            #BACKGROUND:
            draw_bg(background_images, scrolling_x)

            #PLATFORMS:
            for platform in platform_objects_list:
                platform.update_and_draw_platform(side_platform_rects)

            #ITEMS:
            for item in item_object_list:
                if type(item) == items.Item:
                    item.draw_item()
                if type(item) == AnimatedItem:
                    if not item.force_field:
                        item.animate_and_draw_item(ms=time, jason_voorhees=jason_voorhees, pressed_key=pressed_keys)
                        if item.button:
                            force_field_button = item
                    else:
                        item.animate_and_draw_item(ms=time, jason_voorhees=jason_voorhees, pressed_key=pressed_keys, force_field_button=force_field_button)

            #INVISIBLE RECTS
            for rect in invisible_rects:
                if DEBUG:
                    pygame.draw.rect(SCREEN,(255,0,0),rect)

            #ENEMIES
            for enemy in npc_list:
                if type(enemy) == Drone:
                    enemy.update_and_draw_drone(ms=time, jason_voorhees=jason_voorhees)
                else:
                    enemy.update_character(ms=time, jason_voorhees_rect=jason_voorhees.rect, jason_attacks = jason_voorhees.attacking, invisible_rects=invisible_rects)
                    enemy.draw_character()

                if type(enemy) == AlienQueen:
                    if enemy.rect.x < SCREEN_WIDTH-500:
                        new_invisible_rect = pygame.Rect(SCREEN_WIDTH-10, 0, 20, SCREEN_HEIGHT)
                        invisible_rects.append(new_invisible_rect)
                    
                    #CONTROLLING TIME AFTER BOSS DEATH
                    if enemy.alive == False and enemy_death_time is None:
                        enemy_death_time = pygame.time.get_ticks()
                        
                    if enemy_death_time is not None:
                        time_since_death = pygame.time.get_ticks() - enemy_death_time
                    
                    if time_since_death >= 3000:
                        graphic_user_interface.show_next_level(3, player_name, jason_voorhees.score)
            
            #BULLETS
            shoot_bullet(npc_list, item_object_list, bullet_list, level["other"]["bullet"]["folder"])
            for bullet in bullet_list:
                bullet.update()
                bullet.draw()

            #MAIN CHARACTER
            jason_voorhees.check_events_and_set_parameters(pressed_keys)
            jason_voorhees.update_and_draw_character(ms = time, platform_list = platform_objects_list, item_list=item_object_list, npc_list = npc_list, bullet_list=bullet_list)
    
            #DEATH OR TIME RUNS OUT
            if jason_voorhees.life < 1 or remaining_time < 1:
                graphic_user_interface.show_death_screen(level=2, score=jason_voorhees.score, player_name=player_name)

            #DISPLAYS
            life = FONT.render(f"HEALTH: {int(jason_voorhees.life)}", True, (150,0,0))
            score = FONT.render(f"SCORE: {jason_voorhees.score}", True, (150,0,0))
            time_display = FONT.render(f"TIME: {minutes:02d}:{seconds:02d}", True, (150,0,0))
            SCREEN.blit(life, (10,10))
            SCREEN.blit(score, (10,70))
            SCREEN.blit(time_display, (900,10))
            graphic_user_interface.pause_button.draw()

            pygame.display.flip()