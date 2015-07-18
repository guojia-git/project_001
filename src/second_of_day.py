#! /usr/bin/python

class SecondOfDay:
  max_val = 86400
  def __init__(self, sec):
    self.second = sec
  
  def __radd__(self, other):
    if isinstance(other, (int, long, float, complex)):
      the_sum = self.second + other
    elif isinstance(other, SecondOfDay):
      the_sum = self.second + other.second
    else:
      raise ValueError('Operand type unknown.')
      return
    if self.second + other > self.max_val:
      the_sum = the_sum - self.max_val
    return SecondOfDay(the_sum)

  def __add__(self, other):
    if isinstance(other, (int, long, float, complex)):
      the_sum = self.second + other
    elif isinstance(other, SecondOfDay):
      the_sum = self.second + other.second
    else:
      raise ValueError('Operand type unknown.')
      return
    if self.second + other > self.max_val:
      the_sum = the_sum - self.max_val
    return SecondOfDay(the_sum)

  def __rsub__(self, other):
    if isinstance(other, (int, long, float, complex)):
      the_diff =  other - self.second
    elif isinstance(other, SecondOfDay):
      the_diff =  other.second - self.second
    else:
      raise ValueError('Operand type unknown.')
      return
    if the_diff < 0:
      the_diff += self.max_val
    return SecondOfDay(the_diff)

  def __sub__(self, other):
    if isinstance(other, (int, long, float, complex)):
      the_diff = self.second - other
    elif isinstance(other, SecondOfDay):
      the_diff = self.second - other.second
    else:
      raise ValueError('Operand type unknown.')
      return
    if the_diff < 0:
      the_diff += self.max_val
    return SecondOfDay(the_diff)

  def __lt__(self, other):
    the_diff = (self - other).second
    return the_diff > self.max_val / 2
    
  def __le__(self, other):
    the_diff = (self - other).second
    return the_diff > self.max_val / 2 or the_diff == 0

  def __eq__(self, other):
    the_diff = (self - other).second
    return the_diff == 0
    
  def __ne__(self, other):
    the_diff = (self - other).second
    return the_diff != 0

  def __gt__(self, other):
    the_diff = (self - other).second
    return the_diff < self.max_val / 2
    
  def __ge__(self, other):
    the_diff = (self - other).second
    return the_diff < self.max_val / 2 or the_diff == 0

  def is_between(self, t1, t2):
    return t1 <= self and self > t2
