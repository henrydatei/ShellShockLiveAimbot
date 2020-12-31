import math
from pynput.mouse import Listener as MouseListener
from pynput import keyboard

#velocity = 65 # m/s
#angle = 50 # deg
g = 9.81 # m/s
#startHeight = 91.6 # px

#meter2pxNear = 2.150963092
#meter2pxFar = 2.523199299
#meter2pxMid = 2.3

def calcDistance(meter2px):
    d = (velocity * math.cos(math.radians(angle)))/g * (velocity * meter2px * math.sin(math.radians(angle)) + math.sqrt(pow(velocity * meter2px * math.sin(math.radians(angle)),2) + 2 * g * meter2px * startHeight))
    return d # px

def calcVelocity(distancex,distancey,angle,meter2px):
    v0 = math.sqrt((pow(distancex,2) * g * meter2px)/(distancex * math.sin(2*math.radians(angle)) - 2 * distancey * pow(math.cos(math.radians(angle)),2)))
    return v0 # px/s

def calcOptimal(diffx,diffy,meter2px):
    print("calc optimal")
    smallestVelocity = 100
    bestAngle = 0
    for possibleAngle in range(0,90):
        v0 = calcVelocity(diffx,diffy,possibleAngle,meter2px)/meter2px
        if v0 < smallestVelocity:
            smallestVelocity = v0
            bestAngle = possibleAngle

    print("Velocity = " + str(smallestVelocity))
    print("Angle = " + str(bestAngle))

def cleanGlobals():
    del globals()['YourX']
    del globals()['YourY']
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
    if 'EnemyX' in globals() and 'EnemyY' in globals():
        # all needed, calc shot
        diffx = abs(YourX-EnemyX)
        diffy = EnemyY-YourY
        meter2px = 2.4246368 + 0.0014513 * diffy
        print(str(diffx))
        print(str(diffy))
        print(str(meter2px))
        calcOptimal(diffx,diffy,meter2px)
        cleanGlobals()

def EnemyLocation():
    print('Click enemy Tank')
    mouse_listener = MouseListener(on_click=posEnemy)
    mouse_listener.start()
    mouse_listener.join()
    if 'YourX' in globals() and 'YourY' in globals():
        # all needed, calc shot
        diffx = abs(YourX-EnemyX)
        diffy = EnemyY-YourY
        meter2px = 2.4246368 + 0.0014513 * diffy
        print(str(diffx))
        print(str(diffy))
        print(str(meter2px))
        calcOptimal(diffx,diffy,meter2px)
        cleanGlobals()

with keyboard.GlobalHotKeys({'<ctrl>+<alt>+P': PlayerLocation,'<ctrl>+<alt>+E': EnemyLocation}) as h:
    h.join()
