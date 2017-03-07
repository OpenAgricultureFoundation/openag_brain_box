import pygame
from pygame.locals import*
import time, json
import memcache
shared = memcache.Client(['127.0.0.1:11211'], debug=0)


img = pygame.image.load('/home/pi/openag_brain_box/img.bmp')

screen = pygame.display.set_mode((800, 480),pygame.NOFRAME)
pygame.mouse.set_visible(False)

img = pygame.transform.scale(img, (480, 480))

pygame.init()
myfont = pygame.font.SysFont("monospace", 20)

x = 0
y = 0
toggle = False
img_file = '/home/pi/openag_brain_box/img.bmp'
running = True
start_time = time.time()

ph = '6.5'
ec = '3.2'
water_temp = '20.1'
air_temp = '21.1'
humidity = '38'
co2 = '410'
o2 = '17.1'

while running:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            if 320<x<800:
                if toggle:
                    img_file = '/home/pi/openag_brain_box/canny.bmp'
                    toggle = False
                else:
                    img_file = '/home/pi/openag_brain_box/img.bmp'
                    toggle = True
                img = pygame.image.load(img_file)
                img = pygame.transform.scale(img, (480, 480))

    screen.fill((0,0,0))

    if time.time() - start_time > 10:   # update images
        img = pygame.image.load(img_file)
        img = pygame.transform.scale(img, (480, 480))
	start_time = time.time()

    val = shared.get('ph')
    if val is not None:
        ph=val

    val = shared.get('ec')
    if val is not None:
        ec=val

    val = shared.get('water_temp')
    if val is not None:
        water_temp=val

    val = shared.get('air_temp')
    if val is not None:
        air_temp=val

    val = shared.get('humidity')
    if val is not None:
        humidity=val

    val = shared.get('co2')
    if val is not None:
        co2=val

    val = shared.get('o2')
    if val is not None:
        o2=val

    air_temp_string = "air temp: " + air_temp + " C"
    air_temp_label = myfont.render(air_temp_string, 1, (255, 255, 255))

    humidity_string = "humidity: " + humidity + " %"
    humidity_label = myfont.render(humidity_string, 1, (255, 255, 255))

    co2_string = "co2: " + co2 + " ppm"
    co2_label = myfont.render(co2_string, 1, (255, 255, 255))

    o2_string = "o2: " + o2 + " %"
    o2_label = myfont.render(o2_string, 1, (255, 255, 255))

    water_temp_string = "water temp: " + water_temp + " C"
    water_temp_label = myfont.render(water_temp_string, 1, (255, 255, 255))

    ph_string = "pH: " + ph + " ph"
    ph_label = myfont.render(ph_string, 1, (255, 255, 255))

    ec_string = "ec: " + ec + " ms/cm"
    ec_label = myfont.render(ec_string, 1, (255, 255, 255))

    screen.blit(img,(320, 0))
    screen.blit(air_temp_label, (50, 50))
    screen.blit(humidity_label, (50, 100))
    screen.blit(co2_label, (50, 150))
    screen.blit(o2_label, (50, 200))
    screen.blit(water_temp_label, (50, 250))
    screen.blit(ph_label, (50, 300))
    screen.blit(ec_label, (50, 350))

    pygame.display.flip()


pygame.quit ()
