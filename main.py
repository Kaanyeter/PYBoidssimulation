import pygame
import random


#pygame module initialization
pygame.init()

#global parameter
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
MAX_POPULATION_SIZE = 5
CLOCK = pygame.time.Clock()
FPS = 60
RULE_1_CONSTANT = 2
RULE_2_CONSTANT = 1

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boids Simulation")

#function to find average position of all boids
def average_mass(flock):
    x = 0
    y = 0

    for entity in flock:
        x = x + entity.rect.center[0]
        y = y + entity.rect.center[1]
    n = len(flock)

    if len(flock) > 1:
        x = x / n
        y = y / n
    
    #print("x =", x)
    #print("y =", y)

    return (x, y)

def avoid_collisions(entity, flock):
    # Define a minimum distance to maintain between boids
    min_distance = 50

    # Calculate the vector to avoid collisions
    avoid_vector = [0, 0]

    for other_entity in flock:
        if other_entity != entity:
            dx = other_entity.rect.centerx - entity.rect.centerx
            dy = other_entity.rect.centery - entity.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance < min_distance:
                # Calculate the component of the avoid vector
                # proportional to the distance to the other entity
                avoid_vector[0] -= dx / distance
                avoid_vector[1] -= dy / distance

    return avoid_vector            


#create class for Boids (flock)
class Boid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:/Users/senor/OneDrive/python/PYBoidssimulation/arrow.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.move_ip(0, -1)
        
        #population control
        if self.rect.y > SCREEN_WIDTH or self.rect.x > SCREEN_HEIGHT or self.rect.y < 0 or self.rect.x < 0:
            self.kill()



#create sprite group for flock
flock = pygame.sprite.Group()

#game loop
run = True
while run:

    CLOCK.tick(FPS)

    #update background
    screen.fill("blue")

    #update sprite group
    flock.update()

    #draw sprite group
    flock.draw(screen)

    #population size check
    #print(len(flock))

    #boids spawner
    for x in range(MAX_POPULATION_SIZE):

        if random.randrange(0, 100) < 1 and len(flock) < MAX_POPULATION_SIZE:
            entity = Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            flock.add(entity)

    #quit program
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    x,y = average_mass(flock)
    
    #RULE_1 entities moving to average mass 
    for entity in flock:
        a = entity.rect.center[0]
        b = entity.rect.center[1]

        d = x-a
        e = y-b
        vector_length = (d**2 + e**2)**0.5

        if vector_length != 0:

            normalized_vector = (d/vector_length, e/vector_length)
            print(normalized_vector)
        else:
            normalized_vector = (0, 0)

        entity.rect.move_ip(int(RULE_1_CONSTANT*normalized_vector[0]),int(RULE_1_CONSTANT*normalized_vector[1]))
        
        # Inside the main loop
        for entity in flock:
            # Calculate the avoid vector
            avoid = avoid_collisions(entity, flock)

            # Apply the avoid vector to the boid's movement
            entity.rect.move_ip(int(avoid[0] * RULE_2_CONSTANT), int(avoid[1] * RULE_2_CONSTANT))

    #update display
    pygame.display.flip()

pygame.quit()