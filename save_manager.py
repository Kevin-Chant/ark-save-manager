import os

from save_state import SaveState
from save_object import SaveObject
from constants import *

class SaveManager(object):
  def __init__(self):
    self.save_dir = None
    self.save_state = None

  def debug(self):
    print("------------")
    print(self.save_state)
    print("------------")

  def import_save(self, folder_name, params_dict):
    if not self.folder_exists(folder_name):
      raise Exception("Cannot import a nonexistent save")

    so = SaveObject.from_json(params_dict)
    self.save_state.register_save(so)
    self.rename_folder(folder_name, so.uuid)

  def rename_save(self, uuid, name):
    if not self.save_state.rename_save(uuid, name):
      raise Exception("Could not find save with that uuid")

  def set_save_dir(self, dir_string):
    self.save_dir = dir_string
    self.save_state = SaveState.load_from_dir(dir_string)
    os.chdir(dir_string)

  def fname_for_mname(self, map_name):
    return MAP_FOLDER_NAMES[map_name]

  def folder_exists(self, folder_name):
    folders = os.listdir()
    return folder_name in folders

  def rename_folder(self, old_name, new_name):
    if self.folder_exists(new_name):
      raise Exception("Cannot rename folder when the destination already exists")

    os.rename(old_name, new_name)

  def active_save_for_mname(self, map_name):
    saved_obj = self.save_state.active_save_for_mname(map_name)
    if not saved_obj:
      new_obj = SaveObject(map_name=map_name, active=True)
      self.save_state.register_save(new_obj)
    return saved_obj or new_obj

  def deactivate_save(self, uuid):
    save_obj = self.save_state.get_save_by_uuid(uuid)
    if not save_obj.active:
      raise Exception("Save must be active to be deactivated")

    source_folder = self.fname_for_mname(save_obj.map_name)
    self.rename_folder(source_folder, save_obj.uuid)
    self.save_state.deactivate_save(uuid)

  def activate_save(self, uuid_or_name):
    save_obj = self.save_state.get_save_by_uuid_or_name(uuid_or_name)
    if save_obj.active:
      raise Exception("Save must be inactive to be activated")

    map_name = save_obj.map_name
    if self.folder_exists(self.fname_for_mname(map_name)):
      active_save = self.active_save_for_mname(map_name)
      self.deactivate_save(active_save.uuid)

    target_folder = MAP_FOLDER_NAMES[save_obj.map_name]
    self.rename_folder(save_obj.uuid, target_folder)
    self.save_state.activate_save(save_obj.uuid)

