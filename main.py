import pygame
import time
from math import sin, cos, pi
import random
import colorsys
import numpy as np

pygame.init()

def current_time():
    return round(time.time() * 1000)

# Variable
fps = 60
window_size = (1440, 850)

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

min_firework_lifetimeleft = 0.5
max_firework_lifetimeleft = 1

min_child_particles = 100
max_child_particles = 200

color_fade_rate = 0.02
size_change = 0.05

time_tick = current_time()
logo_tick = current_time()
newyear_tick = current_time()
step_newyear_tick = current_time()
step_newyear_counter = 0
step_year_tick = current_time()
show_year_tick = current_time()
icon_tick = current_time()
mouse_pos = (0, 850)

particles = []

def hs_to_rgb(hue, saturation, multiplier=255):
    rgb = colorsys.hsv_to_rgb(hue, saturation, 1)
    return (rgb[0] * multiplier, rgb[1] * multiplier, rgb[2] * multiplier)

window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Logiscool Happy New Year")
clock = pygame.time.Clock()


gravitational_acceleration /= fps

min_firework_lifetimeleft *= fps
max_firework_lifetimeleft *= fps

color_fade_rate = 1 - color_fade_rate

pi2 = pi * 2
half_pi = pi / 2

shooting_angle = -half_pi
shooting_angle_cos_sin = (cos(shooting_angle), sin(shooting_angle))


# Logiscool Image
temp = 10
counter = 0
logiscool_img_init = pygame.image.load('./logiscool.png')
img_height = logiscool_img_init.get_height()
img_width = logiscool_img_init.get_width()
logiscool_img = pygame.transform.scale(logiscool_img_init, (img_width / temp, img_height / temp))
logiscool_reg = logiscool_img.get_rect(center = (window.get_width() / 2, window.get_height() - logiscool_img.get_height() - 280))

font = pygame.font.Font('./QwitcherGrypen.ttf', 192)
color_list = [(165, 0, 80), (196, 214, 0), (0, 156, 222), (0, 66, 106)]

# Happy New Year
newyear_letter1 = font.render('Happy', True, color_list[1])
newyear_letter2 = font.render('New', True, color_list[1])
newyear_letter3 = font.render('Year', True, color_list[1])
newyear_rect1 = newyear_letter1.get_rect(center = (window.get_width() / 2 - 350, window.get_height() / 2 - 200))
newyear_rect2 = newyear_letter2.get_rect(center = (window.get_width() / 2 + 50, window.get_height() / 2 - 200))
newyear_rect3 = newyear_letter3.get_rect(center = (window.get_width() / 2 + 390, window.get_height() / 2 - 200))

# 2024
full_array = np.array([0, 1, 2, 3])
font2 = pygame.font.Font('./QwitcherGrypen.ttf', 325)
year_letter1 = font2.render('2', True, color_list[0])
year_letter2 = font2.render('0', True, color_list[1])
year_letter3 = font2.render('2', True, color_list[2])
year_letter4 = font2.render('4', True, color_list[3])
year_rect1 = year_letter1.get_rect(center = (window.get_width() / 2 - 120, window.get_height() / 2 - 20))
year_rect2 = year_letter2.get_rect(center = (window.get_width() / 2 - 10, window.get_height() / 2 - 20))
year_rect3 = year_letter3.get_rect(center = (window.get_width() / 2 + 100, window.get_height() / 2 - 20))
year_rect4 = year_letter4.get_rect(center = (window.get_width() / 2 + 210, window.get_height() / 2 - 20))

# Logiscool Image
zikina_init = pygame.image.load('./zikina.png')
zikina_init = pygame.transform.scale(zikina_init, (zikina_init.get_width() / 8, zikina_init.get_height() / 8))
zikina_init_temp = pygame.transform.rotate(zikina_init, -20)
zikina_reg = zikina_init.get_rect(center = (window.get_width() / 2 - 600, window.get_height() - zikina_init.get_height() + 150 - 40))

pavito_init = pygame.image.load('./pavito.png')
pavito_init = pygame.transform.scale(pavito_init, (pavito_init.get_width() / 7, pavito_init.get_height() / 7))
pavito_init_temp = pygame.transform.rotate(pavito_init, -20)
pavito_reg = pavito_init.get_rect(center = (window.get_width() / 2 - 450, window.get_height() - pavito_init.get_height() + 50 - 40))

