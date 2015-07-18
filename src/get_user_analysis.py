#!/usr/bin/python

import sys
import os
import data_header as header

idx = 0
for fname in os.listdir("../data/users/"):
# open records for one user
  with open ("../data/users/" + fname) as f:
    wf = open("../data/analyses/user_analysis_" + "%03d" %idx + ".csv", "w")
    idx += 1
#metrics that I want to extract
#1-length of idle period
#2-last end, hour of the day
#3-wheter base station has changed
#4-application
#-
    line = f.readline().strip('\n').split('|')
    last_end_time = int(line[header.ENDTIME])
    last_start_time = int(line[header.STARTTIME])
    last_base_station = line[header.ENHANCE_NODEB]
    for line in f:
      line = line.strip('\n')
      strs = line.split('|')
      start_time = int(strs[header.STARTTIME])
      if start_time <= last_end_time + 20: #consider the same session
        last_end_time = int(strs[header.ENDTIME])
      else:
#1
        idle_period = start_time - last_end_time
        wf.write(str(idle_period) + ',')
#2
        epoch_time = last_end_time
        second_of_day = (epoch_time - 1380585600) % 86400
        hour = float(second_of_day) / 3600.0
        hour = round(hour, 2)
        hour_of_day = 0 if hour == 24.0 else hour
        wf.write("%.02f" %hour_of_day + ',')
#3
        is_base_station_changed = strs[header.ENHANCE_NODEB] != last_base_station
        wf.write(str(int(is_base_station_changed)))
        wf.write(',')
#4        
        second_of_day = (start_time - 1380585600) % 86400
        wf.write(str(second_of_day))
        wf.write(',')
#5        
        end_time = int(strs[header.ENDTIME])
        second_of_day = (start_time - 1380585600) % 86400
        wf.write(str(second_of_day))
        wf.write('\n')
#update
        last_start_time = start_time
        last_end_time = int(strs[header.ENDTIME])
        last_base_station = strs[header.ENHANCE_NODEB]


