from save_manager import SaveManager


sm = SaveManager()
sm.set_save_dir("d:/steam/steamapps/common/ark/shootergame/saved")
sm.debug()
# sm.rename_save("efccd55d-f7a2-4209-bb31-e9775672da84", "Crystal Isles Test Active")
sm.activate_save("Ria & Hubble")
# sm.activate_save("6d0f7b12-3077-4b50-8f9d-9a854a53e653")
sm.debug()
