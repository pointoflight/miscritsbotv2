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
    "nessy": (-5, 105),
    "d_treemur": (325, 150),
    "sledgehog": (100, 270),
    "f_flintly": (-150, -20),
    "d_flutter": (180, -100),
    "munkee": (-250, -35),
    "ursiwave": (-70, 250),
    "gog": (-40, 325),
    "l_twiggum": (0, 0),
    "eggy": (-160, 70),
    "winne": (-260, -70),
    "peepsie": (-50, 180),
    "b_flue": (-50, 190),
    "dorux": (-70, 200),
    "fangly": (170, 320),
    "d_spin": (10, 170),
    "l_bludger": (140, 200),
    "alpha": (120, 120),
    "charpy": (130, 170),
    "freedom": (-30, 190),
    "defilio": (160, -190),
    "fennie": (-100, 200),
    "blazertooth": (0, 0),
    "podo": (-150, 130),
    "d_nessy": (10, 320),
    "manio": (50, 200),
    "l_frostmite": (310, -120)
}

name_searches = {
    "woolly": ["W"],
    "d_slithero": ["D", "Sl"],
    "d_polter": ["D", "Po"],
    "f_vhisp": ["Fo", "V", "sp"],
    "boneshee": ["Bo", "on", "ee"],
    "d_elefauna": ["El", "f"],
    "b_flowerpiller": ["B", "ted"],
    "nessy": ["N", "ss", "S", "Tw", "Sq"],
    "d_treemur": ["T", "mu", "ur"],
    "sledgehog": ["S", "ho"],
    "f_flintly": ["Fo"],
    "d_flutter": ["F", "ut"],
    "munkee": ["M", "K"],
    "ursiwave": ["U", "rs"],
    "gog": ["G"],
    "l_twiggum": ["T", "L"],
    "eggy": [],
    "winne": ["Wi", "Wl"],
    "peepsie": ["P", "ee"],
    "b_flue": ["B"],
    "dorux": ["rux", "x"],
    "fangly": ["Fan", "gly"],
    "d_spin": ["D", "S"],
    "l_bludger": ["Blud", "ger"],
    "alpha": ["Al", "pha"],
    "charpy": ["rpy", "py"],
    "freedom": ["F", "om", "ree"],
    "defilio": ["De"],
    "fennie": ["Fe"],
    "blazertooth": ["B"],
    "podo": ["P"],
    "d_nessy": ["DarkNessy"],
    "manio": ["Ma"],
    "l_frostmite": ["F", "ros"]
}


