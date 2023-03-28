import pygame
from settings import *
from support import *
from mapeditor import myMap

class Player(pygame.sprite.Sprite):
    def __init__(self, pos,movepath, group):
        super().__init__(group)

        # sprite image initialization
        self.import_assets()
        self.status = 'right'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # movement
        self.direction_vector = pygame.math.Vector2(0, 0)
        self.pos_vector = pygame.math.Vector2(self.rect.center)
        self.speed = 100  # can modify later
        self.noMove = []
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction_vector.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction_vector.y = 1
        else:
            self.direction_vector.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction_vector.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction_vector.x = -1
        else:
            self.direction_vector.x = 0

        if self.direction_vector.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        elif self.direction_vector.y == -1:
            self.status = 'back'
        elif self.direction_vector.x == 1:
            self.status = 'left'
        else:
            self.status = 'right'

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)

    def move(self, dt):  # needs to modify later

        #predict
        self.prediretion=self.pos_vector+self.direction_vector* self.speed * dt

        dir_flag=1

        if self.prediretion.x>=SCREEN_WIDTH or self.prediretion.x<0 or self.prediretion.y>=SCREEN_HEIGHT or self.prediretion.y<0:
            dir_flag=0

        if self.direction_vector.magnitude() > 0:
            self.direction_vector = self.direction_vector.normalize()


        if dir_flag==0:
          self.noMove.append(self.direction_vector)

        print(self.noMove)

        if  self.direction_vector not in self.noMove:#directions that we can move
            # horizontal
           self.pos_vector.x += self.direction_vector.x * self.speed * dt
           self.rect.centerx = self.pos_vector.x

            # vertical
           self.pos_vector.y += self.direction_vector.y * self.speed * dt
           self.rect.centery = self.pos_vector.y
           self.noMove=[]



    def import_assets(self):
        self.animations = {'right': [], 'left': [], 'back': [], 'right_idle': [], 'left_idle': [], 'back_idle': []}

        for animation in self.animations.keys():
            full_path = r'./player/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
