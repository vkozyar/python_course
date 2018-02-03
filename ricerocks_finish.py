# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
time = 0.5
global velocity, lives, started
started = False
lives = 3
velocity = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        canvas.draw_image(self.image, self.image_center , self.image_size, self.pos, self.image_size, self.angle)

        
    def update(self):
        self.angle += self.angle_vel
        forward = angle_to_vector(self.angle)
        vel_const = 0.98
        x_move = 90
        
        acc_vel = 0.12 / 48
        
        self.vel[0] *= (1 - acc_vel)
        self.vel[1] *= (1 - acc_vel)
        
        if self.thrust == True:
            self.vel[0] += (( 1 - vel_const ) * forward[0])
            self.vel[1] += (( 1 - vel_const ) * forward[1])
            if self.image_center[0] < 135:
                self.image_center[0] += x_move
        else:
            if self.image_center[0] < 135:
                self.image_center[0] += x_move
        
        if self.thrust == False:
            # hidden fire on ship
            if self.image_center[0] > 90:
                self.image_center[0] -= x_move
        
        #position and velocity update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # if move to the corner - change coordinate to start
        if self.pos[0] >= WIDTH:
            self.pos[0] -= WIDTH
        if self.pos[0] <= 0:
            self.pos[0] = WIDTH

        if self.pos[1] >= HEIGHT:
            self.pos[1] -= HEIGHT
        if self.pos[1] <= 0:
            self.pos[1] = HEIGHT

    def add_vel(self):
        self.angle_vel += .02
    
    def del_vel(self):
        self.angle_vel -= .02
        
    def change_thrust(self):
        #self.thrust = thrust
        if self.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    
    def shoot(self):
        global a_missile, missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 10 * forward[0], self.vel[1] + 10 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_image(self.pos, self.radius, 1, "Red", "Red")
        if self.animated:
            image_tile = (self.age % 20) // 1
            self.image_center = [self.image_center[0] + image_tile * self.image_size[0], self.image_center[1]]
        canvas.draw_image(self.image, self.image_center , self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.lifespan:
            if self.age > self.lifespan:
                return True
            else:
                self.age += 1
        return False
        
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) < self.radius + other_object.get_radius():
            return True
        else:
            return False
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
def draw(canvas):
    global time, rock_group, lives, score, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    #canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # Draw splash before playing
    if started == False:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    # update ship and sprites
    my_ship.update()
    
    # Show Scores amd lives
    canvas.draw_text('Lives: '+ str(lives), (40, 40), 35, "Green")
    canvas.draw_text('Score: '+ str(score), (620, 40), 35, "Green")

    if group_collide(rock_group, my_ship) == True:
        lives -= 1
        
    if group_group_collide(missile_group, rock_group):
        score += 1
        
    if lives <= 0:
        started = False
        rock_group = set([])
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        soundtrack.pause()
        timer.stop()
    
# Key handler

def down(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.del_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.add_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        my_ship.change_thrust()
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def up(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.add_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.del_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        my_ship.change_thrust()
        
def click(pos):
    global started, score, lives
    if (not started):
        started = True
        score = 0
        lives = 3
        timer.start()
        soundtrack.rewind()
        soundtrack.play()


# timer handler that spawns a rock    
def rock_spawner():    
    #global a_rock
    global rock_group
    
    if len(rock_group) >= 12 or started == False:
        #print "len rock_group =", len(rock_group)
        return
    x_pos = random.random() * 0.6 - 0.3
    y_pos = random.random() * 0.6 - 0.3
    rock_avel = random.random() * 0.2 - 0.05
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    
    while dist(rock_pos, my_ship.pos) < 60:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            
    a_rock = Sprite(rock_pos, [x_pos, y_pos] , 0, rock_avel, asteroid_image, asteroid_info)
    rock_group.add(a_rock)
    
def process_sprite_group(canvas, sprite_group):
    for sprite in set(sprite_group):
        sprite.draw(canvas)
        if sprite.update():
              sprite_group.remove(sprite)
        
def group_collide(group, other_object):
    for catch_rock in set(group):
        if catch_rock.collide(other_object):
            explosion_group.add(Sprite(catch_rock.get_position(), (0, 0), 0, 0, explosion_image, explosion_info, explosion_sound))
            group.remove(catch_rock)
            return True

def group_group_collide(group_one, group_two):
    for catch_one in set(group_one):
        for catch_two in set(group_two):
            if catch_one.collide(catch_two):
                explosion_group.add(Sprite(catch_one.get_position(), (0, 0), 0, 0, explosion_image, explosion_info, explosion_sound))
                group_one.remove(catch_one)
                group_two.remove(catch_two)
                return True
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)
frame.set_keydown_handler(down)
frame.set_keyup_handler(up)
frame.set_mouseclick_handler(click)

# get things rolling
timer.start()
frame.start()
