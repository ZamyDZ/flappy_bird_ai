import pygame
import neat
import time
import os 
import random

# Window Size
WIN_WIDTH = 550
WIN_HEIGHT = 800

# Game Images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")))
            ,pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")))
            ,pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Bird Class
class Bird:
    IMGS = BIRD_IMGS
    # Angel, Winkel, tilt the bird
    MAX_ROTATION = 25
    # Rotation velocity
    ROT_VEL = 20
    # Animation time
    ANIMATION_TIME = 5

    # INIT BIRD
    def __init__(self,x,y):
        #Starting Position
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    # Jumping
    def jump(self):
        self.velocity = -10.5 # negativ: 0,0 start in upper left corner
        self.tick_count = 0
        self.height = self.y

    # Move Forward
    def move(self):
        # 1 Frame per Second happend
        self.tick_count += 1
        # Displacement how many pixels we moving up or down this frame
        d = self.velocity * self.tick_count + 1.5 * self.tick_count**2
        # maximum falling speed
        if d >= 16:
            d = 16
        # maximum jumping up speed
        if d < 0:
            d -= 2
        # change y pos base on displacement
        self.y += d
        # tilting bird image
        if d < 0 or self.y < self.height +50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION # max 25 degrees
        else:   # falling down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    # Drawing bird on window
    def draw(self, win):
        # track the frames that passed
        self.img_count += 1
        # select correct img from array ANIMATION
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME *2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME *3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME *3:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME *4 +1:
            self.img = self.IMGS[0]
            self.img_count = 0
        # falling down
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        # Rotate image around the center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)   #blit = draw

# COLLISION
def get_mask(self):
    return pygame.mask,from_surface(self.img)

# Draw the window
def draw_window(win, bird):
    # background
    win.blit(BG_IMG, (0,0))#blit = draw
    bird.draw(win)
    # update display
    pygame.display.update()


def main():
    # bird position
    bird = Bird(200,200)
    # make a pygame window
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # Ingame FPS
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30) # 30 FPS
        for event in pygame.event.get():
            if event.type == pygame.quit:
                run = False
        bird.move()
        draw_window(win, bird)
    pygame.quit()
    quit()


    

if __name__ == "__main__":
    main()