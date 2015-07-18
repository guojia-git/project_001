#! /usr/bin/python
# empirial cumulative distribution function
class Ecdf:
  def __init__(self, l):
    l.sort()
    self.d = dict()
    idx = 1
    for val in l:
      self.d[val] = float(idx) / float(len(l))
      idx += 1
    
  def get_probability(self, val):
    keys = self.d.keys()
    keys.sort()
    idx_lo = 0
    if len(keys) == 0:
      return 0
    idx_hi = len(keys) - 1
# do binary search
    while idx_lo < idx_hi - 1:
      #print(str(idx_lo) + " " +  str(idx_hi) + "\n")
      idx_new = (idx_lo + idx_hi) / 2
      key_new = keys[idx_new]
      if key_new == val:
        return self.d[key_new]
      elif key_new > val:
        idx_hi = idx_new
        continue
      else:
        idx_lo = idx_new
        continue
# get the prediction based on ecdf
    key_new = keys[idx_lo]
    if key_new == val:
      return self.d[key_new]
    elif key_new < val:
      if idx_lo == len(keys) - 1:
        return 1
      else:
        key_lo = key_new
        key_hi = keys[idx_lo + 1]
        return ((val - key_lo) * self.d[key_lo] + (key_hi - val) * self.d[key_hi]) / (key_hi - key_lo)
    elif key_new > val:
      if idx_lo == 0:
        return 0
      else:
        key_lo = keys[idx_lo - 1]
        key_hi = key_new
        return ((val - key_lo) * self.d[key_lo] + (key_hi - val) * self.d[key_hi]) / (key_hi - key_lo)
