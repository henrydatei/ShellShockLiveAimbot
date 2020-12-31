from pynput.mouse import Listener as MouseListener
from pynput import keyboard

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
        print(str(YourX))
        print(str(YourY))
        print(str(EnemyX))
        print(str(EnemyY))

def EnemyLocation():
    print('Click enemy Tank')
    mouse_listener = MouseListener(on_click=posEnemy)
    mouse_listener.start()
    mouse_listener.join()
    if 'YourX' in globals() and 'YourY' in globals():
        # all needed, calc shot
        print(str(YourX))
        print(str(YourY))
        print(str(EnemyX))
        print(str(EnemyY))

with keyboard.GlobalHotKeys({'<ctrl>+<alt>+P': PlayerLocation,'<ctrl>+<alt>+E': EnemyLocation}) as h:
    h.join()
