
import pygame
from math import sin, cos, pi
import random
import colorsys

# initialize pygame
pygame.init()

############# config ##############
fps = 60
window_size = ((1280, 720), (1920, 1080))[1]

rotation_speed = 0.05

gravitational_acceleration = 9.81

min_shoot_speed = 12
max_shoot_speed = 14
min_child_shoot_speed = 3
max_child_shoot_speed = 6

min_mass = 0.5
max_mass = 1

min_firework_size = 4
max_firework_size = 8

# inputed in seconds...
min_firework_lifetimeleft = 0.5
max_firework_lifetimeleft = 1

min_child_particles = 100
max_child_particles = 200

color_fade_rate = 0.02
size_change = 0.03

#########################################


def hs_to_rgb(hue, saturation, multiplier=255):
    rgb = colorsys.hsv_to_rgb(hue, saturation, 1)
    return (rgb[0] * multiplier, rgb[1] * multiplier, rgb[2] * multiplier)


# create window
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("fireworks simulation")
clock = pygame.time.Clock()

# variables
gravitational_acceleration /= fps

# ...then convert to frames
min_firework_lifetimeleft *= fps
max_firework_lifetimeleft *= fps

color_fade_rate = 1 - color_fade_rate

pi2 = pi * 2
half_pi = pi / 2

shooting_angle = -half_pi
shooting_angle_cos_sin = (cos(shooting_angle), sin(shooting_angle))

last_space_status = False

# [x, y, vx, vy, size, [r, g, b], mass, type, lifetime]
# type: 0 = firework, 1 = explosion particle
# color values can be above 255 to allow for virtual over exposure
particles = []

# main loop
while True:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # key handling
    keys = pygame.key.get_pressed()

    mouse_pos = pygame.mouse.get_pos()

    if keys[pygame.K_a]:
        shooting_angle -= rotation_speed
        if shooting_angle < 0:
            shooting_angle += pi2
        shooting_angle_cos_sin = (cos(shooting_angle), sin(shooting_angle))
    if keys[pygame.K_d]:
        shooting_angle += rotation_speed
        if shooting_angle > pi2:
            shooting_angle -= pi2
        shooting_angle_cos_sin = (cos(shooting_angle), sin(shooting_angle))

    if keys[pygame.K_SPACE] and not last_space_status:
        rgb = hs_to_rgb(random.random(), 0.5, 400)

        shoot_speed = random.uniform(min_shoot_speed, max_shoot_speed)
        size = random.uniform(min_firework_size, max_firework_size)
        lifetimeleft = random.uniform(min_firework_lifetimeleft, max_firework_lifetimeleft)
        particles.append([mouse_pos[0], mouse_pos[1], shooting_angle_cos_sin[0] * shoot_speed, shooting_angle_cos_sin[1] * shoot_speed, size, rgb, random.uniform(min_mass, max_mass), 0, lifetimeleft])

        last_space_status = True # <=============== change this to False to make it shoot every frame (very laggy)
    elif not keys[pygame.K_SPACE] and last_space_status:
        last_space_status = False
        

    
    window.fill((0, 0, 0))

    # draw shooting angle line
    pygame.draw.line(window, (255, 255, 255), mouse_pos, (mouse_pos[0] + shooting_angle_cos_sin[0] * 50, mouse_pos[1] + shooting_angle_cos_sin[1] * 50), 8)


    for particle in particles:
        # draw particle

        # calculate sum of values over 255 of each color channel
        overexposure_value = particle[5][0] - 255 if particle[5][0] > 255 else 0 + \
                             particle[5][1] - 255 if particle[5][1] > 255 else 0 + \
                             particle[5][2] - 255 if particle[5][2] > 255 else 0
                              
        # add overexposure value to each color channel
        rgb = (particle[5][0] + overexposure_value, particle[5][1] + overexposure_value, particle[5][2] + overexposure_value)

        # then clamp color values to 255
        rgb = (255 if rgb[0] > 255 else rgb[0], \
               255 if rgb[1] > 255 else rgb[1], \
               255 if rgb[2] > 255 else rgb[2])

        pygame.draw.circle(window, rgb, (particle[0], particle[1]), particle[4])

        # update particle position (move it by its velocity)
        particle[0] += particle[2]
        particle[1] += particle[3]

        # update particle velocity

        # add gravitational acceleration multiplied by the mass of the particle
        particle[3] += gravitational_acceleration * particle[6]


        # update particle size
        particle[4] -= size_change

        # update particle color
        particle[5] = (particle[5][0] * color_fade_rate, particle[5][1] * color_fade_rate, particle[5][2] * color_fade_rate)

        # update particle lifetime
        particle[8] -= 1

        # remove particle if it is too small OR all of is colors values are below 1
        if particle[4] <= 0:
            particles.remove(particle)
        elif particle[5][0] < 1 and particle[5][1] < 1 and particle[5][2] < 1:
            particles.remove(particle)

        # remove particle its lifetime is over if it is a firework and create explosion particles
        elif particle[7] == 0 and particle[8] <= 0:
            # create new particles around curent particle
            particles_count = random.randint(min_child_particles, max_child_particles)

            rgb = hs_to_rgb(random.random(), 0.8, 600)

            for i in range(particles_count):

                # create random velocity vector
                angle = random.uniform(0, pi2)
                speed = random.uniform(min_child_shoot_speed, max_child_shoot_speed)
                vx = cos(angle) * speed + particle[2]
                vy = sin(angle) * speed + particle[3]

                # create particle
                particles.append([particle[0], particle[1], vx, vy, 5, rgb, random.uniform(min_mass, max_mass), 1, 100])
            
            # remove firework
            particles.remove(particle)

    # update display
    pygame.display.update()
    clock.tick(fps)