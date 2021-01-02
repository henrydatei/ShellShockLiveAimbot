import math
from pynput.mouse import Listener as MouseListener
from pynput import keyboard
from pynput.keyboard import Key, Controller
import time

keys = Controller()

def calcVelocity(distancex,distancey,angle):
    # from https://steamcommunity.com/sharedfiles/filedetails/?id=1327582953
    g = -379.106
    q = 0.0518718
    v0 = -2/(g * q) * math.sqrt((-g * distancex * distancex)/(2 * math.cos(math.radians(angle)) * math.cos(math.radians(angle)) * (math.tan(math.radians(angle)) * distancex - distancey)))
    return v0

def calcOptimal(diffx,diffy):
    smallestVelocity = 100
    bestAngle = 0
    for possibleAngle in range(1,90):
        try:
            v0 = calcVelocity(diffx,diffy,possibleAngle)
            if v0 < smallestVelocity:
                smallestVelocity = v0
                bestAngle = possibleAngle
        except Exception as e:
            pass

    print("Velocity = " + str(smallestVelocity))
    print("Angle = " + str(bestAngle))

def calcHighestBelow100(diffx,diffy):
    for possibleAngle in range(1,90):
        v0 = calcVelocity2(diffx,diffy,90-possibleAngle)
        if v0 < 100:
            break

    print("Velocity = " + str(v0))
    print("Angle = " + str(90-possibleAngle))

def cleanGlobals():
    del globals()['YourX']
    del globals()['YourY']
    del globals()['EnemyX']
    del globals()['EnemyY']

def setPowerAndAngle(targetPower,targetAngle,startPower,startAngle,direction):
    diffPower = targetPower - startPower
    if direction == "left":
        diffAngle = targetAngle - startAngle
    else:
        diffAngle = -targetAngle + startAngle
    time.sleep(1)
    if diffPower > 0:
        for i in range(0,diffPower):
            # press arrow up
            keys.tap(Key.up)
            time.sleep(0.1)
    else:
        for i in range(0,-diffPower):
            # press arrow down
            keys.tap(Key.down)
            time.sleep(0.1)
    if diffAngle > 0:
        for i in range(0,diffAngle):
            # press arrow right
            keys.tap(Key.right)
            time.sleep(0.1)
    else:
        for i in range(0,-diffAngle):
            # press arrow left
            keys.tap(Key.left)
            time.sleep(0.1)

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
        print(str(diffx))
        print(str(diffy))
        calcOptimal(diffx,diffy)
        calcHighestBelow100(diffx,diffy)
        cleanGlobals()

def EnemyLocation():
    print('Click enemy Tank')
    mouse_listener = MouseListener(on_click=posEnemy)
    mouse_listener.start()
    mouse_listener.join()
    if 'YourX' in globals() and 'YourY' in globals():
        # all needed, calc shot
        diffx = abs(YourX-EnemyX)
        diffy = -EnemyY+YourY
        print(str(diffx))
        print(str(diffy))
        calcOptimal(diffx,diffy)
        calcHighestBelow100(diffx,diffy)
        cleanGlobals()

with keyboard.GlobalHotKeys({'<ctrl>+<alt>+P': PlayerLocation,'<ctrl>+<alt>+E': EnemyLocation}) as h:
    h.join()
