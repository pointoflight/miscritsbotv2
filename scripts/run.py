from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse


dark_poltergust_offset_coords = (175, -40)
dark_slithero_offset_coords = (-100, 200)
woolly_offset_coords = (-470,380)

search_crit = "f_vhisp"

notifier = Notifier()
bot = MiscritsBot(fight_background="photos/fight/f_vhisp/fight_background.png", 
                  crit_ref="photos/fight/f_vhisp/woolly_ref.png", 
                  my_turn="photos/fight/f_vhisp/my_turn.png",
                  search_loc_x_off=-460,
                  search_loc_y_off=380,
                  notifier=notifier,
                  plat_training=False)


# bot.main_loop()

# ----------------------

# import os
# print(os.getcwd())
# if os.path.exists("photos/fight/d_slithero"):
#     print("File exists!")
# else:
#     print("File does not exist.")

# import random
# loc = HumanMouse.locate_on_screen("photos/fight/woolly/woolly_ref.png")
# if loc:
#     loc = (loc[0] - 470 + random.randint(-2, 2), loc[1] + 380 + random.randint(-2, 2))
#     HumanMouse.move_to(loc, random.randint(0, 10), random.randint(-10, 0))
