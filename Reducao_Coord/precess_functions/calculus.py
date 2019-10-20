import numpy as np

from numpy import cos, sin
from functions.converter import *

# Função que calcula a matriz p0
def calculateP0(alpha, delta):
    a = time2degrees(alpha)
    d = degreeReduction(delta)

    return np.array([
        [cos(radians(d)) * cos(radians(a))],
        [cos(radians(d)) * sin(radians(a))],
        [sin(radians(d))]
    ], dtype=np.float64)

# Função que calcula os valores de t e T
def calculateTimeVariables(jDay):
    t = jDay - 2451545.0
    T = (jDay - 2451545.0) / 36525.0
    
    return t, T

# Função que calcula os valores de eta, zeta e theta em radianos
def calculateAngles(T):
    powT = np.array([np.power(T, i) for i in range(1, 4)], dtype=np.float64)
    
    eCoef = np.array([2306.2181 / 3600,  0.30188 / 3600,  0.017998 / 3600], dtype=np.float64)
    zCoef = np.array([2306.2181 / 3600,  1.09468 / 3600,  0.018203 / 3600], dtype=np.float64)
    tCoef = np.array([2004.3109 / 3600, -0.42665 / 3600, -0.041833 / 3600], dtype=np.float64)

    eta   = np.dot(eCoef, powT)
    zeta  = np.dot(zCoef, powT)
    theta = np.dot(tCoef, powT)  

    return radians(eta), radians(zeta), radians(theta)

# Função que calcula a matriz de precessão P
def calculatePrecessionMatrix(eta, zeta, theta):
    p11 =  cos(zeta) * cos(theta) * cos(eta) - sin(zeta) * sin(eta)
    p12 = -cos(zeta) * cos(theta) * sin(eta) - sin(zeta) * cos(eta)
    p13 = -cos(zeta) * sin(theta)
    p21 =  sin(zeta) * cos(theta) * cos(eta) + cos(zeta) * sin(eta)
    p22 = -sin(zeta) * cos(theta) * sin(eta) + cos(zeta) * cos(eta)
    p23 = -sin(zeta) * sin(theta)
    p31 =              sin(theta) * cos(eta)
    p32 =             -sin(theta) * sin(eta)
    p33 =              cos(theta)

    return np.array([
        [p11, p12, p13],
        [p21, p22, p23],
        [p31, p32, p33]
    ], dtype=np.float64)

# Função que calcula a matriz de nutação N
def calculateNutationMatrix(t, T):
    powT = np.array([np.power(T, i) for i in range(4)], dtype=np.float64)

    c0 = degreeReduction(np.array([23, 26, 21.448], dtype=np.float64))
    c1 = -46.8150  / 3600
    c2 = -0.00059  / 3600
    c3 =  0.001813 / 3600
    coef = np.array([c0, c1, c2, c3], dtype=np.float64)

    e0 = radians(np.dot(coef, powT))

    C1 = radians(125.0 - 0.05295 * t)
    C2 = radians(200.9 + 1.97129 * t)

    deltaPsi = radians(-0.0048 * sin(C1) - 0.0004 * sin(C2))
    deltaE   = radians( 0.0026 * cos(C1) + 0.0002 * cos(C2))

    e = e0 + deltaE

    return np.array([
        [1, -deltaPsi * cos(e), -deltaPsi * sin(e)],
        [deltaPsi * cos(e), 1, -deltaE],
        [deltaPsi * sin(e), deltaE, 1]
    ], dtype=np.float64)

# Função que calcula os valores de delta Alpha e Delta
def calculateDeltas(alpha, delta, t, T):
    a = radians(time2degrees(alpha))
    d = radians(degreeReduction(delta))

    G   = radians(357.528 + 0.985600 * t)
    lmb = radians(280.460 + 0.985647 * t + 1.915 * sin(G) + 0.020 * sin(2 * G))

    deltaAlpha = (-20.5 / 3600 * sin(a) * sin(lmb) - \
                   18.8 / 3600 * cos(a) * cos(lmb)) / cos(d)

    deltaDelta = 20.5 / 3600 * cos(a) * sin(d) * sin(lmb) + \
                 18.8 / 3600 * sin(a) * sin(d) * cos(lmb) - 8.1 / 3600 * cos(d) * cos(lmb)

    return deltaAlpha, deltaDelta

# Função que realiza a redução de coordenadas, exibindo cada parte importante
def coordReduction(alpha, delta, date):
    p0 = calculateP0(alpha, delta)
    print('- Matriz p0:\n', p0, end='\n\n')
    
    jDay = julianDate(date[0], date[1], date[2])
    print('- Data Juliana:', jDay, end='\n\n')

    t, T = calculateTimeVariables(jDay)
    print('- (t, T):', (t, T), end='\n\n')

    eta, zeta, theta = calculateAngles(T)
    print('- (eta, zeta, theta) em radianos:', (eta, zeta, theta), end='\n\n')

    P = calculatePrecessionMatrix(eta, zeta, theta)
    print('- Matriz P:\n', P, end='\n\n')

    P_inv = P.T
    print('- Matriz P^-1:\n', P_inv, end='\n\n')

    p1 = P @ p0
    print('- Matriz p1:\n', p1, end='\n\n')

    N = calculateNutationMatrix(t, T)
    print('- Matriz N:\n', N, end='\n\n')

    p2 = N @ p1
    print('- Matriz p2:\n', p2, end='\n\n')

    dA, dD = calculateDeltas(alpha, delta, t, T)
    print('- (dAlpha, dDelta) em graus:', (dA, dD), end='\n\n')

    realDelta = np.arcsin(p2[2])
    realAlpha = np.arccos(p2[0] / np.cos(realDelta))

    realAlpha = (degrees(realAlpha[0]) + dA) / 15
    realDelta = degrees(realDelta[0]) + dD

    print('- (realAlpha, realDelta) em horas e graus:', (realAlpha, realDelta), end='\n\n')

    hours, minutes, seconds = reformat(realAlpha)
    print('- realAlpha: {0:.0f}h {1:.0f}m {2:.2f}s'.format(hours, minutes, seconds))

    d, minutes, seconds = reformat(realDelta)
    print('- realDelta: %.0fº %.0f´ %.2f´´' % (d, minutes, seconds))



