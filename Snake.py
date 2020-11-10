import pygame as pg
from random import randint
from os import path


# basic variables
WIDTH = 800
HEIGHT = 800
SEG_SIZE = 50
# WIDTH = 600
# HEIGHT = 600
# SEG_SIZE = 100
IN_GAME = True
DIFFICULTIES = (('pathetic', 8), ('pilot', 12), ('martyr', 16))
SPEED = DIFFICULTIES[1][1]
TELEPORT = True
VICTORY = False


# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (238, 118, 0)


# setting up the main window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Rebuild of Evangelion: 4.0+Snake')
clock = pg.time.Clock()


# adding some assets
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')
font_dir = path.join(game_dir, 'font')

field = pg.image.load(path.join(img_dir, 'field.png')).convert()
field_rect = field.get_rect()
defeat = pg.image.load(path.join(img_dir, 'defeat.png')).convert()
defeat_rect = defeat.get_rect()
victory = pg.image.load(path.join(img_dir, 'victory.png')).convert()
victory_rect = victory.get_rect()
head_img = pg.image.load(path.join(img_dir, 'Eva01_head_8px.png')).convert()
torso_img = pg.image.load(path.join(img_dir, 'Eva01_torso_8px.png')).convert()
core_img = pg.image.load(path.join(img_dir, 'core_16px.png')).convert()


# all fonts and texts for messages
font_basic = pg.font.SysFont('arial', 20)
font_menu = pg.font.Font(path.join(font_dir, 'neurotoxin.ttf'), 20)
defeat_lines = ['HUMANITY IS DOOMED.',
                'YOU CANNOT REDO.',
                'OR CAN YOU?..',
                'PRESS R']
pause_lines = ['YOU CAN REST FOR NOW',
               'BUT YOU WILL NOT STOP',
               'THE INEVITABLE.']
victory_lines = ['OMEDETOU!',
                 'YOU DID IT SHINJI!']


