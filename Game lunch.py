# Maze Game.py

from pygame import *
from random import * 

window_width = 1350
window_height = 700
window = display.set_mode((window_width, window_height))
display.set_caption("Danger Maze")

background_picture = image.load("assets/backgrounds/Background_game.png")
win_Background =transform.scale(image.load("assets/backgrounds/Win_Background.png"),(window_width, window_height))
Game_over_Background = transform.scale(image.load("assets/backgrounds/You_Died.png"),(window_width, window_height))

Player_speed = 3
arrow_width = 30
arrow_height = 5

CANON_RANGE = 250   # If the player is within this range, SHOOT!
CANON_COOLDOWN   = 100  # Frames between shots every shoot
CANON_BULLET_SPEED_UP = 5
CANON_BULLET_SPEED_DOWN = 5
CANON_BULLET_WIDTH = 20
CANON_BULLET_HEIGHT = 20
LETHAL_DAMAGE = 9999

DRAGON_RANGE = 150
DRAGON_COOLDOWN = 100
DRAGON_FIRE_BALL_SPEED = 2
FIRE_BALL_WIDTH = 50
FIRE_BALL_HEIGHT = 50

GREAT_DRAGON_ATK_COOLDOWN = 300
GREAT_DRAGON_DEATH_ANIM_SPEED = 2
GREAT_DRAGON_IDLE_ANIM_SPEED = 3
GREAT_DRAGON_ATK_ANIM_SPEED = 2

BUTTON_ANIMATION_FRAMES =5
LASER_Gate_OPEN_Frames = 10
Player_death = False
Blue_Zone = Rect(340, 360, 510, 70) # The zone detection between wall 23(y=360), wall 18(x=340), wall 43(y=430), wall 24(x=850) 
Red_Zone = Rect(340,430,540,230) # The zone detection between wall 43(y=430), wall 18 (x=340), wall 36 (x=880), wall 3 (y=660)

#Sprite classes 
class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class RedButton(GameSprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)
        self.pressing_frames = [transform.scale(image.load(f"assets/mechanisms/Red_button_{i}.png"), (w,h)) for i in [1,2]]
        self.is_pressed = False
        self.animation_frame =0
        self.animation_speed = 5
        self.animation_counter = 0

    def update(self):
        if self.is_pressed:
            self.animation_counter +=1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter =0
                self.animation_frame = min(self.animation_frame + 1, 1)

            self.image = self.pressing_frames[self.animation_frame]
            
            if self.animation_frame == 1:
                Laser_Gate.start_opening()

class LaserGate(GameSprite):
    def __init__(self, picture, w, h, x, y,):
        super().__init__(picture, w, h, x, y)
        self.open_frames = [transform.scale(image.load(f"assets/mechanisms/Red_Laser_Gate_{i}.png"), (w,h)) for i in [1, 2, 3, 4]]    
        self.is_opening = False
        self.is_open =False 
        self.animation_frame = 0
        self.animation_speed = 3
        self.original_height = h 

    def start_opening(self):
        if not self.is_open and not self.is_opening:
            self.is_opening = True    
            

    def update(self):
        if self.is_opening:
            if self.animation_frame < len(self.open_frames) -1 :  
                self.animation_frame += 1
                self.image = self.open_frames[self.animation_frame]

                new_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = new_center
                # self.rect = self.image.get_rect(center = self.rect.center)
            else:    
                self.is_opening = False
                self.is_open = True
                if self in barriers:
                    barriers.remove(self)

                global player
                player.rect = player.rect.copy()     

                       


class Hazard(GameSprite):
    def __init__(self, picture, w, h, x, y, damage):
        super().__init__(picture, w, h, x, y)
        self.damage = damage



class VerticalBullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed_y, damage):
        super().__init__(picture, w, h, x, y)
        self.speed_y = speed_y
        self.damage  = damage
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y < -self.rect.height or self.rect.y > window_height:
            self.kill()

