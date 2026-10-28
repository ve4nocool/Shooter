from random import randint
from pygame import *

WHITE = (255,255,255)
RED = (255,0,0)

font.init()
mixer.init()

mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height - 60:
            self.rect.y -= win_height + randint(0, 50)
            self.rect.x = randint(0, 620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player('rocket.png', 90, 370, 70, 120, 6)

ufos = sprite.Group()
for i in range(5):
    ufo1 = Enemy('ufo.png', randint(0, 620), randint(-150,0), 80, 60, 2)
    ufos.add(ufo1)

bullets = sprite.Group()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
bg = transform.scale(image.load('galaxy.jpg'),(700,500))
clock = time.Clock()
lost = 0
score = 0
finish = False
g = True
fps = 60

while g:
    for e in event.get():
        if e.type == QUIT:
            g = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    
    if not finish:
        window.blit(bg,(0,0))
        text_score = font.SysFont(None, 33).render('Счет: '+str(score), 1, WHITE)
        window.blit(text_score, (10, 10))
        text_lost = font.SysFont(None, 33).render('Пропущено: '+str(lost), 1, WHITE)
        window.blit(text_lost, (10, 35))
        ship.draw()
        ufos.draw(window)
        bullets.draw(window)
        bullets.update()
        ship.update()
        ufos.update()
        collides = sprite.groupcollide(ufos, bullets, True, True)
        
        for collide in collides:
            score += 1
            ufo = Enemy('ufo.png', randint(0, 620), randint(-150,0), 80, 60, 2)
            ufos.add(ufo)
        
        if sprite.spritecollide(ship, ufos, False) or lost >= 3:
            finish = True
            lose = font.SysFont(None, 100).render('ТЫ ПРОИГРАЛ!', 1, RED)
            window.blit(lose, (120,170))

        if score >= 10:
            finish = True
            win = font.SysFont(None, 100).render('ПОБЕДА!', 1, WHITE)
            window.blit(win, (200,200))

    display.update()
    clock.tick(fps)