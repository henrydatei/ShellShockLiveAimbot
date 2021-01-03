import math
from pynput.mouse import Listener as MouseListener
from pynput import keyboard
#from pynput.keyboard import Key, Controller
#from pynput.mouse import Button, Controller
import pynput.keyboard as kb
import pynput.mouse as ms
import time

keys = kb.Controller()
mouse = ms.Controller()

def calcVelocity(distancex,distancey,angle):
    # from https://steamcommunity.com/sharedfiles/filedetails/?id=1327582953
    g = -379.106
    q = 0.0518718
    v0 = -2/(g * q) * math.sqrt((-g * distancex * distancex)/(2 * math.cos(math.radians(angle)) * math.cos(math.radians(angle)) * (math.tan(math.radians(angle)) * distancex - distancey)))
    return v0

def calcOptimal(diffx,diffy):
    smallestVelocity = 100
    bestAngle = 0
    global velocity
    global angle
    for possibleAngle in range(1,90):
        try:
            v0 = calcVelocity(diffx,diffy,possibleAngle)
            if v0 < smallestVelocity:
                smallestVelocity = v0
                bestAngle = possibleAngle
        except Exception as e:
            pass

    print("Smallest Velocity")
    print("Velocity = " + str(smallestVelocity))
    print("Angle = " + str(bestAngle))
    velocity = smallestVelocity
    angle = bestAngle

def calcHighestBelow100(diffx,diffy):
    global highVelocity
    global highAngle
    for possibleAngle in range(1,90):
        v0 = calcVelocity(diffx,diffy,90-possibleAngle)
        if v0 < 100:
            break

    print("Highest Angle with power below 100")
    print("Velocity = " + str(v0))
    print("Angle = " + str(90-possibleAngle))
    highVelocity = v0
    highAngle = 90-possibleAngle

def cleanGlobals():
    try:
        del globals()['YourX']
    except Exception as e:
        pass
    try:
        del globals()['YourY']
    except Exception as e:
        pass
    try:
        del globals()['EnemyX']
    except Exception as e:
        pass
    try:
        del globals()['EnemyY']
    except Exception as e:
        pass

def setPowerAndAngle(targetPower,targetAngle,startPower,startAngle,direction):
    diffPower = targetPower - startPower
    if direction == "left":
        diffAngle = targetAngle - startAngle
    else:
        diffAngle = -targetAngle + startAngle
    if diffPower > 0:
        for i in range(0,diffPower):
            # press arrow up
            keys.tap(kb.Key.up)
            time.sleep(0.1)
    else:
        for i in range(0,-diffPower):
            # press arrow down
            keys.tap(kb.Key.down)
            time.sleep(0.1)
    if diffAngle > 0:
        for i in range(0,diffAngle):
            # press arrow right
            keys.tap(kb.Key.right)
            time.sleep(0.1)
    else:
        for i in range(0,-diffAngle):
            # press arrow left
            keys.tap(kb.Key.left)
            time.sleep(0.1)

def setTo100_90(tankx,tanky):
    mouse.position = (tankx,tanky)
    time.sleep(0.1)
    mouse.press(ms.Button.left)
    time.sleep(0.1)
    mouse.move(0,-tanky)
    time.sleep(0.1)
    mouse.release(ms.Button.left)

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
    #cleanGlobals()
    print('Click your Tank')
    mouse_listener = MouseListener(on_click=posPlayer)
    mouse_listener.start()
    mouse_listener.join()
    if 'EnemyX' in globals() and 'EnemyY' in globals():
        # all needed, calc shot
        diffx = abs(YourX-EnemyX)
        diffy = -EnemyY+YourY
        calcOptimal(diffx,diffy)
        calcHighestBelow100(diffx,diffy)

def EnemyLocation():
    #cleanGlobals()
    print('Click enemy Tank')
    mouse_listener = MouseListener(on_click=posEnemy)
    mouse_listener.start()
    mouse_listener.join()
    if 'YourX' in globals() and 'YourY' in globals():
        # all needed, calc shot
        diffx = abs(YourX-EnemyX)
        diffy = -EnemyY+YourY
        calcOptimal(diffx,diffy)
        calcHighestBelow100(diffx,diffy)

def prepareShot():
    setTo100_90(YourX,YourY)
    if YourX < EnemyX:
        direction = "right"
    else:
        direction = "left"
    setPowerAndAngle(round(velocity),angle,100,90,direction)

def prepareHighShot():
    setTo100_90(YourX,YourY)
    if YourX < EnemyX:
        direction = "right"
    else:
        direction = "left"
    setPowerAndAngle(round(highVelocity),highAngle,100,90,direction)

with keyboard.GlobalHotKeys({'<ctrl>+<alt>+P': PlayerLocation, '<ctrl>+<alt>+E': EnemyLocation, '<ctrl>+<alt>+S': prepareShot, '<ctrl>+<alt>+H': prepareHighShot}) as h:
    h.join()
