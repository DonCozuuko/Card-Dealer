import pygame as pg
import random as r
import os

pg.init()
pg.font.init()

WIN_SIZE = (600, 600)
WIDTH, HEIGHT = WIN_SIZE
SCREEN = pg.display.set_mode(WIN_SIZE)
FONT = pg.font.SysFont(None, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
SNAP = pg.mixer.Sound("Card Dealer/Sounds/snappy.mp3")

GAME_START = False

PATH1 = "Card Dealer/Cards"

CARDS = []
for card in os.listdir(PATH1):
    if 'png' in card:
        CARDS.append(card)

def checkForInput(position, rect):
    if rect and position[0] in range(rect.left, rect.right) and position[1] in range(rect.top, rect.bottom):
        return True
    return False


class Display:
    def __init__(self):
        self.shuffle_btn_rect = None
        self.card_chosen = None
        self.sound_played = None
        self.card_x = WIDTH
        self.animation_speed = 10


    def head(self):
        text = FONT.render("Your Card:", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        text_rect.top = 20
        SCREEN.blit(text, text_rect)


    def shuffle_btn(self):
        text = FONT.render("SHUFFLE", True, BLACK)
        self.shuffle_btn_rect = text.get_rect()
        self.shuffle_btn_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.shuffle_btn_rect.top = 520
        SCREEN.blit(text, self.shuffle_btn_rect)
    
    
    def game_start_msg(self):
        text = FONT.render("Click shuffle to get a card", True, GREY)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        text_rect.top = HEIGHT // 2 - 30
        SCREEN.blit(text, text_rect)


    def display_cards(self):

        if self.card_chosen is None and self.sound_played is None:
            pick = r.randint(0, 51)
            self.card_chosen = CARDS[pick]
            SNAP.play()
            self.sound_played = True
            self.card_x = WIDTH
            self.animation_speed = 10

        image = pg.image.load(f"Card Dealer/Cards/{self.card_chosen}")
        rect = image.get_rect()
        rect.center = (WIDTH // 2, HEIGHT // 2)
    

        if self.card_x > rect.x:
            self.card_x -= self.animation_speed
        else:
            self.card_x = rect.x

        SCREEN.blit(image, (self.card_x, rect.y))


    def draw(self):
        self.head()
        self.shuffle_btn()
        

class Game:
    def __init__(self):
        self.display = Display()
        self.pos = pg.mouse.get_pos()
        

    def check_events(self):
        global GAME_START
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
    
            if event.type == pg.MOUSEBUTTONDOWN and checkForInput(self.pos, self.display.shuffle_btn_rect):
                self.display.card_chosen = None
                self.display.sound_played = None
                GAME_START = True


    def run(self):
        while True:
            self.pos = pg.mouse.get_pos()
            SCREEN.fill(WHITE)
            self.check_events()
            self.display.draw()

            if GAME_START == False:
                self.display.game_start_msg()
            else:
                self.display.display_cards()

            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()