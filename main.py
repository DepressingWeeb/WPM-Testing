import sys
import math
import time
import pygame
from pygame.locals import *
import random
from english_words import english_words_lower_alpha_set

list_of_words = list(english_words_lower_alpha_set)
list_of_words = [list_of_words[i] for i in range(len(list_of_words)) if len(list_of_words[i]) < 7]

black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
width = 1000
height = 600
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()


def quit_game():
    pygame.quit()
    sys.exit()


def generate_text():
    number_of_words = 6
    txt = []
    for i in range(number_of_words):
        txt.append(random.choice(list_of_words))
    return " , ".join(txt)


def create_text(mytext, color, size, i, check, x=200, y=height // 2):
    f = pygame.font.Font("freesansbold.ttf", size)
    textRect = None
    if i > 0:
        textSurface = f.render(mytext[:i], True, green)
        textRect = textSurface.get_rect()
        textRect.midleft = (200, y)
        DISPLAYSURF.blit(textSurface, textRect)
    if check:
        textSurface = f.render(mytext[i:i + 1], True, red)
        textRect1 = textSurface.get_rect()
        if textRect != None:
            textRect1.midleft = textRect.midright
        else:
            textRect1.midleft = (200, y)
        DISPLAYSURF.blit(textSurface, textRect1)
        i += 1
    if i < len(mytext):
        textSurface = f.render(mytext[i:], True, black)
        textRect2 = textSurface.get_rect()
        if textRect != None:
            if not check:
                textRect2.midleft = textRect.midright
            else:
                textRect2.midleft = textRect1.midright
        else:
            if not check:
                textRect2.midleft = (x, y)
            else:
                textRect2.midleft = textRect1.midright
        DISPLAYSURF.blit(textSurface, textRect2)


def create_button(mytext, color, colorOnHover, width, height, x, y, textsize, action=None):
    mousePosX, mousePosY = pygame.mouse.get_pos()

    myRect = pygame.Rect(0, 0, width, height)
    myRect.center = (x, y)
    if myRect.x <= mousePosX <= myRect.x + width and myRect.y <= mousePosY <= myRect.y + height:
        color, colorOnHover = colorOnHover, color
        if pygame.mouse.get_pressed()[0] == 1:
            if action is not None:
                action()
    pygame.draw.rect(DISPLAYSURF, color, myRect)
    f = pygame.font.Font("freesansbold.ttf", textsize)
    textSurface = f.render(mytext, True, black)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    DISPLAYSURF.blit(textSurface, textRect)


def result(WPM):
    while True:
        DISPLAYSURF.fill(white)
        create_text(f"Your WPM is : {WPM}", black, 50, 0, False, 300, height // 2)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
        create_button("NEW GAME", green, blue, 200, 50, width // 2, 500, 30, main_game_loop)
        pygame.display.update()
        clock.tick(60)


def main_game_loop():
    i = 0
    mytext = generate_text()
    nextChar = None
    check = False
    n_of_words = 0
    countdown = 60
    time_now = 0
    checkKeyDown = False
    # main game loop

    while True:

        DISPLAYSURF.fill(white)
        create_text(mytext, black, 30, i, check)
        if checkKeyDown:
            time_now = math.ceil(time.perf_counter() - t)
            countdown = 60 - time_now
        WPM = math.ceil((n_of_words / time_now) * 60) if time_now != 0 else 0
        create_text(f"Countdown : {countdown}", black, 30, 0, False, 700, 50)
        create_text(f"WPM : {WPM}", black, 30, 0, False, 700, 100)
        if countdown <= 0:
            result(WPM)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == KEYDOWN:
                if not checkKeyDown:
                    t = time.perf_counter()
                    checkKeyDown = True
                try:
                    nextChar = chr(event.key)
                except:
                    continue
        if i < len(mytext) and (mytext[i] == " " or mytext[i] == ","):
            n_of_words += 1
            i += 3
        if i < len(mytext) and nextChar == mytext[i]:
            i += 1
            nextChar = None
            check = False
        elif i >= len(mytext):
            i = 0
            mytext = generate_text()
        elif nextChar != None and nextChar != mytext[i]:
            check = True
            nextChar = None

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_game_loop()
