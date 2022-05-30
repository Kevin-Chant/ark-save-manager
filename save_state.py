import json, os

from save_object import SaveObject
from constants import *

# Helper class for pickling the state of the saves folder
# Holds an array of SaveObjects
# Where each SaveObject has the properties `name`, `map_name`, `active`, and `uuid`
class SaveState(object):
  def __init__(self):
    self.state = []

  def register_save(self, save_obj):
    self.state.append(save_obj)
    self.save_state_file()

  def get_save_by_uuid(self, uuid):
    for save in self.state:
      if save.uuid == uuid:
        return save

    raise Exception("Cannot find save with the given uuid")

  def get_save_by_uuid_or_name(self, uuid_or_name):
    for save in self.state:
      if save.uuid == uuid_or_name or save.name == uuid_or_name:
        return save

    raise Exception("Cannot find the specified save")

  def deactivate_save(self, uuid):
    save_obj = self.get_save_by_uuid(uuid)
    save_obj.active = False
    self.save_state_file()

  def activate_save(self, uuid):
    save_obj = self.get_save_by_uuid(uuid)
    save_obj.active = True
    self.save_state_file()

  def rename_save(self, uuid, name):
    found = False
    for save in self.state:
      if save.uuid == uuid:
        save.name = name
        found = True
        self.save_state_file()

    return found

  def active_save_for_mname(self, map_name):
    for save in self.state:
      if save.active and save.map_name == map_name:
        return save

  def all_saves_for_mname(self, map_name):
    return [save for save in self.state if save.map_name == map_name]

  def chdir(self, dir_string):
    os.chdir(dir_string)

  def load_state_file(self):
    with open(STATE_FILE) as f:
      raw_dict = json.loads(f.read().strip())
      self.state = [SaveObject.from_json(j) for j in raw_dict]

  def register_unknown_saves_to_state_file(self):
    # Read from directory for what folders exist
    all_folders = os.listdir()
    valid_folders = [fname for fname in all_folders if fname in FOLDER_MAP_NAMES]
    # Initialize a new SaveObject for each folder that matches an expected name, as long as
    # it isn't already represented
    existing_active_maps = {save_obj.map_name for save_obj in self.state if save_obj.active}
    for fname in valid_folders:
      if FOLDER_MAP_NAMES[fname] not in existing_active_maps:
        save_obj = SaveObject(map_name=FOLDER_MAP_NAMES[fname], active=True)
        self.register_save(save_obj)

  def save_state_file(self):
    with open(STATE_FILE, "w") as f:
      to_write = json.dumps([save_obj.to_json() for save_obj in self.state])
      f.write(to_write)

  def load_from_dir(dir_string):
    ss = SaveState()
    ss.chdir(dir_string)
    try:
      ss.load_state_file()
    except FileNotFoundError:
      pass
    ss.register_unknown_saves_to_state_file()
    return ss

  def __str__(self):
    return "\n".join([str(save_obj) for save_obj in self.state])
