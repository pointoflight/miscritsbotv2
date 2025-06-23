from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse
from fight_info import FightInfo


notifier = Notifier()
bot = MiscritsBot(search_crit="ursiwave",
                  trainer_crit="papa",
                  notifier=notifier,
                  plat_training=True,
                  plat_capture_attempts=1)

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

# import random
# import time 

# while True:
#     loc = HumanMouse.locate_on_screen("photos/fight/common/capture.png")
#     if loc:
#         print("found capture!")
#     else:
#         print("not found capture!")
#     time.sleep(0.1)

# loc = HumanMouse.locate_on_screen("photos/fight/ursiwave/ref.png")
# if loc:
#     loc = (loc[0] + -70 + random.randint(-2, 2), loc[1] + 250 + random.randint(-2, 2))
#     HumanMouse.move_to(loc, random.randint(0, 10), random.randint(-10, 0))
