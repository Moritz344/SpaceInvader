import pygame
import random
import time
import sys
import os

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

current_bullet_color = "white"
colours = ["green","white"]


enemy_nums = 0

enemies = [] # x und y werte werden gespeichert
enemies_2 = []
add_enemy = False


pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("sounds/shoot.mp3")
hit_sound = pygame.mixer.Sound("sounds/hit.mp3")
background_music = pygame.mixer.Sound("sounds/music.mp3")
hit_sound.set_volume(0.1)
shoot_sound.set_volume(0.1)

exploding = pygame.image.load("assets/exlodingInvader.png")
exploding = pygame.transform.scale(exploding,(50,30))

exploding_green = pygame.image.load("assets/explosiongreen.png")
exploding_green = pygame.transform.scale(exploding_green,(50,35))

init_enemy_y = 80
enemy_spacing_x = 80
enemy_spacing_y = 50
enemy_direction = 1
max_pos_y = 280
columns = screen_width // enemy_spacing_x 
rows = (900 - init_enemy_y) // enemy_spacing_y

init_enemy_y_2 = 0
enemy_spacing_y_2 = 0
row_2 = 0

level = 0

def spawn_enemy():
     global enemy_nums,enemy_x,enemy_y,init_enemy_y,col,row,level,enemy_x_2,enemy_y_2
     #add_enemy = True
     level += 1
     if level <= 3:
          enemy_nums = 5
     else:
          enemy_nums = 10
     time.sleep(0.1)
     for i in range(enemy_nums):
          col = i % 5 
          row = i // 5

          enemy_x = col * enemy_spacing_x  + 50
          enemy_y = init_enemy_y + row * enemy_spacing_y #+ 100

          enemy_x_2 = col * enemy_spacing_x + 50
          if enemy_nums == 10:
               enemy_y_2 = init_enemy_y + row * enemy_spacing_y + 100
          else:
               enemy_y_2 = init_enemy_y + row * enemy_spacing_y + 50
               
     
          enemies.append({"x": enemy_x, "y": enemy_y,"speed":1,})
          enemies_2.append({"x2":enemy_x_2,"y2": enemy_y_2,"speed": 1})

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
enemy = pygame.image.load("assets/invader02a.png")
enemy= pygame.transform.scale(enemy,(50,35))
sprites = [
            pygame.image.load("assets/invader02a.png"),
            pygame.image.load("assets/invader02b.png"),

        ]
index = 0
current_time = 0
current_sprite = sprites
animation_speed = 0.015

enemy_2 = pygame.image.load("assets/enemy3_1.png")
enemy_2 = pygame.transform.scale(enemy_2,(50,35))
sprites_2 = [
     pygame.image.load("assets/enemy3_1.png"),
     pygame.image.load("assets/enemy3_2.png")

]
index_2 = 0
current_time_2 = 0
current_sprite_2 = sprites_2

enemy_rect_2 = enemy_2.get_rect()
enemy_rect_2.topleft = (enemy_x_2,enemy_y_2)

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
explosion_duration = 10
explosions = []
explosions_green = []
# Text
pygame.font.init()
font = pygame.font.SysFont("Minecraft",55)
font_big = pygame.font.SysFont("Minecraft",70)
font_medium = pygame.font.SysFont("spaceinvadersregular",60)
font_small = pygame.font.SysFont("Minecraft",30)

bullets = []
score_points = 0

#level

enemy_bullets = []
def show_menu():
     global player_live,level,score_points
     teleport = False
     menu = True
     while menu:
          player_live = 4
          level = 0
          score_points = 0
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
          exit_pos_x = 540
          exit_pos_y = 320
          #pygame.draw.rect(screen,"light grey",[0,0,900,100])
          mouse = pygame.mouse.get_pos()

          button_1 = pygame.draw.rect(screen,grey,[100,300,200,80])
          button_2 = pygame.draw.rect(screen,grey,[exit_pos_x,exit_pos_y,200,80])

          
          

          enemy_img = pygame.image.load("assets/alien.png")
          
          #enemy_img = pygame.transform.scale(enemy_img,(150,50))

          if button_1.collidepoint(mouse):
                text_1 = font.render("START",True,"green")
          else:
                text_1 = font.render("START",True,"white")


          if button_2.collidepoint(mouse):
                text_2 = font.render(":(",True,"red")
                screen.blit(text_2,dest=(exit_pos_x,exit_pos_y))
          else:
                text_2 = font.render("EXIT",True,"white")
                screen.blit(text_2,dest=(exit_pos_x,exit_pos_y))
                #teleport = False


          
          
          #button_3 = pygame.draw.rect(screen,"red",[1000,300,200,80])

         
          #text_2 = font.render("EXIT",True,"black")
          text_3 = font_big.render("SPACEINVADERS",True,"white")
          
          

          screen.blit(text_1,dest=(104,320))
          
          screen.blit(text_3,dest=(90,15))
          #screen.blit(enemy_img,dest=(240,150))
          pygame.display.update()
          clock.tick(60)
