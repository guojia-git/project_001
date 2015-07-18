#!/usr/bin/python

import data_header as header
NUM_USER = 100

users = []
for i in range (1, 10):
  with open ("UserKPIs.baseflow_sample.ALL.2013100" + str(i) + ".dat") as f:
    lines = f.readlines()
    for line in lines:
      line = line.split('|')
      msisdn = line[header.MSISDN]
      if msisdn not in users:
        users += [msisdn]
        if len(users) >= NUM_USER:
          break
  if len(users) >= NUM_USER:
    break

users = users[:NUM_USER]

for i in range(len(users)):
  user = users[i]
  fout = open("../data/users/user_" + "%03d" %i + ".dat", "w")
  for j in range (1, 10):
    with open ("UserKPIs.baseflow_sample.ALL.2013100" + str(j) + ".dat") as f:
      lines = f.readlines()
      for line in lines:
        strs = line.split('|')
        msisdn = strs[header.MSISDN]
        if msisdn == user:
          fout.write(line)
  fout.close()



