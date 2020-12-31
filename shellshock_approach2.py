import math
from pynput.mouse import Listener as MouseListener
from pynput import keyboard

#velocity = 65 # m/s
#angle = 50 # deg
g = 5.5 # fern
#g = 3.3 # nah
#g = 3.8 # von Clemens
#g = 4.3 # mittel
#startHeight = 91.6 # px

def calcVelocity(distancex,distancey,angle):
    v0 = math.sqrt((pow(distancex,2) * g)/(distancex * math.sin(2*math.radians(angle)) - 2 * distancey * pow(math.cos(math.radians(angle)),2)))
    return v0 # px/s

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
        v0 = calcVelocity(diffx,diffy,90-possibleAngle)
        if v0 < 100:
            break

    print("Velocity = " + str(v0))
    print("Angle = " + str(90-possibleAngle))

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
        diffy = EnemyY-YourY
        print(str(diffx))
        print(str(diffy))
        calcOptimal(diffx,diffy)
        calcHighestBelow100(diffx,diffy)
        cleanGlobals()

with keyboard.GlobalHotKeys({'<ctrl>+<alt>+P': PlayerLocation,'<ctrl>+<alt>+E': EnemyLocation}) as h:
    h.join()
