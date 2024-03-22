import pygame
import random
import math


#pygame module initialization
pygame.init()

#global parameters
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
MAX_POPULATION_SIZE = 35
CLOCK = pygame.time.Clock()
FPS = 60
RULE_1_CONSTANT = 1 #constant to multiply velocity - velocity control
RULE_2_CONSTANT = 2 #constant to multiply the seperation rate
RULE_3_CONSTANT = 20 #constant to set minimum seperation distance of boids
SCREEN_BORDER_MARGIN = 50 #constant to set the turning point before screen border

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

    return (x, y)

#function to avoid collisions
def avoid_collisions(entity, flock):
    #Define a minimum distance to maintain between boids

    #Calculate the vector to avoid collisions
    avoid_vector = [0, 0]

    for other_entity in flock:
        if other_entity != entity:
            dx = other_entity.rect.centerx - entity.rect.centerx
            dy = other_entity.rect.centery - entity.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance < RULE_3_CONSTANT:
                # Calculate the component of the avoid vector
                # proportional to the distance to the other entity
                avoid_vector[0] -= dx / distance
                avoid_vector[1] -= dy / distance

    return avoid_vector


#function to align boid to the average heading
def average_heading(flock):
    avg_heading = [0, 0]
    total_entities = len(flock)

    if total_entities == 0:
        return avg_heading

    for entity in flock:
        avg_heading[0] += entity.velocity[0]
        avg_heading[1] += entity.velocity[1]

    avg_heading[0] /= total_entities
    avg_heading[1] /= total_entities

    # Normalize the average heading vector
    avg_heading_length = (avg_heading[0] ** 2 + avg_heading[1] ** 2) ** 0.5
    if avg_heading_length != 0:
        avg_heading[0] /= avg_heading_length
        avg_heading[1] /= avg_heading_length

    return avg_heading

#class for Boids -inherited pygame sprite class
class Boid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load("C:/Users/senor/OneDrive/python/PYBoidssimulation/arrow.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Initialize random velocity

    def update(self):
        # Check if the boid is near the screen borders

        if self.rect.left < SCREEN_BORDER_MARGIN:
            self.velocity[0] += 1  # Steer away from the left border
        elif self.rect.right > SCREEN_WIDTH - SCREEN_BORDER_MARGIN:
            self.velocity[0] -= 1  # Steer away from the right border
        if self.rect.top < SCREEN_BORDER_MARGIN:
            self.velocity[1] += 1  # Steer away from the top border
        elif self.rect.bottom > SCREEN_HEIGHT - SCREEN_BORDER_MARGIN:
            self.velocity[1] -= 1  # Steer away from the bottom border

        # Update position
        self.rect.move_ip(self.velocity[0], self.velocity[1])

        # Calculate the angle of rotation based on the velocity vector
        angle = math.degrees(math.atan2(-self.velocity[1], self.velocity[0]))

        # Rotate the original image and update the sprite
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # population control
        if not screen.get_rect().colliderect(self.rect):  # If boid is outside the screen
            self.kill()


#create sprite group for flock
flock = pygame.sprite.Group()

#check print
print("simulation running")

#Main Loop
run = True
while run:

    CLOCK.tick(FPS)

    #update background
    screen.fill("black")

    #update sprite group
    flock.update()

    #draw sprite group
    flock.draw(screen)

    #boids spawner
    for x in range(MAX_POPULATION_SIZE):

        if random.randrange(0, 100) < 1 and len(flock) < MAX_POPULATION_SIZE:
            entity = Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            flock.add(entity)

    #end simulation by click
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

        else:
            normalized_vector = (0, 0)

        entity.rect.move_ip(int(RULE_1_CONSTANT*normalized_vector[0]),int(RULE_1_CONSTANT*normalized_vector[1]))
        
        #RULE_2 seperation 
        for entity in flock:
            #Calculate the avoid vector
            avoid = avoid_collisions(entity, flock)

            #Apply the avoid vector to the boid's movement
            entity.rect.move_ip(int(avoid[0] * RULE_2_CONSTANT), int(avoid[1] * RULE_2_CONSTANT))

    for entity in flock:
        #Calculate the avoid vector
        avoid = avoid_collisions(entity, flock)

        #Calculate the alignment vector
        alignment = average_heading(flock)

        #Apply the alignment vector to the boid's movement
        entity.velocity[0] += alignment[0]
        entity.velocity[1] += alignment[1]

        #Limit the maximum speed of the boid (optional)
        max_speed = 3
        speed = (entity.velocity[0] ** 2 + entity.velocity[1] ** 2) ** 0.5
        if speed > max_speed:
            entity.velocity[0] = max_speed * (entity.velocity[0] / speed)
            entity.velocity[1] = max_speed * (entity.velocity[1] / speed)

        #Update the position of the boid
        entity.rect.move_ip(int(entity.velocity[0]), int(entity.velocity[1]))

        #Ensure the boid stays within the screen boundaries
        entity.rect.clamp_ip(screen.get_rect())
    #update display
    pygame.display.flip()
pygame.quit()