class ShootingEnemies_y(Hazard):
    def __init__(self, picture, w, h, x, y, damage, direction):
        super().__init__(picture, w, h, x, y, damage)
        self.direction = direction
        self.shooting_cooldown = 0

    def update(self):
        if self.shooting_cooldown >0:
            self.shooting_cooldown -= 1    
        distance_x = abs(player.rect.centerx - self.rect.centerx)       

        if distance_x <= CANON_RANGE:
            if self.shooting_cooldown ==0:
                self.fire_vertical()
                self.shooting_cooldown = CANON_COOLDOWN

        window.blit(self.image, self.rect.topleft)

    def fire_vertical(self):
        spawn_x = self.rect.centerx - CANON_BULLET_WIDTH // 2
        if self.direction == "down":    
            spawn_y = self.rect.bottom
            speed_y = CANON_BULLET_SPEED_UP
            
        else:
            spawn_y = self.rect.top - CANON_BULLET_HEIGHT
            speed_y = -CANON_BULLET_SPEED_DOWN  
            self.shooting_cooldown = CANON_COOLDOWN     
        
        Canon_Bullet = VerticalBullet("assets/hazards/Canon_Bullet.png",CANON_BULLET_WIDTH, CANON_BULLET_HEIGHT, spawn_x, spawn_y, speed_y, self.damage)
        enemy_bullets.add(Canon_Bullet)    

class DamageSprite(GameSprite):
    def __init__(self, picture, w, h, x, y, health, damage):
        super().__init__(picture, w, h, x, y)
        self.health = health
        self.damage = damage
        self.is_dead = False
        self.has_death_animation = False  

    def take_damage(self, amount):
        if not self.is_dead:
            self.health -= amount
            if self.health <= 0:
                self.is_dead = True
                if not self.has_death_animation:
                    self.kill()

class DragonShooter(DamageSprite):
    def __init__(self, picture, w, h, x, y, health, damage):
        super().__init__(picture, w, h, x, y,health, damage)
        self.shooting_cooldown =0
        self.direction = "right"
        self.frames_right = [transform.scale(image.load(f"assets/characters/red_dragon/Red_Dragon_Right_{i}.png"), (w, h) ) for i in range(1,4)]
        self.frames_left = [transform.flip(frame, True, False) for frame in self.frames_right]
        self.current_frame =0
        self.animation_speed = 8
        self.frame_counter = 0
        

    def update(self):
        if self.health <= 0 :
            self.kill()
            return
        
        self.frame_counter +=1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames_right)

        if player.rect.centerx > self.rect.centerx:
           self.direction = "right"
        else:
            self.direction = "left"                 

        if self.direction == "right":
            self.image = self.frames_right[self.current_frame]
        else:
            self.image = self.frames_left[self.current_frame]   

        if self.shooting_cooldown > 0:
            self.shooting_cooldown -=1
        else:
            player_distance = abs(player.rect.centerx - self.rect.centerx)

            if player_distance <= DRAGON_RANGE:
                self.fire_horizontal()
                self.shooting_cooldown = DRAGON_COOLDOWN
    def fire_horizontal(self):      
        if self.direction == "right":
            img = "assets/projectiles/Fire_ball_right.png"
            spawn_x = self.rect.right 
            speed = DRAGON_FIRE_BALL_SPEED
        else:
            img = "assets/projectiles/Fire_ball_left.png"
            spawn_x  = self.rect.left - FIRE_BALL_WIDTH
            speed = - DRAGON_FIRE_BALL_SPEED

        spawn_y = self.rect.centery - FIRE_BALL_HEIGHT//2   
        
        fire_ball = Bullet(img, FIRE_BALL_WIDTH, FIRE_BALL_HEIGHT, spawn_x, spawn_y, speed, self.damage)
        enemy_bullets.add(fire_ball)

class Bullet(GameSprite):
    def __init__(self, picture, width, height, x, y, speed, damage):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
        self.damage = damage
        
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > window_width + 10:
            self.kill()

