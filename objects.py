import pygame
from menu import menu
from math import cos, sin, radians
from pygame import *
from settings import DISPLAY, background_color, WIN_WIDTH, WIN_HEIGHT
from main import zoom, planet_center, angle, longitude, speed_vect, speed1


# Инициализация фона-космоса
world = pygame.Surface(DISPLAY)
world.fill(Color(background_color))

pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15)
tcolor = (255, 255, 255)
r_planet, Mp, dry_mass, fuel_mass, u, m_t, orbit = menu()
h = 100000 if orbit else 0


class GUI:
    def __init__(self, color):
        self.h = 30
        self.color = Color(color)
        self.topx = 0
        self.topy = WIN_HEIGHT-30

    def render(self, sec, simspd, max_spd, max_dst, zoom):
        draw.rect(world, self.color, (self.topx, self.topy, WIN_WIDTH, self.h))
        # Время и ускорение симуляции
        h = sec // 3600
        m = (sec // 60) % 60
        s = sec % 60
        time = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
        timetext = myfont.render(time, 1, (255, 255, 255))
        world.blit(timetext, (self.topx, self.topy))
        boosttext = myfont.render("Cкорость x" + str(simspd), 1, tcolor)
        world.blit(boosttext, (self.topx, self.topy+15))
        masstext1 = myfont.render('Сухая масса: {}кг'.format(dry_mass), 1, tcolor)
        masstext2 = myfont.render('Масса топлива: {}кг'.format(int(rocket.fuelMass)), 1, tcolor)
        world.blit(masstext1, (150, self.topy))
        world.blit(masstext2, (150, self.topy+15))
        planettext1 = myfont.render('Радиус планеты: {}км'.format(int(planet.radius//3)), 1, tcolor)
        planettext2 = myfont.render('Масса планеты: {:.2f}*10^22 кг'.format(planet.mass/10**22), 1, tcolor)
        world.blit(planettext1, (380, self.topy))
        world.blit(planettext2, (380, self.topy+15))
        maxtext = myfont.render('Макс. удаление: {:.0f}км | Макс. скорость: {:.0f}м/c | Масштаб: {}м/пиксель'
                                .format(max_dst//(10**3), max_spd, int(1/zoom)), 1, tcolor)
        world.blit(maxtext, (0, self.topy-15))


class GUI_d:
    def __init__(self, color):
        self.h = 50
        self.color = Color(color)
        self.topx = 150
        self.topy = 0

    def render(self, dist, spd_orb, spd_vert, eng_eff, pks, h_angle, spd_angle):
        draw.rect(world, self.color, (self.topx, self.topy, WIN_WIDTH-300, self.h))
        # Время и ускорение симуляции
        dist_text = myfont.render("==Высота====Скорость====Верт. ск-ть==", 1, tcolor)
        distval = myfont.render('{: 8d}м{: 11.1f}м/c{:11.1f}м/c'
                                .format(int(dist), spd_orb, spd_vert), 1, tcolor)
        pkstext = myfont.render('ПКС: {:.2f} (на этой высоте)'.format(pks), 1, tcolor)
        world.blit(dist_text, (self.topx, self.topy))
        world.blit(distval, (self.topx, self.topy + 15))
        world.blit(pkstext, (self.topx, self.topy + 33))
        # Отображение топлива ракеты
        fuelper = int(rocket.fuelMass/fuel_mass*100)
        fuel_text = myfont.render('Топливо: {}%'.format(fuelper), 1, tcolor)
        world.blit(fuel_text, (0, 0))
        draw.rect(world, Color('DarkGreen'), (0, 15, 100, 20))
        draw.rect(world, Color('Green'), (0, 15, fuelper, 20))
        eng_text = myfont.render('Двигатели: {}%'.format(int(eng_eff*100)), 1, tcolor)
        world.blit(eng_text, (0, 40))
        # Углы наклона
        angtext1 = myfont.render('Угол наклона к', 1, tcolor)
        angtext2 = myfont.render('>горизонт: {:.1f}'.format(h_angle), 1, tcolor)
        angtext3 = myfont.render('>ск-ть: {:.1f}'.format(spd_angle), 1, tcolor)
        world.blit(angtext1, (495, 0))
        world.blit(angtext2, (495, 15))
        world.blit(angtext3, (495, 30))


class Rocket(sprite.Sprite):
    def __init__(self, xpos, ypos, dry_mass, fuel_mass, u, m_t, filename, size):
        self.x = xpos
        self.y = ypos
        self.dryMass = dry_mass
        self.fuelMass = fuel_mass
        self.u = u
        self.m_t = m_t
        self.mass = self.dryMass + self.fuelMass
        self.bitmap = pygame.image.load(filename)
        self.x_size = size[0]
        self.y_size = size[1]
        # self.bitmap.set_colorkey((0, 0, 0))

    def updatemass(self, dryMass, fuelMass):
        self.mass = dryMass + fuelMass

    def rot_center(self, an):
        an = an - 90
        # Функция разворота и скейла спрайта
        #rot_image = pygame.transform.rotate(self.bitmap, an)
        #orig_rect = rot_image.get_rect()
        #rot_rect = orig_rect.copy()
        #rot_rect.center = rot_image.get_rect().center
        #rot_image = rot_image.subsurface(rot_rect).copy()

        rot_image = pygame.transform.rotate(self.bitmap, an)
        return rot_image

    def render(self, an, h_angle,  zm, p_c, spd_vect):
        x_rend = (planet.x + (self.x - planet.x)*zm) - self.x_size // 2
        y_rend = (planet.y + (self.y - planet.y)*zm) - self.y_size // 2
        if p_c:
            #self.rect = self.rot_center(an)
            #world.blit(self.rect, (x_rend, y_rend))
            img = self.rot_center(an)
            img = pygame.transform.scale(img, (self.x_size, self.y_size))
            world.blit(img, (x_rend, y_rend))
            # Вектор скорости
            spd_x = cos(radians(spd_vect)) * 35
            spd_y = sin(radians(spd_vect)) * 35
            pygame.draw.line(world, Color('Green'), (x_rend + self.x_size // 2, y_rend + self.y_size // 2),
                             (x_rend + self.x_size // 2 + spd_x, y_rend + self.y_size // 2 - spd_y))
        else:
            self.rect = self.rot_center(h_angle)
            world.blit(self.rect,
                       (WIN_WIDTH//2 - self.x_size//2, WIN_HEIGHT//2 - self.y_size//2))


class Planet(sprite.Sprite):
    def __init__(self, xpos, ypos, color, radius, mass):
        self.x = xpos
        self.y = ypos
        self.color = color
        self.radius = radius
        self.size = 0
        self.mass = mass
        self.image = pygame.image.load('img/planet.png')
        self.image2 = pygame.image.load('img/planet2.png')

    def scrollX(self, offsetX):
        image2 = pygame.transform.scale(self.image2, (WIN_WIDTH, WIN_HEIGHT // 2))
        width, height = image2.get_size()
        copySurf = image2.copy()
        image2.blit(copySurf, (offsetX % width - width, 0))
        image2.blit(copySurf, (offsetX % width, 0))
        return image2

    def render(self, zm, p_c, dist, gorizontal_distance):
        x_rend = self.x + (self.x-rocket.x)*zm
        y_rend = self.y + (self.y - rocket.y)*zm
        self.size = int(self.radius*2*zm)
        if p_c:
            #draw.circle(world, self.color, (self.x, self.y), int(self.radius*zm)-5, 0)  # -5
            image = pygame.transform.scale(self.image, (self.size, self.size))
            world.blit(image, (self.x-self.size//2, self.y-self.size//2))
        else:
            #draw.rect(world, self.color, (0, WIN_HEIGHT//2 + dist, WIN_WIDTH, WIN_HEIGHT//2))
            image2 = self.scrollX(gorizontal_distance)
            world.blit(image2, (0, WIN_HEIGHT//2 + dist))

# Планета
x_planet = WIN_WIDTH // 2
y_planet = WIN_HEIGHT // 2
planet = Planet(x_planet, y_planet, Color('Dim Gray'), r_planet, Mp)

# Ракета
x = WIN_WIDTH // 2
y = WIN_HEIGHT // 2 - planet.radius - h
rocket = Rocket(x, y, dry_mass, fuel_mass, u, m_t, 'img/rocket.png', (40, 40))

# GUI
gui = GUI('Midnight Blue')
guid = GUI_d('Blue')
