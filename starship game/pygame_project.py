import pygame
import os

pygame.font.init()

WIDTH,HEIGHT=900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game!")

white = (100,100,100)
white2 = (255,255,255)
black = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

BG = pygame.image.load('.//asset//wallpaper-try4 - Copy.png')

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('Arial', 20)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55, 40

SPACESHIP_YELLOW_IMAGE = pygame.image.load(os.path.join('asset','spaceship_yellow.png'))

SPACESHIP_YELLOW = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_YELLOW_IMAGE ,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)

SPACESHIP_RED_IMAGE = pygame.image.load(os.path.join('asset','spaceship_red.png'))

SPACESHIP_RED = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_RED_IMAGE ,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

def draw(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.fill(white)
    WIN.blit(BG,(0,0))
    pygame.draw.rect(WIN,black, BORDER)

    red_health_txt = HEALTH_FONT.render(" Health : " + str(red_health),1, white2)
    yellow_health_txt = HEALTH_FONT.render(" Health : " + str(yellow_health),1, white2)

    WIN.blit(red_health_txt,(WIDTH - red_health_txt.get_width() - 10,10))
    WIN.blit(yellow_health_txt,(10,10))

    WIN.blit(SPACESHIP_YELLOW,(yellow.x,yellow.y))
    WIN.blit(SPACESHIP_RED,(red.x,red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL>-10: #left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width<BORDER.x: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL>0: #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height<HEIGHT-15: #down
        yellow.y += VEL
        


def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL>BORDER.x + BORDER.width+15: #left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width<WIDTH+25: #right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL>0: #up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height<HEIGHT-15: #down
        red.y += VEL
    
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock=pygame.time.Clock()
    run =True 
    while run:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x-red.width+15,red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
            
            if event.type == RED_HIT:
                red_health -= 1
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        
        winner_txt = ""
        if red_health <= 0:
            winner_txt = "!! YELLOW WINS !!"
        
        if yellow_health <= 0:
            winner_txt = "!! RED WINS !!"

        if winner_txt != "":
            pass 
        
        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed,red)
        yellow_movement(keys_pressed,yellow)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        draw(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
    
    pygame.quit()

if __name__ == "__main__":
    main()