class GreatDragon(DamageSprite):
    def __init__(self, w, h, x, y, health, damage):
        super().__init__("assets/characters/great_dragon/Dragon_Idle/001.png", w, h, x, y, health, damage)
        self.has_death_animation = True  # GreatDragon has a death animation
        self.states = {
            "idle": self.load_animation("assets/characters/great_dragon/Dragon_Idle", 161),
            "battle_idle": self.load_animation("assets/characters/great_dragon/Dragon_Idle_Battle", 140),
            "death": self.load_animation("assets/characters/great_dragon/Dragon_Dies", 301),
            "attack_melee": self.load_animation("assets/characters/great_dragon/Dragon_Attack_1", 161),
            "attack_range": self.load_animation("assets/characters/great_dragon/Dragon_Attack_2", 202)
        }
        self.current_state = "idle"
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = GREAT_DRAGON_IDLE_ANIM_SPEED
        self.attack_cooldown = 0
        self.is_in_combat = False
        self.image = self.states[self.current_state][self.current_frame]  # set first frame
        
        #self.adjust_rect()     # Adjust the rect to fit the actual dragon graphic  #new 


    def load_animation(self, folder, frame_count):
        frames = []
        for i in range(1, frame_count + 1):
            frame_number = str(i).zfill(3)
            frame = image.load(f"{folder}/{frame_number}.png")
            frame = transform.scale(frame, (self.rect.width, self.rect.height))
            frames.append(frame)
        return frames
    
    # def adjust_rect(self):


    def take_damage(self, amount):
        if not self.is_dead:
            self.health -= amount
            if self.health <= 0:
                self.is_dead = True
                self.set_state("death")  # Start death animation
                player_blockers.remove(invisible_wall)    # here we want to make that the invisible wall, which prevent the user to by pass the Great_Dragon, will be now deleted since the death animation started

    def set_state(self, new_state):
        self.current_state = new_state
        self.current_frame = 0
        self.frame_counter = 0
        if new_state == "death":
            self.animation_speed = GREAT_DRAGON_DEATH_ANIM_SPEED
        elif "attack" in new_state:
            self.animation_speed = GREAT_DRAGON_ATK_ANIM_SPEED
        else:
            self.animation_speed = GREAT_DRAGON_IDLE_ANIM_SPEED

    def update_combat_state(self, player):
        if self.is_dead or not player or player.is_dead:
            return
        in_Blue = Blue_Zone.colliderect(player.rect)
        in_Red = Red_Zone.colliderect(player.rect)
        if in_Red:
            if not self.is_in_combat:
                self.is_in_combat = True
                self.set_state("battle_idle")
            if self.attack_cooldown <= 0:
                self.random_attack()
        elif in_Blue:
            if not self.is_in_combat:
                self.is_in_combat = True
                self.set_state("battle_idle")
        else:
            if self.is_in_combat:
                self.is_in_combat = False
                self.set_state("idle")

    def random_attack(self):
        attack_type = choice(["attack_melee", "attack_range"])
        self.set_state(attack_type)
        self.attack_cooldown = GREAT_DRAGON_ATK_COOLDOWN

    def handle_attack_effects(self, player):
        if not player or player.is_dead:
            return
        if self.current_state == "attack_melee" and self.current_frame == 60:
            if GREAT_DRAGON_MELEE_DAMAGE_ZONE.rect.colliderect(player.rect): 
                player.take_damage(self.damage)
        elif self.current_state == "attack_range" and self.current_frame == 125:
            self.GreatDragon_fireball()

    def GreatDragon_fireball(self):
        Great_fire_ball = GreatDragonFireball("assets/projectiles/Great_Dragon_Fireball.png", 50, 50, 
                                              self.rect.centerx, self.rect.centery, 
                                              target=player, speed=4, damage=self.damage)
        enemy_bullets.add(Great_fire_ball)


    def update(self, player):
        # Continue updating even if marked dead, to play death animation
        if self.current_state != "death" and not self.is_dead:
            self.update_combat_state(player)

        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame += 1

            total_frames = len(self.states[self.current_state])
            if self.current_frame >= total_frames:
                if self.current_state == "death":
                    self.kill()  # Remove after death animation finishes
                    return
                elif "attack" in self.current_state:
                    self.set_state("battle_idle")
                else:
                    self.current_frame = 0  # Loop back for idle states

        if "attack" in self.current_state:
            self.handle_attack_effects(player)

        self.image = self.states[self.current_state][self.current_frame]


        # old_center = self.rect.center  # Save the current center of the dragon so it doesn’t “jump” when rect changes.
        # self.rect = self.image.get_bounding_rect()  # Replace self.rect with a tight rectangle around the image (ignores transparent pixels).
        # self.rect.center = old_center  # Restore the center so the dragon stays visually in the same place.
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1   

