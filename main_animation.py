# animation3.py

"""Multiple-shot cannonball animation. This program simulates the trajectory of a object launched from the ground at any
angle and initial velocity using kinematics (neglects air resistance).

[Update 11/27/2023] The following changes have been made to Zelle's original program:

- Launch window size increased to 1280x960 and max. horizontal distance increased from 210m to 420m.
- Added display for initial velocity and angle (top left of the program window).
- Initial launch angle and velocity now increment by 2.5 degrees and 1 m/s, respectively, with each arrow key press.
- Simulation is updated every 1/120th of a second instead of the original 1/30 seconds (smoother).
- The current x and y position (m) relative to launch point, as well as velocity (m/s), is displayed next to each
cannonball while fired. This display will disappear after the cannonball hits the ground (y = 0.0m).
- Added display for last launch x-distance and final speed (using kinematics, final speed should be the same as init.).
The display ONLY updates for the LAST cannonball launched (i.e. if 3 balls were launched successively, the counter will
only show final distance/velocity of the 3rd ball). Display will show N/A (>420m) for cannonballs that land beyond the
simulation window.
"""

from math import sqrt, sin, cos, radians, degrees, pi
from graphics import *
from ch10_projectile import Projectile

class Launcher:

    def __init__(self, win):
        """Create initial launcher with angle 45 degrees and velocity 40
        win is the GraphWin to draw the launcher in.
        """
        
        # draw the base shot of the launcher
        base = Circle(Point(0,0), 3)
        base.setFill("red")
        base.setOutline("red")
        base.draw(win)

        # save the window and create initial angle and velocity
        self.win = win
        self.angle = radians(45.0)
        self.vel = 40.0
        
        # create initial "dummy" arrow
        self.arrow = Line(Point(0,0), Point(0,0)).draw(win)
        # replace it with the correct arrow
        self.redraw()


    def redraw(self):
        """undraw the arrow and draw a new one for the
        current values of angle and velocity.
        """
        
        self.arrow.undraw()
        pt2 = Point(self.vel*cos(self.angle), self.vel*sin(self.angle))
        self.arrow = Line(Point(0,0), pt2).draw(self.win)
        self.arrow.setArrow("last")
        self.arrow.setWidth(3)

        
    def adjAngle(self, amt):
        """ change angle by amt degrees """
        
        self.angle = self.angle+radians(amt)
        self.redraw()

        
    def adjVel(self, amt):
        """ change velocity by amt"""
        
        self.vel = self.vel + amt
        self.redraw()

    def fire(self):
        """ uses ShotTracker to display and fire the cannonball"""
        return ShotTracker(self.win, degrees(self.angle), self.vel, 0.0)
  

class ShotTracker:

    """ Graphical depiction of a projectile flight using a Circle """

    def __init__(self, win, angle, velocity, height):
        """win is the GraphWin to display the shot, angle, velocity, and
        height are initial projectile parameters.
        """
        
        self.proj = Projectile(angle, velocity, height)
        self.marker = Circle(Point(0,height), 3)
        self.marker.setFill("red")
        self.marker.setOutline("red")
        self.marker.draw(win)
        self.statX = Text(Point(self.proj.getX(), self.proj.getY()+20), "x (m):")
        self.statXval = Text(Point(self.proj.getX()+15, self.proj.getY()+20), "")
        self.statX.draw(win)
        self.statXval.draw(win)
        self.statY = Text(Point(self.proj.getX(), self.proj.getY()+15), "y (m):")
        self.statYval = Text(Point(self.proj.getX()+15, self.proj.getY()+15), "")
        self.statY.draw(win)
        self.statYval.draw(win)
        self.statV = Text(Point(self.proj.getX(), self.proj.getY()+10), "Speed (m/s):")
        self.statVval = Text(Point(self.proj.getX()+23, self.proj.getY()+10), "")
        self.statV.draw(win)
        self.statVval.draw(win)

        
    def update(self, dt):
        """ Move the shot dt seconds farther along its flight """

        self.proj.update(dt)
        center = self.marker.getCenter()
        dx = self.proj.getX() - center.getX()
        dy = self.proj.getY() - center.getY()
        self.marker.move(dx,dy)
        self.statX.move(dx,dy)
        self.statXval.setText(round(self.proj.getX(),1))
        self.statXval.move(dx, dy)
        self.statY.move(dx, dy)
        self.statYval.move(dx, dy)
        self.statV.move(dx, dy)
        self.statVval.move(dx, dy)
        self.statVval.setText(round(self.proj.getVel(),1))
        if self.proj.getY() >= 0 and self.proj.getX() <= 420:
            self.statYval.setText(round(self.proj.getY(),1))
            self.statVval.setText(round(self.proj.getVel(), 1))
        else:
            self.statX.undraw()
            self.statXval.undraw()
            self.statY.undraw()
            self.statYval.undraw()
            self.statV.undraw()
            self.statVval.undraw()

        
    def getX(self):
        """ return the current x coordinate of the shot's center """
        return self.proj.getX()

    def getY(self):
        """ return the current y coordinate of the shot's center """
        return self.proj.getY()

    def getVel(self):
        """return the current speed of the shot"""
        return self.proj.getVel()

    def undraw(self):
        """ undraw the shot """
        self.marker.undraw()


