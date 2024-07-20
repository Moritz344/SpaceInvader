import pygame 
import random
import time

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
caption = pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# player var
player_speed = 5
player_x = 350
player_y = 500

health_bar_x = 50
health_bar_y = 10
# enemy var

enemy_nums = 40

enemies = [] # x und y werte werden gespeichert

enemies_red = []
enemy_red_num = 3

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("sounds/shoot.mp3")
hit_sound = pygame.mixer.Sound("sounds/hit.mp3")
background_music = pygame.mixer.Sound("sounds/music.mp3")
hit_sound.set_volume(0.1)
shoot_sound.set_volume(0.1)


init_enemy_y = 50
enemy_spacing_x = 80
enemy_spacing_y = 60

columns = screen_width // enemy_spacing_x 
rows = (400 - init_enemy_y) // enemy_spacing_y 

for i in range(enemy_nums):
          col = i % columns 
          row = i // columns 
          enemy_x = col * enemy_spacing_x
          enemy_y = init_enemy_y + row * enemy_spacing_y
     
          enemies.append([enemy_x,enemy_y])


enemy_speed = 0.5
enemy_speed_2 = 0.5


# Farben
black = (0,0,0)
white = (255,255,255)

# images
player = pygame.image.load("assets/player.png")
player_rect = player.get_rect()
player_rect.topleft = (player_x,player_y)
player_health = 3
background = pygame.image.load("assets/background.png")

# enemy 1
enemy = pygame.image.load("assets/enemy_3.png")
enemy= pygame.transform.scale(enemy,(50,50))
enemy_rect = enemy.get_rect()
enemy_rect.topleft = (enemy_x,enemy_y)

# enemy 2
enemy_2 = pygame.image.load("assets/enemy_3.png")
enemy_rect_2 = enemy_2.get_rect()
enemy_2 = pygame.transform.scale(enemy_2,(50,50))
enemy_rect_2.topleft = (enemy_x,enemy_y)

# bullet
bullet_size = 5
bullet_color = black
bullet_speed = 0.3

# Cooldown settings
cooldown_time = 200  # Cooldown time in milliseconds
last_shot_time = 0  # Time of the last shot

# Text
pygame.font.init()
font = pygame.font.SysFont("Minecraft",30)
font_big = pygame.font.SysFont("Minecraft",60)
font_medium = pygame.font.SysFont("Minecraft",40)

bullets = []
score_points = 0

def show_menu():
     menu = True
     while menu:
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    menu = False
                    
               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         menu = False
               if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_text_hitbox.collidepoint(event.pos):
                         menu = False


          mouse = pygame.mouse.get_pos()
          screen.blit(background,dest=(0,0))
          new_game = font_big.render("SPACE INVADERS",True,"green")
          screen.blit(new_game,dest=(130,100))

          start_text = font_medium.render("Start",True,"green")
          start_text_hitbox = pygame.draw.rect(screen,black,[320,300,130,50])

          if start_text_hitbox.collidepoint(mouse):
               start_text = font_medium.render("Start",True,white)
          else:
               start_text = font_medium.render("Start",True,"green")

          screen.blit(start_text,dest=(320,300))
          
          pygame.display.update()
          clock.tick(60)
show_menu()

def pause():
     stop = True
     while stop:
          global run
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    run = False
                    stop = False
                    
               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         stop = False
                    stop = False
               

          mouse = pygame.mouse.get_pos()
          
          pause_text = font_big.render("Paused",True,black)
          small_text = font.render("Press Any Key To Play",True,black)
          score_text_p = font_medium.render(f"Score: {score_points}",True,black)
          


          


          
          screen.fill(white)
          #button = pygame.draw.rect(screen,white,[310,300,150,50])
          #if button.collidepoint(mouse):
               #back_text = font_big.render("Back",True,"green")
          #else:
               #back_text = font_big.render("Back",True,black)

          screen.blit(pause_text,dest=(270,40))
          #screen.blit(back_text,dest=(310,300))
          screen.blit(small_text,dest=(200,500))
          #screen.blit(score_text_p,dest=(250,150))

          pygame.display.update()
          clock.tick(60)

run = True
while run:
     for event in pygame.event.get():
          current_time = pygame.time.get_ticks()
          if event.type == pygame.QUIT:
               run = False
          if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                    shoot_sound.play()
                    if current_time - last_shot_time > cooldown_time:
                         last_shot_time = current_time
                         bullet_pos = [player_x + 40,player_y]
                   
                         bullets.append(bullet_pos)
               if event.key == pygame.K_ESCAPE:
                    pause()

                    
     # update position
     player_rect.topleft = (player_x,player_y)
     enemy_rect.topleft = (enemy_x,enemy_y)
     
     
     


     # drawing player related things: hitbox,health_bar...
     screen.blit(background,dest=(0,0))
     hitbox = pygame.draw.rect(screen,black,[player_x + 14,player_y + 15,60,60])
     screen.blit(player,player_rect.topleft)

     health_bar = pygame.draw.rect(screen,"green",[player_x + 26,player_y + 80,health_bar_x,health_bar_y - 5])
     outline = pygame.draw.rect(screen,black,[player_x + 21,player_y + 60,50,10],3)
     
     for i in enemies:
          screen.blit(enemy,(i[0],i[1]))
     
     for i2 in enemies_red:
          screen.blit(enemy_2,(i2[0],i2[1]))
                
     def input_func():
          global player_x
          # Keyboard input
          pressed = pygame.key.get_pressed()
          if pressed[pygame.K_d]:
               player_x += player_speed
          elif pressed[pygame.K_a]:
               player_x -= player_speed
     
     def bullet_func():
          # bullet
          for bullet in bullets:
               bullet[1] -= 10

               if bullet[1] < 0:
                    bullets.remove(bullet)
          
          # bullet[1] und 0 x und y

     
          for bullet in bullets:
               player_bullet = pygame.draw.rect(screen,white,[bullet[0],bullet[1],4,20])

     # Kollision
     if player_x < 0:
          player_x = 0
     if player_x > 710:
          player_x = 710
     
     if enemy_nums == 0:
          enemy_nums = 40
          time.sleep(0.1)
          for i in range(enemy_nums):
               col = i % columns 
               row = i // columns 
               enemy_x = col * enemy_spacing_x
               enemy_y = init_enemy_y + row * enemy_spacing_y
     
               enemies.append([enemy_x,enemy_y])
     
     def object_collision():
          global health_bar_x,score_points,enemy_nums
          for i in enemies:
               enemy_rect = pygame.Rect(i[0],i[1],50,50)
               if hitbox.colliderect(enemy_rect):
                    health_bar_x -= 10
                    enemies.remove(i)
               
                    if health_bar_x == 0:
                         run = False
               

               for bullet in bullets:
                    bullet_rect = pygame.Rect(bullet[0],bullet[1],9,20)

                    if bullet_rect.colliderect(enemy_rect):
                         hit_sound.play()
                         score_points += 100
                         enemy_nums -= 1
                         bullets.remove(bullet)
                         #print("enemy dead")
                         i[0] = col * enemy_spacing_x
                         i[1] = init_enemy_y + row * enemy_spacing_y
                         enemies.remove(i)
                         break
                    
     

     score_text = font.render(f"{score_points}",True,white)
     screen.blit(score_text,dest=(10,0))

     if __name__ == "__main__":
          object_collision()
          bullet_func()
          input_func()
          

     pygame.display.update()
     clock.tick(60)

