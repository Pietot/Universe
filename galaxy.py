"""
Simulate a galaxy with many stars. All stars are attracted by each other
"""


# By Piétôt
# Discord : Piétôt#1754
# Start : 07/09/2023 at 16:03 FR
# End : 10/09/2023 at 2:38 FR

# v1.1 :
# Time : 30 min
# Changelogs : Fixed collision


import random as rdm

import math
import time
import pyautogui
import pygame


class Particle:
    """ A Particle
    """

    def __init__(self, column: int, line: int,
                 mass: int, is_black_hole: bool = False) -> None:
        # Unit in pixel
        self.column = column
        self.line = line
        # No unit
        self.mass = mass
        self.is_black_hole = is_black_hole
        # Unit in pixel. Euclidean division to have a value between 1 and 15
        self.diameter = round(mass//33.3) if not is_black_hole else 20
        distance_column = MIDDLE_SCREEN[0] - self.column
        distance_line = MIDDLE_SCREEN[1] - self.line
        # First int : positive => toward the left, negative => toward the right
        # Second int : positive => downward, negative => upward
        self.velocity = [(distance_line/50),
                         (-distance_column/50)]
        self.acceleration = [0.0, 0.0]

    def draw(self) -> None:
        """ Draws the circle of a particle in the Pygame's screen
        """
        if not self.is_black_hole:
            pygame.draw.circle(screen, (255, 255, 255),
                               (self.column, self.line), self.diameter)
            return None
        pygame.draw.circle(screen, (0, 0, 0),
                           (self.column, self.line), self.diameter)
        return None

    def update(self, delta_t: float = 1.0) -> None:
        """ Update the position of a article
        """
        self.velocity[0] += self.acceleration[0]*delta_t
        self.velocity[1] += self.acceleration[1]*delta_t
        self.column += self.velocity[0]*delta_t
        self.line += self.velocity[1]*delta_t
        self.collision()

    def collision(self) -> None:
        """ Verify if two particles are in collision and merge them if so

            For the loop, we make a copy since we may remove an item from the iterated list.
            Doing so can result in unexpected behaviour, that's why it's preferred to use a copy.
            Even if in this case there is no issues.
        """
        for prtcl_2 in particles.copy():
            if self != prtcl_2:
                distance = math.dist([self.column, self.line], [
                                     prtcl_2.column, prtcl_2.line])
                if ((distance - (self.diameter+prtcl_2.diameter)/2 < 0) and
                        (self.mass >= prtcl_2.mass)):
                    self.mass += prtcl_2.mass
                    self.diameter = diameter_new_circle(
                        self.diameter, prtcl_2.diameter)
                    self.acceleration = [float(sum(i)) for i in zip(
                        self.acceleration, prtcl_2.acceleration)]
                    particles.remove(prtcl_2)


def gravity(prtcl_1: Particle) -> list[float]:
    """ Calculates the acceleration (and direction) of a particle
        depending of it's mass and position.

    Args:
        prtcl (Particle): The particle

    Returns:
        list[float]: The acceleration of the particule
    """
    force = 0
    acceleration_column, acceleration_line = prtcl_1.acceleration[0], prtcl_1.acceleration[1]
    for prtcl_2 in particles:
        if prtcl_1 != prtcl_2:
            distance_column = prtcl_2.column - prtcl_1.column
            distance_line = prtcl_2.line - prtcl_1.line
            distance = math.sqrt(distance_column**2 + distance_line**2)
            force = min(GRAVITY *
                        ((prtcl_1.mass * prtcl_2.mass) / (distance**2)), 500)
            acceleration_column += (force*distance_column/distance)
            acceleration_line += (force*distance_line/distance)
    return [acceleration_column/prtcl_1.mass, acceleration_line/prtcl_1.mass]


def diameter_new_circle(diameter1: int, diameter2: int) -> int:
    """ Finds the diameter of the sum of two areas of two circles
    Args:
        diameter1 (int): Obvious
        diameter2 (int): Obvious

    Returns:
        int: The diamter of the new circle
    """
    area_new_circle = (math.pi*((diameter1/2)**2) +
                       math.pi*((diameter2/2)**2))
    radius_new_circle = math.sqrt(area_new_circle/math.pi)
    diamter_new_circle = 2 * radius_new_circle
    return round(diamter_new_circle)


def random_position() -> tuple[int, int]:
    """ Generate a random position for a Particle in a circle. 

    Returns:
        tuple[int, int]: The coordinate column and line of the position 
    """
    angle = rdm.uniform(0, 2 * math.pi)
    # The first int defines the minimum distance and the second int defines the limit.
    distance = rdm.uniform(300, MIDDLE_SCREEN[1])
    column = round(distance * math.cos(angle)) + MIDDLE_SCREEN[0]
    line = round(distance * math.sin(angle)) + MIDDLE_SCREEN[1]
    return column, line


if __name__ == "__main__":
    # Images shown
    HERTZ = 144
    # Images generated for the simulation
    FPS = 10
    WIDTH, HEIGHT = pyautogui.size()
    MIDDLE_SCREEN = (WIDTH // 2, HEIGHT // 2)
    GRAVITY = 6.674
    NB_PARTICLES = 100

    pygame.init()  # pylint: disable=maybe-no-member

    screen = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN)  # pylint: disable=maybe-no-member
    clock = pygame.time.Clock()

    pygame.display.flip()

    particles = [
        Particle(column=coordinate[0],
                 line=coordinate[1], mass=rdm.randint(50, 500))
        for _ in range(NB_PARTICLES)
        for coordinate in [random_position()]
    ]

    previous_time = time.time()
    running: bool = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running: bool = False

        current_time = time.time()
        delta_time = (current_time - previous_time)*FPS
        previous_time = current_time

        screen.fill((50, 50, 50))

        # 2 loops cause we calculate every acceleration of every particles without moving them
        for particle in particles:
            particle.acceleration = gravity(prtcl_1=particle)

        for particle in particles:
            if not particle.is_black_hole:
                particle.update(delta_t=delta_time)
            particle.draw()

        pygame.display.flip()
        clock.tick(HERTZ)

    pygame.quit()
