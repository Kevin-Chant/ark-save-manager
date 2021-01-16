import keyboard, sys, time, os, math
from save_manager import SaveManager
from constants import *
from gui_helpers import *
import tkinter as tk
from tkinter import font

class CmdGui(object):
  def __init__(self):
    self.root = tk.Tk()
    self.display_buffer = tk.StringVar()
    self.save_manager = SaveManager()
    save_dir = load_save_dir_from_file()
    if save_dir is not None:
      self.save_manager.set_save_dir(save_dir)
      run_setup = False
    else:
      run_setup = True
    self.ui_state = {
      "in_setup": run_setup,
      "choosing_action": False,
      "selected_pane": "map",
      "highlighted_map": "The Island",
      "highlighted_save_indices": {},
      "highlighted_action": None,
    }

  def import_save(self, _curr_save_obj):
    save_folder_path = prompt_for_save_to_import()
    save_folder_name = save_folder_path.split("/")[-1]
    if save_folder_name in FOLDER_MAP_NAMES.keys():
      map_name = FOLDER_MAP_NAMES[save_folder_name]
      active = True
    else:
      map_name = infer_map_name_from_save_folder(save_folder_path)
      active = False
    params_dict = {"map_name": map_name, "active": active}
    self.save_manager.import_save(save_folder_path, params_dict)

  def activate_save(self, curr_save_obj):
    self.save_manager.activate_save(curr_save_obj.uuid)

  def deactivate_save(self, curr_save_obj):
    self.save_manager.deactivate_save(curr_save_obj.uuid)

  def rename_save(self, curr_save_obj):
    new_name = prompt_for_new_name()
    self.save_manager.rename(curr_save_obj.uuid, new_name)

  def active_save_obj(self):
    return self.save_manager.active_save_for_mname(self.highlighted_map())

  def selected_save_list(self):
    return self.save_manager.get_save_list_for_mname(self.highlighted_map())

  def selected_save_obj(self):
    save_list = self.selected_save_list()
    save_index = self.highlighted_save_index()
    if len(save_list) == 0 or save_index is None:
      return None
    return save_list[save_index]

  def in_setup(self):
    return self.ui_state["in_setup"]

  def choosing_action(self):
    return self.ui_state["choosing_action"]

  def selected_pane(self):
    return self.ui_state["selected_pane"]

  def highlighted_map(self):
    return self.ui_state["highlighted_map"]

  def highlighted_save_index(self):
    return self.ui_state["highlighted_save_indices"].get(self.highlighted_map(), None)

  def highlighted_action(self):
    return self.ui_state["highlighted_action"]

  def currently_valid_actions(self):
    curr_save = self.selected_save_obj()
    if curr_save is None:
      return []
    return valid_actions_for_save_obj(curr_save)

  def handle_current_action(self):
    func_name = fx_name_for_action(self.highlighted_action())
    save_obj = self.selected_save_obj()
    func_call = f"self.{func_name}(save_obj)"
    eval(func_call)
    self.ui_state["choosing_action"] = False
    self.ui_state["highlighted_action"] = None

  def handle_set_save_dir(self):
    save_dir = prompt_for_save_dir()
    self.save_manager.set_save_dir(save_dir)
    self.ui_state["in_setup"] = False

  def set_choosing_action(self, is_choosing):
    if is_choosing:
      actions = self.currently_valid_actions()
      # Don't allow action selection unless there are valid actions
      if self.selected_pane() != "save" or len(actions) == 0:
        return
      self.ui_state["highlighted_action"] = actions[0]
    else:
      self.ui_state["highlighted_action"] = None

    self.ui_state["choosing_action"] = is_choosing

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
      action_list = self.currently_valid_actions()
      curr_action_index = action_list.index(self.highlighted_action())
      next_index = wrap_index(curr_action_index + offset, action_list)
      self.ui_state["highlighted_action"] = action_list[next_index]
    elif self.selected_pane() == "map":
      curr_map_index = MAP_NAMES.index(self.highlighted_map())
      next_index = wrap_index(curr_map_index + offset, MAP_NAMES)
      self.ui_state["highlighted_map"] = MAP_NAMES[next_index]
    else:
      save_list = self.selected_save_list()
      # No saves to select
      if len(save_list) == 0:
        return
      save_name_list = [save.name for save in save_list]
      curr_save_index = self.highlighted_save_index()
      next_index = wrap_index(curr_save_index + offset, save_name_list)
      self.ui_state["highlighted_save_indices"][self.highlighted_map()] = next_index

  def display_header(self):
    title = "Ark Save Management"
    lines = [
      "",
      " " * math.floor((TOTAL_TERMINAL_SIZE - len(title)) / 2) + title + " " * math.ceil((TOTAL_TERMINAL_SIZE - len(title)) / 2),
      "",
      "Use Up/Down/Left/Right to move your selection",
      "Press Enter to take an action on your current selection",
      "-" * TOTAL_TERMINAL_SIZE,
      "",
    ]

    return "\n".join(lines)

  def get_save_name(self, i):
    save_list = self.selected_save_list()
    if i >= len(save_list):
      return ""

    name = save_list[i].name
    if name is None:
      name = "Unnamed Save"
    return name

  def display_main_section(self):
    lines = []
    for i in range(NUM_ROWS):
      map_name = MAP_NAMES[i]
      save_name = self.get_save_name(i)
      if save_name != "" and self.active_save_obj() == self.selected_save_list()[i]:
        save_name = f"<{save_name}>"
      row_to_display=""
      row_to_display += "|" + " " * (LEFT_BORDER_WIDTH-1)
      if map_name == self.highlighted_map():
        if self.selected_pane()=="map":
          row_to_display += "> " + map_name + " " * (MAX_MAP_NAME_WIDTH - len(map_name) - 2)
        else:
          row_to_display += "*" + map_name + " " * (MAX_MAP_NAME_WIDTH - len(map_name) - 1)
      else:
        row_to_display += map_name + " " * (MAX_MAP_NAME_WIDTH - len(map_name))
      row_to_display += " " * (RIGHT_BORDER_WIDTH-1) + "|"
      row_to_display += " " * MIDDLE_PADDING_WIDTH
      row_to_display += "|" + " " * (LEFT_BORDER_WIDTH-1)
      if i == self.highlighted_save_index() and self.selected_pane()=="save":
        row_to_display += "> " + save_name + " " * (MAX_SAVE_NAME_WIDTH - len(save_name) - 2)
      else:
        row_to_display += save_name + " " * (MAX_SAVE_NAME_WIDTH - len(save_name))
      row_to_display += " " * (RIGHT_BORDER_WIDTH-1) + "|"
      lines.append(row_to_display)
    lines.append("")

    return "\n".join(lines)


  def display_footer(self):
    lines = ["-" * TOTAL_TERMINAL_SIZE]
    for action in self.currently_valid_actions():
      if action == self.highlighted_action():
        lines.append("> " + action)
      else:
        lines.append(action)
    lines.append("")
    return "\n".join(lines)

  def print_debug(self):
    os.system("clear")
    print(self.ui_state)
    sys.stdout.flush()

  def display_setup_prompt(self):
    lines = [
      highlight("Please select the 'Saved' folder found in your Ark installation."),
      "(Press Enter to open the file dialog)",
      "",
    ]
    return "\n".join(lines)

  def render_setup(self):
    new_display = ""
    new_display += self.display_header()
    new_display += self.display_setup_prompt()
    self.display_buffer.set(new_display)

    self.print_debug()

  def render(self):
    if self.in_setup():
      return self.render_setup()

    new_display = ""
    new_display += self.display_header()
    new_display += self.display_main_section()
    new_display += self.display_footer()
    self.display_buffer.set(new_display)

    self.print_debug()

  def on_keypress(self, key):
    if self.in_setup():
      if key == 'enter':
        self.handle_set_save_dir()
    else:
      if key == 'down':
        self.move_highlight(1)
      if key == 'up':
        self.move_highlight(-1)

      if self.choosing_action():
        if key == 'esc':
          self.set_choosing_action(False)
        if key == 'enter':
          self.handle_current_action()
      else:
        if key == 'left':
          self.set_active_pane('map')
        if key == 'right':
          self.set_active_pane('save')
        if key == 'enter':
          self.set_choosing_action(True)

    self.render()
    return

  def connect_key_listeners(self):
    callback = lambda key_event: self.on_keypress(key_event.name)
    keyboard.on_press(callback)

  def main_loop(self):
    self.connect_key_listeners()
    monospaced_font = font.Font(family='Consolas', size=12)
    tk.Label(self.root, justify=tk.LEFT, textvariable=self.display_buffer, font=monospaced_font).pack()
    self.render()
    self.root.mainloop()

  def main_menu_loop(self):
    exit = False
    while exit is False:
      self.render()
      time.sleep(0.10)
      while True:
        if self.in_setup():
          if keyboard.is_pressed('enter'):
            self.handle_set_save_dir()
            break
        else:
          if keyboard.is_pressed('down'):
            self.move_highlight(1)
            break
          if keyboard.is_pressed('up'):
            self.move_highlight(-1)
            break

          if self.choosing_action():
            if keyboard.is_pressed('escape'):
              self.set_choosing_action(False)
              break
            if keyboard.is_pressed('enter'):
              self.handle_current_action()
              break
          else:
            if keyboard.is_pressed('left'):
              self.set_active_pane('map')
              break
            if keyboard.is_pressed('right'):
              self.set_active_pane('save')
              break
            if keyboard.is_pressed('enter'):
              self.set_choosing_action(True)
              break
        time.sleep(0.05)


if __name__ == "__main__":
  gui = CmdGui()
  # gui.main_menu_loop()
  gui.main_loop()