class ProjectileApp:

    def __init__(self):
        """ Prepares and draws the program window """
        self.win = GraphWin("Projectile Animation", 1280, 960)
        self.win.setCoords(-20, -20, 420, 310)
        Line(Point(-20,0), Point(420,0)).draw(self.win)
        for x in range(0, 420, 100):
            Text(Point(x,-7), str(x)).draw(self.win)
            Line(Point(x,0), Point(x,2)).draw(self.win)

        self.launcher = Launcher(self.win)
        initAngleTxt = Text(Point(10, 300), "Initial Angle (degrees):")
        self.initAngle = Text(Point(45,300), self.launcher.angle * (180/pi))
        initAngleTxt.draw(self.win)
        self.initAngle.draw(self.win)
        initVelTxt = Text(Point(7,285), "Initial Velocity (m/s):")
        self.initVel = Text(Point(45,285), self.launcher.vel)
        initVelTxt.draw(self.win)
        self.initVel.draw(self.win)
        finPosTxt = Text(Point(15,-15), "Last Shot Distance (m):")
        finPosTxt.draw(self.win)
        finVelTxt = Text(Point(120,-15), "Last Shot Final Speed (m/s):")
        finVelTxt.draw(self.win)
        self.shots = []

    def updateShots(self, dt):
        """ Updates each cannonball after firing, as well as their respective x, y-distance and velocity display. """
        alive = []
        x = ""
        y = ""
        v = ""
        for shot in self.shots:
            shot.update(dt)
            x = round(shot.getX(), 1)
            v = round(shot.getVel(), 1)
            if shot.getY() > 0.0 and shot.getX() < 420:
                alive.append(shot)
                y = round(shot.getY(), 1)
            elif shot.getY() > 0.0 and shot.getX() > 420:
                x = "N/A (>420)"
                y = 0.0
                v = "N/A"
                shot.undraw()
            else:
                y = 0.0
                shot.undraw()
        self.shots = alive
        return x, y, v


    def run(self):

        finPos = Text(Point(60, -15), "")
        finPos.setTextColor("green")
        finPos.draw(self.win)
        finVel = Text(Point(165, -15), "")
        finVel.setTextColor("blue")
        finVel.draw(self.win)
        # main event/animation loop.
        while True:
            # updates each shot at 120 fps (120 times a sec.)
            x, y, v = self.updateShots(1/120)
            # sets last shot final horizontal distance and speed upon landing on the ground (y=0.0m).
            if x != "" and y <= 0.0:
                finPos.setText(x)
                finVel.setText(v)

            key = self.win.checkKey()
            if key in ["q", "Q"]:
                break

            if key == "Up":
                self.launcher.adjAngle(2.5)
                self.initAngle.setText(round(self.launcher.angle * (180/pi), 1))
            elif key == "Down":
                self.launcher.adjAngle(-2.5)
                self.initAngle.setText(round(self.launcher.angle * (180 / pi), 1))
            elif key == "Right":
                self.launcher.adjVel(1)
                self.initVel.setText(round(self.launcher.vel, 1))
            elif key == "Left":
                self.launcher.adjVel(-1)
                self.initVel.setText(round(self.launcher.vel, 1))
            elif key == "f":
                self.shots.append(self.launcher.fire())
           
            update(240)

        self.win.close()
           

if __name__ == "__main__":
    ProjectileApp().run()