show_menu()

def load_highscore():
     if os.path.exists("score.txt"):
          with open("score.txt","r") as file:
               data = file.readlines()
               data = [int(score_points.strip()) for score_points in data]
               return data
     else:
          return []

def save_score(data):
     with open("score.txt","w") as file:
          data.sort(reverse=True)

          for score_points in data:
               file.write(f"{score_points}\n")


def update_score(highscore_list):
     highscore_list.append(score_points)
     return highscore_list


class Protection:
     def __init__(self,x,y):
          self.pos_x = x
          self.pos_y = y

          self.width = 80
          self.height = 40

          self.width_2 = 80
          self.height_2 = 40

          self.height_reduced = False  

          self.obj_colour_2 = "dark green"
          self.block_1_width = 40
          self.block_1_height = 20
          self.block_2_height = 20
          self.block_3_height = 20
          self.block_4_height = 20

          self.obj_colour = "dark green"
          
          self.block_6_height = 20
          self.block_6_width = 40
          self.block_7_height = 20
          self.block_8_height = 20
          self.block_9_height = 20

     def update(self):
               
               #self.obj_1 = pygame.draw.rect(screen,self.obj_colour,[self.pos_x + 0 ,self.pos_y ,self.width,self.height])
               self.obj_1_block_1 = pygame.draw.rect(screen,self.obj_colour,[self.pos_x,self.pos_y,self.block_1_width,self.block_1_height])
               self.obj_2_block_2 = pygame.draw.rect(screen,self.obj_colour,[self.pos_x + 40,self.pos_y,40,self.block_2_height])
               self.obj_3_block_3 = pygame.draw.rect(screen,self.obj_colour,[self.pos_x,self.pos_y + 20,self.block_1_width,self.block_3_height])
               self.obj_4_block_4 = pygame.draw.rect(screen,self.obj_colour,[self.pos_x + 40,self.pos_y + 20,40,self.block_4_height])



               self.obj_6_block_6 = pygame.draw.rect(screen,self.obj_colour  ,[self.pos_x + 500,self.pos_y,40,self.block_6_height])
               self.obj_7_block_7 = pygame.draw.rect(screen,self.obj_colour,[self.pos_x + 540,self.pos_y,self.block_1_width,self.block_7_height])
               self.obj_8_block_8 = pygame.draw.rect(screen,self.obj_colour,[self.pos_x + 500,self.pos_y + 20,40,self.block_8_height])
               self.obj_9_block_9 = pygame.draw.rect(screen,self.obj_colour,[self.pos_x + 540,self.pos_y + 20,self.block_1_width,self.block_9_height])

class Item():
     def __init__(self,x,y,spawn_delay=15):
          self.x = x
          self.y = y
          
          self.items = [{"x": self.x,"y":self.y,"speed":2 }]

          self.spawn_delay = spawn_delay
          self.last_spawn_time = time.time()
          self.active = True
          
          self.heart_img = pygame.image.load("assets/heart.png")
          self.heart_img = pygame.transform.scale(self.heart_img,(50,50))

     def update(self):
        # Falls es keine aktiven Items gibt, überprüfen, ob ein neues Item gespawnt werden soll
        if not self.items:
            if time.time() - self.last_spawn_time >= self.spawn_delay:
                # Füge ein neues Item hinzu
                self.items.append({"x": random.randint(0, 500), "y": 10, "speed": 2})
                self.last_spawn_time = time.time()
                self.active = True

        # looping through the items
        for item in self.items[:]:  # copy
            if self.active:
                
                item["y"] += item["speed"]

                self.y = item["y"]
                self.x = item["x"]

               
                screen.blit(self.heart_img, dest=(self.x, self.y))
                self.item_rect = pygame.Rect(self.x, self.y, 50, 50)

                # checking if item left the screen
                if item["y"] > screen_height:
                    self.items.remove(item)  
                    self.active = False  
                    self.last_spawn_time = time.time() 
        #print(self.last_spawn_time - time.time())
        #print(self.x, self.y)

