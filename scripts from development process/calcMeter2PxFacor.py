from pynput.mouse import Listener as MouseListener
from pynput import keyboard

import math
import mpmath

g = 9.81

def calcMeters2px(d,g,alpha,v,y):
    x = (pow(d,2) * g * mpmath.csc(math.radians(alpha)) * mpmath.sec(math.radians(alpha)) - 2 * pow(v,2) * y * mpmath.cot(math.radians(alpha)))/(2 * d * pow(v,2))
    return x

def cleanGlobals():
    #del globals()['YourX']
    #del globals()['YourY']
    del globals()['EnemyX']
    del globals()['EnemyY']

def posPlayer(x, y, button, pressed):
    if pressed:
        print("Your position: " + str(x) + ", " + str(y))
        global YourX
        YourX = x
        global YourY
        YourY = y
    return False

def posEnemy(x, y, button, pressed):
    if pressed:
        print("Enemy position: " + str(x) + ", " + str(y))
        global EnemyX
        EnemyX = x
        global EnemyY
        EnemyY = y
    return False

def PlayerLocation():
    print('Click your Tank')
    mouse_listener = MouseListener(on_click=posPlayer)
    mouse_listener.start()
    mouse_listener.join()

def EnemyLocation():
    print('Click enemy Tank')
    mouse_listener = MouseListener(on_click=posEnemy)
    mouse_listener.start()
    mouse_listener.join()
    YourX = 542
    YourY = 382
    diffx = abs(YourX-EnemyX)
    diffy = EnemyY-YourY
    #velocity = 50
    #alpha = 45
    #velocity = 85
    #alpha = 70
    velocity = 50
    alpha = 70
    print(str(diffy) + " | " + str(calcMeters2px(diffx,g,alpha,velocity,diffy)))
    cleanGlobals()

with keyboard.GlobalHotKeys({'<ctrl>+<alt>+P': PlayerLocation,'<ctrl>+<alt>+E': EnemyLocation}) as h:
    h.join()
