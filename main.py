import random
import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'img')


WIDTH = 800
HEIGHT = 338
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 70)
k = 0


background = pygame.image.load(path.join(img_dir, 'fon1.jpg')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'player.png'))
monster_img = pygame.image.load(path.join(img_dir, 'angry_monster.png'))
default_img = pygame.image.load(path.join(img_dir, 'hand.png'))


def move(rect):
    speed_x = 0
    key_state = pygame.key.get_pressed()
    if key_state[pygame.K_LEFT]:
        speed_x = -8
    if key_state[pygame.K_RIGHT]:
        speed_x = 8
    rect.x += speed_x
    if rect.right > WIDTH:
        rect.right = WIDTH
    if rect.left < 0:
        rect.left = 0


def attack(attacking, protector):
    mod = abs(attacking.fire - protector.protect)
    return mod


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.fire = random.randint(1, 30)
        self.protect = random.randint(1, 30)
        self.shield = 50
        self.bullets = pygame.sprite.Group()
        self.power = random.randint(1, 6)
        self.image = pygame.transform.scale(player_img, (120, 140))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def death(self):
        if self.shield < 0:
            self.kill()

    def draw_shield_bar(self, surf):
        if self.shield < 0:
            self.shield = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        x = self.rect.left + 10
        y = self.rect.top - 10
        fill = (self.shield / 50) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, GREEN, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (120, 140))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_x = 0
        self.last_up = pygame.time.get_ticks()
        self.bullets = pygame.sprite.Group()
        self.direction = 1

    def shoot(self):
        if self.shield > 0:
            # mod = abs(self.fire - monster.protect + 1)
            # print("Модификатор", mod)
            # i = 0
            # while i != mod:
            #     i += 1
            #     print("i = ", i, ", mod = ", mod)
            #
            #     while pygame.time.get_ticks() - self.last_up < 100:
            #         now1 = pygame.time.get_ticks()
            #         print("now1", now1)
            #         print("last_up_1", self.last_up)
            #         clock.tick()
            #         now2 = pygame.time.get_ticks()
            #         print("now2", now2)
            #         print("last_up_2", self.last_up)
            #
            #     now3 = pygame.time.get_ticks()
            #     print("now3", now3)
            #     print("last_up_3", self.last_up)
            #
            #     if now3 - self.last_up > 100:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            all_sprites.add(bullet)
            self.bullets.add(bullet)
            # self.last_up = pygame.time.get_ticks()
            # print("last_up_4", self.last_up)
            self.power = random.randint(1, 6)


class Monster(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(monster_img, (120, 140))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_x = 0
        self.last_up = pygame.time.get_ticks()
        self.bullets = pygame.sprite.Group()
        self.direction = -1

    def shoot(self):
        if self.shield > 0 and player.shield > 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            all_sprites.add(bullet)
            self.bullets.add(bullet)
            self.last_up = pygame.time.get_ticks()
            self.power = random.randint(1, 6)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, route):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.power = random.randint(1, 6)
        self.direction = route


    def update(self):
        self.rect.x += self.direction * self.speedy
        if self.rect.bottom > WIDTH:
            self.kill()


all_sprites = pygame.sprite.Group()
player = Player(600, 250)
monster = Monster(100, 250)
all_sprites.add(player, monster)
message = font.render("Game Over", True, pygame.Color(RED))


running = True

while running:
    clock.tick(FPS)
    now = pygame.time.get_ticks()
    if now - monster.last_up > random.randrange(1000, 3000, 100):
        monster.shoot()
    if k < 4 and player.shield <= 25:
        k += 1
        player.shield = player.shield + 15
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    all_sprites.update()

    bullets_hits1 = pygame.sprite.spritecollide(monster, player.bullets, True, pygame.sprite.collide_circle)
    for bullet in bullets_hits1:
        if bullet.power >= 5:
            monster.shield -= player.power
            print("player", player.power, "bullet", bullet.power)


    bullets_hits2 = pygame.sprite.spritecollide(player, monster.bullets, True, pygame.sprite.collide_circle)
    for bullet in bullets_hits2:
        if bullet.power >= 5:
            player.shield -= monster.power
            print("monster", monster.power, "bullet", bullet.power)

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    player.draw_shield_bar(screen)
    monster.draw_shield_bar(screen)
    move(player.rect)
    if player.shield <= 0 or monster.shield <= 0:
        screen.blit(
            message,
            message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        )
    pygame.display.flip()

pygame.quit()
