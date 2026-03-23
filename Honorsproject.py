"""
Honors python 1 Project
Tofu kitchen survivor
Martin Peraza 5/6/2025
"""
"""
reflection:
this project has showed me that I'm actually capable of learning a lot on my own. when I started this project, I genuenly had no idea on how pygame worked or what i would need to make in order to create a game,
I jsut had a basic idea for a game, and startedwatching tutorials in to how to do stuff. to my surprise, it was easier to learn than I thought, and I was able to to learn new methods and functions that came with the varius modules I imported,
specially the pygame, the json, the math, and the os and os.path. some of my friends did help me a lot with my game in terms of feedback. I was doing the game, but I still did not knew if someone apart from me would find it 
entertaining, so I needed people to test my game to see waht would be fun to be added and/or changed. with this feedback, I did things like adding moving platforms, changing them to blue, make the game harder with time, 
make some traps (specially the laser enemy) easier to avoid, etc. I feel amazed of what I was capable, and still i feel I could do so much more, like making the dificulty system even better, adding completly animated sprites, but
I feel happy with what I already have.
"""
#importing required modules
import pygame
import sys
from pygame.locals import *
from pygame.locals import QUIT
import math
import random
from random import randint
import getpass
import hashlib
import os
import os.path
import json
global high_score
# File where all high scores will be stored
SCORE_FILE = "high_scores.json"

# Get the current user's name
username = "user"
# Load existing scores safely
def load_scores():
    """
    function to load the current saved score in the json dictionary file.
    mainly made to address currupted or modified files. ask the user if they
    want to delete the file in case it is currupted. deletes it if yes, and closes the
    program if not. if yes, it also creates an new file with an empty dictionary to store
    the new scores.

    """
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("The file got corrupted or was manually modified.")
            data_text = input("Do you want to delete the file? All the scores will be lost, but the game will not work otherwise. (y/n): ").lower()
            if data_text == "y":
                os.remove(SCORE_FILE)
                return {}
            else:
                print("Game exiting due to corrupted score file.")
                exit()
    else:
        return {}

scores = load_scores()
# Get this user's current high score
high_score = scores.get(username, 0)
#start screen function
def start_screen():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.Font("MightySouly-lxggD.ttf", 36)
    small_font = pygame.font.Font("MightySouly-lxggD.ttf", 18)

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Title
        title = font.render("Tofu Kitchen Survivor", True, (255, 255, 0))
        screen.blit(title, title.get_rect(center=(400, 50)))

        # Explaining controls
        controls_title = small_font.render("Controls:", True, (255, 255, 255))
        screen.blit(controls_title, (50, 120))
        screen.blit(small_font.render("LEFT ARROW / RIGHT ARROW to move", True, (200, 200, 200)), (70, 150))
        screen.blit(small_font.render("UP ARROW or SPACE to jump", True, (200, 200, 200)), (70, 180))

        # Enemy descriptions
        enemy_title = small_font.render("Enemies:", True, (255, 255, 255))
        screen.blit(enemy_title, (50, 230))
        screen.blit(small_font.render("- Chese shreder: Comes from screen edges, avoid it!!.", True, (255, 100, 100)), (70, 260))
        screen.blit(small_font.render("- Wasabi machine: A machine that shoots wasai at you. be caerful!", True, (255, 100, 100)), (70, 290))
        screen.blit(small_font.render("- Fire trap: Two fire pilars aproach from the sides, find the off switch to survive.", True, (255, 100, 100)), (70, 320))
        #miscelaneus
        screen.blit(small_font.render("- A heart appears some time. try to get it to optain an extra life!!!",True,(255,100,100)),(70,350))
        # Instructions to start
        start_msg = font.render("Press ENTER to Start", True, (0, 255, 0))
        screen.blit(start_msg, start_msg.get_rect(center=(400, 500)))

        # Input and starting the actual game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

        pygame.display.flip()
        clock.tick(60)


