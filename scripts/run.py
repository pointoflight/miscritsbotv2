from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse
from fight_info import FightInfo


notifier = Notifier(num_notifs=50)

bot = MiscritsBot(search_crit="charpy",
                  trainer_crit="papa",
                  notifier=notifier,
                  plat_training=False,
                  capture_tiers=["A+", "A", "B+"],
                  plat_capture_attempts=0)

bot.main_loop()

# fix: truth: quest first , congrats you have recevied a new crit! later. cuurently doesn't work for this