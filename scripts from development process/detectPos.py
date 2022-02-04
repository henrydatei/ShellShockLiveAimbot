import cv2
import numpy as np
from sklearn.cluster import KMeans

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
        xgroups = cluster(zeros[0], maxX)
        ygroups = cluster(zeros[1], maxY)
        X = []
        for i in range(len(zeros[0])):
            X.append((zeros[0][i], zeros[1][i]))
        model = KMeans(n_clusters = max(len(xgroups), len(ygroups)))
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
    x, y = findPos("player.png", "screen2.png", maxX = 33, maxY = 16, threshold = 0.1, oneResult = True)
    x = x + 16 # 16
    y = y - 100 # 100
    return((x,y))

def findEnemys():
    liste = []
    res = findPos("enemy.png", "screen2.png")
    for pos in res:
        liste.append((pos[1], pos[0]))
    return liste

print(findPlayer())
print(findEnemys())