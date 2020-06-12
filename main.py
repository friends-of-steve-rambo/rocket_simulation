#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from settings import *
from objects import *
from math import sqrt, atan2, degrees
import pygame
from pygame import *
from physics import *

done_all = False  # Флаг завершения main loop
zoom = 0.25  # Приближение камеры
planet_center = False  # Положение камеры
angle = 90  # Угол наклона ракеты
longitude = 90  # Угол относительно нормали к поверхности планеты
speed_vect = 90  # Угол относительно вектора скорости
landed = True  # Флаг совершенной посадки
sim_speed = 1  # Ускорение времени
FPS = 100
dt = sim_speed/FPS  # Интервал моделирования
lag = False  # Флаг на случай просадок фпс для компенсации расчета времени

def main():
    global zoom, planet_center, angle, longitude, speed_vect, FPS, dt, \
        landed, lag, sim_speed

    # Ставим пластинку с Боуи:
    pygame.mixer.init()
    pygame.mixer.music.load('sound/SpaceOddity.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    # Подключаем рёв двигателей
    eng_sound = pygame.mixer.Sound('sound/engine.wav')
    eng_sound.set_volume(0.1)

    # Запуск окна
    pygame.init()
    window = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption('ИТМО Rocket launcher')
    pygame.display.set_icon(pygame.image.load('img/rocket.png'))

    # Флаги остановки, паузы, управления
    done = False  # Флаг завершения игры
    debuginfo = True
    an_plus = an_minus = False  # флаги управления поворотом
    eng_on = False  # Двигатель вкл\выкл

    # Максимумы
    max_speed = max_dist = 0.0

    # Начальные условия для ракеты
    eff = 1.0  # Двигатели 100% мощности
    if orbit:
        vx = speed1(planet.mass, planet.radius+h)
        planet_center = True
        zoom = WIN_WIDTH / (planet.radius * 3)
    else:
        vx = 0.0
        planet_center = False
        zoom = 0.25
    vy = 0.0

    # Инициализация "часов"
    lag = False
    lag_delay = 0.0
    timer = pygame.time.Clock()
    seconds2 = 0.0
    fly_time = 0.0
    pygame.time.set_timer(USEREVENT + 1, 1000) # Событие 1 - обовление телеметрии

    while not done:
        timer.tick(FPS)  # ограничитель FPS, расчет реального FPS и
        real_fps = round(timer.get_fps(), 3)
        if real_fps < 5:
            lag = True
            lag_delay = round((pygame.time.get_ticks()/1000 - seconds2), 4)
        else:
            lag = False
            dt = sim_speed/real_fps
            seconds2 += round(dt, 4)


        # Обработка нажатия клавиш и событий
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
                exit()
            if e.type == USEREVENT + 1:  # Вывод отладки по счётчику
                debuginfo = True
            if e.type == USEREVENT + 2:  # Счётчик времени с момента взлёта
                fly_time += 0.1
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    rocket.fuelMass = fuel_mass
                if e.key == pygame.K_2:
                    zoom += 0.000005
                    print(zoom)
                if e.key == pygame.K_3:
                    if zoom > 0.000005:
                        zoom -= 0.000005
                if e.key == pygame.K_KP_PLUS:
                    if sim_speed >= 100:
                        sim_speed += 100
                    else:
                        sim_speed += 1 if sim_speed < 10 else 10
                    if sim_speed > 1000:
                        sim_speed = 1000
                if e.key == pygame.K_KP_MINUS:
                    if sim_speed > 100:
                        sim_speed -= 100
                    else:
                        sim_speed -= 1 if sim_speed <= 10 else 10
                    if sim_speed < 1:
                        sim_speed = 1
                if e.key == pygame.K_LCTRL:
                    if eff > 0:
                        eff -= 0.1
                    else:
                        eff = 0
                if e.key == pygame.K_LSHIFT:
                    if eff < 1:
                        eff += 0.1
                    else:
                        eff = 1
                if e.key == pygame.K_LEFT:
                    an_plus = True
                if e.key == pygame.K_RIGHT:
                    an_minus = True
                if e.key == pygame.K_UP:
                    eng_on = True
                if e.key == pygame.K_LALT:
                    planet_center = not planet_center
                    zoom = WIN_WIDTH / (planet.radius * 3) if planet_center else 0.25

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    an_plus = False
                if e.key == pygame.K_RIGHT:
                    an_minus = False
                if e.key == pygame.K_UP:
                    eng_on = False

        zoom = round(zoom, 6)
        eff = round(eff, 1)

        # Изменение от управленя
        if an_plus:
            angle += 0.5
            if angle > 360:
                angle = 0
        if an_minus:
            angle -= 0.5
            if angle < 0:
                angle = 360

        # Эффекты двигателя
        if eng_on and eff > 0:
            rocket.bitmap = pygame.image.load('img/rocket2.png')
            eng_sound.play()
        else:
            rocket.bitmap = pygame.image.load('img/rocket.png')
            eng_sound.stop()

        # Расчет движения
        rocket.updatemass(rocket.dryMass, rocket.fuelMass)
        r = sqrt((planet.x - rocket.x) ** 2 + (planet.y - rocket.y) ** 2)  # Дистанция до центра планеты
        distance = r - planet.radius  # Высота над поверхностью

        if distance <= 0 and not landed:  # Когда ракета касается поверхности - она села
            landed = True
            vx, vy = 0.0, 0.0
        if distance > 1 and landed:
            landed = False  # Когда ракета отрывается, она в полёте (O,RLY???)
            pygame.time.set_timer(USEREVENT + 2, int(100 / sim_speed))
        if landed:  # Если ракета на земле => сила тяжести уравновешивается с реакцией опоры
            ax, ay = 0.0, 0.0
            if eng_on and eff > 0 and rocket.fuelMass > 0:
                axe, aye = a_engines(angle, rocket.mass, rocket.u, rocket.m_t, eff)
                rocket.fuelMass -= rocket.m_t * dt * eff
            else:
                axe, aye = 0.0, 0.0
        else:
            ax, ay = acceleration(Mp, planet.x, planet.y, rocket.x, rocket.y, r)
            if eng_on and rocket.fuelMass > 0:
                axe, aye = a_engines(angle, rocket.mass, rocket.u, rocket.m_t, eff)
                rocket.fuelMass -= rocket.m_t * dt * eff
            else:
                axe, aye = 0.0, 0.0
        vx, vy = speed(dt, vx, vy, ax, ay, axe, aye)
        if r < planet.radius - 1:
            vx, vy = axe, aye
        rocket.x += vx*dt
        rocket.y += vy*dt
        if distance < 0 and not eng_on:
            rocket.x = planet.x + planet.radius * math.cos(math.radians(longitude))
            rocket.y = planet.y - planet.radius * math.sin(math.radians(longitude))

        longitude = 90 - degrees(atan2(rocket.x - planet.x, planet.y - rocket.y))
        if longitude < 0:
            longitude = 360 + longitude
        speed_vect = 90 - degrees(atan2(vx, -vy))
        if speed_vect < 0:
            speed_vect = 360 + speed_vect

        # показатели
        r_speed = sqrt(vx ** 2 + vy ** 2)
        vert_speed = math.cos(math.radians(abs(speed_vect-longitude))) * r_speed
        pks = speed1(planet.mass, r)
        # Угол наклона ракеты к горизонту и к скорости
        h_angle = 90-longitude+angle
        if h_angle > 180:
            h_angle = -360.0 + h_angle
        if h_angle < -180:
            h_angle = 360 + h_angle
        spd_angle = abs(angle-speed_vect)
        if spd_angle > 180:
            spd_angle = 360 - spd_angle

        max_speed = r_speed if r_speed > max_speed else max_speed
        max_dist = distance if distance > max_dist else max_dist

        # Отрисовка
        world.fill(Color(background_color))
        planet.render(zoom, planet_center, distance)
        rocket.render(angle, h_angle, zoom, planet_center, speed_vect)
        gui.render(int(seconds2), sim_speed, max_speed, max_dist, zoom)
        guid.render(distance, r_speed, vert_speed, eff, pks, h_angle, spd_angle)
        window.blit(world, (0, 0))
        display.update()


        # Изменение камеры от высоты:
        #if distance > 300 and not planet_center:
        #    planet_center = True
        #zoom = WIN_WIDTH / (planet.radius * 3) if planet_center else 0.25

        # Отладка
        if debuginfo:
            #print('[{:.2f}]: Зум {}, Ск-ть: {:.2f}({:.2f} {:.2f}),'
            #      'Угол: {}/{}, Двиг: {}({:.4f},{:.4f}), Дист: {:.2f}м, Посадка: {}'
            #      .format(seconds2, zoom, r_speed, ax, -ay,
            #              angle, longitude, eng_on, axe, aye, distance, landed))
            #print(rocket.mass, rocket.fuelMass)
            debuginfo = False

if __name__ == "__main__":
    while not done_all:
        main()
