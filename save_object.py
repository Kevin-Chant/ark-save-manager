import uuid, json

class SaveObject(object):
  def __init__(self, name=None, map_name="The Island", active=False, set_uuid=None):
    self.name = name
    self.map_name = map_name
    self.active = active
    self.uuid = set_uuid or str(uuid.uuid4())

  def __str__(self):
    res = f"{self.map_name} -- {self.name}"
    if self.active:
      res += " [*]"
    return res

  def from_json(dict):
    so = SaveObject()
    so.name = dict.get("name", None)
    so.map_name = dict["map_name"]
    so.active = dict["active"]
    so.uuid = dict.get("uuid", str(uuid.uuid4()))
    return so

  def to_json(self):
    return self.__dict__