sunface_init = pygame.image.load('./sunface.png')
sunface_init = pygame.transform.scale(sunface_init, (sunface_init.get_width() / 7, sunface_init.get_height() / 7))
sunface_init_temp = pygame.transform.rotate(sunface_init, -20)
sunface_reg = sunface_init.get_rect(center = (window.get_width() / 2 - 300, window.get_height() - sunface_init.get_height() + 100 - 40))

exrobot_init = pygame.image.load('./exrobot.png')
exrobot_init = pygame.transform.scale(exrobot_init, (exrobot_init.get_width() / 8, exrobot_init.get_height() / 8))
exrobot_init_temp = pygame.transform.rotate(exrobot_init, -20)
exrobot_reg = exrobot_init.get_rect(center = (window.get_width() / 2 - 100, window.get_height() - exrobot_init.get_height() + 100 - 40))

kripton_init = pygame.image.load('./kripton.png')
kripton_init = pygame.transform.scale(kripton_init, (kripton_init.get_width() / 7, kripton_init.get_height() / 7))
kripton_init_temp = pygame.transform.rotate(kripton_init, -20)
kripton_reg = kripton_init.get_rect(center = (window.get_width() / 2 + 100, window.get_height() - kripton_init.get_height() + 100 - 40))

spook_init = pygame.image.load('./spook.png')
spook_init = pygame.transform.scale(spook_init, (spook_init.get_width() / 7, spook_init.get_height() / 7))
spook_init_temp = pygame.transform.rotate(spook_init, -20)
spook_reg = spook_init.get_rect(center = (window.get_width() / 2 + 350, window.get_height() - spook_init.get_height() + 100 - 40))

squid_init = pygame.image.load('./squid.png')
squid_init = pygame.transform.scale(squid_init, (squid_init.get_width() / 7, squid_init.get_height() / 7))
squid_init_temp = pygame.transform.rotate(squid_init, -20)
squid_reg = squid_init.get_rect(center = (window.get_width() / 2 + 600, window.get_height() - squid_init.get_height() + 50 - 40))

