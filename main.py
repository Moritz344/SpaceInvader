import pygame
import random
import time
import sys

#HORRIBLE CODE

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



enemy_nums = 0

enemies = [] # x und y werte werden gespeichert
enemies_red = []
enemy_red_num = 3
add_enemy = False

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("sounds/shoot.mp3")
hit_sound = pygame.mixer.Sound("sounds/hit.mp3")
background_music = pygame.mixer.Sound("sounds/music.mp3")
hit_sound.set_volume(0.1)
shoot_sound.set_volume(0.1)

init_enemy_y = 80
enemy_spacing_x = 80
enemy_spacing_y = 50
enemy_direction = 1
max_pos_y = 280
columns = screen_width // enemy_spacing_x 
rows = (900 - init_enemy_y) // enemy_spacing_y



def spawn_enemy():
     global enemy_nums,enemy_x,enemy_y,init_enemy_y,col,row
     #add_enemy = True
     #level += 1
     
     enemy_nums += 5
     time.sleep(0.1)
     for i in range(enemy_nums):
          col = i % 5 
          row = i // 5

          enemy_x = col * enemy_spacing_x  + 50
          enemy_y = init_enemy_y + row * enemy_spacing_y #+ 100
               
     
          enemies.append({"x": enemy_x, "y": enemy_y,"speed":1})
     init_enemy_y += enemy_spacing_y
     if init_enemy_y >= 280:
          print("Maximum y erreicht!")
          init_enemy_y = 100
          enemy_y = 0

spawn_enemy()


enemy_speed = 0.5
enemy_speed_2 = 0.5


# Farben
black = (0,0,0)
white = (255,255,255)

# images
player = pygame.image.load("assets/player.png")
player = pygame.transform.scale(player,(50,50))
player_2 = pygame.transform.scale(player,(25,25))
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
cooldown_time = 500  # Cooldown time in milliseconds
last_shot_time = 0  # Time of the last shot

cooldown_time_2 = 300
last_shot_time_2 = 0

# Text
pygame.font.init()
font = pygame.font.SysFont("Minecraft",55)
font_big = pygame.font.SysFont("Minecraft",70)
font_medium = pygame.font.SysFont("spaceinvadersregular",60)
font_small = pygame.font.SysFont("Minecraft",30)

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
                    if button_1.collidepoint(event.pos):
                         menu = False
                    if button_2.collidepoint(event.pos):
                         sys.exit("bye")
                    
          grey = (32,32,32)
          home = pygame.image.load("assets/background.png")
          #screen.blit(home,dest=(0,0))
          screen.fill(grey)
          #pygame.draw.rect(screen,"light grey",[0,0,900,100])
          mouse = pygame.mouse.get_pos()

          button_1 = pygame.draw.rect(screen,grey,[100,300,200,80])
          button_2 = pygame.draw.rect(screen,grey,[500,300,200,80])

          enemy_img = pygame.image.load("assets/alien.png")
          
          #enemy_img = pygame.transform.scale(enemy_img,(150,50))

          if button_1.collidepoint(mouse):
                text_1 = font.render("START",True,"green")
          else:
                text_1 = font.render("START",True,"white")


          if button_2.collidepoint(mouse):
                text_2 = font.render("EXIT",True,"green")
          else:
                text_2 = font.render("EXIT",True,"white")



          
          #button_3 = pygame.draw.rect(screen,"red",[1000,300,200,80])

         
          #text_2 = font.render("EXIT",True,"black")
          text_3 = font_big.render("SPACEINVADERS",True,"white")
          
          screen.blit(text_1,dest=(104,320))
          screen.blit(text_2,dest=(540,320))
          screen.blit(text_3,dest=(90,15))
          #screen.blit(enemy_img,dest=(240,150))
          pygame.display.update()
          clock.tick(60)
show_menu()

def gameover():
     gameover = True
     while gameover:
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    gameover = False
          
          pygame.display.update()
          clock.tick(FPS)



class Protection:
     def __init__(self,x,y):
          self.pos_x = x
          self.pos_y = y

          self.width = 80
          self.height = 40

          self.width_2 = 80
          self.height_2 = 40

          self.height_reduced = False  

          self.obj_colour = "white"
          self.obj_colour_2 = "white"

     def update(self):
               
               self.obj_1 = pygame.draw.rect(screen,self.obj_colour,[self.pos_x + 0 ,self.pos_y ,self.width,self.height])
               self.obj_2 = pygame.draw.rect(screen,self.obj_colour_2,[self.pos_x + 500 ,self.pos_y,self.width_2,self.height_2])

player_live = 3
def decrease_player_life(amount):
     global player_live
     player_live -= amount

     if player_live < 0:
          player_live = 0

