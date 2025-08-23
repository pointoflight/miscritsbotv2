from fight_info import FightInfo
from fight import MiscritsBot
from notifier import Notifier
from human_mouse import HumanMouse
import pyautogui
import time
import random


# fight_info = FightInfo()

# crit_hp = fight_info.get_capture_chance_and_crit_name(name=False, chance=False)
# print(crit_hp)
# Example: get tier
# tier = fight_info.get_tier()
# print("Tier:", tier)

# Example: analyze capture chance
# capture_chance = crit_name = None

# while crit_name is None:
#     crit_name = fight_info.get_crit_name()
# print("Capture chance:", capture_chance)
# print("Critter name:", crit_name)

# ----------------------

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


# # while True:
# train_crits = HumanMouse.locate_all_on_screen("photos/fight/common/red.png", min_distance=30, confidence=0.8)
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

# green_matches = HumanMouse.locate_all_on_screen(
#                 "photos/breed/green.png",
#                 min_distance=15,
#                 confidence=0.85
#             )

# print("len(green_matches):", len(green_matches))

loc = HumanMouse.locate_on_screen("photos/breed/release_yes.png")
if loc:
    loc = (loc[0] + -0 + random.randint(-2, 2), loc[1] + 0 + random.randint(-2, 2))
    HumanMouse.move_to(loc) # random.randint(0, 10), random.randint(-10, 0))
else:
    print("not found")

# HumanMouse.move_to((0, 0))
# red_matches = HumanMouse.locate_all_on_screen("photos/fight/common/red.png", 
#                                                         min_distance=30, confidence=0.8)
# print("!! len(red_matches):", len(red_matches))
# import random

# # Parameters
# total_rolls = 1000000  # Total number of rolls
# streak_threshold = 3  # Wait for streak of at least 2 non-"1" rolls

# # Biased die probabilities
# prob_1 = 0.5
# prob_2 = 0.25
# prob_3 = 0.25

# sides = [1, 2, 3]
# weights = [prob_1, prob_2, prob_3]

# # Track results
# streak_strategy_wins = 0
# streak_strategy_guesses = 0

# current_streak = 0
# rolls = []

# # Pre-roll all results for consistent comparison
# for _ in range(total_rolls):
#     roll = random.choices(sides, weights=weights, k=1)[0]
#     rolls.append(roll)

# # Simulate Streak Strategy
# for roll in rolls:
#     if roll != 1:
#         current_streak += 1
#     else:
#         current_streak = 0

#     if current_streak >= streak_threshold:
#         next_roll = random.choices(sides, weights=weights, k=1)[0]
#         streak_strategy_guesses += 1
#         if next_roll == 1:
#             streak_strategy_wins += 1
#         current_streak = 0  # Reset after guessing

# # Simulate Always Guess "1" Strategy (same number of guesses)
# random_strategy_wins = 0
# for _ in range(streak_strategy_guesses):
#     roll = random.choices(sides, weights=weights, k=1)[0]
#     if roll == 1:
#         random_strategy_wins += 1

# # Results
# print(f"Total Rolls: {total_rolls}")
# print(f"Total Streak Strategy Guesses: {streak_strategy_guesses}")
# print(f"Streak Strategy Wins: {streak_strategy_wins}")
# print(f"Streak Strategy Win Rate: {streak_strategy_wins / streak_strategy_guesses * 100:.2f}%")

# print(f"Always Guess '1' Wins: {random_strategy_wins}")
# print(f"Always Guess '1' Win Rate: {random_strategy_wins / streak_strategy_guesses * 100:.2f}%")