rotate_angle = [10, 8, 6, 2, -2, -6, -8, -10]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    x_random = random.random() * 1440
    window.fill((0, 0, 0))

    if current_time() - icon_tick > 400:
        icon_tick = current_time()
        np.random.shuffle(rotate_angle)
        zikina_init_temp = pygame.transform.rotate(zikina_init, rotate_angle[0])
        np.random.shuffle(rotate_angle)
        pavito_init_temp = pygame.transform.rotate(pavito_init, rotate_angle[0])
        np.random.shuffle(rotate_angle)
        sunface_init_temp = pygame.transform.rotate(sunface_init, rotate_angle[0])
        np.random.shuffle(rotate_angle)
        exrobot_init_temp = pygame.transform.rotate(exrobot_init, rotate_angle[0])
        np.random.shuffle(rotate_angle)
        kripton_init_temp = pygame.transform.rotate(kripton_init, rotate_angle[0])
        np.random.shuffle(rotate_angle)
        spook_init_temp = pygame.transform.rotate(spook_init, rotate_angle[0])
        np.random.shuffle(rotate_angle)
        squid_init_temp = pygame.transform.rotate(squid_init, rotate_angle[0])

    window.blit(zikina_init_temp, zikina_reg)
    window.blit(pavito_init_temp, pavito_reg)
    window.blit(sunface_init_temp, sunface_reg)
    window.blit(exrobot_init_temp, exrobot_reg)
    window.blit(kripton_init_temp, kripton_reg)
    window.blit(spook_init_temp, spook_reg)
    window.blit(squid_init_temp, squid_reg)

    if current_time() - logo_tick > 2000:
        if temp > 1.0:
            logiscool_img = pygame.transform.scale(logiscool_img_init, (img_width / temp / 4, img_height / temp / 4))
            logiscool_reg = logiscool_img.get_rect(center = (window.get_width() / 2, window.get_height() - logiscool_img.get_height() - 300 - counter *  4.5))
            temp -= 0.1
            counter += 1
            newyear_tick = current_time()
            step_newyear_tick = current_time()
        else:
            if current_time() - newyear_tick > 1000:
                if step_newyear_counter < 3:
                    if current_time() - step_newyear_tick > 500:
                        step_newyear_tick = current_time()
                        step_newyear_counter += 1
                        show_year_tick = current_time()
                if step_newyear_counter == 1:
                    window.blit(newyear_letter1, newyear_rect1)
                elif step_newyear_counter == 2:
                    window.blit(newyear_letter1, newyear_rect1)
                    window.blit(newyear_letter2, newyear_rect2)
                elif step_newyear_counter > 2:
                    window.blit(newyear_letter1, newyear_rect1)
                    window.blit(newyear_letter2, newyear_rect2)
                    window.blit(newyear_letter3, newyear_rect3)

                    # 2024
                    np.random.shuffle(full_array)
                    if current_time() - step_year_tick > 500:
                        step_year_tick = current_time()
                        # np.random.shuffle(full_array)
                        year_letter1 = font2.render('2', True, color_list[full_array[0]])
                        year_letter2 = font2.render('0', True, color_list[full_array[1]])
                        year_letter3 = font2.render('2', True, color_list[full_array[2]])
                        year_letter4 = font2.render('4', True, color_list[full_array[3]])
                    if current_time() - show_year_tick > 500:
                        window.blit(year_letter1, year_rect1)
                        window.blit(year_letter2, year_rect2)
                        window.blit(year_letter3, year_rect3)
                        window.blit(year_letter4, year_rect4)

        window.blit(logiscool_img, logiscool_reg)

    if current_time() - time_tick > 100:
        time_tick = current_time()
        mouse_pos = (x_random, 850)
        rgb = hs_to_rgb(random.random(), 0.5, 400)
        shoot_speed = random.uniform(min_shoot_speed, max_shoot_speed)
        size = random.uniform(min_firework_size, max_firework_size)
        lifetimeleft = random.uniform(min_firework_lifetimeleft, max_firework_lifetimeleft)
        particles.append([mouse_pos[0], mouse_pos[1], shooting_angle_cos_sin[0] * shoot_speed, shooting_angle_cos_sin[1] * shoot_speed, size, rgb, random.uniform(min_mass, max_mass), 0, lifetimeleft])

    for particle in particles:
        overexposure_value = particle[5][0] - 255 if particle[5][0] > 255 else 0 + \
                             particle[5][1] - 255 if particle[5][1] > 255 else 0 + \
                             particle[5][2] - 255 if particle[5][2] > 255 else 0

        rgb = (particle[5][0] + overexposure_value, particle[5][1] + overexposure_value, particle[5][2] + overexposure_value)
        rgb = (255 if rgb[0] > 255 else rgb[0], \
               255 if rgb[1] > 255 else rgb[1], \
               255 if rgb[2] > 255 else rgb[2])

        pygame.draw.circle(window, rgb, (particle[0], particle[1]), particle[4])

        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[3] += gravitational_acceleration * particle[6]
        particle[4] -= size_change
        particle[5] = (particle[5][0] * color_fade_rate, particle[5][1] * color_fade_rate, particle[5][2] * color_fade_rate)
        particle[8] -= 1

        if particle[4] <= 0:
            particles.remove(particle)
        elif particle[5][0] < 1 and particle[5][1] < 1 and particle[5][2] < 1:
            particles.remove(particle)
        elif particle[7] == 0 and particle[8] <= 0:
            particles_count = random.randint(min_child_particles, max_child_particles)
            rgb = hs_to_rgb(random.random(), 0.8, 600)

            for i in range(particles_count):
                angle = random.uniform(0, pi2)
                speed = random.uniform(min_child_shoot_speed, max_child_shoot_speed)
                vx = cos(angle) * speed + particle[2]
                vy = sin(angle) * speed + particle[3]
                particles.append([particle[0], particle[1], vx, vy, 5, rgb, random.uniform(min_mass, max_mass), 1, 100])

            particles.remove(particle)

    pygame.display.update()
    clock.tick(fps)