class MiscritsBot:
    def __init__(self, search_crit, trainer_crit, notifier=None, plat_training=False, capture_tiers=["B+", "A", "A+", "S+", "S"], plat_capture_attempts=0):
        self.notifier = notifier
        self.trainer_crit = trainer_crit
        self.search_crit = search_crit
        self.fight_background = "photos/fight/" + search_crit + "/fight_background.png"
        self.crit_ref = "photos/fight/" + search_crit + "/ref.png"
        self.my_turn = "photos/fight/" + search_crit + "/my_turn.png"
        self.search_loc_x_off = offset_coords[search_crit][0]
        self.search_loc_y_off = offset_coords[search_crit][1]
        self.plat_training = plat_training
        self.plat_capture_attempts = plat_capture_attempts
        self.fight_info = FightInfo()
        self.rs_captured = 0
        self.abprs_captured = 0
        self.sp_captured = 0
        self.scrits_captured = 0
        self.ap_reds = 0
        self.levels_up = 0
        self.tries = 0
        self.capture_tiers = capture_tiers

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
                time.sleep(0.2)
            count += 1
            stop += 1

    def crit_name_match(self, crit_name):
        if crit_name:
            for name_search in name_searches[self.search_crit]:
                if name_search in crit_name:
                    return True
        return False

    def notify_if_found(self, crit_name, crit_tier="N", capture_chance="0"):
        if self.crit_name_match(crit_name):
            print("⚠️ " + capture_chance + " " + crit_tier + " " + crit_name + self.search_crit + " encountered!")
            for _ in range(self.notifier.num_notifs):
                if self.notifier:
                    self.notifier.send_telegram("⚠️ " + capture_chance + "% " + crit_tier + " " + self.search_crit + " encountered!")
                time.sleep(1)
            return True
        return False

    def look_for_fight_over_or_not(self, my_turn_path, fight_complete_path, confidence=0.8):
        while True:

            my_turn = HumanMouse.locate_on_screen(my_turn_path, confidence)
            fight_complete = HumanMouse.locate_on_screen(fight_complete_path, confidence)
            if my_turn:
                print(my_turn_path, "found!")
                return "my_turn"
            if fight_complete:
                print(fight_complete_path, "found!")
                return "fight_complete"
            else:
                print("no targets found!")
                time.sleep(0.1)

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
                time.sleep(0.01)

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
            return False, None, None

        loc = (loc[0] + self.search_loc_x_off + random.randint(-2, 2), loc[1] + self.search_loc_y_off + random.randint(-2, 2))
        HumanMouse.move_to(loc, random.randint(0, 5), random.randint(-5, 0))
        time.sleep(0.1)

        search_for_miscrit = self.look_for_target_until_found("photos/fight/common/search_for_miscrit.png")
        if not search_for_miscrit:
            return False, None, None
        time.sleep(0.05)
        HumanMouse.click()
        time.sleep(1.5)

        outcome, _ = self.look_for_fight_or_potion(self.fight_background, self.crit_ref)
        if outcome == "potion":
            time.sleep(17)
            return False, None, None

        self.tries += 1
        capture_attempts = 0
        crit_name = '--'
        capture_chance = "0"
        crit_tier = "N"
        found = False

        while True:
            turn_ret = self.look_for_fight_over_or_not(self.my_turn, "photos/fight/common/fight_continue.png")

            if turn_ret == 'my_turn':
                print("-> my turn")

                # print("!! getting capture chance and crit_name")
                crit_name, capture_chance = self.fight_info.get_capture_chance_and_crit_name()
                # print("!! got capture chance and crit_name = ", crit_name, capture_chance)
                crit_tier = self.fight_info.get_tier()
                found = self.notify_if_found(crit_name, crit_tier=crit_tier, capture_chance=capture_chance)
                if not crit_name:
                    crit_name = "--"

                print("before deciding to capture/attack: ", crit_tier, crit_name, "found=", found, capture_chance, "%", "capture attempts = ", capture_attempts)
                # time.sleep(2)

                if (crit_tier in self.capture_tiers and int(capture_chance) >= 80 and capture_attempts == 0 and not found) or \
                    (found and int(capture_chance) >= 40 and capture_attempts - 1 < self.plat_capture_attempts):
                    capture_button = HumanMouse.locate_on_screen("photos/fight/common/capture.png", confidence=0.8)
                    if capture_button:
                        HumanMouse.move_to(capture_button, 0, 0)
                        HumanMouse.click()
                        HumanMouse.move_to(capture_button, 0, 200)
                        if capture_attempts > 0:
                            time.sleep(1)
                            plat_capture_button = HumanMouse.locate_on_screen("photos/fight/common/plat_capture.png", confidence=0.8)
                            HumanMouse.move_to(plat_capture_button, 0, 0)

                        capture_attempts += 1
                        time.sleep(5.4)

                        if HumanMouse.locate_on_screen("photos/fight/common/captured.png", confidence=0.8):
                            captured_okay = HumanMouse.locate_on_screen("photos/fight/common/captured_okay.png", confidence=0.8)
                            HumanMouse.move_to(captured_okay, 0, 0)
                            HumanMouse.click()
                            time.sleep(3)

                        continue
                else:
                    attack_move = self.look_for_target_until_found("photos/fight/common/" + self.trainer_crit + "_attack.png")
                    HumanMouse.move_to(attack_move, 0, 0)
                    HumanMouse.click()
                    HumanMouse.move_to(attack_move, 0, -200)
                    time.sleep(2)
            else:
                fight_complete = self.look_for_target_until_found("photos/fight/common/fight_continue.png")
                time.sleep(1.5) # TODO: maybe a little optimize. necessary to wait though as it takes time to appear.
                is_ready_to_train = self.ready_to_train("photos/fight/common/ready_to_train.png")
                HumanMouse.move_to(fight_complete, 0, 0)
                HumanMouse.click()
                return is_ready_to_train, found, crit_tier

    def train_crit(self, crit):
        HumanMouse.move_to(crit, 0, 0)
        HumanMouse.click()

        train_now = self.look_for_target_until_found("photos/fight/common/train_now.png")
        HumanMouse.move_to(train_now, 0, 0)
        HumanMouse.click()

        if self.plat_training:
            time.sleep(1) # TODO: optimize, maybe no sleep needed.
            plat_train = self.look_for_target_until_found("photos/fight/common/plat_train.png")
            HumanMouse.move_to(plat_train, 0, 0)
            time.sleep(1) # TODO: optimize, maybe no sleep needed.
            HumanMouse.click()
            time.sleep(0.5) # TODO: optimize, maybe no sleep needed.
            plat_train = HumanMouse.locate_on_screen("photos/fight/common/plat_train.png")
            if plat_train:
                HumanMouse.move_to(plat_train, 0, 0)
                HumanMouse.click()
            time.sleep(2)

        # print("self.plat_training = ", self.plat_training)
        time.sleep(1)
        train_continue_button = self.look_for_target_until_found("photos/fight/common/train_continue.png")
        # print("!!! moving to train continue")
        HumanMouse.move_to(train_continue_button, 0, 0)
        time.sleep(0.1)
        HumanMouse.click()
        time.sleep(0.1)
        HumanMouse.click()
        time.sleep(1)
        self.levels_up += 1
        # self.notifier.send_telegram("LEVEL UP! total levels = " + str(self.levels_up))

        if HumanMouse.locate_on_screen("photos/fight/common/new_abilities.png"):
            cont = self.look_for_target_until_found("photos/fight/common/abilities_continue.png")
            HumanMouse.move_to(cont, 0, 0)
            HumanMouse.click()
            time.sleep(2)

        if HumanMouse.locate_on_screen("photos/fight/common/evolved.png"):
            time.sleep(0.5) # TODO: not needed? why wait to click okay after already found? but only evolves 3 times max so only 1.5 seconds to be saved.
            eokay = self.look_for_target_until_found("photos/fight/common/evolved_okay.png")
            HumanMouse.move_to(eokay, 0, 0)
            HumanMouse.click()
            time.sleep(1) # TODO: optimize?

        
    def main_loop(self):
        while True:
            is_ready_to_train, fight_crit_found, fight_tier = self.fight_on_location(self.crit_ref)
            time.sleep(1) # Wait between clikc continue and see if captured congrats.
            
            print("! finished fight line 300")
            # quest success first and then captured.
            if HumanMouse.locate_on_screen("photos/fight/common/quest_success.png"):
                print("! quest success found")
                quest_okay = HumanMouse.locate_on_screen("photos/fight/common/quest_okay.png")
                if quest_okay:
                    HumanMouse.move_to(quest_okay, 0, 0)
                    HumanMouse.click()
            else:
                print("!quest success not found")
            
            if HumanMouse.locate_on_screen("photos/fight/common/congrats.png"):
                # captured_crit_name = self.fight_info.get_captured_crit_name()
                # print("captured crit name = ", captured_crit_name)

                # print("before keep/release: ")
                # print("fight_tier =", fight_tier)

                rs = HumanMouse.locate_on_screen("photos/fight/common/RS6.png", confidence=0.95) or \
                    HumanMouse.locate_on_screen("photos/fight/common/RS7.png", confidence=0.95)
                red_matches = HumanMouse.locate_all_on_screen("photos/fight/common/red.png", 
                                                              min_distance=30, confidence=0.8)
                ap_red = fight_tier == "A+" and len(red_matches) == 1
                abprs = (fight_tier == "A" and len(red_matches) == 1) or \
                    (fight_tier == "B+" and len(red_matches) == 2)
                
                print("!! len(red_matches):", len(red_matches))
                print("red_matches:" , red_matches)
                print("is RS:" , rs)
                print("fight_crit_found:", fight_crit_found)

                if fight_crit_found:
                    self.scrits_captured += 1
                    # self.notifier.send_telegram("⚠️ search crit CAPTURED!")
                elif rs:
                    if fight_tier == "A+": # same as len(red_matches) == 1 cuz it's already RS.
                        self.rs_captured += 1
                    elif abprs:
                        self.abprs_captured += 1
                    # self.notifier.send_telegram("RS CAPTURED!")
                elif fight_tier == "S+":
                    self.sp_captured += 1
                    # self.notifier.send_telegram("S+ CAPTURED!")
                elif ap_red:
                    self.ap_reds += 1
                    # self.notifier.send_telegram("A+ red CAPTURED!")

                if (rs and (abprs or fight_tier == "A+")) or fight_crit_found: # or fight_tier in ["S+", "S"] or ap_red:
                    keep = HumanMouse.locate_on_screen("photos/fight/common/keep.png")
                    if keep:
                        HumanMouse.move_to(keep, 0, 0)
                        HumanMouse.click()
                        if fight_crit_found:
                            self.notifier.send_telegram(":) " + fight_tier + " " + self.search_crit + " CAPTURED!")
                        
                        # if False: # TODO: add feature to move crit into inventory if in team after capture.
                        # my_crits = HumanMouse.locate_on_screen("photos/fight/common/my_miscrits.png")
                        # if my_crits:
                        #     HumanMouse.move_to(my_crits, 0, 0)
                        #     HumanMouse.click()
                        #     time.sleep(0.3) # TODO: maybe optimize little everywhere not just here. All sleeps.
                        #     order_of = HumanMouse.locate_on_screen("photos/fight/common/order_of.png")
                        #     if order_of:
                        #         order_of = (order_of[0], order_of[1] + 200)
                        #         HumanMouse.smooth_drag(order_of, 0, 200)
                        #         save = HumanMouse.locate_on_screen("photos/fight/common/save.png")
                        #         HumanMouse.move_to(save, 0, 0)
                        #         HumanMouse.click()
                        #         time.sleep(0.8)
                else:
                    release = HumanMouse.locate_on_screen("photos/fight/common/release.png")
                    if release:
                        HumanMouse.move_to(release, 0, 0)
                        HumanMouse.click()
                        release_confirm = self.look_for_target_until_found("photos/fight/common/release_confirm.png")
                        release_yes = HumanMouse.locate_on_screen("photos/fight/common/release_yes.png")
                        HumanMouse.move_to(release_yes, 0, 0)
                        HumanMouse.click()
                        time.sleep(2.6)


            if is_ready_to_train:
                train = self.look_for_target_until_found("photos/fight/common/train.png")
                HumanMouse.move_to(train, 0, 0)
                HumanMouse.click()
                time.sleep(0.1)
                train_crits = HumanMouse.locate_all_on_screen(
                    "photos/fight/common/ready_to_train_box.png", min_distance=40, confidence=0.6)
                print("!! train crits length:", len(train_crits))
                for crit in train_crits:
                    self.train_crit(crit)

                cross = self.look_for_target_until_found("photos/fight/common/cross.png")
                HumanMouse.move_to(cross, 0, 0)
                HumanMouse.click()
                time.sleep(1)
            
            if HumanMouse.locate_on_screen("photos/fight/common/quest_success.png"):
                print("! quest success found")
                quest_okay = HumanMouse.locate_on_screen("photos/fight/common/quest_okay.png")
                if quest_okay:
                    HumanMouse.move_to(quest_okay, 0, 0)
                    HumanMouse.click()
            else:
                print("!quest success not found")

                for _ in range(3):
                    time.sleep(0.5)
                    if HumanMouse.locate_on_screen("photos/fight/common/rank_up.png"):
                        time.sleep(0.5) # TODO: same here, max 3 times. 
                        ruokay = self.look_for_target_until_found("photos/fight/common/rankup_okay.png")
                        HumanMouse.move_to(ruokay, 0, 0)
                        HumanMouse.click()
                        time.sleep(1)
                    else:
                        break
            
            print("search crits:", self.scrits_captured, "RS:", self.rs_captured, "a/b+ RS:", self.abprs_captured, \
                  "S+:", self.sp_captured, "A+ reds:", self.ap_reds, "levels up:", self.levels_up, "tries:", self.tries)
            
            HumanMouse.random_move(x=random.randint(-400, -100), y=random.randint(-400, -100))
