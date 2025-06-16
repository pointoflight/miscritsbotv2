from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse
import random

notifier = Notifier()
bot = MiscritsBot(fight_background="photos/fight/d_polter/fight_background.png", 
                  crit_ref="photos/fight/d_polter/dpolter_ref.png", 
                  my_turn="photos/fight/d_polter/my_turn.png",
                  search_loc_x_off=175,
                  search_loc_y_off=-40,
                  notifier=notifier)

# import os
# print(os.getcwd())
# if os.path.exists("photos/fight/d_polter/dpolter_ref.png"):
#     print("File exists!")
# else:
#     print("File does not exist.")
bot.main_loop()

# loc = bot.locate_on_screen("photos/fight/d_polter/dpolter_ref.png")
# loc = (loc[0] + 175 + random.randint(-2, 2), loc[1] - 40 + random.randint(-2, 2))
# HumanMouse.move_to(loc, random.randint(0, 10), random.randint(-10, 0))
