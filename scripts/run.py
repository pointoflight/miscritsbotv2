from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse
from fight_info import FightInfo


notifier = Notifier(num_notifs=50)

bot = MiscritsBot(search_crit="eggy",
                  trainer_crit="papa",
                  notifier=notifier,
                  plat_training=True,
                  capture_tiers=["B+", "A", "A+"],
                  plat_capture_attempts=0)

bot.main_loop()

# ----------------------

# import pyautogui
# import time

# print("Move your mouse. Press Ctrl+C to stop.\n")

# try:
#     while True:
#         x, y = pyautogui.position()
#         print(f"X: {x}, Y: {y}", end='\r')  # Overwrites same line
#         time.sleep(0.05)  # Adjust refresh rate as needed
# except KeyboardInterrupt:
#     print("\nStopped.")

# fi = FightInfo()
# captured_name = fi.get_captured_crit_name_and_rating()
# print(captured_name)
# import os
# print(os.getcwd())
# if os.path.exists("photos/fight/d_slithero"):
#     print("File exists!")
# else:
#     print("File does not exist.")


# import time 
# import pyautogui

# # while True:
# train_crits = HumanMouse.locate_all_on_screen("photos/fight/common/ready_to_train_box.png", min_distance=40, confidence=0.6)
# # centers = [pyautogui.center(crit) for crit in train_crits]

# print("!! train crits:", train_crits)

# for train_crit in train_crits:
#     HumanMouse.move_to(train_crit)
#     time.sleep(0.5)
# if loc:
#     print("found capture!")
# else:
#     print("not found capture!")
# time.sleep(0.1)

# import random

# loc = HumanMouse.locate_on_screen("photos/fight/eggy/ref.png")
# if loc:
#     loc = (loc[0] + -160 + random.randint(-2, 2), loc[1] + 70 + random.randint(-2, 2))
#     HumanMouse.move_to(loc) # random.randint(0, 10), random.randint(-10, 0))
# else:
#     print("not found")