class GreatDragonFireball(Bullet):
    def __init__(self, picture, w, h, x, y, target, speed,damage):
        super().__init__(picture, w, h, x, y, speed, damage)
        self.target = target
        self.creation_time = time.get_ticks()
        self.lifespan = 5000

    def update(self):
        if not self.target or self.target.is_dead:
            self.kill()
            return

        if self.target and not self.target.is_dead:
            distance_x = self.target.rect.centerx - self.rect.centerx
            distance_y = self.target.rect.centery - self.rect.centery
            distance = max(1, (distance_x**2 + distance_y**2)**0.5)

            self.rect.x += (distance_x / distance) * self.speed
            self.rect.y += (distance_y / distance) * self.speed

        if time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

class Player(DamageSprite):
    def __init__(self, w, h, x, y, x_speed, y_speed, health):
        super().__init__(f"assets/characters/archer/move/1.1_Archer.Hero.Move.right.png",w,h,x,y, health,  0)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.direct = "right" # for different positions
        self.frame_index = 0
        self.frame_counter = 0 
        self.animation_speed = 10  # time between each photo
        self.frames_right = [transform.scale(image.load(f"assets/characters/archer/move/1.{i}_Archer.Hero.Move.right.png"),(w,h)) for i in range(1, 11)]
        self.frames_left = [transform.scale(image.load(f"assets/characters/archer/move/1.{i}_Archer.Hero.Move.left.png"),(w,h)) for i in range(1, 11)]  
        self.is_shooting = False
        self.shoot_frames_right = [transform.scale(image.load(f"assets/characters/archer/aiming/1.{i}_Archer.Hero.Aiming.right.png"), (w,h)) for i in range(1,11)]
        self.shoot_frames_left = [transform.scale(image.load(f"assets/characters/archer/aiming/1.{i}_Archer.Hero.Aiming.left.png"), (w,h)) for i in range(1,11)]
        self.shoot_frame_index = 0
        self.shot_frame_counter= 0
        self.shoot_frame_animation_speed = 5
        self.arrow_fire_permission = True
        self.death_frames_right = [transform.scale(image.load(f"assets/characters/archer/died/1.{i}_Archer.Hero.Died.right.png"), (w,h)) for i in range(1,11)]
        self.death_frames_left = [transform.scale(image.load(f"assets/characters/archer/died/1.{i}_Archer.Hero.Died.left.png"), (w,h)) for i in range(1,11)]
        self.is_dead =False 
        self.death_frame_number = 0
        self.death_speed = 10
        self.death_counter = 0
        self.death_animation_complete = False

    def fire(self):

        if not self.is_shooting and not self.is_dead :
            self.is_shooting = True
            self.shoot_frame_index = 0
            self.shoot_frame_counter = 0
 
    def update(self):

        if self.is_dead:
            self.death_counter += 1
            if self.death_counter >= self.death_speed:
                self.death_counter = 0
                self.death_frame_number += 1
                if self.direct == "right":
                    if self.death_frame_number < len(self.death_frames_right):
                        self.image = self.death_frames_right[self.death_frame_number] 
                    else:
                        self.death_animation_complete = True   
                else :
                    if self.death_frame_number < len(self.death_frames_left):
                        self.image = self.death_frames_left[self.death_frame_number]    
                    else:
                        self.death_animation_complete = True
            return

        if self.is_shooting :
            self.shoot_frame_counter += 1
            if self.shoot_frame_counter >= self.shoot_frame_animation_speed:
                self.shoot_frame_counter = 0
                self.shoot_frame_index += 1

                if self.shoot_frame_index == 7 and  self.arrow_fire_permission == True :
                    self.arrow_fire_permission = False
                    if self.direct == "right":
                        img = "assets/projectiles/Simple_Arrow_Right.png"
                        start_x = self.rect.right
                        speed = 5
                    else:
                        img = "assets/projectiles/Simple_Arrow_Left.png"
                        start_x = self.rect.left - arrow_width
                        speed = -5

                    start_y = self.rect.centery - arrow_height//2
                    Simple_Arrow = Bullet(img, arrow_width, arrow_height, start_x, start_y, speed, damage = 2)
                    player_bullets.add(Simple_Arrow)

               
                if self.shoot_frame_index >= len(self.shoot_frames_right):
                    self.is_shooting = False
                    self.shoot_frame_index = 0
                    self.shoot_frame_counter = 0
                    self.arrow_fire_permission = True

            if self.direct == "right":                                          # this four  sentences it is the same as this "ternary conditional expression":
                self.image = self.shoot_frames_right[self.shoot_frame_index]    # frame_list = (self.shoot_frames_right
            else:                                                               #                 if self.direct == "right"
                self.image =self.shoot_frames_left[self.shoot_frame_index]      #                 else self.shoot_frames_left)
                                                                          
            return    
        

        hit_hazard_player = sprite.spritecollide(self, hazards, False)
        for hazard in hit_hazard_player:
            self.take_damage(hazard.damage) 
            if self.health <= 0 :
                self.is_dead = True
                self.death_frame_number=0
                self.death_counter = 0 
                return  
            
        hit_enemies = sprite.spritecollide(self, enemies, False)
        for enemy in hit_enemies:
            if isinstance(enemy, DamageSprite) and not isinstance(enemy, GreatDragon):
                self.take_damage(enemy.damage)
                if self.health <= 0:
                    self.is_dead =True
                    self.death_frame_number = 0
                    self.death_counter = 0
                    return
        #                                                                                                                                                                                                                                ⫭---------⇾ our group which we name it as basket
        #                                                                                                                                                                                                                                |
        #                                                                                                                                                                                                                                |         ⊢-----⇾  False or True                                                                                                                                                                                                                                      |         |                     
        platforms_collisions = sprite.spritecollide(self, barriers,  False) + sprite.spritecollide(self, player_blockers,  False) # why we do + sign, because the spritecollide function accept on group at time "spritecollide(sprite, group, dokill)"
        if Laser_Gate.is_open and Laser_Gate in platforms_collisions:
            platforms_collisions.remove(Laser_Gate)


        self.rect.x += self.x_speed
        platforms_collisions = sprite.spritecollide(self, barriers, False) 
        if self.x_speed > 0: # Player is moving right
            for p in platforms_collisions:
                self.rect.right = min(self.rect.right, p.rect.left)
                self.direct="right"
        elif self.x_speed < 0: # Player is moving left
            for p in platforms_collisions:
                self.rect.left = max(self.rect.left, p.rect.right)       
                self.direct = "left"

        self.rect.y += self.y_speed
        platforms_collisions = sprite.spritecollide(self, barriers, False) 
        if self.y_speed > 0: # Player is moving down
            for p in platforms_collisions:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: # Player is moving up
            for p in platforms_collisions:
                self.rect.top = max(self.rect.top, p.rect.bottom) 
  
        death_collisions = sprite.spritecollide(self, player_blockers, False) #detect if player is touching the invisible kill-wall guarding Great Dragon ≄ separate from barriers, since this doesn't block movement, it kills on contact instead
        if death_collisions: #Instant death on contact,  subtract full current health so this works regardless of player's HP value
            self.take_damage(self.health)
            
        if self.x_speed != 0 or self.y_speed !=0:
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed: 
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1 ) % len(self.frames_right) 
        else:
            self.frame_index = 0

        if self.direct == "right":
            self.image = self.frames_right[self.frame_index]
        else :
            self.image = self.frames_left[self.frame_index]


