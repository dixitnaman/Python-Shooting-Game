import pygame
import math
import random
import time

from pygame import mixer

# initilaize
pygame.init()

# screen size
screen = pygame.display.set_mode((800, 600))

# background and music
background = pygame.image.load("background.jpg")
mixer.music.load('backgound.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# title & icon
pygame.display.set_caption("Arrow Game")
icon = pygame.image.load("target.png")
pygame.display.set_icon(icon)

# character
char = pygame.image.load("centaur.png")
charX = 25
charY = 270
charY_change = 0

# enemy
enemy = []
enemyX = []
enemyY = []
enemyY_change = []
enemyX_change = []
no_of_enemies = 5

for i in range(no_of_enemies):
    enemy.append(pygame.image.load("goblin.png"))
    enemyX.append(random.randint(300, 750))
    enemyY.append(random.randint(10, 500))
    enemyY_change.append(2)
    enemyX_change.append(40)

# arrow
arrow = pygame.image.load("bow.png")
arrowX = 25
arrowY = 0
arrowX_change = 5
arrow_state = "ready"

# score
score_value: int = 0
font = pygame.font.Font("freesansbold.ttf", 35)
textX = 600
textY = 550

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("SCORE:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():#-----------------------------------
    if enemyX[j] >= 900:#-----------------------------------
        return True#-----------------------------------
        # over_text = over_font.render("GAME OVER", True, (255, 255, 255))#-----------------------------------
        # screen.blit(over_text, (200, 250))#-----------------------------------

def player(x, y):
    screen.blit(char, (x, y))


def villan(x, y, i):
    screen.blit(enemy[i], (x, y))


def fire_arrow(x, y):
    global arrow_state
    arrow_state = "fire"
    screen.blit(arrow, (x + 29, y - 14))


def isCollision(enemyX, enemyY, arrowX, arrowY):
    distance = math.sqrt((math.pow(enemyX - arrowX, 2)) + (math.pow(enemyY - arrowY, 2)))
    if distance < 40:
        return True
    else:
        return False


# game basic window

game_over = False#-----------------------------------
running = True
while running:
    screen.fill((47, 47, 47))
    screen.blit(background, (0, 0))
    if game_over == True: #-----------------------------------
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))#-----------------------------------
        screen.blit(over_text, (200, 250))#-----------------------------------


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                charY_change = -4
            if event.key == pygame.K_DOWN:
                charY_change = 4
            if event.key == pygame.K_SPACE:
                if arrow_state == "ready":
                    arrow_sound = mixer.Sound('fire.wav')
                    arrow_sound.play()
                    arrowY = charY
                    fire_arrow(arrowX, arrowY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                charY_change = 0

    charY += charY_change

    # player boundary
    if charY <= 10:
        charY = 10
    elif charY >= 530:
        charY = 530

    for i in range(no_of_enemies):
        # game over
        if enemyX[i] < 80:
            for j in range(no_of_enemies):
                enemyX[j] = 20000
            game_over = True#---------------------------- -------
            # break#-----------------------------------

        # enemy boundary
        enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 10:
            enemyY_change[i] = 3
            enemyX[i] -= enemyX_change[i]
        elif enemyY[i] >= 530:
            enemyY_change[i] = -3
            enemyX[i] -= enemyX_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], arrowX, arrowY)
        if collision:
            dead_sound = mixer.Sound('explosion.wav')
            dead_sound.play()
            arrowX = 25
            arrow_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(500, 750)
            enemyY[i] = random.randint(10, 500)
        villan(enemyX[i], enemyY[i], i)

    if arrowX >= 800:
        arrowX = 25
        arrow_state = "ready"

    if arrow_state == "fire":
        fire_arrow(arrowX, arrowY)
        arrowX += arrowX_change

    player(charX, charY)
    show_score(textX, textY)
    pygame.display.update()
