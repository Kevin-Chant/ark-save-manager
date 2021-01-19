import keyboard, sys, time, os, math
from save_manager import SaveManager
from constants import *
from gui_helpers import *
import tkinter as tk
from tkinter import font

class CmdGui(object):
  def __init__(self):
    self.root = tk.Tk()
    self.font = font.Font(family='Consolas', size=12, weight=font.NORMAL)
    self.bold_font = font.Font(family='Consolas', size=12, weight=font.BOLD)
    self.save_manager = SaveManager()
    save_dir = load_save_dir_from_file()
    if save_dir is not None:
      self.save_manager.set_save_dir(save_dir)
      run_setup = False
    else:
      run_setup = True
    self.ui_state = {
      "in_setup": run_setup,
      "highlighted_map": "The Island",
      "highlighted_save_index": None,
      "save_list_scroll_offset": 0,
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

  def activate_save(self, save_obj):
    self.save_manager.activate_save(save_obj.uuid)

  def deactivate_save(self, save_obj):
    self.save_manager.deactivate_save(save_obj.uuid)

  def rename_save(self, save_obj):
    new_name = prompt_for_new_name()
    self.save_manager.rename(save_obj.uuid, new_name)

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

  def highlighted_map(self):
    return self.ui_state["highlighted_map"]

  def highlighted_save_index(self):
    return self.ui_state["highlighted_save_index"]

  def save_list_scroll_offset(self):
    return self.ui_state["save_list_scroll_offset"]

  def print_debug(self):
    os.system("clear")
    print(self.ui_state)
    sys.stdout.flush()

  def update_maps(self):
    for map_label in self.map_labels:
      if map_label['text'] == self.highlighted_map():
        map_label.configure(font=self.bold_font)
      else:
        map_label.configure(font=self.font)

  def update_saves(self):
    [text_var.set("") for text_var in self.save_text_vars]

    save_list = self.selected_save_list()
    offset = self.save_list_scroll_offset()
    highlighted_save_index = self.highlighted_save_index()

    for i, save_obj in enumerate(save_list[offset:offset+NUM_ROWS]):
      self.save_text_vars[i].set(save_obj.name or "Unnamed Save")
      if save_obj.active:
        self.save_labels[i].configure(fg="cyan")
      else:
        self.save_labels[i].configure(fg="black")
    for i in range(NUM_ROWS):
      if i - offset == highlighted_save_index:
        self.save_labels[i].configure(bg="red")
      else:
        self.save_labels[i].configure(bg="white")

  def update_actions(self):
    if self.selected_save_obj() is None:
      self.action_buttons[1].configure(state="disabled")
      self.action_buttons[2].configure(state="disabled")
    else:
      self.action_buttons[1].configure(state="normal")
      self.action_buttons[2].configure(state="normal")
      if self.selected_save_obj().active:
        self.action_buttons[2]['command'] = self.handle_deactivate_save
        self.button_text_var.set("Deactivate Save")
      else:
        self.action_buttons[2]['command'] = self.handle_activate_save
        self.button_text_var.set("Activate Save")

  def handle_prompt_for_save_dir(self):
    prompt_for_save_dir(self.root)
    self.save_manager.set_save_dir(dirpath)
    self.ui_state["in_setup"] = False

    self.setup_frame.destroy()
    self.initial_render()

  def select_map(self, map_index):
    self.ui_state["highlighted_map"] = MAP_NAMES[map_index]
    self.ui_state["highlighted_save_index"] = None

    self.print_debug()

    self.update_maps()
    self.update_saves()
    self.update_actions()

  def select_save(self, save_index):
    if save_index >= len(self.selected_save_list()):
      return

    self.ui_state["highlighted_save_index"] = save_index

    self.update_saves()
    self.update_actions()

  def handle_import_save(self):
    title = "Select the save you'd like to import."
    dirpath = filedialog.askdirectory(title=title, parent=self.root)
    # TODO
    return

  def handle_rename_save(self):
    return

  def handle_activate_save(self):
    self.activate_save(self.selected_save_obj())

    self.update_saves()
    self.update_actions()

  def handle_deactivate_save(self):
    self.deactivate_save(self.selected_save_obj())

    self.update_saves()
    self.update_actions()

  def set_up_header(self):
    self.header_frame = tk.Frame(self.root)
    self.header_frame.configure(background="green")
    self.header_frame.grid(row=0, column=0, columnspan=3)
    self.header_label = tk.Label(self.header_frame, text="Ark Save Management", font=(None, 16))
    self.header_label.pack()

  def set_up_map_column(self):
    self.map_frame = tk.Frame(self.root)
    self.map_frame.configure(background="black")
    self.map_frame.grid(row=1, column=0)
    self.map_labels = [tk.Label(self.map_frame, text=MAP_NAMES[i], font=self.font) for i in range(NUM_ROWS)]
    for i, label in enumerate(self.map_labels):
      label.bind("<Button-1>", lambda event,i=i: self.select_map(i))
      label.pack()

  def set_up_save_column(self):
    self.save_frame = tk.Frame(self.root)
    self.save_frame.configure(background="blue")
    self.save_frame.grid(row=1, column=1)
    self.save_text_vars = [tk.StringVar() for i in range(NUM_ROWS)]
    self.save_labels = [tk.Label(self.save_frame, textvariable=text_var, font=self.font) for text_var in self.save_text_vars]
    for i, label in enumerate(self.save_labels):
      label.bind("<Button-1>", lambda event,i=i: self.select_save(i))
      label.pack()

  def set_up_action_column(self):
    self.action_frame = tk.Frame(self.root)
    self.action_frame.configure(background="red")
    self.action_frame.grid(row=1, column=2)

    import_button = tk.Button(self.action_frame, text="Import Save", command=lambda: self.handle_import_save())
    rename_button = tk.Button(self.action_frame, text="Rename Save", command=lambda: self.handle_rename_save())

    self.button_text_var = tk.StringVar()
    self.button_text_var.set("Activate Save")
    activate_button = tk.Button(self.action_frame, textvariable=self.button_text_var, command=lambda: self.handle_activate_save())
    activate_button.configure(state="disabled")

    self.action_buttons = [import_button, rename_button, activate_button]
    [button.pack() for button in self.action_buttons]

  def render_setup(self):
    self.root.configure(background="white")
    self.root.geometry("200x200")
    self.setup_frame = tk.Frame(self.root)
    tk.Label(self.setup_frame, text="To run this helper you must select your Ark save directory").pack()
    tk.Label(self.setup_frame, text="This is usually found in steamapps/common/ARK/ShooterGame/Saved").pack()

    tk.Button(self.setup_frame, text="Select Saved Directory", command=lambda: self.handle_prompt_for_save_dir).pack()


  def initial_render(self):
    self.root.configure(background="turquoise")
    self.root.grid_columnconfigure(0, weight=2)
    self.root.grid_columnconfigure(1, weight=2)
    self.root.grid_columnconfigure(2, weight=1)
    self.root.geometry("800x600")

    self.set_up_header()
    self.set_up_map_column()
    self.set_up_save_column()
    self.set_up_action_column()
    self.select_map(0)

  def main_loop(self):
    if self.in_setup():
      self.render_setup()
    else:
      self.initial_render()
    self.root.mainloop()

if __name__ == "__main__":
  gui = CmdGui()
  gui.main_loop()
