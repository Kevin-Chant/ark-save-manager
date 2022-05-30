MAP_NAMES = ["The Island", "Genesis: Part 1", "Scorched Earth", "Aberration", "Extinction", "The Center", "Ragnarok", "Valguero", "Crystal Isles"]
MAP_FOLDER_NAMES = {
  "The Island": "SavedArksLocal",
  "Genesis: Part 1": "", # TODO
  "Scorched Earth": "ScorchedEarth_PSavedArksLocal",
  "Aberration": "Aberration_PSavedArksLocal",
  "Extinction": "ExtinctionSavedArksLocal", # TODO
  "The Center": "", # TODO
  "Ragnarok": "RagnarokSavedArksLocal",
  "Valguero": "", # TODO
  "Crystal Isles": "CrystalIslesSavedArksLocal",
}
FOLDER_MAP_NAMES = {folder_name: map_name for map_name, folder_name in MAP_FOLDER_NAMES.items()}
MAP_ARK_FILE_NAMES = {
  "The Island": "TheIsland.ark",
  "Genesis: Part 1": "", # TODO
  "Scorched Earth": "ScorchedEarth_P.ark",
  "Aberration": "Aberration_P.ark",
  "Extinction": "", # TODO
  "The Center": "", # TODO
  "Ragnarok": "Ragnarok.ark",
  "Valguero": "", # TODO
  "Crystal Isles": "CrystalIsles.ark",
}
STATE_FILE = ".arksavemanager"
SAVE_DIR_FILENAME = ".arksavemanagerdir"
COLORS = {"primary": "#4968BB", "secondary": "#839BF4", "background": "#A8AABC", "accent": "#F5D059", "text_light": "#F8F9FF"}
