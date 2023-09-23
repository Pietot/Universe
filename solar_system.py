"""
Simulate a solar system, all planets are attracted by the stars but not with each other
"""


# By Piétôt
# Discord : Piétôt#1754
# Start : 04/09/2023 at 00:38
# End : 07/092023 at 16:03 FR


import random as rdm

import math
import time
import pyautogui
import pygame


class Particle():
    """ A Particle
    """

    def __init__(self, column: int, line: int,
                 mass: int) -> None:
        # Unit in pixel
        self.column = column
        self.line = line
        # No unit
        self.mass = mass
        # Unit in pixel. Euclidean division to have a value between 1 and 15
        self.diameter = mass//3.3
        distance_column = MIDDLE_SCREEN[0] - self.column
        distance_line = MIDDLE_SCREEN[1] - self.line
        distance = math.sqrt(distance_column**2 + distance_line**2)
        # First int : positive => toward the left, negative => toward the right
        # Second int : positive => downward, negative => upward
        self.velocity = [(distance_line/(distance**(1/1.3))),
                         (-distance_column/(distance**(1/1.3)))]
        self.acceleration = [0, 0]

    def draw(self) -> None:
        """ Draws the circle of a particle in the Pygame's screen
        """
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.column, self.line), self.diameter)

    def update(self, delta_t: float = 1.0) -> None:
        """ Update the position of a article

        Args:
            delta_t (float, optional): The step of time
        """
        self.acceleration = gravity(prtcl=self)
        self.velocity[0] += self.acceleration[0]*delta_t
        self.velocity[1] += self.acceleration[1]*delta_t
        self.column += self.velocity[0]*delta_t
        self.line += self.velocity[1]*delta_t


def gravity(prtcl: Particle) -> list[float]:
    """ Calculates the acceleration (and direction) of a particle
        depending of it's mass and position.

    Args:
        prtcl (Particle): The particle

    Returns:
        list[float]: The acceleration of the particule
    """
    distance_column = MIDDLE_SCREEN[0] - prtcl.column
    distance_line = MIDDLE_SCREEN[1] - prtcl.line
    distance = math.sqrt(distance_column**2 + distance_line**2)
    force = GRAVITY * ((prtcl.mass * SOLAR_MASS) / (distance**2))
    acceleration_column = max(min(force*distance_column/distance, 1), -1)
    acceleration_line = max(min(force*distance_line/distance, 1), -1)
    return [acceleration_column, acceleration_line]


if __name__ == "__main__":
    HERTZ = 144
    FPS = 60
    WIDTH, HEIGHT = pyautogui.size()
    MIDDLE_SCREEN = (WIDTH // 2, HEIGHT // 2)
    GRAVITY = 6.674
    SOLAR_MASS = 100
    NB_PARTICLE = 100

    pygame.init()  # pylint: disable=maybe-no-member

    screen = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN)  # pylint: disable=maybe-no-member
    clock = pygame.time.Clock()

    pygame.display.flip()

    particles = [Particle(column=rdm.randint(0, WIDTH), line=rdm.randint(0, WIDTH),
                          mass=rdm.randint(1, 50))
                 for _ in range(NB_PARTICLE)]

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

        for particle in particles:
            particle.update(delta_t=delta_time)
            particle.draw()

        pygame.draw.circle(screen, (255, 255, 0), MIDDLE_SCREEN, 20)

        pygame.display.flip()
        clock.tick(HERTZ)

    pygame.quit()