def game(high_score, scores, username):
    """
this is literally the whole game, I just put it inside a function so the restart
screen works and makes easier to call with the password system. the arguments are
the external files related variables and score vairables to make them global inside the
funtion.
"""#game window
    gameWindow=pygame.display.set_mode((800,600))
    background_img=pygame.image.load("pixil-frame-0.png").convert()
    background_img=pygame.transform.scale(background_img,(800,600))
    #setting games frames
    Frames=60
    timer=pygame.time.Clock()
    #game is now running
    GameRuning= True
    #defining the player
    Tofu_The_Player=pygame.image.load("tofu-player-pixilart.png").convert_alpha()
    crop_rect = Tofu_The_Player.get_bounding_rect()
    Tofu_The_Player=Tofu_The_Player.subsurface(crop_rect).copy()
    Tofu_The_Player = pygame.transform.scale(Tofu_The_Player, (40, 33))
    rect=Tofu_The_Player.get_rect()
    #player's initial position
    rect.x=400
    rect.y=500
    #base movements speed
    speed=5
    #setting base droung hight to apply gravity
    base_floor=500
    #variables needed for jumping mechanic
    gravity=1
    jump=False
    jump_speed=20
    jump_hight=jump_speed
    vy=0
    landed=False
    #live system variables
    lives=5
    invincible=False
    invinciblble_start_time=0
    invincibility_duration=1000
    last_time_spawned=0
    heart_cd=10000
    dead=False
    #spike wall vars
    wall_spawned=False
    wall_speed=4
    spawn_time=5000
    time_spawned=0
    wall_direction = 0
    wall_trap_speed=0.7
    #spawner variables
    trap_generator = 0
    trap_timer = 0
    trap_interval = 3000
    #display the lives, game over screen and score
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font("MightySouly-lxggD.ttf", 36)
    small_font=pygame.font.Font("MightySouly-lxggD.ttf",18)
    score=0
    score_check=0
    score_interval=1000

    #basic lateral movement
    def movement(dx):
        rect.x+=dx*speed
    #creating the platform class
    class Platform:
        """
platform class that consist on a rect obj that detects collisions with the player, if so, attaches its top to the bottom of the player to 'land' on it, also has a mooving variant of the regular platform
"""
        def __init__(self, x, y, moving=False):
            self.surface =pygame.image.load("pixil-frame-0 (2).png").convert_alpha()
            self.plt_crop_rect=self.surface.get_bounding_rect()
            self.surface=self.surface.subsurface(self.plt_crop_rect).copy()
            self.surface=pygame.transform.scale(self.surface,(60,6))
            self.plt_rect = self.surface.get_rect()
            self.plt_rect.x = x
            self.plt_rect.y = y
            self.start_x = x
            self.direction = 1
            self.moving = moving
            self.range = 100
            self.speed = 2

        def update(self):
            if self.moving:
                self.plt_rect.x += self.direction * self.speed
                if abs(self.plt_rect.x - self.start_x) >= self.range:
                    self.direction *= -1

        def draw(self, screen):
            screen.blit(self.surface, self.plt_rect)

        def get_obj(self):
            return self.plt_rect


            screen.blit(self.surface, self.plt_rect)
    #creating damage inducing entity
    class Damage:
        """
        this class works as a hitbox. it is invicible and attaches to the object
        I want for it to cause damage. it ruturns weather or not it has collided with
        the player.
        It has to update so that it moves with the object it is attached to
        """
        def __init__(self, attached_obj):
            self.attached_obj = attached_obj
            attached_rect = attached_obj.get_obj()
            # positionating the damage entity in the same position as the attached object
            self.surface = pygame.Surface((attached_rect.width, attached_rect.height), pygame.SRCALPHA)
            self.surface.fill((0, 0, 0, 0))#making it transparent
            self.d_rect = self.surface.get_rect(topleft=(attached_rect.x, attached_rect.y))

        def update(self):
            #update system to mantain the damage entity attached to the object every loop
            attached_rect = self.attached_obj.get_obj()
            self.d_rect.topleft = attached_rect.topleft
            # detect if it collided with the player
        def check_damage(self, player_rect):
            return self.d_rect.colliderect(player_rect)
        def draw(self, screen):
            pass # this is just for debugging
    #creating a spike wall enemy class
    class spike_wall:
        """
        vertical wall that spawns in a random Y position and in the closest X extreme of the screen to the player.
        it uses the damage class to cause damage
        """
        def __init__(self, init_x_position):
          self.surface =pygame.image.load("pixil-frame-0 (3).png").convert_alpha()
          self.spw_crop_rect=self.surface.get_bounding_rect()
          self.surface=self.surface.subsurface(self.spw_crop_rect).copy()
          self.surface=pygame.transform.scale(self.surface,(20,200))
          self.spw_rect=self.surface.get_rect()
          self.spw_rect.x=init_x_position
          self.spw_rect.y=randint(0,400)
        def get_wall(self):
          return self.surface
          #returns object
        def get_obj(self):
          return self.spw_rect
          #draws on the screen
        def draw(self,screen):
          screen.blit(self.surface, self.spw_rect)
    class LaserEnemy:
        """
        entity that 'shoot' two rounds of lasers. due to its complexity, I decided to
        not use the damage class to cause damage and instead uses its own damage system
        it slowly rotates to point to the player position and shoot, and the entity itself always
        spawns below the floor (I'm not going to lie I just followed a tutorial, this thing is
        more complex than trying to untagle the christmas lights.)
        """
        def __init__(self, x, y):
          #creating the surface
            self.surface =pygame.image.load("wasabi-inator.png").convert_alpha()
            self.wasabi_crop_rect=self.surface.get_bounding_rect()
            self.surface=self.surface.subsurface(self.wasabi_crop_rect).copy()
            self.surface=pygame.transform.scale(self.surface,(70,90))
            #create laser enemy object
            self.rect = self.surface.get_rect(topleft=(x, y))
            #setting laser parameters
            NUM_FRAMES=4
            self.laser_sheet = pygame.image.load("pixilart-sprite.png").convert_alpha()
            self.laser_frames = []

            frame_width = self.laser_sheet.get_width() // NUM_FRAMES  
            frame_height = self.laser_sheet.get_height()

            for i in range(NUM_FRAMES):
                frame = self.laser_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                self.laser_frames.append(frame)

            self.current_frame = 0
            self.frame_timer = 0
            self.frame_speed = 100  # milliseconds per frame

            self.laser_length = 800
            self.angle = (math.pi/ 2)*-1
            self.aim_speed = 0.007
            self.cooldown = 2000  # time between shots
            self.last_shot = pygame.time.get_ticks()
            self.laser_duration = 500
            self.laser_active = False
            self.laser_start_time = 0
            self.laser_color = (255, 0, 0)

        def update(self, player_rect):
            # Calculate desired angle
            dx = player_rect.centerx - self.rect.centerx
            dy = player_rect.centery - self.rect.centery
            desired_angle = math.atan2(dy, dx)

            # smoothly adjust angle
            diff = (desired_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
            self.angle += max(-self.aim_speed, min(self.aim_speed, diff))

            # fire laser
            now = pygame.time.get_ticks()
            if not self.laser_active and now - self.last_shot >= self.cooldown:
                self.laser_active = True
                self.laser_start_time = now
                self.last_shot = now
            # Update animation frame if laser is active
            if self.laser_active:
                now = pygame.time.get_ticks()
                if now - self.frame_timer > self.frame_speed:
                    self.frame_timer = now
                    self.current_frame = (self.current_frame + 1) % len(self.laser_frames)
            else:
                self.current_frame = 0  # reset to start

            #despawn logic
            if self.laser_active and now - self.laser_start_time > self.laser_duration:
                self.laser_active = False

        def check_hit(self, player_rect):
            if not self.laser_active:
                return False
            # laser line vector
            x1 = self.rect.centerx
            y1 = self.rect.centery
            x2 = x1 + self.laser_length * math.cos(self.angle)
            y2 = y1 + self.laser_length * math.sin(self.angle)

            # check intersection with player rect (rough method using line-rect collision)
            return player_rect.clipline((x1, y1), (x2, y2))

        def draw(self, screen):
            # Draw enemy body
            screen.blit(self.surface, self.rect)

            if self.laser_active:
                # Enemy center (laser start)
                origin_x = self.rect.centerx
                origin_y = self.rect.centery

                # Get current animation frame
                frame = self.laser_frames[self.current_frame]

                # Scale the frame to match desired laser length
                laser_height = frame.get_height()
                scaled_laser = pygame.transform.scale(frame, (self.laser_length, laser_height))

                # Rotate the scaled laser
                rotated_laser = pygame.transform.rotate(scaled_laser, -math.degrees(self.angle))

                # Get rotated image rect and position its center
                rotated_rect = rotated_laser.get_rect()
                offset_x = math.cos(self.angle) * (self.laser_length / 2)
                offset_y = math.sin(self.angle) * (self.laser_length / 2)
                rotated_rect.center = (origin_x + offset_x, origin_y + offset_y)

                # Draw rotated laser
                screen.blit(rotated_laser, rotated_rect)

    # creating traping walls class
    class WallObject:
        """
        consists in a large vertical wall that uses the damage class to cause damage that
        slowly moves.
        """
        def __init__(self, x, y, width=30, height=800):
            self.surface =pygame.image.load("fire-wall-pixilart.png").convert_alpha()
            self.wll_crop_rect=self.surface.get_bounding_rect()
            self.surface=self.surface.subsurface(self.wll_crop_rect).copy()
            self.surface=pygame.transform.scale(self.surface,(width,height))
            self.rect = self.surface.get_rect(topleft=(x, y))
            self.x_float = float(x)
        #move right or left depending if it is the right or left wall
        def move(self, dx):
            self.x_float += dx
            self.rect.x = int(self.x_float)

        def draw(self, screen):
            screen.blit(self.surface, self.rect)

        def get_obj(self):
            return self.rect



    class SwitchObject:
        """
        simple rect object used for the next class.
        """
        def __init__(self):
            self.surface =pygame.image.load("switch.png").convert_alpha()
            self.switch_crop_rect=self.surface.get_bounding_rect()
            self.surface=self.surface.subsurface(self.switch_crop_rect).copy()
            self.surface=pygame.transform.scale(self.surface,(60,60))
            x = randint(100, 700)
            y = randint(100, 475)
            self.rect = self.surface.get_rect(topleft=(x, y))
        def get_obj(self):
            return self.rect
        def draw(self, screen):
            screen.blit(self.surface, self.rect)

    class WallTrap:
        """
        conbines the two prevous classes a wall trap enemy. it consists in the two
        vertical walls that slowly moves that will eventually damage the player,
        but if the player touches the switch, which spawn in a random x and y position
        inside the players reach, they despawn.
        """
        def __init__(self):
            self.wall_left = WallObject(0, 0)
            self.wall_right = WallObject(790, 0)
            self.switch = SwitchObject()
            self.active = True
            self.wall_left.rect.x = 0
            self.wall_right.rect.x = 790
        #move until both walls completly swiped the screen
        def update(self):
          if self.active:
            if self.wall_left.rect.x < 390:
                self.wall_left.move(wall_trap_speed)
            if self.wall_right.rect.x > 400:
                self.wall_right.move(-wall_trap_speed)

        #check collisions with the player
        def check_collisions(self, player_rect):
            return (
                self.wall_left.rect.colliderect(player_rect) or
                self.wall_right.rect.colliderect(player_rect)
            )

        def check_switch(self, player_rect):
            return self.switch.rect.colliderect(player_rect)

        def draw(self, screen):
            if self.active:
                self.wall_left.draw(screen)
                self.wall_right.draw(screen)
                self.switch.draw(screen)
    class extra_life:
      """
      simple rect object that spawn in a random y and x location. it it collides witht he player,
      it gives the player an extra live.
      """
      def __init__(self):
        self.surface =pygame.image.load("heart.png").convert_alpha()
        self.heart_crop_rect=self.surface.get_bounding_rect()
        self.surface=self.surface.subsurface(self.heart_crop_rect).copy()
        self.surface=pygame.transform.scale(self.surface,(30,30))
        x = randint(100, 700)
        y = randint(100, 500)
        self.heart_rect = self.surface.get_rect(topleft=(x, y))
      def get_obj(self):
        return self.heart_rect
      def get_heart(self):
        return self.surface
      def draw(self, screen):
            screen.blit(self.surface, self.heart_rect)
      def collide(self,player_rect):
        return self.heart_rect.colliderect(player_rect)
#default variables for trap spawning
    spike=None
    spike_damage=None
    laser_enemy = None
    wall_traps=None
    heart=None
    #platform list
    platforms=[
        Platform(400,400),
        Platform(200,250),
        Platform(100,400),
        Platform(700,300),
        Platform(500,125),
        Platform(575,325)
    ]
    #moving platform list
    moving_platforms = [
        Platform(400,300,moving=True),
        Platform(600,400,moving=True),
        Platform(300,100,moving=True),
    ]

    while GameRuning:
#main game loop
        for event in pygame.event.get():
          #closing the game
            if event.type == pygame.QUIT:
                GameRuning = False
                #input
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if landed:
                    vy = -jump_speed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if landed:
                    vy = -jump_speed

        if keys := pygame.key.get_pressed():
            if keys[pygame.K_RIGHT]:
                movement(1)
            if keys[pygame.K_LEFT]:
                movement(-1)

        #physics
        vy += gravity
        rect.y += vy

        # reset landed
        landed = False

        # platform collisions
        if vy > 0:
            for plat in platforms:
                pr = plat.get_obj()
                if rect.colliderect(pr):
                    rect.bottom = pr.top
                    vy = 0
                    landed = True
                    break
                # Always update moving platforms
        for plat in moving_platforms:
            plat.update()

        # Check collision separately (only when falling)
        if vy > 0:
            for plat in moving_platforms:
                pr = plat.get_obj()
                if rect.colliderect(pr):
                    rect.bottom = pr.top
                    vy = 0
                    landed = True
                    # Move player with platform
                    rect.x += plat.direction * plat.speed



        # ground collision
        if rect.bottom > base_floor:
            rect.bottom = base_floor
            vy = 0
            landed = True
        #damage system
        current_time=pygame.time.get_ticks()
        if spike_damage:
         spike_damage.update()
         if not invincible and spike_damage.check_damage(rect):
            lives -= 1
            invincible = True
            invincible_start_time = current_time
        if invincible and current_time - invincible_start_time> invincibility_duration:
            invincible=False
        if lives<=0:
            dead=True
        if dead:
            break
       #score system
        if current_time - score_check > score_interval:
          score += 100
          score_check = current_time
        #traps spawner
        if not wall_spawned and trap_generator == 1:
          if rect.x > 400:
            spike = spike_wall(800)
            wall_direction = -1
          else:
            spike = spike_wall(0)
            wall_direction = 1
          spike_damage = Damage(spike)
          wall_spawned = True
          time_spawned = current_time
    #moving the wall if it is spawned
        if wall_spawned and spike:
          spike.spw_rect.x += wall_speed * wall_direction

        rect.x = max(0, min(rect.x, 800 - rect.width))
        #despawning wall
        if wall_spawned and current_time - time_spawned > spawn_time:
          wall_spawned = False
          spike = None
          spike_damage = None
          #spawning laser enemy
        if laser_enemy is None and trap_generator == 2:
          laser_enemy = LaserEnemy(400-25, base_floor+25)
          time_spawned = current_time
        if laser_enemy:
          laser_enemy.update(rect)
          #laser enemy damage logic
          if not invincible and laser_enemy.check_hit(rect):
              lives -= 1
              invincible = True
              invincible_start_time = current_time
              #despawning laser enemy
        if laser_enemy and current_time - time_spawned > spawn_time:
          laser_enemy = None
          #wall trap spawn
        if wall_traps is None and trap_generator == 3:
          wall_traps = WallTrap()
          wall_trap_1_damage = Damage(wall_traps.wall_left)
          wall_trap_2_damage = Damage(wall_traps.wall_right)

        if wall_traps:
          wall_traps.update()

          wall_trap_1_damage.update()
          wall_trap_2_damage.update()
    # damaged by wall traps and despawning
          if wall_traps.check_collisions(rect):
              if not invincible:
                 lives -= 1
              invincible = True
              invincible_start_time = current_time
              wall_traps = None

        if wall_traps and wall_traps.check_switch(rect):
            wall_traps = None
        #life spawner
        if heart is None and current_time-last_time_spawned>heart_cd:
          if randint(1,2)==1:
                  heart=extra_life()
          last_time_spawned=current_time
        if heart:
          if heart.collide(rect):
            lives+=1
            heart=None
        #trap generator
        if current_time - trap_timer > trap_interval:
          trap_generator = randint(1, 3)
          trap_timer = current_time
        #high score
        #render
        gameWindow.blit(background_img,(0,0))
        gameWindow.blit(Tofu_The_Player, rect)
        for plat in platforms:
            plat.draw(gameWindow)
        for plat in moving_platforms:
            plat.draw(gameWindow)
        if wall_spawned:
         spike.draw(gameWindow)
        if laser_enemy:
          laser_enemy.draw(gameWindow)
        if wall_traps:
          wall_traps.draw(gameWindow)
        if heart:
          heart.draw(gameWindow)
          #lives and score counter
        lives_text = font.render(f"Lives: {lives}", True, (0, 0, 255))
        text_rect = lives_text.get_rect(topright=(790, 10))
        score_text=font.render(f"Score: {score}",True,(0,0,255))
        score_rect=score_text.get_rect(topleft=(0,10))
        gameWindow.blit(lives_text, text_rect)
        gameWindow.blit(score_text,score_rect)
        pygame.display.flip()
        timer.tick(Frames)
    #game over screen
    while dead:
        # This was so painfull to make :(
        #saving score logic
        if score > high_score:
            scores[username] = score
            high_score = score
            with open(SCORE_FILE, "w") as f:
                json.dump(scores, f)

        for event in pygame.event.get():
            if score > high_score:
                high_score = score
                scores[username] = high_score
                with open(SCORE_FILE, "w") as f:
                    json.dump(scores, f)

            if event.type == pygame.QUIT:
                GameRuning = False
                dead = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # reset game state
                    rect.x = 100
                    rect.y = 500
                    lives = 5
                    score=0
                    score_check=0
                    vy = 0
                    invincible = False
                    spike = None
                    spike_damage = None
                    laser_enemy = None
                    wall_traps = None
                    heart = None
                    trap_generator = 0
                    trap_timer = pygame.time.get_ticks()
                    dead = False
                    GameRuning = True
                    game(high_score, scores, username)
    #game over screen render
        gameWindow.fill((0, 0, 0))
        #game over message
        pan=pygame.image.load("pan-pixilart.png").convert_alpha()
        pan_rect=pan.get_rect(center=(400,150))
        pan = pygame.transform.scale(pan, (400, 400))
        game_over1 = font.render("You are Cooked!!!", True, (255, 255, 0))
        game_over2 = font.render("Press R to Play Again", True, (255, 255, 0))
        leader_board = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

        #final score
        score_display=font.render(f"Your score: {score}",True,(255,255,0))
        high_score_display=font.render(f"High score: {high_score}",True,(255,255,0))
        gameWindow.blit(game_over1, game_over1.get_rect(center=(400, 50)))
        gameWindow.blit(pan,pan_rect)
        gameWindow.blit(game_over2, game_over2.get_rect(center=(400, 500)))
        gameWindow.blit(score_display,score_display.get_rect(topleft=(100,100)))
        y_offset = 200
        gameWindow.blit(high_score_display,high_score_display.get_rect(topleft=(100,150)))

        pygame.display.flip()
        timer.tick(Frames)
start_screen()
game(high_score, scores, username)
pygame.quit()
sys.exit()
