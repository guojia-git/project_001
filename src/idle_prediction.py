#! /usr/bin/python
import sys
import numpy
from ecdf import Ecdf
from second_of_day import SecondOfDay
import analysis_header as header
from user_clustering import *


def experiment(fpath):
################
# Init
################

# temperary: for user model
  clusters = clustering(fpath)
  start_hour = clusters[0]
  end_hour = clusters[1]

# preparing the idle model and the test sets
  idle_training = [[], []]
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
        if time >= start_hour and time < end_hour:
          idle_training[0] += [float(dat[header.IDLE_PERIOD])]
        else:
          idle_training[1] += [float(dat[header.IDLE_PERIOD])]
      else:
        testing_set += [dat]

  idle_ecdf = [Ecdf(x) for x in idle_training]


##########################
# Checking out predictions
##########################

  TIME_INC = 300

# time progresses by 300 seconds
  last_end = SecondOfDay(int(testing_set[0][header.END]))
  last_start = SecondOfDay(int(testing_set[0][header.START]))
  cur_time = SecondOfDay(last_end.second)
  cur_start = SecondOfDay(last_start.second)
  cur_end = SecondOfDay(last_end.second)
  testing_idx = 1

  true_cnt = 0
  all_cnt = 0
  while 1:
# skip over the data transmission period in between our data transmission
    while cur_end <= cur_time:
      cur_record = testing_set[testing_idx]
      last_end = SecondOfDay(cur_end.second)
      cur_end = SecondOfDay(int(cur_record[header.END]))
      cur_start = SecondOfDay(int(cur_record[header.START]))
      if testing_idx == len(testing_set) - 1:
        break
      else:
        testing_idx += 1
    if testing_idx == len(testing_set) - 1:
      break
    
    #print(str(cur_time.second) + ',' + str(cur_end.second))
# if not in transmission
    if cur_start > cur_time:
      diff = cur_time - last_end
      elapsed_time = diff.second
      if cur_time >= start_hour * 3600 and cur_time < end_hour * 3600:
        e = idle_ecdf[0]
      else:
        e = idle_ecdf[1]
      pt0 = e.get_probability(elapsed_time) 
      if pt0 != 0:
        pt1 = e.get_probability(elapsed_time + TIME_INC)
        if pt0 == 1:
          prob = 1
        else:
          prob = 1 - (1 - pt1) / (1 - pt0)
        all_cnt += 1
        if prob < 0.5 and (cur_time + TIME_INC < cur_start):
          #print(True)
          true_cnt += 1
        elif prob > 0.5 and (cur_time + TIME_INC >= cur_start):
          #print(True)
          true_cnt += 1
        else:
          #print(False)
          true_cnt += 0
    cur_time += TIME_INC

  print("Total: " + str(all_cnt))
  print("Summary: %.02f" %(true_cnt / float(all_cnt)) if all_cnt != 0 else "Summary: 0")
  return [all_cnt, true_cnt]
  

fpath = "../data/analyses/user_analysis_009.csv"

ratios = []

for i in range(0, 100):
  fpath = "../data/analyses/user_analysis_%03d" %i + ".csv"
  result = experiment(fpath)
  if result[0] == 0:
    continue
  ratio = float(result[1]) / float(result[0])
  ratios += [ratio]

print(numpy.mean(ratios))
print(numpy.std(ratios) * 1.96)




