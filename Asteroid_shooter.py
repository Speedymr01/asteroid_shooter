import pygame, sys, time
from random import randint, uniform
pygame.init()
pygame.mixer.init()

def laser_update(laser_list,speed = 1000):
    for rect in laser_list:
        rect.y -= speed * dt
        if rect.bottom < 0:
            laser_list.remove(rect)


def meteor_update(meteor_list, speed = 500):
    for meteor_tuple in meteor_list:
        direction = meteor_tuple[1]
        meteor_rect = meteor_tuple[0]
        meteor_rect.center += direction * speed * dt
        #rect.y +=speed * dt
        if meteor_rect.top > WINDOW_HIGHT:
            meteor_list.remove(meteor_tuple)


def display_score():
    # opening highscore file
    highcorefile = open('HighScore.txt', mode= 'r')
    highcore = highcorefile.read()
    highcore = round(float(highcore))

    # Creating High Score text
    highscore = f'Highscore: {str(highcore)}'
    highscore_surf = font.render(highscore, True, (255, 255, 255))
    highscore_rect = highscore_surf.get_rect(midbottom = ((WINDOW_WIDTH/4)*3, WINDOW_HIGHT - 30))
    
    #Creating Score text
    score_text = f'Score: {round(score)}'
    text_surf = font.render(score_text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH/4, WINDOW_HIGHT - 30))
    display_surface.blit(text_surf, text_rect)
    display_surface.blit(highscore_surf, highscore_rect)
    pygame.draw.rect(display_surface, (255, 255, 255), highscore_rect.inflate(30, 30), width = 8, border_radius =  5)
    pygame.draw.rect(display_surface, (255, 255, 255), text_rect.inflate(30, 30), width = 8, border_radius = 5)
    
    

def laser_timer(can_shoot, duration = 200):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot


# initing
WINDOW_WIDTH, WINDOW_HIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIGHT))
pygame.display.set_caption('Asteroid Shooter')
clock = pygame.time.Clock()
score = 0


# inmort ship
ship_surf = pygame.image.load('graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HIGHT/2))

# Background inmort
background_surf = pygame.image.load('graphics/background.png').convert()

#Laser inmort
laser_surf = pygame.image.load('graphics/laser.png').convert_alpha()
laser_list = []

# laser timer
can_shoot = True
shoot_time = None


# import text
font = pygame.font.Font('graphics/subatomic.ttf', 50)

# inmort meteor
meteor_surf = pygame.image.load('graphics/meteor.png').convert_alpha()
meteor_list = []

# Meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 250)

# inmort sound
level_up_sound = pygame.mixer.Sound('sounds/273975-Ambient-Game-Objective-Complete-Simple-Run-1.wav')
level_up_sound.set_volume(0.6)
speed_up_sound = pygame.mixer.Sound('sounds/422590-Mobile-Game-Melodic-Stinger-Floating-Level-Up-1.wav')
speed_up_sound.set_volume(0.5)
laser_sound = pygame.mixer.Sound('sounds/8-bit-laser-151672.mp3')
laser_sound.set_volume(0.4)
explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
explosion_sound.set_volume(0.2)
Game_over_sound = pygame.mixer.Sound('sounds/game-over-39-199830.mp3')
Game_over_sound.set_volume(0.3)
level1music = pygame.mixer.Sound('sounds/level0.wav')
level2music = pygame.mixer.Sound('sounds/level1.wav')
level3music = pygame.mixer.Sound('sounds/level-.wav')
level1music.set_volume(0.1)
pygame.mixer.music.load('sounds/level1.wav')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
pygame.mixer.music.queue('sounds/level0.wav')
pygame.mixer.music.queue('sounds/level-.wav')
pygame.mixer.music.queue('sounds/level1.wav')
pygame.mixer.music.queue('sounds/level0.wav')
pygame.mixer.music.queue('sounds/level-.wav')
pygame.mixer.music.queue('sounds/level1.wav')
pygame.mixer.music.queue('sounds/level0.wav')
pygame.mixer.music.queue('sounds/level-.wav')
pygame.mixer.music.queue('sounds/level1.wav')
pygame.mixer.music.queue('sounds/level0.wav')
pygame.mixer.music.queue('sounds/level-.wav')
pygame.mixer.music.queue('sounds/level1.wav')

#pygame.mixer.music.load('sounds/music.wav')
#pygame.mixer.music.set_volume(0.09)
#pygame.mixer.music.play(-1)


while True:   # main game loop

    # input loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            highcorefile = open('HighScore.txt', mode= 'r')
            highcore = highcorefile.read()
            highcorefile.close()
            if int(highcore) < score:
                Hiscorefile = open('HighScore.txt', mode= 'w')
                Hiscorefile.write(str(score))
                Hiscorefile.close()
                pygame.quit()
                sys.exit()
            else:
                pygame.quit()
                sys.exit()



        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:

            # Laser
            laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
            laser_list.append(laser_rect)

            # Timer logic
            can_shoot = False
            shoot_time = pygame.time.get_ticks()

            # Laser sound
            laser_sound.play()
            



        if event.type == meteor_timer:
            # Randome pos
            randx = randint(-100, WINDOW_WIDTH + 100)
            randy = randint(-100, -50)
            # create rect
            meteor_rect = meteor_surf.get_rect(center = (randx, randy))
            
            # Randome direction
            direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
            
            meteor_list.append((meteor_rect, direction))





    # Frame rate limiter
    dt = clock.tick(120) / 1000

    # mouse input
    ship_rect.center = pygame.mouse.get_pos()

    # Meteor speed
    speed = score*1.5 + 200
    if score % 40 == 0 and score > 5:
        speed_up_sound.play()
        score += 0.1


    # movement
    laser_update(laser_list)
    meteor_update(meteor_list, speed)
    can_shoot = laser_timer(can_shoot, 300)

    # Collision
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        highcorefile = open('HighScore.txt', mode= 'r')
        highcore = highcorefile.read()
        highcorefile.close()
        if ship_rect.colliderect(meteor_rect):
            if int(highcore) < score:
                Hiscorefile = open('HighScore.txt', mode= 'w')
                Hiscorefile.write(str(score))
                Hiscorefile.close()
                level1music.stop()
                level2music.stop()
                Game_over_sound.play()
                time.sleep(4)
                pygame.quit()
                sys.exit()
            else:
                pygame.mixer.music.fadeout(1)
                Game_over_sound.play()
                time.sleep(2)
                pygame.quit()
                sys.exit()
    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            if laser_rect.colliderect(meteor_tuple[0]):
                meteor_list.remove(meteor_tuple)
                laser_list.remove(laser_rect)
                explosion_sound.play()
                score += 1


    # graphics
    display_surface.fill((0, 0, 0))
    display_surface.blit(background_surf, (0, 0))
    
    display_score()
    

    # display lasers
    for rect in laser_list:
        display_surface.blit(laser_surf, rect)

    # display meteors
    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf, meteor_tuple[0])
    
    display_surface.blit(ship_surf, ship_rect)


    # final graphics draw on screen
    pygame.display.update()