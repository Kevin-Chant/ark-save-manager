import os
import tkinter as tk
from tkinter import filedialog
from colorama import Fore, Back, Style
from constants import *

LEFT_BORDER_WIDTH = 2
RIGHT_BORDER_WIDTH = 2
MIDDLE_PADDING_WIDTH = 4
MAX_MAP_NAME_WIDTH = max([len(mn) for mn in MAP_NAMES]) + 2
MAX_SAVE_NAME_WIDTH = 25

TOTAL_TERMINAL_SIZE = LEFT_BORDER_WIDTH + MAX_MAP_NAME_WIDTH + RIGHT_BORDER_WIDTH + MIDDLE_PADDING_WIDTH + LEFT_BORDER_WIDTH + MAX_SAVE_NAME_WIDTH + RIGHT_BORDER_WIDTH
NUM_ROWS = len(MAP_NAMES)

def get_hidden_tk_root():
  root = tk.Tk()
  root.withdraw()
  return root

def load_save_dir_from_file():
  if os.path.exists(SAVE_DIR_FILENAME):
    with open(SAVE_DIR_FILENAME) as f:
      try:
        return f.readlines()[0].strip()
      except:
        return None
  else:
    return None

def prompt_for_save_dir(root):
  title = "Select the Saved folder in your Ark installation."
  dirpath = filedialog.askdirectory(title=title, parent=root)
  write_save_dir_to_file(dirpath)
  return dirpath

def write_save_dir_to_file(dirpath):
  with open(SAVE_DIR_FILENAME, 'w') as f:
    f.write(dirpath)

def active(text):
  return Fore.BLUE + Style.BRIGHT + text + Style.RESET_ALL

def action_text(text, active):
  styles = None
  if active:
    styles = Style.BRIGHT + Fore.GREEN
  else:
    styles = Style.DIM + Fore.WHITE
  return styles + text + Style.RESET_ALL

def wrap_index(i, l):
  if i < 0:
    return 0
  if i >= len(l):
    return len(l) - 1
  return i

def infer_map_name_from_save_folder(save_folder_path):
  for map_name, ark_file_name in MAP_ARK_FILE_NAMES:
    if os.path.exists(os.path.join(save_folder_path, ark_file_name)):
      return map_name
