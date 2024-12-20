# projectile.py

"""
Provides a simple class for modeling the flight of projectiles.

[Update 11/26/2023] The following changes have been made to Zelle's original class:
- Added getVel() method that returns the current speed of the projectile.
"""
   
from math import sqrt, sin, cos, radians

class Projectile:

    """Simulates the flight of simple projectiles near the earth's
    surface, ignoring wind resistance. Tracking is done in two
    dimensions, height (y) and distance (x)."""

    def __init__(self, angle, velocity, height):
        """Create a projectile with given launch angle, initial
        velocity and height."""
        self.xpos = 0.0
        self.ypos = height
        theta = radians(angle)
        self.xvel = velocity * cos(theta)
        self.yvel = velocity * sin(theta)

    def update(self, time):
        """Update the state of this projectile to move it time seconds
        farther into its flight"""
        self.xpos = self.xpos + time * self.xvel
        yvel1 = self.yvel - 9.8 * time
        self.ypos = self.ypos + time * (self.yvel + yvel1) / 2.0
        self.yvel = yvel1

    def getY(self):
        "Returns the y position (height) of this projectile."
        return self.ypos

    def getX(self):
        "Returns the x position (distance) of this projectile."
        return self.xpos

    def getVel(self):
        "Returns velocity (speed, m/s) of this projectile."
        self.vel = sqrt((self.xvel)**2 + (self.yvel)**2)
        return self.vel