class Enemy_x(DamageSprite):        
    def __init__(self, w, h, x, y, speed, health, damage):
        super().__init__( f"assets/characters/ork/11.1_Ork.Walk.right.png",w, h, x, y, health, damage)
        self.speed = speed
        self.direction ="left"
        self.frame_index = 0
        self.frame_counter = 0 
        self.animation_speed = 5
        self.frames_right = [transform.scale(image.load(f"assets/characters/ork/11.{i}_Ork.Walk.right.png") ,(w,h)) for i in range (1,8)]
        self.frames_left = [transform.scale(image.load(f"assets/characters/ork/11.{i}_Ork.Walk.left.png") ,(w,h)) for i in range (1,8)]
        self.is_dead = False
    
    def update(self):
        if self.health <= 0 or self.is_dead:
            return
        
        
        if self.rect.x <= 375:
            self.direction = "right" 
        elif self.rect.x == 755:   #1350 -595 = 755
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed    

        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1 ) % len(self.frames_right)        
            
        if self.direction == "right":
            self.image = self.frames_right[self.frame_index]
        else :
            self.image = self.frames_left[self.frame_index]

# what sprite.Group() is for? : sprite.Group() creates an empty container, think of it like an empty basket you can drop sprite objects into; Example: barriers = sprite.Group() made one basket for walls. and enemies ... and what each basket do you decide as decided in the classes above

