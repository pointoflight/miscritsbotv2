import time
import os
from human_mouse import HumanMouse

class Helper:

    @staticmethod
    def look_for_target_until_found(target_path: str, confidence: float = 0.8):
        """Continuously searches for a target on screen until found or timeout triggers."""

        while True:

            target = HumanMouse.locate_on_screen(target_path, confidence)
            if target:
                print(f"[SEARCH] {target_path} found!")
                return target

            print(f"[SEARCH] {target_path} not found.")
            time.sleep(0.2)
            
class BattleArena:

    def __init__(self):
        pass

    def go_to_arena(self):
        home = Helper.look_for_target_until_found("photos/ba/home.png")
        HumanMouse.move_to(home, -750, -200)
        HumanMouse.click()
        time.sleep(3.5)
        HumanMouse.click()

    def start_match(self):
        ba_girl = Helper.look_for_target_until_found("photos/ba/ba_girl.png")
        HumanMouse.move_to(ba_girl, -10, 0)
        time.sleep(1) # TODO: remove maybe not needed
        HumanMouse.click()
        time.sleep(3)
        join = Helper.look_for_target_until_found("photos/ba/join_battle.png")
        HumanMouse.move_to(join, 0, 0)
        HumanMouse.click()
        time.sleep(1.5)
        join_red = Helper.look_for_target_until_found("photos/ba/join_battle_red.png")
        HumanMouse.move_to(join_red, 0, 0)
        HumanMouse.click()

    def look_for_fight_over_or_not(self, 
                                   confidence: float = 0.8) -> str:
        """Checks if it's the player's turn or the fight is complete."""
        while True:
            my_turn = HumanMouse.locate_on_screen('photos/ba/my_turn.png', confidence)
            fight_complete = HumanMouse.locate_on_screen('photos/ba/ba_continue.png', confidence)

            if my_turn:
                print(f"[CHECK] my_turn.png found → my turn.")
                return "my_turn"

            if fight_complete:
                print(f"[CHECK] ba_continue.png found → fight complete.")
                return "fight_complete"

            print("[CHECK] No fight indicators found...")
            # time.sleep(0.1)

    def finish_match(self):
        ba_continue = Helper.look_for_target_until_found("photos/ba/ba_continue.png")
        HumanMouse.move_to(ba_continue, 0, 0)
        HumanMouse.click()
        time.sleep(0.5)

        cross = Helper.look_for_target_until_found("photos/ba/cross.png")
        HumanMouse.move_to(cross, 0, 0)
        HumanMouse.click()
        time.sleep(1.5)

        if HumanMouse.locate_on_screen('photos/ba/reward.png'):
            cross = Helper.look_for_target_until_found("photos/ba/cross.png")
            HumanMouse.move_to(cross, 0, 0)
            HumanMouse.click()
            time.sleep(1)

        keep_crit = None
        keep_crit = HumanMouse.locate_on_screen('photos/ba/keep_crit.png')
        if keep_crit:
            HumanMouse.move_to(keep_crit, 0, 0)
            HumanMouse.click()
            time.sleep(1)

    def go_home(self):
        home_button = Helper.look_for_target_until_found("photos/ba/home_button.png")
        HumanMouse.move_to(home_button, 0, 0)
        HumanMouse.click()
        time.sleep(0.5)
        home_yes = Helper.look_for_target_until_found("photos/ba/home_yes.png")
        HumanMouse.move_to(home_yes, 0, 0)
        HumanMouse.click()
        time.sleep(2)

    def perform_attack(self, move):
        items = HumanMouse.locate_on_screen('photos/fight/common/items.png')
        if move == 0:
            HumanMouse.move_to(items, -100, 70)
        elif move == 1:
            HumanMouse.move_to(items, 300, 70)
        HumanMouse.click()
        time.sleep(4)

    def play_match(self):
        move = 0
        while True:
            turn_status = self.look_for_fight_over_or_not()
            if turn_status == 'my_turn':
                self.perform_attack(move)
                move = 1 - move
            elif turn_status == 'fight_complete':
                self.finish_match()
                break

    def go_to_heal(self):
        home = Helper.look_for_target_until_found("photos/ba/home.png")
        HumanMouse.move_to(home, 320, 20)
        HumanMouse.click()
        time.sleep(3)
        HumanMouse.click()
        time.sleep(1)

    def heal(self):
        master = Helper.look_for_target_until_found("photos/ba/heal_master.png")
        HumanMouse.move_to(master, 0, 0)
        HumanMouse.click()
        time.sleep(4)

        heal = Helper.look_for_target_until_found("photos/ba/heal_crits.png")
        HumanMouse.move_to(heal, 0, 0)
        HumanMouse.click()
        time.sleep(8)

        heal_okay = Helper.look_for_target_until_found("photos/ba/heal_okay.png")
        HumanMouse.move_to(heal_okay, 0, 0)
        HumanMouse.click()
        time.sleep(1)

    def main(self):
        self.go_home()
        c = 0
        while c < 25:
            self.go_to_arena()
            self.start_match()
            self.play_match()
            self.go_home()
            self.go_to_heal()
            self.heal()
            self.go_home()
            c += 1
            print(c, "trials done")

ba = BattleArena()
ba.main()
# os.system("shutdown /s /f /t 0")
# ba.finish_match()