from colorama import Fore, Back, Style
from constants import *

LEFT_BORDER_WIDTH = 2
RIGHT_BORDER_WIDTH = 2
MIDDLE_PADDING_WIDTH = 4
MAX_MAP_NAME_WIDTH = max([len(mn) for mn in MAP_NAMES])
MAX_SAVE_NAME_WIDTH = 25

TOTAL_TERMINAL_SIZE = LEFT_BORDER_WIDTH + MAX_MAP_NAME_WIDTH + RIGHT_BORDER_WIDTH + MIDDLE_PADDING_WIDTH + LEFT_BORDER_WIDTH + MAX_SAVE_NAME_WIDTH + RIGHT_BORDER_WIDTH
NUM_ROWS = len(MAP_NAMES)

def highlight(text, primary=True):
  styles = Fore.BLACK
  if primary:
    styles += Back.YELLOW
  else:
    styles += Back.WHITE
  return styles + text + Style.RESET_ALL

def active(text):
  return Fore.BLUE + Style.BRIGHT + text + Style.RESET_ALL
