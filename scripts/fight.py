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
    "l_frostmite": (310, -120),
    "f_waddles": (-200, 50),
    "inferno": (0, 100),
    "d_jelly": (-10, 200),
    "f_croaky": (10, -200),
    "ekkult": (70, 180),
    "gravitron": (-150, 120),
    "eclipso": (-100, 170),
    "smolderfry": (-200, 0),
    "pyrex": (70, -150),
    "lithos": (-170, 180),
    "void": (-120, -190),
    "beat": (-280, -20)
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
    "l_frostmite": ["F", "ros"],
    "f_waddles": ["Fo", "W"],
    "inferno": ["In", "fer"],
    "d_jelly": ["J", "lly"],
    "f_croaky": ["Fo", "Croa"],
    "ekkult": ["E", "kk"],
    "gravitron": ["G", "rav"],
    "eclipso": ["Ec", "lip"],
    "smolderfry": ["Sm", "old"],
    "pyrex": ["Py", "ex"],
    "lithos": ["Li", "hos"],
    "void": ["Vo", "ron"],
    "beat": ["Be", "eo"]
}


class MiscritsBot:
    def __init__(self, search_crit, trainer_crit, notifier=None, logger=None,
                 plat_training=False, capture_tiers=["B+", "A", "A+", "S+", "S"], 
                 plat_capture_attempts=0):
        self.notifier = notifier
        self.logger = logger
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

    def look_for_target_until_found(self, target_path: str, confidence: float = 0.8):
        """Continuously searches for a target on screen until found or timeout triggers."""
        count, stop = 0, 0

        while True:
            if stop > 1 and target_path == "photos/fight/common/search_for_miscrit.png":
                HumanMouse.move_to((0, 0))
                print(f"[SEARCH] {target_path} - giving up after {stop} attempts.")
                return False

            if count > 2:
                time.sleep(0.2)
                count = 0

            target = HumanMouse.locate_on_screen(target_path, confidence)
            if target:
                print(f"[SEARCH] {target_path} found!")
                return target

            print(f"[SEARCH] {target_path} not found.")
            time.sleep(0.2)

            count += 1
            stop += 1

    def crit_name_match(self, crit_name: str) -> bool:
        """Checks if a given crit_name matches any of the search patterns."""
        if not crit_name:
            return False

        for name_search in name_searches[self.search_crit]:
            if name_search in crit_name:
                return True
        return False

    def notify_if_found(
        self, crit_name: str, crit_tier: str = "N", capture_chance: str = "0"
    ) -> bool:
        """Notifies when the searched crit is found."""
        if self.crit_name_match(crit_name):
            message = (
                f"⚠️ {capture_chance}% {crit_tier} {crit_name} "
                f"{self.search_crit} encountered!"
            )
            self.logger.info(f"[NOTIFY] {message}")

            for _ in range(self.notifier.num_notifs):
                if self.notifier:
                    self.notifier.send_telegram(message)
                time.sleep(1)

            return True

        return False

    def look_for_fight_over_or_not(
        self, my_turn_path: str, fight_complete_path: str, confidence: float = 0.8
    ) -> str:
        """Checks if it's the player's turn or the fight is complete."""
        while True:
            my_turn = HumanMouse.locate_on_screen(my_turn_path, confidence)
            fight_complete = HumanMouse.locate_on_screen(fight_complete_path, confidence)

            if my_turn:
                print(f"[CHECK] {my_turn_path} found → my turn.")
                return "my_turn"

            if fight_complete:
                print(f"[CHECK] {fight_complete_path} found → fight complete.")
                return "fight_complete"

            print("[CHECK] No fight indicators found...")
            time.sleep(0.1)

    def look_for_fight_or_potion(
        self, fight_path: str, potion_path: str, confidence: float = 0.8
    ) -> tuple[str, tuple[int, int]]:
        """Determines whether a fight or potion prompt is found."""
        while True:
            fight = HumanMouse.locate_on_screen(fight_path, confidence)
            potion = HumanMouse.locate_on_screen(potion_path, confidence)

            if fight:
                print(f"[CHECK] {fight_path} found → fight.")
                return "fight", fight

            if potion:
                print(f"[CHECK] {potion_path} found → potion.")
                return "potion", potion

            print("[CHECK] No fight/potion indicators found...")
            time.sleep(0.01)

    def ready_to_train(self, image_path: str, confidence: float = 0.8) -> bool:
        """Checks if crit is ready to train."""
        is_ready = HumanMouse.locate_on_screen(image_path, confidence)

        if is_ready:
            print("[TRAIN] Ready to train!")
            return True

        print("[TRAIN] Not ready to train.")
        return False

    def fight_on_location(self, image_path):
        """Initiates a fight at the given location on screen."""

        target_location = self.look_for_target_until_found(image_path)
        if not target_location:
            return False, None

        self._move_to_target_with_offset(target_location)
        time.sleep(0.1)

        if not self._initiate_fight():
            return False, None

        outcome, _ = self.look_for_fight_or_potion(
            self.fight_background,
            self.crit_ref
        )

        if outcome == "potion":
            time.sleep(17)
            return False, None

        self.tries += 1
        return self._fight_loop()

    # -----------------------------
    # Helper methods
    # -----------------------------

    def _move_to_target_with_offset(self, location: tuple[int, int]) -> None:
        """Moves mouse to target location with random offsets."""
        x_offset = self.search_loc_x_off + random.randint(-2, 2)
        y_offset = self.search_loc_y_off + random.randint(-2, 2)
        adjusted_location = (location[0] + x_offset, location[1] + y_offset)

        HumanMouse.move_to(
            adjusted_location,
            random.randint(0, 5),
            random.randint(-5, 0)
        )

    def _initiate_fight(self) -> bool:
        """Clicks on 'search for miscrit' if available to start the fight."""
        search_button = self.look_for_target_until_found(
            "photos/fight/common/search_for_miscrit.png"
        )
        if not search_button:
            return False

        time.sleep(0.05)
        HumanMouse.click()
        time.sleep(1.5)
        return True

    def _fight_loop(self):
        """Main fight loop handling turns, capture, and attacks."""
        capture_attempts = 0
        captured = False
        crit_name = "--"
        capture_chance = "0"
        crit_tier = "N"
        found = False

        while True:
            turn_status = self.look_for_fight_over_or_not(
                self.my_turn,
                "photos/fight/common/fight_continue.png"
            )

            if turn_status == 'my_turn':
                (crit_name,
                 capture_chance,
                 crit_tier,
                 found) = self._gather_crit_info()

                self._log_fight_status(
                    crit_tier, crit_name, found,
                    capture_chance, capture_attempts
                )

                if self._should_attempt_capture(
                    crit_tier, capture_chance,
                    capture_attempts, found
                ):
                    captured, capture_attempts = self._attempt_capture(
                        crit_tier, found, capture_attempts
                    )
                    if captured:
                        continue
                else:
                    self._perform_attack()
            else:
                return self._finalize_fight(captured)

    def _gather_crit_info(self):
        """Fetches crit name, capture chance, tier, and notifies if found."""
        crit_name, capture_chance = self.fight_info.get_capture_chance_and_crit_name()
        crit_tier = self.fight_info.get_tier()
        found = self.notify_if_found(
            crit_name, crit_tier=crit_tier, capture_chance=capture_chance
        )

        if not crit_name:
            crit_name = "--"

        return crit_name, capture_chance, crit_tier, found

    def _log_fight_status(self, crit_tier, crit_name, found,
                          capture_chance, capture_attempts) -> None:
        """Logs fight decision-making details."""
        print(
            f"[TURN] Tier={crit_tier} | Name={crit_name} | "
            f"Found={found} | CaptureChance={capture_chance}% | "
            f"Attempts={capture_attempts}"
        )

    def _should_attempt_capture(self, crit_tier, capture_chance,
                                capture_attempts, found) -> bool:
        """Decides whether to attempt capturing the crit."""
        capture_chance = int(capture_chance)

        return (
            (crit_tier in self.capture_tiers
             and capture_chance >= 80
             and capture_attempts == 0
             and not found)
            or
            (found and capture_chance >= 55
             and capture_attempts - 1 < self.plat_capture_attempts)
        )

    def _attempt_capture(self, crit_tier, found, capture_attempts):
        """Handles crit capture attempts including plat captures."""
        capture_button = HumanMouse.locate_on_screen(
            "photos/fight/common/capture.png", confidence=0.8
        )
        if not capture_button:
            return False, capture_attempts

        print(f"[ACTION] Attempting capture (Attempt #{capture_attempts + 1})")

        HumanMouse.move_to(capture_button, 0, 0)
        HumanMouse.click()
        HumanMouse.move_to(capture_button, 0, 200)

        if capture_attempts > 0:
            print("[ACTION] Performing plat capture...")
            time.sleep(1)
            plat_capture_button = HumanMouse.locate_on_screen(
                "photos/fight/common/plat_capture.png", confidence=0.8
            )
            HumanMouse.move_to(plat_capture_button, 0, 0)

        capture_attempts += 1
        time.sleep(5.4)

        captured = False
        if HumanMouse.locate_on_screen(
            "photos/fight/common/captured.png", confidence=0.8
        ):
            print("[RESULT] Capture successful!")
            captured = self.capture_or_release(crit_tier, found)
            time.sleep(1)
        else:
            print("[RESULT] Capture failed.")

        return captured, capture_attempts

    def _perform_attack(self) -> None:
        """Executes an attack move if capture is not attempted."""
        attack_image = f"photos/fight/common/{self.trainer_crit}_attack.png"
        attack_move = self.look_for_target_until_found(attack_image)

        print("[ACTION] Attacking instead of capturing.")

        HumanMouse.move_to(attack_move, 0, 0)
        HumanMouse.click()
        HumanMouse.move_to(attack_move, 0, -200)
        time.sleep(2)

    def _finalize_fight(self, captured: bool):
        """Handles cleanup when the fight is over."""
        fight_continue = self.look_for_target_until_found(
            "photos/fight/common/fight_continue.png"
        )
        time.sleep(1.5)  # necessary delay for UI
        is_ready_to_train = self.ready_to_train(
            "photos/fight/common/ready_to_train.png"
        )

        print("[END] Fight complete. Ready to train:", is_ready_to_train)

        HumanMouse.move_to(fight_continue, 0, 0)
        HumanMouse.click()

        return is_ready_to_train, captured

    def train_crit(self, crit):
        print(f"[TRAIN] Starting training for crit at {crit}")

        HumanMouse.move_to(crit, 0, 0)
        HumanMouse.click()

        train_now = self.look_for_target_until_found("photos/fight/common/train_now.png")
        print("[TRAIN] 'Train Now' button found, proceeding.")
        HumanMouse.move_to(train_now, 0, 0)
        HumanMouse.click()

        if self.plat_training:
            print("[TRAIN] Platinum training enabled.")
            time.sleep(1)  # TODO: optimize, maybe no sleep needed.

            plat_train = self.look_for_target_until_found("photos/fight/common/plat_train.png")
            print("[TRAIN] 'Platinum Train' option found.")
            HumanMouse.move_to(plat_train, 0, 0)
            time.sleep(1)  # TODO: optimize, maybe no sleep needed.
            HumanMouse.click()

            time.sleep(0.5)  # TODO: optimize, maybe no sleep needed.
            plat_train = HumanMouse.locate_on_screen("photos/fight/common/plat_train.png")
            if plat_train:
                print("[TRAIN] Clicking 'Platinum Train' again (detected still visible).")
                HumanMouse.move_to(plat_train, 0, 0)
                HumanMouse.click()

            time.sleep(2)

        time.sleep(1)
        train_continue_button = self.look_for_target_until_found("photos/fight/common/train_continue.png")
        print("[TRAIN] Found 'Continue' button after training.")
        HumanMouse.move_to(train_continue_button, 0, 0)
        time.sleep(0.1)
        HumanMouse.click()
        time.sleep(0.1)
        HumanMouse.click()
        time.sleep(1)

        self.levels_up += 1
        print(f"[TRAIN] Training complete. Total levels gained so far: {self.levels_up}")

        if HumanMouse.locate_on_screen("photos/fight/common/new_abilities.png"):
            print("[TRAIN] New abilities detected — continuing.")
            cont = self.look_for_target_until_found("photos/fight/common/abilities_continue.png")
            HumanMouse.move_to(cont, 0, 0)
            HumanMouse.click()
            time.sleep(2)

        if HumanMouse.locate_on_screen("photos/fight/common/evolved.png"):
            print("[TRAIN] Evolution detected!")
            time.sleep(0.5)  # TODO: optimize, maybe no sleep needed.
            eokay = self.look_for_target_until_found("photos/fight/common/evolved_okay.png")
            HumanMouse.move_to(eokay, 0, 0)
            HumanMouse.click()
            print("[TRAIN] Evolution confirmed and continued.")
            time.sleep(1)  # TODO: optimize?

    def capture_or_release(self, fight_tier: str, fight_crit_found: bool) -> bool:
        """Decides whether to keep or release a captured crit."""

        # Locate possible RS indicators
        rs = (
            HumanMouse.locate_on_screen("photos/fight/common/RS6.png", confidence=0.95)
            or HumanMouse.locate_on_screen("photos/fight/common/RS7.png", confidence=0.95)
        )

        # Locate all red matches on screen
        red_matches = HumanMouse.locate_all_on_screen(
            "photos/fight/common/red.png",
            min_distance=30,
            confidence=0.8
        )

        # Capture conditions
        ap_red = fight_tier == "A+" and len(red_matches) == 1
        abprs = (
            (fight_tier == "A" and len(red_matches) == 1)
            or (fight_tier == "B+" and len(red_matches) == 2)
        )

        # -----------------------------
        # Debug logging
        # -----------------------------
        print(
            f"[CAPTURE DECISION] "
            f"Tier={fight_tier} | Found={fight_crit_found} | "
            f"RS={bool(rs)} | RedMatches={len(red_matches)}"
        )

        # -----------------------------
        # Update internal counters
        # -----------------------------
        if fight_crit_found:
            self.scrits_captured += 1
            print("[CAPTURE] Search crit captured!")
            # self.notifier.send_telegram("⚠️ search crit CAPTURED!")

        elif rs:
            if fight_tier == "A+":  # equivalent to len(red_matches) == 1
                self.rs_captured += 1
                print("[CAPTURE] RS A+ captured!")
            elif abprs:
                self.abprs_captured += 1
                print("[CAPTURE] RS A/B+ captured!")
            # self.notifier.send_telegram("RS CAPTURED!")

        elif fight_tier == "S+":
            self.sp_captured += 1
            print("[CAPTURE] S+ captured!")
            # self.notifier.send_telegram("S+ CAPTURED!")

        elif ap_red:
            self.ap_reds += 1
            print("[CAPTURE] A+ red captured!")
            # self.notifier.send_telegram("A+ red CAPTURED!")

        # -----------------------------
        # Decide whether to keep or release
        # -----------------------------
        keep_condition = (rs and (abprs or fight_tier == "A+")) or fight_crit_found or fight_tier in ["S+", "S"]

        if keep_condition:
            keep = HumanMouse.locate_on_screen("photos/fight/common/captured_keep.png")
            if keep:
                print("[ACTION] Keeping crit...")
                HumanMouse.move_to(keep, 0, 0)
                HumanMouse.click()
                time.sleep(1.6)

                if fight_crit_found:
                    msg = f":) {fight_tier} {self.search_crit} CAPTURED!"
                    self.notifier.send_telegram(msg)

                return True

        else:
            release = HumanMouse.locate_on_screen("photos/fight/common/captured_release.png")
            if release:
                print("[ACTION] Releasing crit...")
                HumanMouse.move_to(release, 0, 0)
                HumanMouse.click()

                release_confirm = self.look_for_target_until_found(
                    "photos/fight/common/release_confirm.png"
                )
                release_yes = HumanMouse.locate_on_screen(
                    "photos/fight/common/release_yes.png"
                )
                HumanMouse.move_to(release_yes, 0, 0)
                HumanMouse.click()
                time.sleep(1.6)  # TODO: optimize, maybe no sleep needed.

                return False

    def remove_crit_from_team(self):
        my_crits = HumanMouse.locate_on_screen("photos/fight/common/my_miscrits.png")
        if my_crits:
            HumanMouse.move_to(my_crits, 0, 0)
            HumanMouse.click()
            time.sleep(0.3) # TODO: maybe optimize little everywhere not just here. All sleeps.
            order_of = HumanMouse.locate_on_screen("photos/fight/common/order_of.png")
            if order_of:
                order_of = (order_of[0], order_of[1] + 200)
                HumanMouse.smooth_drag(order_of, 0, 200)
                save = HumanMouse.locate_on_screen("photos/fight/common/save.png")
                HumanMouse.move_to(save, 0, 0)
                HumanMouse.click()
                time.sleep(0.8)

    def main_loop(self):
        while True:
            is_ready_to_train, captured = self.fight_on_location(self.crit_ref)
            time.sleep(1)  # TODO: Remove? Not needed after update? Wait between click continue and see if captured congrats.

            print("[MAIN] Fight finished (line 300)")

            # --- Quest success handling ---
            if HumanMouse.locate_on_screen("photos/fight/common/quest_success.png"):
                print("[QUEST] Success found")
                time.sleep(1)
                quest_okay = HumanMouse.locate_on_screen("photos/fight/common/quest_okay.png")
                if quest_okay:
                    HumanMouse.move_to(quest_okay, 0, 0)
                    HumanMouse.click()
                    print("[QUEST] Confirmed success (clicked OK)")

            # --- Remove captured crit from team (not needed when team is full - 4 crits) ---
            # if captured:
            #     self.remove_crit_from_team()

            # --- Training check ---
            if is_ready_to_train:
                print("[TRAIN] Crit(s) ready to train")
                train = self.look_for_target_until_found("photos/fight/common/train.png")
                HumanMouse.move_to(train, 0, 0)
                HumanMouse.click()
                time.sleep(0.1)

                train_crits = HumanMouse.locate_all_on_screen(
                    "photos/fight/common/ready_to_train_box.png", min_distance=40, confidence=0.6
                )
                # print(f"[TRAIN] Crits ready to train: {len(train_crits)}")
                for crit in train_crits:
                    self.train_crit(crit)

                cross = self.look_for_target_until_found("photos/fight/common/cross.png")
                HumanMouse.move_to(cross, 0, 0)
                HumanMouse.click()
                time.sleep(1)

            # --- Quest success check (again) ---
            if HumanMouse.locate_on_screen("photos/fight/common/quest_success.png"):
                print("[QUEST] Success found (second check)")
                quest_okay = HumanMouse.locate_on_screen("photos/fight/common/quest_okay.png")
                if quest_okay:
                    HumanMouse.move_to(quest_okay, 0, 0)
                    HumanMouse.click()
                    print("[QUEST] Confirmed success (clicked OK)")
            # else:
            #     print("[QUEST] No success detected (second check)")

            for attempt in range(3):
                time.sleep(0.5)
                if HumanMouse.locate_on_screen("photos/fight/common/rank_up.png"):
                    time.sleep(0.5)  # TODO: same here, max 3 times. 
                    ruokay = self.look_for_target_until_found("photos/fight/common/rankup_okay.png")
                    HumanMouse.move_to(ruokay, 0, 0)
                    HumanMouse.click()
                    print(f"[RANK-UP] Rank-up {attempt+1}")
                    time.sleep(1)
                else:
                    break

            # --- Progress summary ---
            self.logger.info(
                f"[STATS] Search Crits: {self.scrits_captured} | "
                f"RS: {self.rs_captured} | "
                f"A/B+ RS: {self.abprs_captured} | "
                f"S+: {self.sp_captured} | "
                f"A+ Reds: {self.ap_reds} | "
                f"Levels Up: {self.levels_up} | "
                f"Tries: {self.tries}"
            )

            HumanMouse.move_to((0, 0))