player_blockers = sprite.Group() # this is for invisible wall that prevent the player to be close to the Great_Dragon and kill the player once he collide with it, once the dragon dead the wall disapears, and the player can go for the button
barriers = sprite.Group()
enemies  = sprite.Group()

player_bullets = sprite.Group()
enemy_bullets  = sprite.Group()

hazards  = sprite.Group()
gates = sprite.Group()


#Game Borders                        w   h   x     y
wall_1 = GameSprite('assets/environment/desertwall.jpg', 40, 660, 0, 0) # wall 1
wall_2 = GameSprite('assets/environment/desertwall.jpg', 1350, 40, 0, 0) # wall 2
wall_3 = GameSprite('assets/environment/desertwall.jpg', 1350, 40, 0, 660) # wall 3
wall_4 = GameSprite('assets/environment/desertwall.jpg', 40, 580, 1310, 0) # wall 4
#Mase's walls                         w   h   x     y 
wall_5 = GameSprite('assets/environment/desertwall.jpg', 30, 120, 90, 90) # wall 5
wall_6 = GameSprite('assets/environment/desertwall.jpg', 25, 7, 92.5, 210) # wall 6
wall_7 = GameSprite('assets/environment/desertwall.jpg', 15, 15, 97.5, 217) # wall 7
wall_8 = GameSprite('assets/environment/desertwall.jpg', 30, 10, 90, 232) # wall 8
wall_9 = GameSprite('assets/environment/desertwall.jpg', 30, 10, 90, 292)  # wall 9
wall_10 = GameSprite('assets/environment/desertwall.jpg', 15, 15, 97.5, 302)  # wall 10
wall_11 = GameSprite('assets/environment/desertwall.jpg', 25, 7, 92.5, 317)  # wall 11
wall_12 = GameSprite('assets/environment/desertwall.jpg', 30,  336, 90, 324) # wall 12
wall_13 = GameSprite('assets/environment/desertwall.jpg', 110, 30, 340, 250) # wall 13
wall_14 = GameSprite('assets/environment/desertwall.jpg', 120, 30, 120, 90) # wall 14
wall_15 = GameSprite('assets/environment/desertwall.jpg', 25, 490, 165, 120) # wall 15
wall_18 = GameSprite('assets/environment/desertwall.jpg', 30, 410, 340, 280) # wall 18
wall_19 = GameSprite('assets/environment/desertwall.jpg', 240, 30, 300, 90) # wall 19
wall_20 = GameSprite('assets/environment/desertwall.jpg', 30, 50, 510, 40) # wall 20
wall_21 = GameSprite('assets/environment/desertwall.jpg', 30,160, 490, 120) # wall 21
wall_22 = GameSprite('assets/environment/desertwall.jpg', 220, 30, 520, 250) # wall 22
#                                       w   h   x     y 
wall_23 = GameSprite('assets/environment/desertwall.jpg', 380, 30, 370, 330) # wall 23
wall_24 = GameSprite('assets/environment/desertwall.jpg', 30, 230, 820, 200) # wall 24
wall_25 = GameSprite('assets/environment/desertwall.jpg', 700, 30, 560, 170) # wall 25
wall_26 = GameSprite('assets/environment/desertwall.jpg', 30, 80, 590, 90) # wall 26
wall_27 = GameSprite('assets/environment/desertwall.jpg', 30, 80, 670, 40) # wall 27
wall_28 = GameSprite('assets/environment/desertwall.jpg', 30, 80, 750, 90) # wall 28
wall_29 = GameSprite('assets/environment/desertwall.jpg', 30, 80, 830, 40) # wall 29
wall_30 = GameSprite('assets/environment/desertwall.jpg', 30, 80, 910, 90) # wall 30
wall_31 = GameSprite('assets/environment/desertwall.jpg', 30, 80, 990, 40) # wall 31
wall_32 = GameSprite('assets/environment/desertwall.jpg', 30, 80, 1070, 90) # wall 32
wall_33 = GameSprite('assets/environment/desertwall.jpg', 30, 80, 1150, 40) # wall 33
wall_34 = GameSprite('assets/environment/desertwall.jpg', 30, 80, 1230, 90) # wall 34
wall_35 = GameSprite('assets/environment/desertwall.jpg', 350, 30, 960, 250) # wall 35
wall_36 = GameSprite('assets/environment/desertwall.jpg', 30, 410, 880, 250) # wall 36
wall_37 = GameSprite('assets/environment/desertwall.jpg', 30, 120, 960, 280) # wall 37
wall_38 = GameSprite('assets/environment/desertwall.jpg', 30, 200, 960, 460) # wall 38
wall_39 = GameSprite('assets/environment/desertwall.jpg', 30, 330, 1040, 330) # wall 39
wall_40 = GameSprite('assets/environment/desertwall.jpg', 190, 30, 1070, 330) # wall 40
wall_41 = GameSprite('assets/environment/desertwall.jpg', 180, 30, 1130, 420) # wall 41
wall_42 = GameSprite('assets/environment/desertwall.jpg', 30, 20, 720, 360) # wall 42
wall_43 = GameSprite('assets/environment/desertwall.jpg', 450, 30, 430, 430) # wall 43
wall_44 = GameSprite('assets/environment/desertwall.jpg', 30, 20, 590, 410) # wall 44
wall_45 = GameSprite('assets/environment/desertwall.jpg', 30, 20, 510, 360) # wall 45
wall_46 = GameSprite('assets/environment/desertwall.jpg', 30, 20, 430, 410) # wall 46
wall_47 = GameSprite('assets/environment/desertwall_triangle.png', 40, 15, 1310, 580) # wall 47
wall_48 = GameSprite('assets/environment/desertwall.jpg', 7, 35, 120, 150) # wall 48


                                   #   w   h   x     y
