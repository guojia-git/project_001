#! /usr/bin/python
import analysis_header as header
import sys
import math
import numpy as np
from sklearn.preprocessing import * 
from sklearn import cluster
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


fpath = "../data/analyses/user_analysis_030.csv"
SESSION_LEN = 20 # in minutes
NUM_BINS = 1440 / SESSION_LEN #int
BIN_UNIT = SESSION_LEN / 60.0 #float

# the SESSION_LEN bins
idle_cnts = [0 for i in range (NUM_BINS)]
testing_set = []

with open(fpath) as f:
  lines = f.readlines()
  line_cnt = 0
  line_thr = len(lines) * 3 / 4
  for line in lines:
    dat = line.split(',')
    line_cnt += 1
    if line_cnt < line_thr:
      time = float(dat[header.LAST_END])
      index = int(math.floor(time / BIN_UNIT))
      idle_cnts[index] += 1
    else:
      testing_set += [dat]

# construct training set
training_set = [[] for i in range(NUM_BINS)]
for t, dp in zip(range(NUM_BINS), training_set):
  t_ang = t / float(NUM_BINS) * 2 * math.pi
  t_x = math.cos(t_ang)
  t_y = math.sin(t_ang)
  dp += [t_x, t_y, idle_cnts[t]]
  

# test clustering
sc = cluster.SpectralClustering(n_clusters = 2)
#sc = cluster.KMeans(n_clusters = 2)
#sc = cluster.Ward(n_clusters = 2)
sc.fit(np.array(training_set))
if hasattr(sc, 'labels_'):
  y_pred = sc.labels_.astype(np.int)
else:
  y_pred = sc.predict(training_set)
#print(y_pred)

#y_pred = [0, 1, 0, 1, 0, 0, 0, 0]

# find the best 2 class clustering using DP
# [1, 1, 0, 1, 0, 0] -> [1, 1, 0, 0, 0, 0]
best_division = [0, 0, 0] # [end pos, len - 1, target cluster]
best_distance = 0
max_distance = len(y_pred)

# ** first check the case where 0 is in the middle **
target_cluster = 0 # the elements in the middle
# initialize the distance
init_distance = 0
for i in range (len(y_pred)):
  if y_pred[i] == 1 - target_cluster:
    init_distance += 1
# case where target cluster is only 1 element
# [1, 1, 0, 1, 1, 1]
distances_cur = []
for pos in range (len(y_pred)):
  if y_pred[pos] == target_cluster:
    distance = init_distance + 1
    distances_cur += [distance]
    if distance > best_distance:
      best_distance = distance
      best_division = [pos, 0, target_cluster]
  else:
    distance = init_distance - 1
    distances_cur += [distance]
distances_pre = distances_cur
# the rest of the cases
for length in range (1, len(y_pred)):
  distances_pre = distances_cur
  distances_cur = []
  for pos in range (length, len(y_pred)):
    distance = distances_pre[pos - length]
    distance = distance + 1 if y_pred[pos] == target_cluster else distance - 1
    distances_cur += [distance]
    if distance > best_distance:
      best_distance = distance
      best_division = [pos, length, target_cluster]

# **another way around**
target_cluster = 1 # the elements in the middle
# initialize the distance
init_distance = 0
for i in range (len(y_pred)):
  if y_pred[i] == 1 - target_cluster:
    init_distance += 1
# case where target cluster is only 1 element
# [1, 1, 0, 1, 1, 1]
distances_cur = []
for pos in range (len(y_pred)):
  if y_pred[pos] == target_cluster:
    distance = init_distance + 1
    distances_cur += [distance]
    if distance > best_distance:
      best_distance = distance
      best_division = [pos, 0, target_cluster]
  else:
    distance = init_distance - 1
    distances_cur += [distance]
distances_pre = distances_cur
# the rest of the cases
for length in range (1, len(y_pred)):
  distances_pre = distances_cur
  distances_cur = []
  for pos in range (length, len(y_pred)):
    distance = distances_pre[pos - length]
    distance = distance + 1 if y_pred[pos] == target_cluster else distance - 1
    distances_cur += [distance]
    if distance > best_distance:
      best_distance = distance
      best_division = [pos, length, target_cluster]
print(best_division)
print(max_distance - best_distance)

y_estm = (best_division[0] - best_division[1]) * [1 - best_division[2]] \
       + best_division[1] * [best_division[2]] \
       + (len(y_pred) - best_division[0] - 1) * [1 - best_division[2]]

# Figure
fig = plt.figure()
# original plot
x1 = []
y1 = []
z1 = []
x2 = []
y2 = []
z2 = []
for xi, yi in zip(training_set, y_pred):
  if yi == 0:
    x1 += [xi[0]]
    y1 += [xi[1]]
    z1 += [xi[2]]
  else:
    x2 += [xi[0]]
    y2 += [xi[1]]
    z2 += [xi[2]]
ax = fig.add_subplot(211, projection='3d')
ax.scatter(x1, y1, z1, color='r')
ax.scatter(x2, y2, z2, color='b')

# original plot
x1 = []
y1 = []
z1 = []
x2 = []
y2 = []
z2 = []
for xi, yi in zip(training_set, y_estm):
  if yi == 0:
    x1 += [xi[0]]
    y1 += [xi[1]]
    z1 += [xi[2]]
  else:
    x2 += [xi[0]]
    y2 += [xi[1]]
    z2 += [xi[2]]
ax = fig.add_subplot(212, projection='3d')
ax.scatter(x1, y1, z1, color='r')
ax.scatter(x2, y2, z2, color='b')


plt.show()
