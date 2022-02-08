import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pyscreenshot as ImageGrab
from pynput.mouse import Listener as MouseListener

def calcVelocity(distancex,distancey,angle):
    # from https://steamcommunity.com/sharedfiles/filedetails/?id=1327582953
    g = -379.106
    q = 0.0518718
    v0 = -2/(g * q) * math.sqrt((-g * distancex * distancex)/(2 * math.cos(math.radians(angle)) * math.cos(math.radians(angle)) * (math.tan(math.radians(angle)) * distancex - distancey)))
    return v0

def calcTrajectory(x, y, angle, power, wind, timestep = 0.1, maxTime = 10):
    g = 379.106
    q = 0.0518718
    a = 0.4757

    v = (-g*q)/2 * power
    v_x = v * math.cos(math.radians(angle))
    v_y = v * math.sin(math.radians(angle))

    trajectory = []

    for time in range(int(maxTime / timestep)):
        w = wind * a
        deltaX = v_x * timestep + w/2 * timestep * timestep
        deltaY = v_y * timestep + g/2 * timestep * timestep
        deltaVX = w * timestep
        deltaVY = g * timestep
        trajectory.append((x,1080-y))
        x = x + deltaX
        y = y + deltaY
        v_x = v_x + deltaVX
        v_y = v_y + deltaVY
        if 1080-y < 0 or x < -200 or x > 2200:
            break

    return trajectory

# https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
def distancePointFromLine(x, y, p1x, p1y, p2x, p2y):
    return (abs((p2x - p1x) * (p1y - y) - (p1x - x) * (p2y - p1y)))/(math.sqrt((p2x - p1x)**2 + (p2y - p1y)**2))

def checkHit(x, y, trajectory, maxDistance = 10):
    for index in range(len(trajectory) - 1):
        d = distancePointFromLine(x, y, trajectory[index][0], trajectory[index][1], trajectory[index + 1][0], trajectory[index + 1][1])
        if d <= maxDistance:
            return True
    return False

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

    print("Smallest Velocity")
    print("Velocity = " + str(smallestVelocity))
    print("Angle = " + str(bestAngle))
    return smallestVelocity, bestAngle

# https://stackoverflow.com/questions/14783947/grouping-clustering-numbers-in-python
def cluster(data, maxgap):
    '''Arrange data into groups where successive elements
       differ by no more than *maxgap*

        >>> cluster([1, 6, 9, 100, 102, 105, 109, 134, 139], maxgap=10)
        [[1, 6, 9], [100, 102, 105, 109], [134, 139]]

        >>> cluster([1, 6, 9, 99, 100, 102, 105, 134, 139, 141], maxgap=10)
        [[1, 6, 9], [99, 100, 102, 105], [134, 139, 141]]

    '''
    data.sort()
    groups = [[data[0]]]
    for x in data[1:]:
        if abs(x - groups[-1][-1]) <= maxgap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups

def findPos(needlepic, haystackpic, maxX = 40, maxY = 40, threshold = 0.25, oneResult = False):
    small_image = cv2.imread(needlepic)
    large_image = cv2.imread(haystackpic)

    result = cv2.matchTemplate(small_image, large_image, cv2.TM_SQDIFF_NORMED)
    if not oneResult:
        with np.nditer(result, op_flags = ["readwrite"]) as it:
            for x in it:
                if x[...] < threshold:
                    x[...] = 0
                else:
                    x[...] = 1
        zeros = np.where(result == 0)
        xgroups = cluster(zeros[1], maxX)
        ygroups = cluster(zeros[0], maxY)
        X = []
        for i in range(len(zeros[0])):
            X.append((zeros[1][i], zeros[0][i]))
        #print(X)
        model = KMeans(n_clusters = max(len(xgroups), len(ygroups))) # something here returns wrong results
        model.fit(X)
        #print(model.cluster_centers_)

        #plt.imshow(result, cmap='hot', interpolation='nearest')
        #plt.show()
        return model.cluster_centers_
    else:
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)
        MPx, MPy = mnLoc
        return mnLoc

def findPlayer():
    x, y = findPos("pics/player.png", "pics/screen.png", maxX = 33, maxY = 16, threshold = 0.1, oneResult = True)
    x = x + 20
    y = 1080 - y - 15
    print("Found player at: " + str(x) + ", " + str(y))
    return((x,y))

def findEnemies():
    # liste = []
    # res = findPos("pics/enemy.png", "pics/screen.png")
    # for pos in res:
    #     x = int(pos[1])
    #     y = int(1080 - pos[0])
    #     liste.append((x, y))
    #     print("Found enemy at: " + str(x) + ", " + str(y))
    # return liste
    x, y = findPos("pics/enemy.png", "pics/screen.png", oneResult = True)
    x = x + 20
    y = 1080 - y - 15
    print("Found enemy at: " + str(x) + ", " + str(y))
    return((x,y))

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
    mouse_listener = MouseListener(on_click = posPlayer)
    mouse_listener.start()
    mouse_listener.join()

def EnemyLocation():
    mouse_listener = MouseListener(on_click = posEnemy)
    mouse_listener.start()
    mouse_listener.join()

def calcOptimalWithWind(player, enemy, wind):
    noWindPower, noWindAngle = calcOptimal(abs(player[0] - enemy[0]), player[1] - enemy[1])
    for change in range(10):
        for angle in range(math.floor(noWindAngle - change), math.ceil(noWindAngle + change + 1)):
            for power in range(math.floor(noWindPower - change), math.ceil(noWindPower + change + 1)):
                trajectory = calcTrajectory(player[0], player[1], angle, power, wind)
                if checkHit(enemy[0], enemy[1], trajectory):
                    print("Angle: " + str(angle))
                    print("Power: " + str(power))
                    return angle, power
    print("Simulation for shot will never hit exactly!")

im = ImageGrab.grab(bbox = (0,0,1920,930))
im.save('pics/screen.png')

try:
    player = findPlayer()
except:
    print("Could not find player, please click on it")
    PlayerLocation()
    global YourX
    global YourY
    player = (YourX, YourY)
try:
    enemy = findEnemies()
except:
    print("Could not find enemy, please click on it")
    EnemyLocation()
    global EnemyX
    global EnemyY
    enemy = (EnemyX, EnemyY)

image = cv2.circle(cv2.imread('pics/screen.png'), (player[0], 1080-player[1]), 5, (0,0,255), -1)
image = cv2.circle(image, (enemy[0], 1080-enemy[1]), 5, (0,0,255), -1)
cv2.imshow("test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
calcOptimalWithWind(player, enemy, 0)


