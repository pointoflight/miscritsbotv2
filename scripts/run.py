from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse


# dark_poltergust_offset_coords = (175, -40)
# dark_slithero_offset_coords = (-100, 200)
# woolly_offset_coords = (-460,380)


notifier = Notifier()
bot = MiscritsBot(search_crit="f_flintly",
                  trainer_crit="papa",
                  notifier=notifier,
                  plat_training=False)

bot.main_loop()

# ----------------------

# import os
# print(os.getcwd())
# if os.path.exists("photos/fight/d_slithero"):
#     print("File exists!")
# else:
#     print("File does not exist.")

# import random
# import time

# start = time.time()
# loc = HumanMouse.locate_on_screen("photos/fight/f_flintly/ref.png")
# end = time.time()

# print(f"Time taken: {end - start:.4f} seconds")

# if loc:
#     loc = (loc[0] + -150 + random.randint(-2, 2), loc[1] + -20 + random.randint(-2, 2))
#     HumanMouse.move_to(loc, random.randint(0, 10), random.randint(-10, 0))
