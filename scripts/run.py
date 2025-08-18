from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse
from fight_info import FightInfo


notifier = Notifier(num_notifs=1)

bot = MiscritsBot(search_crit="smolderfry",
                  trainer_crit="papa",
                  notifier=notifier,
                  plat_training=False,
                  capture_tiers=["A+", "A", "B+"],
                  plat_capture_attempts=0)

bot.main_loop()

# fix: truth: quest first , congrats you have recevied a new crit later. currently doesn't work for this
# add IST time to all print statements, and print to a file instead of fix buffer terminal
# fix for double spawn captures. (need to attempt capture for second crit)
# fix name check for Dark Nessy. For now its justD