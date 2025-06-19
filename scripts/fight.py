import pyautogui
import time
import random

from human_mouse import HumanMouse
from notifier import Notifier
from fight_info import FightInfo

offset_coords = {
    "woolly": (-460, 380),
    "d_slithero": (-100, 200),
    "d_polter": (175, -40),
    "f_vhisp": (133, 260),
    "boneshee": (250, 80),
    "d_elefauna": (-170, 300),
    "b_flowerpiller": (-5, 105),
    "d_treemur": (325, 150),
    "sledgehog": (100, 270),
    "f_flintly": (-150, -20)
}

name_searches = {
    "woolly": ["W"],
    "d_slithero": ["D", "Sl"],
    "d_polter": ["D", "Po"],
    "f_vhisp": ["Fo", "V", "sp"],
    "boneshee": ["Bo", "on", "ee"],
    "d_elefauna": ["El", "f"],
    "b_flowerpiller": ["B", "we", "ted", "er"],
    "d_treemur": ["T", "mu", "ur"],
    "sledgehog": ["S", "ho"],
    "f_flintly": ["Fl", "Fo", "tl"]
}


class MiscritsBot:
    def __init__(self, search_crit, trainer_crit, notifier=None, plat_training=False):
        self.notifier = notifier
        self.trainer_crit = trainer_crit
        self.search_crit = search_crit
        self.fight_background = "photos/fight/" + search_crit + "/fight_background.png"
        self.crit_ref = "photos/fight/" + search_crit + "/ref.png"
        self.my_turn = "photos/fight/" + search_crit + "/my_turn.png"
        self.search_loc_x_off = offset_coords[search_crit][0]
        self.search_loc_y_off = offset_coords[search_crit][1]
        self.plat_training = plat_training
        self.fight_info = FightInfo()

    def look_for_target_until_found(self, target_path, confidence=0.8):
        count, stop = 0, 0
        while True:
            if stop > 1 and target_path == "photos/fight/common/search_for_miscrit.png":
                HumanMouse.random_move(x=random.randint(-400, -100), y=random.randint(-400, -100))
                return False
            if count > 2:
                HumanMouse.random_move()
                time.sleep(0.2)
                count = 0
            target = HumanMouse.locate_on_screen(target_path, confidence)
            if target:
                print(target_path, "found!")
                return target
            else:
                print(target_path, "not found!")
                time.sleep(1)
            count += 1
            stop += 1

    def look_for_fight_over_or_not(self, my_turn_path, fight_complete_path, confidence=0.8):
        while True:
            crit_name = self.fight_info.get_crit_name()
            print(crit_name, "encountered!")
            check = False
            if crit_name:
                for name_search in name_searches[self.search_crit]:
                    if name_search in crit_name:
                        check = True
                        break
                if check:
                    print("⚠️ " + self.search_crit + " Encountered!")
                    for _ in range(300):
                        if self.notifier:
                            self.notifier.send_telegram("⚠️ " + self.search_crit + " Encountered!")
                        time.sleep(1)

            my_turn = HumanMouse.locate_on_screen(my_turn_path, confidence)
            fight_complete = HumanMouse.locate_on_screen(fight_complete_path, confidence)
            if my_turn:
                print(my_turn_path, "found!")
                return "my_turn", my_turn
            if fight_complete:
                print(fight_complete_path, "found!")
                return "fight_complete", fight_complete
            else:
                print("no targets found!")
                time.sleep(1)

    def look_for_fight_or_potion(self, fight_path, potion_path, confidence=0.8):
        while True:
            fight = HumanMouse.locate_on_screen(fight_path, confidence)
            potion = HumanMouse.locate_on_screen(potion_path, confidence)
            if fight:
                print(fight_path, "found!")
                return "fight", fight
            if potion:
                print(potion_path, "found!")
                return "potion", potion
            else:
                print("no targets found!")
                time.sleep(1)

    def ready_to_train(self, image_path, confidence=0.8):
        is_ready_to_train = HumanMouse.locate_on_screen(image_path, confidence)
        if is_ready_to_train:
            print("ready to train!")
            return True
        else:
            print("not ready to train")
            return False

    def fight_on_location(self, image_path, confidence=0.8):
        loc = self.look_for_target_until_found(image_path)
        if not loc:
            return False

        loc = (loc[0] + self.search_loc_x_off + random.randint(-2, 2), loc[1] + self.search_loc_y_off + random.randint(-2, 2))
        HumanMouse.move_to(loc, random.randint(0, 10), random.randint(-10, 0))
        time.sleep(0.1)

        search_for_miscrit = self.look_for_target_until_found("photos/fight/common/search_for_miscrit.png")
        if not search_for_miscrit:
            return False
        time.sleep(0.2)
        HumanMouse.click()
        time.sleep(1.5)

        outcome, _ = self.look_for_fight_or_potion(self.fight_background, self.crit_ref)
        if outcome == "potion":
            time.sleep(17)
            return False

        while True:
            what_next, _ = self.look_for_fight_over_or_not(self.my_turn, "photos/fight/common/fight_continue.png")
            if what_next == 'my_turn':
                attack_move = self.look_for_target_until_found("photos/fight/common/" + self.trainer_crit + "_attack.png")
                HumanMouse.move_to(attack_move, 0, 0)
                HumanMouse.click()
            else:
                fight_complete = self.look_for_target_until_found("photos/fight/common/fight_continue.png")
                time.sleep(1.5)
                is_ready_to_train = self.ready_to_train("photos/fight/common/ready_to_train.png")
                HumanMouse.move_to(fight_complete, 0, 0)
                HumanMouse.click()
                return is_ready_to_train

    def main_loop(self):
        while True:
            is_ready_to_train = self.fight_on_location(self.crit_ref)
            if is_ready_to_train:
                train = self.look_for_target_until_found("photos/fight/common/train.png")
                HumanMouse.move_to(train, 0, 0)
                HumanMouse.click()

                trainer_crit_loc = self.look_for_target_until_found("photos/fight/common/" + self.trainer_crit + ".png")
                HumanMouse.move_to(trainer_crit_loc, 20, 40)
                HumanMouse.click()

                train_now = self.look_for_target_until_found("photos/fight/common/train_now.png")
                HumanMouse.move_to(train_now, 0, 0)
                HumanMouse.click()

                if self.plat_training:
                    time.sleep(1)
                    plat_train = self.look_for_target_until_found("photos/fight/common/plat_train.png")
                    HumanMouse.move_to(plat_train, 0, 0)
                    time.sleep(1)
                    HumanMouse.click()
                    time.sleep(0.5)
                    plat_train = HumanMouse.locate_on_screen("photos/fight/common/plat_train.png")
                    if plat_train:
                        HumanMouse.move_to(plat_train, 0, 0)
                        HumanMouse.click()
                    time.sleep(2)

                cont = self.look_for_target_until_found("photos/fight/common/train_continue.png")
                HumanMouse.move_to(cont, 0, 0)
                HumanMouse.click()
                time.sleep(0.1)
                HumanMouse.click()
                time.sleep(1)

                if HumanMouse.locate_on_screen("photos/fight/common/new_abilities.png"):
                    cont = self.look_for_target_until_found("photos/fight/common/abilities_continue.png")
                    HumanMouse.move_to(cont, 0, 0)
                    HumanMouse.click()
                    time.sleep(2)

                if HumanMouse.locate_on_screen("photos/fight/common/evolved.png"):
                    time.sleep(0.5)
                    eokay = self.look_for_target_until_found("photos/fight/common/evolved_okay.png")
                    HumanMouse.move_to(eokay, 0, 0)
                    HumanMouse.click()
                    time.sleep(1)

                cross = self.look_for_target_until_found("photos/fight/common/cross.png")
                HumanMouse.move_to(cross, 0, 0)
                HumanMouse.click()

                time.sleep(0.5)
                if HumanMouse.locate_on_screen("photos/fight/common/rank_up.png"):
                    time.sleep(0.5)
                    ruokay = self.look_for_target_until_found("photos/fight/common/rankup_okay.png")
                    HumanMouse.move_to(ruokay, 0, 0)
                    HumanMouse.click()
                    time.sleep(1)

            HumanMouse.random_move(x=random.randint(-400, -100), y=random.randint(-400, -100))