invisible_wall = GameSprite('assets/environment/Invisible_wall.png', 30, 200, 650, 460) #The which prevent the user to by pass the Great_Dragon, and Kill him immediately

GREAT_DRAGON_MELEE_DAMAGE_ZONE =  GameSprite('assets/environment/Invisible_wall.png', 510, 200, 370, 460)

Red_Button = RedButton("assets/mechanisms/Red_button_1.png",40,40,835,620)

Great_Dragon = GreatDragon(300,255,575,460, health =35, damage= 50) #health = 35

Laser_Gate = LaserGate("assets/mechanisms/Red_Laser_Gate_1.png",80,30,740,250)

Portal_Gate = GameSprite("assets/environment/Portal_1.1.png", 80,80,1265,580)

spikes_16 = Hazard('assets/hazards/bone_shield_Right.png', 8,   30,  240,  90,        LETHAL_DAMAGE  )
spikes_17 = Hazard('assets/hazards/bone_shield_Left.png',  8,   30,  290,  90,        LETHAL_DAMAGE  )
#                                          w     h    x       y     damage
canon_up = ShootingEnemies_y("assets/hazards/Canon_Up.png",               40,  50,    50,  610,    LETHAL_DAMAGE,    direction= "up")
canon_down = ShootingEnemies_y("assets/hazards/Canon_Down.png",           40,  50,   127,  145,    LETHAL_DAMAGE,    direction = "down" )
#                                                           w,   h,     x,   y,     damage_number      bullet_direction
player = Player( 40, 40, 85, 250,     0,          0,         100) 
#              w    h   x   y    x_speed   y_speed health_number
Red_Ork = Enemy_x(40, 50,              755, 280,     2,           2,       LETHAL_DAMAGE) 
#                 w ,  h,                x,   y, speed, health_number,  damage_number
Red_Dragon = DragonShooter("assets/characters/red_dragon/Red_Dragon_Right_1.png", 113, 91, 300,  145,   health =9, damage=35)  #health= 9
#                                                    w    h    x     y   


