import math

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

traj = calcTrajectory(1795, 884, 89, 49, 64)
print(checkHit(1600, 400, traj))