prot = Protection(100,450)
run = True
while run:
     for event in pygame.event.get():
          current_time = pygame.time.get_ticks()
          if event.type == pygame.QUIT:
               run = False
          if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                    
                    if current_time - last_shot_time > cooldown_time:
                         last_shot_time = current_time
                         bullet_pos = [player_x + 20,player_y - 20]
                         shoot_sound.play()
                         
                         bullets.append(bullet_pos)
               if event.key == pygame.K_ESCAPE:
                    show_menu( )
                         
               
                    
     # update position
     player_rect.topleft = (player_x,player_y)
     
     
     # enemy bullets
     
     for i3 in enemies:
          enemy_rect.topleft = (i3["x"] ,i3["y"])
          if random.randint(1,600) < 2:
               for i in range(1):
                    enemy_bullet_pos = [i3["x"] + 25,i3["y"] + 50]
                    enemy_bullets.append(enemy_bullet_pos)
          

     
     
     
     


     grey = (32,32,32)
     screen.fill(grey)
     hitbox_rect = pygame.rect.Rect(player_x - 5,player_y ,60,60)
     #pygame.draw.rect(screen,"red",[player_x - 5,player_y ,60,60],5)
     screen.blit(player,player_rect.topleft)

    
     for i3 in enemies:
          screen.blit(enemy,(i3["x"],i3["y"]))
          
          i3["x"] += i3["speed"] * enemy_direction

          if i3["x"] <= 0 or i3["x"] >= screen_width - enemy.get_width():
                    enemy_direction *= -1
                    break
               

     
     
     def input_func():
          global player_x
          # Keyboard input
          pressed = pygame.key.get_pressed()
          if pressed[pygame.K_d]:
               player_x += player_speed
          elif pressed[pygame.K_a]:
               player_x -= player_speed
     
     def bullet_func():
          global player_live
          # bullet
          for bullet in bullets:
               bullet[1] -= 10

               if bullet[1] < 0:
                    bullets.remove(bullet)
               
          
          # bullet[1] und 0 x und y

     
          for bullet in bullets:
               player_bullet = pygame.draw.rect(screen,white,[bullet[0],bullet[1],4,20])
               if player_bullet.colliderect(prot.obj_1) and not prot.height_reduced:
                    prot.height -= 5
                    prot.height_reduced = True
                    prot.obj_colour = "grey"
                    bullets.remove(bullet)  
               if player_bullet.colliderect(prot.obj_2) and not prot.height_reduced:
                    prot.height_2 -= 5
                    prot.height_reduced = True
                    
                    prot.obj_colour_2 = "grey"
                    bullets.remove(bullet)  
               else:
                    prot.height_reduced = False

          for i in enemy_bullets:
               i[1] += 10

               
               enemy_attack = pygame.draw.rect(screen,white,[i[0],i[1],4,20])
                    #enemy_attack_rect = pygame.rect.Rect(i3["x"],i3["y"],4,20)
               if i[1] > screen_height:
                    enemy_bullets.remove(i)
                    print("enemy removed!")

               
               
               if enemy_attack.colliderect(prot.obj_1) and not prot.height_reduced:
                    prot.obj_colour = "grey"
                    prot.height -= 5
                    prot.height_reduced = True
                    enemy_bullets.remove(i)
               if enemy_attack.colliderect(prot.obj_2) and not prot.height_reduced:
                    prot.obj_colour_2 = "grey"
                    prot.height_2 -= 5
                    prot.height_reduced = True
                    enemy_bullets.remove(i)
               
                    
               else:
                    prot.height_reduced = False
               if enemy_attack.colliderect(hitbox_rect):
                    player_live -= 1
                    print("Player hit!",player_live)
                    enemy_bullets.remove(i)
                    decrease_player_life(1)
                    
               



     # Kollision
     if player_x < 0:
          player_x = 0
     if player_x > 750:
          player_x = 750
     

     if len(enemies) == 0:
          add_enemy = True
          enemy_nums += 5
          if add_enemy:
               spawn_enemy()    

     else:
          add_enemy = False
     
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
                   

    
     
                    
     

     score_text = font_small.render(f"SCORE {score_points}",True,white)
     level_text = font.render(f"LEVEL {level}",True,white)
     fps_text = font.render(f"FPS {FPS}",True,white)
    #pygame.draw.line(screen, "white", (0, screen_height - 30), (screen_width, screen_height - 30), 2)


     screen.blit(score_text,dest=(10,10))
     #screen.blit(level_text,dest=(10,50))
     #screen.blit(fps_text,dest=(10,100))

     if __name__ == "__main__":
          object_collision()
          bullet_func()
          input_func()
          
          prot.update()
     pygame.display.update()
     clock.tick(FPS); #<--- wtf                                                                                                                                                                                                                          secret = "HIDDEN SECRET!!!"
          
