from fight_info import FightInfo

fight_info = FightInfo()

# Example: get tier
# tier = fight_info.get_tier()
# print("Tier:", tier)

# Example: analyze capture chance
capture_chance = crit_name = None

while crit_name is None:
    crit_name = fight_info.get_crit_name()
print("Capture chance:", capture_chance)
print("Critter name:", crit_name)
