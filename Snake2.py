import pygame as pg
import random
# from os import path


# basic variables
WIDTH = 800
HEIGHT = 800
SEG_SIZE = 50
IN_GAME = True
SPEED = 10
TELEPORT = True


# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


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

        # a dictionary of tuple values where the nested tuple represents
        # coordinates and the second element represents the prohibited
        # direction in which the snake will eat itself
        self.mapping = {
            pg.K_UP: ((0, -SEG_SIZE), pg.K_DOWN),
            pg.K_DOWN: ((0, SEG_SIZE), pg.K_UP),
            pg.K_LEFT: ((-SEG_SIZE, 0), pg.K_RIGHT),
            pg.K_RIGHT: ((SEG_SIZE, 0), pg.K_LEFT),
            pg.K_w: ((0, -SEG_SIZE), pg.K_s),
            pg.K_s: ((0, SEG_SIZE), pg.K_w),
            pg.K_a: ((-SEG_SIZE, 0), pg.K_d),
            pg.K_d: ((SEG_SIZE, 0), pg.K_a),
        }

        self.direction = self.mapping[pg.K_RIGHT]

    def move(self):
        self.body[0].update(self.body[-1].rect.x, self.body[-1].rect.y)
        self.body.insert(-1, self.body.pop(0))
        self.body[-1].update(self.direction[0][0], self.direction[0][1])

    def change_direction(self, event):
        if event.key in self.mapping:
            if event.key != self.direction[1]:
                self.direction = self.mapping[event.key]

    def eat(self):
        global all_sprites
        back = self.body[0].rect
        new_seg = Segment(back.x, back.y)
        self.body.insert(0, new_seg)
        all_sprites.add(new_seg)

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
    global food
    x = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) // SEG_SIZE)
    y = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) // SEG_SIZE)
    food.update(x, y)


# setting up main window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Rebuild of Evangelion: 4.0+Snake')
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
snake = Snake()
food = Food()
for seg in snake.body:
    all_sprites.add(seg)
all_sprites.add(food)
spawn_food()


# the main loop
while IN_GAME:
    clock.tick(SPEED)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            snake.change_direction(event)

    snake.move()
    if TELEPORT is False and snake.out_of_bounds():
        IN_GAME = False
        break
    elif snake.body[-1].rect.topleft == food.rect.topleft:
        snake.eat()
        spawn_food()

    elif snake.collides():
        IN_GAME = False
        break

    # print(f'Top: {snake.body[-1].rect.top}, bottom: {snake.body[-1].rect.bottom}, left: {snake.body[-1].rect.left}, right: {snake.body[-1].rect.right}')
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pg.display.flip()

    # pg.display.update()

pg.quit()
