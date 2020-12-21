MAP_NAMES = ["The Island", "Genesis: Part 1", "Scorched Earth", "Abberation", "Extinction", "The Center", "Ragnarok", "Valguero", "Crystal Isles"]
MAP_FOLDER_NAMES = {
  "The Island": "SavedArksLocal",
  "Genesis: Part 1": "", # TODO
  "Scorched Earth": "ScorchedEarth_PSavedArksLocal",
  "Abberation": "Abberation_PSavedArksLocal",
  "Extinction": "", # TODO
  "The Center": "", # TODO
  "Ragnarok": "RagnarokSavedArksLocal",
  "Valguero": "", # TODO
  "Crystal Isles": "CrystalIslesSavedArksLocal",
}
FOLDER_MAP_NAMES = {folder_name: map_name for map_name, folder_name in MAP_FOLDER_NAMES.items()}
STATE_FILE = ".arksavemanager"
