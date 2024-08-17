import pygame 
import random
import time
import sys

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
caption = pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 60
# player var
player_speed = 5
player_x = 350
player_y = 500


# enemy var

enemy_nums = 20

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
     
          enemies.append({"x":enemy_x,"y":enemy_y})


enemy_speed = 0.5
enemy_speed_2 = 0.5


# Farben
black = (0,0,0)
white = (255,255,255)

# images
player = pygame.image.load("assets/player.png")
player = pygame.transform.scale(player,(50,50))
player_rect = player.get_rect()
player_rect.topleft = (player_x,player_y)
player_health = 3
background = pygame.image.load("assets/background.png")

# enemy 1
enemy = pygame.image.load("assets/enemy_3.png")
enemy= pygame.transform.scale(enemy,(50,50))
enemy_rect = enemy.get_rect()
enemy_rect.topleft = (enemy_x,enemy_y)



# bullet
bullet_size = 5
bullet_color = black
bullet_speed = 0.3

# Cooldown settings
cooldown_time = 200  # Cooldown time in milliseconds
last_shot_time = 0  # Time of the last shot

cooldown_time_2 = 300
last_shot_time_2 = 0

# Text
pygame.font.init()
font = pygame.font.SysFont("Minecraft",30)
font_big = pygame.font.SysFont("Minecraft",60)
font_medium = pygame.font.SysFont("Minecraft",40)

bullets = []
score_points = 0

#level
level = 0

enemy_bullets = []
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



class Protection:
     def __init__(self,x,y):
          self.pos_x = x
          self.pos_y = y
          self.width = 80
          self.height = 40

     def update(self):
               self.width = 80
               self.height = 40
               
               self.obj_1 = pygame.draw.rect(screen,"white",[self.pos_x + 0 ,self.pos_y ,self.width,self.height])
               #pygame.draw.rect(screen,"blue",[self.pos_x + 300 ,self.pos_y,self.width,self.height])
               self.obj_2 = pygame.draw.rect(screen,"white",[self.pos_x + 500 ,self.pos_y,self.width,self.height])


prot = Protection(100,450)
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
                         bullet_pos = [player_x + 30,player_y - 50]
                         
                         bullets.append(bullet_pos)
               if event.key == pygame.K_ESCAPE:
                    show_menu( )
                         
               

                    
     # update position
     player_rect.topleft = (player_x,player_y)
     
     
     # enemy bullets
     
     for x in enemies:
          enemy_rect.topleft = (x["x"] ,x["y"])

     
          if random.randint(1,500) < 2:
               for i in range(3):

                    enemy_bullet_pos = [x["x"] + 25 + i,x["y"] + 50]
                    enemy_bullets.append(enemy_bullet_pos)
          

     
     
     
     


     # drawing player related things: hitbox,health_bar...
     #screen.blit(background,dest=(0,0))
     grey = (32,32,32)
     screen.fill(grey)
     #hitbox = pygame.draw.rect(screen,black,[player_x + 14,player_y + 15,60,60])
     hitbox_rect = pygame.rect.Rect(player_x + 14,player_y + 15,60,60)
     screen.blit(player,player_rect.topleft)

     
     #outline = pygame.draw.rect(screen,black,[player_x + 21,player_y + 60,50,10],3)
     
     for i3 in enemies:
          screen.blit(enemy,(i3["x"],i3["y"]))
     
     #for i2 in enemies_red:
          #screen.blit(enemy_2,(i2[0],i2[1]))
     
     
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

          for i in enemy_bullets:
               i[1] += 10

               
               enemy_attack = pygame.draw.rect(screen,white,[i[0],i[1],4,20])
                    #enemy_attack_rect = pygame.rect.Rect(i3["x"],i3["y"],4,20)
               if i[1] > screen_height:
                    enemy_bullets.remove(i)
                    print("enemy removed!")
               
               if enemy_attack.colliderect(prot.obj_1) or enemy_attack.colliderect(prot.obj_2):
                    enemy_bullets.remove(i)
               
               if enemy_attack.colliderect(hitbox_rect):
                    enemy_bullets.remove(i)
                    
               



     # Kollision
     if player_x < 0:
          player_x = 0
     if player_x > 710:
          player_x = 710
     
     if enemy_nums == 0:
          level += 1
          enemy_nums = 20
          time.sleep(0.1)
          for i in range(enemy_nums):
               col = i % columns 
               row = i // columns 
               enemy_x = col * enemy_spacing_x
               enemy_y = init_enemy_y + row * enemy_spacing_y
     
               enemies.append({"x": enemy_x, "y": enemy_y})
     
     def object_collision():
          global score_points,enemy_nums
          for n in enemies:
               enemy_rect = pygame.Rect(n["x"],n["y"],50,50)
               
                    
               

               for bullet in bullets:
                    bullet_rect = pygame.Rect(bullet[0],bullet[1],9,20)

                    if bullet_rect.colliderect(enemy_rect):
                         hit_sound.play()
                         score_points += 100
                         enemy_nums -= 1
                         bullets.remove(bullet)
                         n[0] = col * enemy_spacing_x
                         n[1] = init_enemy_y + row * enemy_spacing_y
                         enemies.remove(n)
                         break
                    #if prot.obj_1.colliderect(bullet_rect):
                         #bullets.remove(bullet)
                    #if prot.obj_2.colliderect(bullet_rect):
                         #bullets.remove(bullet)
                    

                    
                    
     

     score_text = font.render(f"SCORE {score_points}",True,white)
     level_text = font.render(f"LEVEL {level}",True,white)
     fps_text = font.render(f"FPS {FPS}",True,white)

     screen.blit(score_text,dest=(10,0))
     screen.blit(level_text,dest=(310,0))
     screen.blit(fps_text,dest=(660,0))

     if __name__ == "__main__":
          object_collision()
          bullet_func()
          input_func()
          
          prot.update()
     pygame.display.update()
     clock.tick(FPS)

