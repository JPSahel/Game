import pygame
import sys
import traceback
from ui import UI
from spritesheet import SpriteSheet
from entity import Entity

import random
try:
    pygame.init()
    clock = pygame.time.Clock()
    

    # Load Assets
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Insert Name")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    colors = {"WHITE": WHITE, "BLACK": BLACK}

    # Background images
    background_image = pygame.image.load("Assets/background/city1.png").convert()

    # UI ASSETS
    button_map = pygame.image.load("Assets/buttons/ButtonMap1.png").convert()
    textbox_image = pygame.image.load("Assets/ui/textbox.png").convert_alpha()

    player=pygame.image.load("Assets/character/anim_list.png").convert_alpha()
    spritesheet_character = SpriteSheet(player)

    opponent = pygame.image.load("Assets/enemies/anim_list.png").convert_alpha()
    spritesheet_opponent = SpriteSheet(opponent)
    # Fonts
    title_font = pygame.font.Font("Assets/fonts/joystix_monospace.otf", 28)
    button_font = pygame.font.Font("Assets/fonts/joystix_monospace.otf", 18)




    # Constants
    BUTTON_WIDTH = 192
    BUTTON_HEIGHT = 64

    # UI class
    ui = UI(screen, button_font, BUTTON_WIDTH, BUTTON_HEIGHT, colors)
    textbox_image = pygame.image.load("Assets/ui/textbox.png").convert_alpha()

    # Initialize button positions and states
    start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
    basic_button_rect = pygame.Rect(50,400,BUTTON_WIDTH,BUTTON_HEIGHT)
    power_button_rect = pygame.Rect(50,500,BUTTON_WIDTH,BUTTON_HEIGHT)
    heal_button_rect = pygame.Rect(50,600,BUTTON_WIDTH,BUTTON_HEIGHT)
    #basic_button_rect =pygame.Rect
    start_state = "normal"
    exit_state = "normal"
    basic_state ="normal"
    power_state ="normal"
    heal_state ="normal"

    button_textures = ui.slice_button_map(button_map, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Assign button textures
    normal_texture = button_textures[0]  # Normal state
    hovered_texture = button_textures[1]  # Hovered state
    clicked_texture = button_textures[2]  # Clicked state
    textures = {"normal": normal_texture, "hovered": hovered_texture, "clicked": clicked_texture}

    attacks = {"basic": "basic", "power": "power", "heal":"heal", "special":"special"}


    # Game State
    game_state = "menu"

    def get_image(sheet,frame,width,height, scale):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame*width), 0, width, height))
        image = pygame.transform.scale(image,(width*scale,height*scale))
        image.set_colorkey((0,0,0))
        return image
    

    #Create animation list for character
    animation_list =[]
    animation_steps = [6,8,8,11,13,3,4]
    action = 0# 0 is idle/ 1 is running / 2 is attack / 3 is heal / 4 is special
    last_update = pygame.time.get_ticks()
    animation_cooldown = 250
    frame = 0
    step_counter = 0
    for animation in animation_steps:
        tmp_img_list = []
        for _ in range(animation):
            tmp_img_list.append(spritesheet_character.get_image(step_counter,128,128,3))
            step_counter += 1
        animation_list.append(tmp_img_list)
    
    
    #Create animation list for Opponent
    animation_list_opp = []
    action_opp = 0
    frame_opp = 0
    last_update_opp = pygame.time.get_ticks()
    step_count_opp = 0
    animation_cooldown_opp = 250

    for animation in animation_steps:
        tmp_img_list = []
        for _ in range(animation):
            img_unflip = spritesheet_opponent.get_image(step_count_opp,128,128,3)
            flipped = pygame.transform.flip(img_unflip, True, False).convert_alpha()
            tmp_img_list.append(flipped)
            step_count_opp += 1
        animation_list_opp.append(tmp_img_list)

    main_chara = Entity(100,"alive",10)
    opponent = Entity(100,"alive",10)
    turn = True
    #Dialouge Textbox 
    dialogues = ["Here is a Demo of a Turn-Based RPG on Pygame", "You have three abilities, Attack, Power attack and heal. You can attack for normal damage, Power Attacks Deal tripple for the cost of your health ", "and heal to recover a small amount of hp Enjoy"]
    dialogue_index = 0
    show_textbox = True
    running = True
