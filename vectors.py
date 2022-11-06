#para los vectores

class V2(object):
  def __init__(self, x, y = None):
    self.x = x
    self.y = y

  def __repr__(self):
    return "V2(%s, %s)" % (self.x, self.y)


class V3(object):
  def __init__(self, x, y = None, z = None):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self):
    return 'V3({self.x}, {self.y}, {self.z})'

