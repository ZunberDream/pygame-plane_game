import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("plane_game")
clock = pygame.time.Clock()
text_UI = pygame.font.Font(None, 36)

time = 0
bullets_time = 0
bullets_shoot_speed = 10
my_plane_x = 400
my_plane_y = 300
my_plane_speed = 5
bullets = []
enemies = []
enemies_time = 0
enemies_shoot_speed = 100
my_health = 100
draw_my_health = 100

def draw_plane(x,y,type):
    if(type == "my"):
        pygame.draw.rect(screen, (0, 0, 139), (x-15, y-25, 30, 50))
        pygame.draw.polygon(screen, (0, 0, 139), [(x+10,y-20), (x+10,y+15), (x+30,y+20)])
        pygame.draw.polygon(screen, (0, 0, 139), [(x-10,y-20), (x-10,y+15), (x-30,y+20)])
        pygame.draw.polygon(screen, (0, 0, 139), [(x,y-50), (x-20,y+20), (x+20,y+20)])
        pygame.draw.polygon(screen, (0, 0, 139), [(x+10,y+20), (x-10,y+20), (x-20,y+30), (x,y+25), (x+20,y+30)])
    if(type == "enemy"):
        pygame.draw.polygon(screen, (139, 0, 0), [(x,y+25), (x+20,y-25), (x-20,y-25)])
        pygame.draw.polygon(screen, (139, 0, 0), [(x,y-15), (x-40,y-25), (x,y+20)])
        pygame.draw.polygon(screen, (139, 0, 0), [(x,y-15), (x+40,y-25), (x,y+20)])

def my_plane_move():
    global my_plane_x, my_plane_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        my_plane_x -= my_plane_speed
        if(my_plane_x < 0):
            my_plane_x = 0
    if keys[pygame.K_RIGHT]:
        my_plane_x += my_plane_speed
        if(my_plane_x > 800):
            my_plane_x = 800
    if keys[pygame.K_UP]:
        my_plane_y -= my_plane_speed
        if(my_plane_y < 0):
            my_plane_y = 0
    if keys[pygame.K_DOWN]:
        my_plane_y += my_plane_speed
        if(my_plane_y > 600):
            my_plane_y = 600

def bullets_run():
    global bullets_time
    bullets_time += 1
    if(bullets_time == bullets_shoot_speed):
        bullets.append({"x": my_plane_x-10, "y": my_plane_y-10, "speed":10, "size":1})
        bullets.append({"x": my_plane_x+10, "y": my_plane_y-10, "speed":10, "size":1})
        bullets_time = 0
    for p in bullets[:]:
        if(p["y"] < -100):
            bullets.remove(p)
            continue
        p["y"] -= p["speed"]
        pygame.draw.rect(screen, (255, 255, 255), (p["x"]-2.5*p["size"], p["y"]-5*p["size"], 5*p["size"], 10*p["size"]))
        for enemy in enemies[:]:
            if (abs(p["x"] - enemy["x"]) < 25 and abs(p["y"] - enemy["y"]) < 30):
                bullets.remove(p)
                enemies.remove(enemy)
                break

def enemies_run():
    global enemies_time, my_health
    enemies_time += 1
    if(enemies_time == enemies_shoot_speed):
        enemies_time = 0
        enemies.append({"x":random.randint(50,750) , "y":-50 , "speed":5, "size":1})
    for p in enemies[:]:
        if(p["y"] > 800):
            enemies.remove(p)
            continue
        p["y"] += p["speed"]
        if abs(p["x"] - my_plane_x) < 50 and abs(p["y"] - my_plane_y) < 50:
            my_health -= 10
            enemies.remove(p)
            continue
        draw_plane(p["x"], p["y"], "enemy")

def draw_UI():
    global draw_my_health
    pygame.draw.rect(screen, (255, 0, 0), (16, 546, 100*3+8, 38))
    pygame.draw.rect(screen, (150, 0, 0), (20, 550, draw_my_health*3, 30))
    my_health_text = text_UI.render(f"HP: {my_health} / 100", True, (0, 0, 0))
    draw_my_health += (my_health - draw_my_health) * 0.1
    screen.blit(my_health_text, (22, 552))
    

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time += 1

    screen.fill((10, 10, 30))

    bullets_run()

    enemies_run()

    my_plane_move()

    draw_UI()

    draw_plane(my_plane_x, my_plane_y, "my")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()