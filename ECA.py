import numpy as np
import matplotlib.pyplot as plt
import easygui
plt.rcParams["image.cmap"] = "binary"

cellNum = 300
steps = 150

initial = np.zeros(cellNum)
initial[cellNum // 2] = 1

var = easygui.enterbox("Enter a number between 0 and 255")

ruleNumber = int(var)
if ruleNumber < 0:
    ruleNumber = 0
if ruleNumber > 255:
    ruleNumber = 255

def ruleIndex(triplet):
    L, C, R = triplet
    index = 7 - (4 * L + 2 * C + R)
    return int(index)

def generate(cells, n, ruleNum):
    ruleString = np.binary_repr(ruleNum, 8)
    rule = np.array([int(bit) for bit in ruleString])

    cellNum = len(cells)
    gen = np.zeros((n, cellNum))
    gen[0, :] = cells
    for i in range(1, n):
        allTriplets = np.stack([np.roll(gen[i - 1, :], 1), gen[i - 1, :], np.roll(gen[i - 1, :], -1)])
        gen[i, :] = rule[np.apply_along_axis(ruleIndex, 0, allTriplets)]
    return(gen)

data = generate(initial, steps, ruleNumber)

fig, ax = plt.subplots(figsize=(10, 5))
ax.matshow(data)
ax.axis(False)
plt.show()