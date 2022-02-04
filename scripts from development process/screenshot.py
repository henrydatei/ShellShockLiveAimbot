import pyscreenshot as ImageGrab

# fullscreen
im=ImageGrab.grab(bbox = (0,150,1920,1080))
im.show()
im.save('screen2.png')