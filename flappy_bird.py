import pygame
import neat
import time
import os 
import random
pygame.font.init()

# Window Size
WIN_WIDTH = 550
WIN_HEIGHT = 800

# Game Images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")))
            ,pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")))
            ,pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Score Fonts
STAT_FONT = pygame.font.SysFont("commicsans", 50)

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
    # COLLISION MASK
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


# CLASS PIPE
class Pipe:
    # space between pipes
    GAP = 200
    # pipes moving towards the bird
    VEL = 5
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self,win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    # COLLISION WITH BIRD
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Point of collision, returns None if no collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        #Check if there is a Collision
        if t_point or b_point:
            return True
        return False

#CLASS GROUND
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


# Draw the window
def draw_window(win, birds, pipes, base, score):
    # background
    win.blit(BG_IMG, (0,0))#blit = draw
    # draw pipes
    for pipe in pipes:
        pipe.draw(win)
    # Score font
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (0, 10)) # WIN_WIDTH -10 - text.get_width() YT SETTINGS
    # draw base 
    base.draw(win)
    # draw bird
    for bird in birds:
        bird.draw(win)
    # update display
    pygame.display.update()


def main(genomes, config):
    # Tracking the Neural Network
    nets = []
    ge = []
    # Init Birds
    birds = []  #Bird(230,350)#starting position

    # Adding Elemnts to the Lists
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        birds.append(Bird(230,350))
        ge.append(g)


    # init Base
    base = Base(730)
    # init pipes
    pipes = [Pipe(600)]
    # make a pygame window
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # Ingame FPS
    clock = pygame.time.Clock()
    # Score
    score = 0

    run = True
    while run and len(birds) > 0:
        clock.tick(30) # 30 FPS
        for event in pygame.event.get():
            if event.type == pygame.quit:
                run = False
                pygame.quit()
                quit()
        #bird.move()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        #else:
        #    run = False
        #    break

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()
            # Use Neural Network to calculate the action/ouput
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            #output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            # ACTION: JUMP !
            if output[0] > 0.5:
                bird.jump()

        # List of removed pipes
        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            for x, bird in enumerate(birds):
                #Collision
                if pipe.collide(bird):
                    # Removing failing birds
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            # Passing a Pipe
            if not pipe.passed and pipe.x < bird.x or bird.y > pipe.bottom and bird.y < pipe.top: # or bird.y <= 0 AB 2 OR !!!
                pipe.passed = True
                add_pipe = True
        
        
        # passed pipe, increase score
        if add_pipe:
            score += 1
            #Increase Bird Fitness through a reward
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        
        # remove passed pipes
        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() >= 730:
                # Remove failing birds
                #birds.pop(x)
                #nets.pop(x)
                #ge.pop(x)
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        # Move the Base
        base.move()
        # Draw the window
        draw_window(win, birds, pipes, base, score)


def run(config_path):
    # NEAT config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    # Create population
    p = neat.Population(config)

    # Reporter for the Output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run the main 50 times
    winner = p.run(main,50)

if __name__ == "__main__":
    # import NEAT config
    #local_dir = os.path.dirname(__file__)
    config_path = os.path.join("/home/zamy/ml/flappy/config-feedforward.txt")

    print(config_path)
    # run with config File
    run(config_path)

    #main()