# classes and sprites
class Segment(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = pg.transform.scale(torso_img,
                                             (SEG_SIZE, SEG_SIZE))
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rot = 90

    def update(self, x, y, direction):
        self.rect.x = x
        self.rect.y = y
        self.rotate(direction)

    def rotate(self, direction):
        if pg.K_UP in direction:
            rot = 180
        elif pg.K_DOWN in direction:
            rot = 0
        elif pg.K_LEFT in direction:
            rot = -90
        elif pg.K_RIGHT in direction:
            rot = 90
        self.image = pg.transform.rotate(self.image_orig, rot)


class Head(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = pg.transform.scale(head_img,
                                             (SEG_SIZE, SEG_SIZE))
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rot = 90

    def update(self, x, y, direction):
        self.rect.x += x
        self.rect.y += y
        self.rotate(direction)
        if TELEPORT is True:
            if self.rect.top < 0:
                self.rect.top = HEIGHT
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = 0
            elif self.rect.left < 0:
                self.rect.left = WIDTH
            elif self.rect.right > WIDTH:
                self.rect.right = 0

    def rotate(self, direction):
        if pg.K_UP in direction:
            rot = 180
        elif pg.K_DOWN in direction:
            rot = 0
        elif pg.K_LEFT in direction:
            rot = -90
        elif pg.K_RIGHT in direction:
            rot = 90
        self.image = pg.transform.rotate(self.image_orig, rot)


class Food(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(core_img, (SEG_SIZE, SEG_SIZE))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Snake:

    def __init__(self):
        self.body = [
            Segment(SEG_SIZE, 8*SEG_SIZE),
            Segment(2*SEG_SIZE, 8*SEG_SIZE),
            Head(3*SEG_SIZE, 8*SEG_SIZE)]
    # Segment(0, SEG_SIZE),
    # Segment(SEG_SIZE, SEG_SIZE),
    # Segment(2*SEG_SIZE, SEG_SIZE),
    # Segment(3*SEG_SIZE, SEG_SIZE),
    # Segment(4*SEG_SIZE, SEG_SIZE),
    # Segment(4*SEG_SIZE, 2*SEG_SIZE),
    # Segment(3*SEG_SIZE, 2*SEG_SIZE),
    # Segment(2*SEG_SIZE, 2*SEG_SIZE),
    # Segment(SEG_SIZE, 2*SEG_SIZE),
    # Segment(0, 2*SEG_SIZE),
    # Segment(0, 3*SEG_SIZE),
    # Segment(SEG_SIZE, 3*SEG_SIZE),
    # Segment(2*SEG_SIZE, 3*SEG_SIZE),
    # Segment(3*SEG_SIZE, 3*SEG_SIZE),
    # Segment(4*SEG_SIZE, 3*SEG_SIZE),
    # Segment(4*SEG_SIZE, 4*SEG_SIZE),
    # Segment(3*SEG_SIZE, 4*SEG_SIZE),
    # Segment(2*SEG_SIZE, 4*SEG_SIZE),
    # Segment(SEG_SIZE, 4*SEG_SIZE),
    # Segment(0, 4*SEG_SIZE),
    # Segment(0, 5*SEG_SIZE),
    # Segment(SEG_SIZE, 5*SEG_SIZE),
    # Head(2*SEG_SIZE, 5*SEG_SIZE)]

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
        self.body[0].update(
            self.body[-1].rect.x, self.body[-1].rect.y, self.direction[1])
        self.body.insert(-1, self.body.pop(0))
        self.body[-1].update(
            self.direction[0][0], self.direction[0][1], self.direction[1])

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
    # returns True if the food is spawned successfully
    # or False in the other case
    global food, snake
    FREE_SPACES = []

    snake_segments = [segment.rect.topleft for segment in snake.body]

    for x in range(WIDTH // SEG_SIZE):
        for y in range(HEIGHT // SEG_SIZE):
            if (x*SEG_SIZE, y*SEG_SIZE) not in snake_segments:
                FREE_SPACES.append((x*SEG_SIZE, y*SEG_SIZE))

    if FREE_SPACES:
        x, y = FREE_SPACES[randint(0, len(FREE_SPACES)-1)]
        food.update(x, y)
        return True
    else:
        return False


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
    global IN_GAME, VICTORY
    IN_GAME = True
    VICTORY = False
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
                      for i, line in enumerate(pause_lines, -1)])

    while True:
        clock.tick(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return


def menu(text, record):
    global DIFFICULTIES, SPEED, TELEPORT, VICTORY

    background = victory if VICTORY else defeat
    background_rect = victory_rect if VICTORY else defeat_rect

    while True:
        clock.tick(10)

        screen.fill(BLACK)
        screen.blit(background, background_rect)
        draw_text(screen, f'record: {record}',
                  font_basic, WHITE, 14, 11, centered=False)

        for i, line in enumerate(text, -1):
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
                screen, dif_text, font_basic, color,
                WIDTH*3/4, SEG_SIZE+i*30, centered=False
                )
            )

        draw_text(screen, 'GOING THROUGH WALLS:',
                  font_menu, ORANGE, WIDTH*1/4, SEG_SIZE)

        on_off = draw_text(screen, 'ON' if TELEPORT else 'OFF',
                           font_basic, WHITE, WIDTH*1/4+160, SEG_SIZE)

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
    global IN_GAME, VICTORY

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
            if not spawn_food():
                VICTORY = True
                return menu(victory_lines, snake.length)

        elif snake.collides():
            IN_GAME = False
            return menu(defeat_lines, snake.length)

        screen.fill(BLACK)
        screen.blit(field, field_rect)
        all_sprites.draw(screen)
        draw_text(screen, f'record: {str(snake.length)}',
                  font_basic, WHITE, 14, 11, centered=False)
        pg.display.flip()


start_game()

pg.quit()

# add 8-bit styled soundtrack from Evangelion


# next time I rewrite this, try making Sprites Segment
# and Head nested in class Snake to for preserving incupsulation
# principals
