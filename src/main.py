import pygame
import math

pygame.init()
pygame.font.init()

WIDTH = 1920
HEIGHT = int(WIDTH / 16 * 9)
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("PYlanetarium")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 71, 81)



FONT = pygame.font.SysFont("fonts\RobotoMono-VariableFont_wght.ttf", 16)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 350 / AU  # 1AU = 100 pixels
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.orbitColor = (color[0] / 3, color[1] / 3, color[2] / 3)
        self.mass = mass

        self.TIMESTEP = 3600 # 1 hour in sec


        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.orbitColor, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if not planet.sun:
                continue
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
    


def drawGrid():
    size = 20
    offset = [[WIDTH / 2, HEIGHT / 2], [0, HEIGHT / 2],[0, -(size*2-4)], [WIDTH / 2, -(size*2-4)]]
    blockSizeX = int(WIDTH / size) #Set the size of the grid block
    # blockSizeY = int(HEIGHT / size ) #Set the size of the grid block
    # for x in range(0, WIDTH, blockSizeX):
    #     for y in range(0, HEIGHT, blockSizeX):
    #         rect = pygame.Rect(x - offsetX, y - offsetY, blockSizeX, blockSizeX)
    #         pygame.draw.rect(WIN, (50, 50, 50), rect, 1)
    i = 0
    while i < 4:
        for x in range(0, int(WIDTH / 2), blockSizeX):
            for y in range(0, int(HEIGHT / 2), blockSizeX):
                rect = pygame.Rect(x + offset[i][0], y + offset[i][1], blockSizeX, blockSizeX)
                pygame.draw.rect(WIN, (50, 50, 50), rect, 1)
        i += 1

def main():
    publicTimeScale = 1
    timePast = 0

    run = True
    FPS = 60
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    # Text
    
    
    
    while run:
        clock.tick(FPS)
        WIN.fill((0, 0, 0))
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_LEFT:
                    publicTimeScale -= 1
                    for planet in planets:
                        planet.TIMESTEP -= 3600
                if event.key == pygame.K_RIGHT:
                    publicTimeScale += 1
                    for planet in planets:
                        planet.TIMESTEP += 3600

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        time_scale_text_surface = FONT.render(f"Time scale: {publicTimeScale} hour(s)", True, WHITE) 
        WIN.blit(time_scale_text_surface, (0,0))
        timePast += publicTimeScale
        print (f"Time elapsed {timePast} hour(s)", end="\r")

        pygame.display.flip()
    pygame.quit()


main()