run = True

enemies.add(Red_Ork,canon_up, canon_down,Red_Dragon, Great_Dragon, )    #canon_up  
barriers.add(wall_1, wall_2, wall_3, wall_4, wall_5, wall_6, wall_7, wall_8, wall_9, wall_10,wall_11, wall_12, wall_13, wall_14, wall_15,wall_18, wall_19, wall_20,wall_21,wall_22,wall_23, wall_24, wall_25,wall_26, wall_27,wall_28, wall_29, wall_30,wall_31, wall_32,wall_33, wall_34,wall_35, wall_36, wall_37, wall_38, wall_39,wall_40, wall_41, wall_42, wall_43, wall_44,wall_45, wall_46, wall_47,wall_48, Laser_Gate, canon_down )
player_blockers.add(invisible_wall)
hazards.add(spikes_16, spikes_17)
gates.add(Laser_Gate)

clock = time.Clock()
finish = False

while run:
    clock.tick(50)
    for e in event.get():
        
        if e.type == QUIT:
            time.delay(10)
            run = False

        elif e.type == KEYDOWN: 
            
            if e.key == K_UP:
                player.y_speed = -Player_speed 
            elif e.key == K_DOWN:
                player.y_speed = Player_speed 
            elif e.key == K_LEFT:
                player.x_speed = -Player_speed 
                player.direct = "left"
            elif e.key == K_RIGHT:
                player.x_speed = Player_speed 
                player.direct = "right"
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key ==  K_UP or e.key ==K_DOWN:
                player.y_speed = 0               
            elif e.key == K_LEFT or e.key == K_RIGHT:
                player.x_speed = 0
    
    if not finish:
        window.blit(background_picture, (0, 0))
        player_bullets.update()
        enemy_bullets.update()

        player_bullets.draw(window)
        enemy_bullets.draw(window)

        sprite.groupcollide(player_bullets, barriers, True, False)
        sprite.groupcollide(enemy_bullets, barriers, True, False)

        
    #Player bullets → enemies    
        hit_player_bullets =sprite.groupcollide(player_bullets, enemies, True, False)
        for bullet, hit_list in hit_player_bullets.items():
            for enemy in hit_list:
                enemy.take_damage(bullet.damage)

    #Enemy bullets → player
        hit_enemy_bullets = sprite.spritecollide(player, enemy_bullets, True, sprite.collide_mask) # Mask code x

        for bullet in hit_enemy_bullets:
            player.take_damage(bullet.damage)
 

        if not Red_Button.is_pressed and sprite.collide_rect(player, Red_Button):
            Red_Button.is_pressed =True

        for i in barriers:
            i.reset()

        Red_Button.update()
        Red_Button.reset()
    # Red Button is updated first so the Great Dragon animation appears on top of it

        for obj in enemies:
            if isinstance(obj, GreatDragon):
                obj.update(player)
            else:
                obj.update()
            obj.reset()

        for h in hazards:
            h.reset()

        

        Laser_Gate.update()
        Laser_Gate.reset()

        player.update()
        player.reset()

        Portal_Gate.reset()

       
        if Laser_Gate.is_open and Laser_Gate in barriers:
            barriers.remove(Laser_Gate)

        if sprite.collide_rect(player, Portal_Gate):
            finish = "win"
        elif Red_Ork.alive() and sprite.collide_rect(player, Red_Ork):
            player.take_damage(Red_Ork.damage)
        
        #if sprite.collide_rect(Great_Dragon, player):
       #    player.take_damage(Great_Dragon.damage)
        
        if player.death_animation_complete:
            finish = "die"

    else:
        
        if finish == "win":
            window.blit(win_Background, (0, 0))
        else: 
            window.blit(Game_over_Background, (0, 0))
    
    display.update()