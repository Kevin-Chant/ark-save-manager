# -*- coding: utf-8 -*-
import keyboard, sys, time, os, math
from save_manager import SaveManager
from constants import *
from gui_helpers import *

class CmdGui(object):
  def __init__(self):
    self.save_manager = SaveManager()
    # TODO: set save directory based on input
    self.save_manager.set_save_dir("d:/steam/steamapps/common/ark/shootergame/saved")
    self.ui_state = {
      "choosing_action": False,
      "selected_pane": "map",
      "highlighted_map": "The Island",
      "highlighted_save_indices": {},
    }

  def active_save_obj(self):
    return self.save_manager.active_save_for_mname(self.highlighted_map())

  def selected_save_list(self):
    return self.save_manager.get_save_list_for_mname(self.highlighted_map())

  def choosing_action(self):
    return self.ui_state["choosing_action"]

  def selected_pane(self):
    return self.ui_state["selected_pane"]

  def highlighted_map(self):
    return self.ui_state["highlighted_map"]

  def highlighted_save_index(self):
    return self.ui_state["highlighted_save_indices"].get(self.highlighted_map(), None)

  def set_active_pane(self, pane):
    if pane == "save" and self.highlighted_save_index() == None:
      save_list = self.selected_save_list()
      if len(save_list) > 0:
        self.ui_state["highlighted_save_indices"][self.highlighted_map()] = 0
      else:
        # Point back to map if there's no saves to be selected
        pane = "map"
    self.ui_state["selected_pane"] = pane


  def move_highlight(self, offset):
    if self.choosing_action():
      # TODO
      return
    elif self.selected_pane() == "map":
      curr_map_index = MAP_NAMES.index(self.highlighted_map())
      next_index = curr_map_index + offset
      if next_index < 0:
        next_index = 0
      if next_index >= len(MAP_NAMES):
        next_index = len(MAP_NAMES) - 1
      self.ui_state["highlighted_map"] = MAP_NAMES[next_index]
    else:
      save_list = self.selected_save_list()
      # No saves to select
      if len(save_list) == 0:
        return
      save_name_list = [save.name for save in save_list]
      curr_save_index = self.highlighted_save_index()
      next_index = curr_save_index + offset
      if next_index < 0:
        next_index = 0
      if next_index >= len(save_name_list):
        next_index = len(save_name_list) - 1
      self.ui_state["highlighted_save_indices"][self.highlighted_map()] = next_index

  def clear_terminal(self):
    os.system('clear')

  def print_header(self):
    title = "Ark Save Management"
    print("")
    print(" " * math.floor((TOTAL_TERMINAL_SIZE - len(title)) / 2) + title + " " * math.ceil((TOTAL_TERMINAL_SIZE - len(title)) / 2))
    print("")
    print("Use Up/Down/Left/Right to move your selection")
    print("Press Enter to take an action on your current selection")
    print("-" * TOTAL_TERMINAL_SIZE)

  def get_map_name(self, i, no_highlight=False):
    name = MAP_NAMES[i]
    if not no_highlight and name == self.highlighted_map():
      return highlight(name, self.selected_pane() == "map" and not self.choosing_action())
    else:
      return name

  def get_save_name(self, i, no_highlight=False):
    save_list = self.selected_save_list()
    if i >= len(save_list):
      return ""

    name = save_list[i].name
    if name is None:
      name = "Unnamed Save"
    if not no_highlight:
      if self.active_save_obj() == save_list[i]:
        name = active(name)
      if i == self.highlighted_save_index():
        name = highlight(name, self.selected_pane() == "save" and not self.choosing_action())
      return name
    else:
      return name

  def print_main_section(self):
    for i in range(NUM_ROWS):
      row_to_print=""
      row_to_print += "|" + " " * (LEFT_BORDER_WIDTH-1)
      row_to_print += self.get_map_name(i) + " " * (MAX_MAP_NAME_WIDTH - len(self.get_map_name(i, True)))
      row_to_print += " " * (RIGHT_BORDER_WIDTH-1) + "|"
      row_to_print += " " * MIDDLE_PADDING_WIDTH
      row_to_print += "|" + " " * (LEFT_BORDER_WIDTH-1)
      row_to_print += self.get_save_name(i) + " " * (MAX_SAVE_NAME_WIDTH - len(self.get_save_name(i, True)))
      row_to_print += " " * (RIGHT_BORDER_WIDTH-1) + "|"
      print(row_to_print)


  def print_footer(self):
    print("-" * TOTAL_TERMINAL_SIZE)
    print("DEBUG")
    print(self.ui_state)
    return

  def render(self):
    self.clear_terminal()
    self.print_header()
    self.print_main_section()
    self.print_footer()
    sys.stdout.flush()

  def main_menu_loop(self):
    exit = False
    while exit is False:
      self.render()
      time.sleep(0.10)
      while True:
        if keyboard.is_pressed('down'):
          self.move_highlight(1)
          break
        if keyboard.is_pressed('up'):
          self.move_highlight(-1)
          break

        if self.choosing_action():
          if keyboard.is_pressed('escape'):
            self.ui_state["choosing_action"] = False
            break
        else:
          if keyboard.is_pressed('left'):
            self.set_active_pane('map')
            break
          if keyboard.is_pressed('right'):
            self.set_active_pane('save')
            break
          if keyboard.is_pressed('enter'):
            self.ui_state["choosing_action"] = True
            break
        time.sleep(0.05)


if __name__ == "__main__":
  gui = CmdGui()
  gui.main_menu_loop()