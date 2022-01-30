import cv2
import matplotlib.pyplot as plt
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

method = cv2.TM_SQDIFF_NORMED

# Read the images from the file
small_image = cv2.imread('enemy.png')
large_image = cv2.imread('screen.png')

result = cv2.matchTemplate(small_image, large_image, method)
with np.nditer(result, op_flags = ["readwrite"]) as it:
    for x in it:
        if x[...] < 0.25:
            x[...] = 0
        else:
            x[...] = 1
zeros = np.where(result == 0)
xgroups = cluster(zeros[0], 40)
ygroups = cluster(zeros[1], 25)
X = []
for i in range(len(zeros[0])):
    X.append((zeros[0][i], zeros[1][i]))
model = KMeans(n_clusters = max(len(xgroups), len(ygroups)))
model.fit(X)
print(model.cluster_centers_)

plt.imshow(result, cmap='hot', interpolation='nearest')
plt.show()

# We want the minimum squared difference
mn,_,mnLoc,_ = cv2.minMaxLoc(result)

# Draw the rectangle:
# Extract the coordinates of our best match
MPx,MPy = mnLoc

# Step 2: Get the size of the template. This is the same size as the match.
trows,tcols = small_image.shape[:2]

# Step 3: Draw the rectangle on large_image
cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

# Display the original image with the rectangle around the match.
cv2.imshow('output',large_image)

# The image is only displayed if we call this
cv2.waitKey(0)