player_live = 4
def decrease_player_life(amount):
     global player_live
     player_live -= amount

     if player_live < 0:
          player_live = 0

highscores = load_highscore()

prot = Protection(100,450)
item = Item(random.randint(0,500),random.randint(0,100))
highscores = update_score(highscores)
save_score(highscores)

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
                    shoot_sound.play() 
     
     
     
     


     grey = (32,32,32)
     screen.fill(grey)
     hitbox_rect = pygame.rect.Rect(player_x - 5,player_y ,60,60)
     #pygame.draw.rect(screen,"red",[player_x - 5,player_y ,60,60],5)
     screen.blit(player,player_rect.topleft)

     
     for enemy_2 in enemies_2:
          index_2 += 0.01
          if index_2 >= len(sprites_2):
               index_2 = 0
          current_sprite_2 = sprites_2[int(index_2)]
          current_sprite_2 = pygame.transform.scale(current_sprite_2,(50,35))


          screen.blit(current_sprite_2,(enemy_2["x2"],enemy_2["y2"]))
          enemy_2["x2"] += enemy_2["speed"] * enemy_direction
          

          if enemy_2["x2"] <= 0 or enemy_2["x2"] >= screen_width - enemy.get_width():
                    enemy_direction *= -1
                    break
    
     for i3 in enemies:
          index += 0.01
         
          if index >= len(sprites):
               index = 0

          

          current_sprite = sprites[int(index)]
         
          current_sprite = pygame.transform.scale(current_sprite,(50,35))
          screen.blit(current_sprite,(i3["x"],i3["y"]))

         

          
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
          global player_live,enemy_attack,player_bullet
          # bullet
          for bullet in bullets:
               bullet[1] -= 10

               if bullet[1] < 0:
                    bullets.remove(bullet)
               
          
          # bullet[1] und 0 x und y

     
          for bullet in bullets:
               player_bullet = pygame.draw.rect(screen,white,[bullet[0],bullet[1],4,20])
               if player_bullet.colliderect(prot.obj_1_block_1) and not prot.height_reduced:
                    #prot.height -= 5
                    prot.block_1_height = 0
                    prot.height_reduced = True
                    #prot.obj_colour = "grey"
                    bullets.remove(bullet)
               if player_bullet.colliderect(prot.obj_2_block_2) and not prot.height_reduced:
                    #prot.height_2 -= 5
                    prot.height_reduced = True
                    prot.block_2_height = 0
                    prot.obj_colour_2 = "grey"
                    bullets.remove(bullet)
               if player_bullet.colliderect(prot.obj_3_block_3) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_3_height = 0
                    bullets.remove(bullet)
               if player_bullet.colliderect(prot.obj_4_block_4) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_4_height = 0
                    bullets.remove(bullet)

               if player_bullet.colliderect(prot.obj_6_block_6) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_6_height = 0
                    bullets.remove(bullet)
               if player_bullet.colliderect(prot.obj_7_block_7) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_7_height = 0
                    bullets.remove(bullet)
               if player_bullet.colliderect(prot.obj_8_block_8) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_8_height = 0
                    bullets.remove(bullet)
               if player_bullet.colliderect(prot.obj_9_block_9) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_9_height = 0
                    bullets.remove(bullet)
               
               else:
                    prot.height_reduced = False

          for item_ in item.items:
               for bullet in bullets:
                    player_bullet = pygame.draw.rect(screen,white,[bullet[0],bullet[1],4,20])
                    if player_bullet.colliderect(item.item_rect):
                         player_live += 1
                         print("Item: Kollision mit Spieler bullet")
                         item.items.remove(item_)

          

          for i in enemy_bullets:
               i[1] += 5
               #i[0] += random.randint(0,2)

               
               
               enemy_attack = pygame.draw.rect(screen,current_bullet_color,[i[0],i[1],4,20])

               if i[1] > screen_height:
                    enemy_bullets.remove(i)
                    print("enemy: bullet removed!")

               
               
               if enemy_attack.colliderect(prot.obj_1_block_1) and not prot.height_reduced:
                    prot.block_1_height = 0
                    prot.height_reduced = True
                    enemy_bullets.remove(i)
               elif enemy_attack.colliderect(prot.obj_2_block_2) and not prot.height_reduced:
                    prot.block_2_height = 0
                    prot.height_reduced = True
                    enemy_bullets.remove(i)
               elif enemy_attack.colliderect(prot.obj_3_block_3) and not prot.height_reduced:
                    prot.block_3_height = 0
                    prot.height_reduced = True
                    enemy_bullets.remove(i)
               elif enemy_attack.colliderect(prot.obj_4_block_4) and not prot.height_reduced:
                    prot.block_4_height = 0
                    prot.height_reduced = True
                    enemy_bullets.remove(i)

               elif enemy_attack.colliderect(prot.obj_6_block_6) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_6_height = 0
                    enemy_bullets.remove(i)
               elif enemy_attack.colliderect(prot.obj_7_block_7) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_7_height = 0
                    enemy_bullets.remove(i)
               elif enemy_attack.colliderect(prot.obj_8_block_8) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_8_height = 0
                    enemy_bullets.remove(i)
               elif enemy_attack.colliderect(prot.obj_9_block_9) and not prot.height_reduced:
                    prot.height_reduced = True
                    prot.block_9_height = 0
                    enemy_bullets.remove(i)

               
                    
               else:
                    prot.height_reduced = False
               if enemy_attack.colliderect(hitbox_rect):
                    player_live -= 1
                    print("Player hit!",player_live)
                    enemy_bullets.remove(i)
                    decrease_player_life(1)
               
               # player bullet collision with enemy bullet
               for bullet in bullets:
                    bullet_rect = pygame.Rect(bullet[0],bullet[1],9,20)
                    if bullet_rect.colliderect(enemy_attack):
                         enemy_bullets.remove(i)
                         


               
                    
     if player_live == 0:
               show_menu() 
               


     # Kollision
     if player_x < 0:
          player_x = 0
     if player_x > 750:
          player_x = 750
     

     if len(enemies) == 0 and len(enemies_2) == 0:
          add_enemy = True
          enemy_nums += 10
          if add_enemy:
               spawn_enemy()    

     else:
          add_enemy = False
     
     def object_collision():
          global score_points,enemy_nums,enemy_rect_2,bullet_rect
          for n in enemies:
               enemy_rect = pygame.Rect(n["x"],n["y"],50,35)
               
               
                    
 

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

                         explosions.append({"pos": (n["x"],n["y"] ), "timer": explosion_duration})
                         
                         #screen.blit(exploding,dest=(bullet[0] ,bullet[1] - 40))
                         break
                    


          for n in enemies_2:
               enemy_rect_2 = pygame.Rect(n["x2"], n["y2"], 50, 35)
               
               for bullet in bullets:
                    bullet_rect = pygame.Rect(bullet[0], bullet[1], 9, 20)
                    if bullet_rect.colliderect(enemy_rect_2):
                         hit_sound.play()
                         score_points += 150  # Punkte für enemy_2
                         enemy_nums -= 1
                         bullets.remove(bullet)
                         enemies_2.remove(n)
                         explosions_green.append({"pos2": (n["x2"], n["y2"]), "timer2": explosion_duration})
                         break
                   
     for explosion in explosions:
          screen.blit(exploding,dest=(explosion["pos"]))
          explosion["timer"] -= 1
          
          if explosion["timer"] <= 0:
               explosions.remove(explosion)

     for explosion2 in explosions_green:
          screen.blit(exploding_green,dest=(explosion2["pos2"]))
          explosion2["timer2"] -= 1

          if explosion2["timer2"] <= 0:
               explosions_green.remove(explosion2)

     
     
           
     

     score_text = font_small.render(f"SCORE {score_points}",True,white)
     highscore_text = font_small.render(f"HighScore {highscores[0] if highscores else 0}",False,white)
     level_text = font_small.render(f"LEVEL {level}",True,white)
     fps_text = font.render(f"FPS {FPS}",True,white)
     player_live_text = font_small.render(f"LIVES {player_live}",True,white)
    #pygame.draw.line(screen, "white", (0, screen_height - 30), (screen_width, screen_height - 30), 2)


     screen.blit(score_text,dest=(10,10))
     screen.blit(player_live_text,dest=(650,10))
     screen.blit(level_text,dest=(10,50))
     screen.blit(highscore_text,dest=(270,10))
     #screen.blit(fps_text,dest=(10,100))

     if __name__ == "__main__":
          object_collision()
          bullet_func()
          input_func()
          
          prot.update()
          item.update()
     pygame.display.update()
     clock.tick(FPS); #<--- wtf                                                                                                                                                                                                                          secret = "HIDDEN SECRET!!!"
          
