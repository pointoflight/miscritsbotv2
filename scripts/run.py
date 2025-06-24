from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse
from fight_info import FightInfo


notifier = Notifier(num_notifs=50)

bot = MiscritsBot(search_crit="gog",
                  trainer_crit="papa",
                  notifier=notifier,
                  plat_training=True,
                  plat_capture_attempts=0)

bot.main_loop()

# ----------------------

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

# while True:
#     loc = HumanMouse.locate_on_screen("photos/fight/common/capture.png")
#     if loc:
#         print("found capture!")
#     else:
#         print("not found capture!")
#     time.sleep(0.1)

# import random

# loc = HumanMouse.locate_on_screen("photos/fight/gog/ref.png")
# if loc:
#     loc = (loc[0] + -40 + random.randint(-2, 2), loc[1] + 325 + random.randint(-2, 2))
#     HumanMouse.move_to(loc, random.randint(0, 10), random.randint(-10, 0))