### Turn Timer

    animation_done = False
    turncomplete = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #print(mouse_x,mouse_y)
        for event in pygame.event.get():
            #print(mouse_x,mouse_y)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                if game_state == "menu":
                    start_state = "hovered" if start_button_rect.collidepoint(mouse_x, mouse_y) else "normal"
                    exit_state = "hovered" if exit_button_rect.collidepoint(mouse_x, mouse_y) else "normal"
                elif game_state == "stage1":
                    basic_state = "hovered" if basic_button_rect.collidepoint(mouse_x,mouse_y) else "normal"
                    power_state = "hovered" if power_button_rect.collidepoint(mouse_x,mouse_y) else "normal"
                    heal_state = "hovered" if heal_button_rect.collidepoint(mouse_x,mouse_y) else "normal"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "menu":
                    if start_button_rect.collidepoint(mouse_x, mouse_y):
                        start_state = "clicked"
                        print("Game Start")
                        game_state ="tutorial"
                    elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                        exit_state = "clicked"
                        running = False
                elif game_state == "tutorial":
                    if done:
                        show_textbox = False
                    else:
                        dialogue_index += 1
                elif game_state == "stage1":
                    if (turn == True) & (turncomplete == True):

                        if basic_button_rect.collidepoint(mouse_x, mouse_y):

                            action = 2
                            turn = False
                            main_chara.attack(opponent)
                            main_chara.checkState()
                            opponent.checkState()
                            turncomplete = False
                            print("Your Turn")
                            print("Your HP :", main_chara.hp)
                            print("You Are ", main_chara.state)
                            print("You Basic Attack")
                            print("Your Opponents hp: ", opponent.hp, "and he is currently: ", opponent.state)
                        if power_button_rect.collidepoint(mouse_x, mouse_y):
                            action = 4
                            turn = False
                            main_chara.power(opponent)
                            main_chara.checkState()
                            opponent.checkState()
                            turncomplete = False
                            print("Your Turn")
                            print("Your HP :", main_chara.hp)
                            print("You Are ", main_chara.state)
                            print("You Power Attack")
                            print("Your Opponents hp: ", opponent.hp, "and he is currently: ", opponent.state)
                        if heal_button_rect.collidepoint(mouse_x,mouse_y):
                            action = 3
                            turn = False
                            main_chara.heal()
                            main_chara.checkState()
                            opponent.checkState()
                            turncomplete = False
                            print("Your Turn")
                            print("Your HP :", main_chara.hp)
                            print("You Are ", main_chara.state)
                            print("You Heal")
                            print("Your Opponents hp: ", opponent.hp, "and he is currently: ", opponent.state)
                    else:
                        print("Please wait animation is playing")
        if turn == False:
            opponent.checkState()
            atkchoice = random.randrange(2,4)
            action_opp = atkchoice
            if atkchoice == 2:
                opponent.attack(main_chara)
                opponent.checkState()
                main_chara.checkState()
                print("Their Turn")
                print("Their HP :", opponent.hp)
                print("They are ", opponent.state)
                print("They attack")
                print("Your hp: ", main_chara.hp, "and you are currently: ", main_chara.state)
            elif atkchoice == 3:
                opponent.heal()
                opponent.checkState()
                main_chara.checkState()
                print("Their Turn")
                print("Their HP :", opponent.hp)
                print("They are ", opponent.state)
                print("They heal")
                print("Your hp: ", main_chara.hp, "and you are currently: ", main_chara.state)
            elif atkchoice == 4:
                opponent.power(main_chara)
                opponent.checkState()
                main_chara.checkState()
                print("Their Turn")
                print("Their HP :", opponent.hp)
                print("They are ", opponent.state)
                print("They power attack")
                print("Your hp: ", main_chara.hp, "and you are currently: ", main_chara.state)
            turn = True
        if game_state == "tutorial":
            screen.blit(background_image, (0, 0))
            if show_textbox:
                dialogue_index, done = ui.draw_textbox(
                    dialogues,
                    (250,250),
                    textbox_image,
                    button_font,
                    40,
                    256,
                    dialogue_index
                )
            if show_textbox == False:
                game_state = "stage1"

        if game_state == "menu":
            screen.blit(background_image, (0, 0))
            title_surface = title_font.render("Turn Based RPG Demo", True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
            screen.blit(title_surface, title_rect)
            ui.draw_button_with_texture("Start Game", start_button_rect.x, start_button_rect.y, start_state, textures)
            ui.draw_button_with_texture("Exit", exit_button_rect.x, exit_button_rect.y, exit_state, textures)
        if game_state == "stage1":
            screen.blit(background_image, (0, 0))
            #display
            #update animation
            # Update animation
            current_time = pygame.time.get_ticks()

            if turn == True:
                if animation_done == False:
                    if current_time - last_update >= animation_cooldown:
                        frame += 1
                        last_update = current_time
                        
                        # If the current animation completes, reset to idle (action 0)
                        
                        if frame >= len(animation_list[action]):
                            frame = 0
                            if action in {2, 3, 4}:  # Actions that require switching back to idle
                                action = 0
                                animation_done = True
                                print("Player Animation done: ",animation_done)
                # If the current animation completes, reset to idle (action 0)
            if animation_done == True:
                if (current_time - last_update_opp >= animation_cooldown_opp):
                    frame_opp +=1
                    last_update_opp = current_time
                    if frame_opp >= len(animation_list_opp[action_opp]):
                        frame_opp = 0
                        if action_opp in {2, 3, 4}:  # Actions that require switching back to idle
                            action_opp = 0
                            animation_done = False
                            turncomplete = True
                            print("Bool for Finished Anim: ", animation_done)
            
            screen.blit(animation_list[action][frame],(300,320))
            screen.blit(animation_list_opp[action_opp][frame_opp],(900,320))
            
            ui.draw_button_with_texture("Basic Attack", basic_button_rect.x, basic_button_rect.y, basic_state, textures)
            ui.draw_button_with_texture("Power Attack", power_button_rect.x, power_button_rect.y, power_state, textures)
            ui.draw_button_with_texture("Heal", heal_button_rect.x, heal_button_rect.y, heal_state, textures)
            # Display text box
            

        # Refresh the display
        pygame.display.flip()

    pygame.quit()

except Exception as e:
    with open("crashlog.txt", "w") as log_file:
        log_file.write("An error occurred:\n")
        log_file.write(str(e) + "\n")
        log_file.write(traceback.format_exc())
    print("An error occurred. Check crashlog.txt for details.")
    pygame.quit()
    sys.exit()
