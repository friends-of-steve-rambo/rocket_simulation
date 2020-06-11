import math

G = 6.67408 * 10**(-11)


def acceleration(Mp, x_p, y_p, x_r, y_r, r):
    try:
        ax = G * Mp * (x_p - x_r) / (r ** 3)
        ay = G * Mp * (y_p - y_r) / (r ** 3)
    except ArithmeticError:
        ax, ay = 0.0, 0.0
    return ax, ay


def a_engines(angle,
              mass, u, m_t, eff):
    F = u * m_t * eff
    try:
        ax = F / mass * math.cos(math.radians(angle))
        ay = -F / mass * math.sin(math.radians(angle))
    except ArithmeticError:
        ax, ay = 0.0, 0.0
    return ax, ay


def speed(dt, vx, vy, ax, ay, axe, aye):
    vx += dt * (ax + axe)
    vy += dt * (ay + aye)
    return vx, vy


def speed1(mp, r):
    v = math.sqrt(G*mp/r)
    return v
