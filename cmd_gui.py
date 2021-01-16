import keyboard, sys, time, os, math
from save_manager import SaveManager
from constants import *
from gui_helpers import *

class CmdGui(object):
  def __init__(self):
    self.save_manager = SaveManager()
    # TODO: set save directory based on input
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
    for action in self.currently_valid_actions():
      if action == self.highlighted_action():
        print(highlight(action_text(action, self.choosing_action())))
      else:
        print(action_text(action, self.choosing_action()))
    return

  def print_debug(self):
    print("DEBUG")
    print(self.ui_state)

  def print_setup_prompt(self):
    print(highlight("Please select the 'Saved' folder found in your Ark installation."))
    print("(Press Enter to open the file dialog)")

  def render_setup(self):
    self.clear_terminal()
    self.print_header()
    self.print_setup_prompt()
    self.print_debug()
    sys.stdout.flush()

  def render(self):
    if self.in_setup():
      return self.render_setup()

    self.clear_terminal()
    self.print_header()
    self.print_main_section()
    self.print_footer()
    self.print_debug()
    sys.stdout.flush()

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
  gui.main_menu_loop()