import time
import random

from human_mouse import HumanMouse
from notifier import Notifier
from fight_info import FightInfo

offset_coords = {
    0: (-120, -200), 1:(-110, 50)
}


class MiscritsBot:
    def __init__(self, search_crit, trainer_crit, heal=False,
                 plat_training=False, capture_tiers=["B+", "A", "A+", "S+", "S"], 
                 move_page=1, plat_capture_attempts=0, notifier=None, logger=None):
        self.notifier = notifier
        self.logger = logger
        self.trainer_crit = trainer_crit
        self.search_crit = search_crit
        self.fight_background = "photos/fight/" + search_crit + "/fight_background.png"
        self.crit_ref = "photos/fight/" + search_crit + "/ref.png"
        self.my_turn = "photos/fight/" + search_crit + "/my_turn.png"
        # self.search_loc_x_off = offset_coords[search_crit][0]
        # self.search_loc_y_off = offset_coords[search_crit][1]
        self.plat_training = plat_training
        self.plat_capture_attempts = plat_capture_attempts
        self.fight_info = FightInfo()
        self.tries = 0
        self.capture_tiers = capture_tiers
        self.heal = heal
        self.move_page = move_page
        self.timer = {0: 0, 1: 0}
        self.alternate = 1

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
            # time.sleep(0.1)

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

    def fight_on_location(self):
        """Initiates a fight at the given location on screen."""

        target_location = self.look_for_target_until_found(self.crit_ref)
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
            # time.sleep(15)
            return False, None

        self.tries += 1
        return self._fight_loop()

    # -----------------------------
    # Helper methods
    # -----------------------------

    def _move_to_target_with_offset(self, location: tuple[int, int]) -> None:
        """Moves mouse to target location with random offsets."""
        x_offset = offset_coords[self.alternate][0] + random.randint(-2, 2)
        y_offset = offset_coords[self.alternate][1] + random.randint(-2, 2)
        adjusted_location = (location[0] + x_offset, location[1] + y_offset)

        HumanMouse.move_to(
            adjusted_location,
            random.randint(0, 5),
            random.randint(-5, 0)
        )

    def _initiate_fight(self) -> bool:
        """Clicks on 'search for miscrit' if available to start the fight."""
        elapsed_time = time.time() - self.timer[self.alternate]

        if elapsed_time < 25:
            print("[SLEEP] Waiting for",25 - elapsed_time,"seconds to start fight!")
            time.sleep(25 - elapsed_time)

        HumanMouse.click()
        self.timer[self.alternate] = time.time()
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
        page = 1
        crit_hp = "0"

        while True:
            turn_status = self.look_for_fight_over_or_not(
                self.my_turn,
                "photos/fight/common/fight_continue.png"
            )

            if turn_status == 'my_turn':
                crit_hp = self._gather_crit_info()

                self._log_fight_status(
                    crit_tier, crit_name, found,
                    capture_chance, capture_attempts, crit_hp
                )

                self._perform_attack(crit_hp)
            else:
                return self._finalize_fight(captured)

    def _gather_crit_info(self):
        """Fetches crit name, capture chance, tier, and notifies if found."""
        crit_name, capture_chance, crit_hp, crit_tier = \
            self.fight_info.get_capture_chance_crit_name_tier(name=False, chance=False, hp=True, tier=False)

        return crit_hp

    def _log_fight_status(self, crit_tier, crit_name, found,
                          capture_chance, capture_attempts, crit_hp) -> None:
        """Logs fight decision-making details."""
        print(
            f"[TURN] Tier={crit_tier} | Name={crit_name} | "
            f"Found={found} | CaptureChance={capture_chance}% | "
            f"Attempts={capture_attempts} | "
            f"CritHP={crit_hp}"
        )


    def use_magical_heal(self):
            items_image = f"photos/fight/common/items.png"
            items_move = self.look_for_target_until_found(items_image)

            print("[ACTION] Using Magical heal.")

            HumanMouse.move_to(items_move, 0, 0)
            HumanMouse.click()
            # HumanMouse.move_to(attack_move, 0, -200)
            time.sleep(0.1)

            HumanMouse.move_to(items_move, 642, 70)
            while not HumanMouse.locate_on_screen(
                "photos/fight/common/magical_heal.png", confidence=0.8):
                HumanMouse.click()
                time.sleep(0.05)
            
            magical_heal = f"photos/fight/common/magical_heal.png"
            magical_heal_move = self.look_for_target_until_found(magical_heal)

            HumanMouse.move_to(magical_heal_move, 0, 0)
            HumanMouse.click()
            time.sleep(0.1)

            abilities = f"photos/fight/common/abilities.png"
            abilities_move = self.look_for_target_until_found(abilities)

            HumanMouse.move_to(abilities_move, 0, 0)
            HumanMouse.click()

    def _perform_attack(self, crit_hp) -> None:
        """Executes an attack move if capture is not attempted."""

        if self.heal and int(crit_hp) < 100:
            self.use_magical_heal() #TODO: handle case where no magical heals
            time.sleep(1.5)
        else:
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
        time.sleep(0.5)  # necessary delay for UI

        print("[END] Fight complete.")

        HumanMouse.move_to(fight_continue, 0, 0)
        HumanMouse.click()

        return

    def main_loop(self):
        while True:
            self.alternate = 1 - self.alternate
            self.fight_on_location()
            time.sleep(0.5)  # TODO: Remove? Not needed after update? Wait between click continue and see if captured congrats.

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


            # --- Progress summary ---
            self.logger.info(
                f"Tries: {self.tries}"
            )

            HumanMouse.move_to((0, 0))
