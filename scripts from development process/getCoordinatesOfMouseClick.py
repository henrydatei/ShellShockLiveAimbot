from pynput.mouse import Listener as MouseListener

def posPlayer(x, y, button, pressed):
    if pressed:
        print("Your position: " + str(x) + ", " + str(y))
    return True

mouse_listener = MouseListener(on_click=posPlayer)
mouse_listener.start()
mouse_listener.join()
