from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse
from fight_info import FightInfo
from logger import setup_logger

logger = setup_logger()

notifier = Notifier(num_notifs=10)

bot = MiscritsBot(search_crit="winne",
                  trainer_crit="grav",
                  heal=False,
                  plat_training=False,
                  capture_tiers=["S+", "S", "A+"],
                  plat_capture_attempts=0,
                  notifier=notifier,
                  logger=logger)

logger.info("Bot started.")
bot.main_loop()
logger.info("Bot stopped.")

# fix: truth: quest first , congrats you have recevied a new crit later. currently doesn't work for this
# add IST time to all print statements, and print to a file instead of fix buffer terminal
# fix for double spawn captures. (need to attempt capture for second crit)
# fix name check for Dark Nessy. For now its justD