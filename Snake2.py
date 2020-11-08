import pygame as pg
from random import randint
# from os import path


# basic variables
WIDTH = 800
HEIGHT = 800
SEG_SIZE = 50
IN_GAME = True
SPEED = 12
TELEPORT = True


# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (238, 118, 0)


DIFFICULTIES = (
    ('pathetic', 8),
    ('pilot', 12),
    ('martyr', 16)
)


# setting up the main window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Rebuild of Evangelion: 4.0+Snake')
clock = pg.time.Clock()


# all fonts and texts for messages
font_rec = pg.font.SysFont('arial', 16)
font_menu = pg.font.SysFont('arial', 20)
defeat_lines = ['HUMANITY IS DOOMED.',
                'YOU CANNOT REDO.',
                'OR CAN YOU?..',
                'PRESS R']
pause_lines = ['YOU CAN REST FOR NOW',
               'BUT YOU WILL NOT STOP',
               'THE INEVITABLE.']


# classes and sprites
class Segment(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((SEG_SIZE, SEG_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Head(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((SEG_SIZE, SEG_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if TELEPORT is True:
            if self.rect.top < 0:
                self.rect.top = HEIGHT
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = 0
            elif self.rect.left < 0:
                self.rect.left = WIDTH
            elif self.rect.right > WIDTH:
                self.rect.right = 0


class Food(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((SEG_SIZE, SEG_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Snake:

    def __init__(self):
        self.body = [
            Segment(SEG_SIZE, 8*SEG_SIZE),
            Segment(2*SEG_SIZE, 8*SEG_SIZE),
            Head(3*SEG_SIZE, 8*SEG_SIZE)
        ]

        # a dictionary of tuples where the first nested tuple represents
        # the coordinates and the second one represents the prohibited
        # direction (for both types of keys) in which the snake will eat itself
        self.mapping = {
            pg.K_UP: ((0, -SEG_SIZE), (pg.K_DOWN, pg.K_s)),
            pg.K_DOWN: ((0, SEG_SIZE), (pg.K_UP, pg.K_w)),
            pg.K_LEFT: ((-SEG_SIZE, 0), (pg.K_RIGHT, pg.K_d)),
            pg.K_RIGHT: ((SEG_SIZE, 0), (pg.K_LEFT, pg.K_a)),
            pg.K_w: ((0, -SEG_SIZE), (pg.K_s, pg.K_DOWN)),
            pg.K_s: ((0, SEG_SIZE), (pg.K_w, pg.K_UP)),
            pg.K_a: ((-SEG_SIZE, 0), (pg.K_d, pg.K_RIGHT)),
            pg.K_d: ((SEG_SIZE, 0), (pg.K_a, pg.K_LEFT)),
        }

        self.direction = self.mapping[pg.K_RIGHT]
        self.length = len(self.body)

    def move(self):
        self.body[0].update(self.body[-1].rect.x, self.body[-1].rect.y)
        self.body.insert(-1, self.body.pop(0))
        self.body[-1].update(self.direction[0][0], self.direction[0][1])

    def change_direction(self, event):
        if event.key in self.mapping:
            if self.out_of_bounds() is False:
                if event.key not in self.direction[1]:
                    self.direction = self.mapping[event.key]

    def eat(self):
        global all_sprites
        back = self.body[0].rect
        new_seg = Segment(back.x, back.y)
        self.body.insert(0, new_seg)
        all_sprites.add(new_seg)
        self.length += 1

    def collides(self):
        head = self.body[-1].rect.topleft
        for i in range(len(self.body)-1):
            if head == self.body[i].rect.topleft:
                return True
        return False

    def out_of_bounds(self):
        head = self.body[-1].rect
        if (head.top < 0 or head.bottom > HEIGHT or
           head.left < 0 or head.right > WIDTH):
            return True
        return False


def spawn_food():
    global food, snake

    snake_segments = [segment.rect.topleft for segment in snake.body]

    while True:
        x = SEG_SIZE * randint(1, (WIDTH-SEG_SIZE) // SEG_SIZE)
        y = SEG_SIZE * randint(1, (HEIGHT-SEG_SIZE) // SEG_SIZE)
        if (x, y) not in snake_segments:
            break
    food.update(x, y)


def start_game():
    global all_sprites, snake, food
    all_sprites = pg.sprite.Group()
    snake = Snake()
    food = Food()
    for seg in snake.body:
        all_sprites.add(seg)
    all_sprites.add(food)
    spawn_food()
    main()


def restart_game():
    global IN_GAME
    IN_GAME = True
    screen.fill(BLACK)
    pg.display.flip()
    start_game()


def draw_text(surf, text, font, color, x, y, centered=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered is True:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)
    return text_rect


def pause():
    pg.display.update([draw_text(screen, line, font_menu,
                      ORANGE, WIDTH/2, HEIGHT/2+i*30)
                      for i, line in enumerate(pause_lines)])

    while True:
        clock.tick(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return


def menu(text, record):
    global DIFFICULTIES, SPEED, TELEPORT

    while True:
        clock.tick(10)

        screen.fill(BLACK)
        draw_text(screen, f'record: {record}', font_rec, WHITE, 40, 17)

        for i, line in enumerate(text):
            draw_text(screen, line, font_menu,
                      ORANGE, WIDTH/2, HEIGHT/2+i*30)

        draw_text(screen, 'CHOOSE YOUR DESTINY:',
                  font_menu, ORANGE, WIDTH*3/4, SEG_SIZE)

        dif_rects = []
        for i, dif in enumerate(DIFFICULTIES, 1):
            if SPEED == dif[1]:
                dif_text = '> ' + dif[0]
                color = WHITE
            else:
                dif_text = dif[0]
                color = ORANGE

            dif_rects.append(draw_text(
                screen, dif_text, font_menu, color,
                WIDTH*3/4, SEG_SIZE+i*30, centered=False
                )
            )

        draw_text(screen, 'GOING THROUGH WALLS:',
                  font_menu, ORANGE, WIDTH*1/4, SEG_SIZE)

        on_off = draw_text(screen, 'ON' if TELEPORT else 'OFF',
                           font_menu, WHITE, WIDTH*1/4+130, SEG_SIZE)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    restart_game()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                if dif_rects[0].collidepoint(pos):
                    SPEED = DIFFICULTIES[0][1]
                elif dif_rects[1].collidepoint(pos):
                    SPEED = DIFFICULTIES[1][1]
                elif dif_rects[2].collidepoint(pos):
                    SPEED = DIFFICULTIES[2][1]
                elif on_off.collidepoint(pos):
                    TELEPORT = not TELEPORT


# the main loop
def main():
    global IN_GAME

    while IN_GAME:
        clock.tick(SPEED)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pause()
                else:
                    snake.change_direction(event)

        snake.move()

        if TELEPORT is False and snake.out_of_bounds() is True:
            IN_GAME = False
            return menu(defeat_lines, snake.length)

        elif snake.body[-1].rect.topleft == food.rect.topleft:
            snake.eat()
            spawn_food()

        elif snake.collides():
            IN_GAME = False
            return menu(defeat_lines, snake.length)

        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(screen, f'record: {str(snake.length)}',
                  font_rec, WHITE, 17, 17, centered=False)
        pg.display.flip()


start_game()

pg.quit()

# add 8-bit styled soundtrack from Evangelion
# add pictures to sprites
# image background during game and after defeat


# next time I rewrite this, try making Sprites Segment
# and Head nested in class Snake to for preserving incupsulation
# principals
