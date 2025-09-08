import time
from human_mouse import HumanMouse
import pyautogui

class BreedHelper:
    def look_for_target_until_found(self, target_path: str, confidence: float = 0.8):
        """Continuously searches for a target on screen until found or timeout triggers."""
        count = 0

        while count < 500:
            target = HumanMouse.locate_on_screen(target_path, confidence)
            if target:
                print(f"[SEARCH] {target_path} found!")
                return target

            # print(f"[SEARCH] {target_path} not found.")
            time.sleep(0.01)
            count += 1

        return None

    def main(self, stats):
        while True:
            brash = HumanMouse.locate_on_screen("photos/breed/brash.png")
            HumanMouse.move_to(brash, -100, 50)
            HumanMouse.click()
            time.sleep(1)

            message = HumanMouse.locate_on_screen("photos/breed/breed_message.png")
            HumanMouse.move_to(message, 0, 0)
            HumanMouse.click()
            time.sleep(0.1)

            filters = HumanMouse.locate_on_screen("photos/breed/filters.png")
            HumanMouse.move_to(filters, 0, 0)
            HumanMouse.click()
            time.sleep(0.1)

            spd_red = HumanMouse.locate_on_screen("photos/breed/speed_red.png")
            HumanMouse.move_to(spd_red, -70, 0)
            HumanMouse.click()
            time.sleep(0)

            search_box = HumanMouse.locate_on_screen("photos/breed/filter_miscrits.png")
            breeders = HumanMouse.locate_on_screen(f"photos/breed/breeders.png")

            for count, stat in enumerate(stats):
                
                HumanMouse.move_to(search_box, 0, 50)
                HumanMouse.click()
                pyautogui.hotkey("ctrl", "a")
                pyautogui.press("backspace")

                pyautogui.typewrite(stat, interval=0.05)
                time.sleep(0.1)

                stat_crit = HumanMouse.locate_on_screen(f"photos/breed/{stat}.png", confidence=0.95)
                if not stat_crit:
                    return
                
                HumanMouse.smooth_drag_to(stat_crit, (breeders[0] + count * 150, breeders[1] + 150))

            breed = HumanMouse.locate_on_screen("photos/breed/breed.png")
            HumanMouse.move_to(breed, 0, 0)
            HumanMouse.click()
            time.sleep(0.1)

            yes = HumanMouse.locate_on_screen("photos/breed/yes.png")
            HumanMouse.move_to(yes, 0, 0)
            HumanMouse.click()
            time.sleep(1.0)

            breed_result = self.look_for_target_until_found("photos/breed/green.png")

            if breed_result:
                green_matches = HumanMouse.locate_all_on_screen(
                    "photos/breed/green.png",
                    min_distance=15,
                    confidence=0.85
                )
            else:
                break

            print("len(green_matches):", len(green_matches))

            # return 
            if len(green_matches) >= 4:
                keep = HumanMouse.locate_on_screen("photos/breed/keep.png")
                HumanMouse.move_to(keep, 0, 0)
                HumanMouse.click()
            else:
                release = HumanMouse.locate_on_screen("photos/breed/release.png")
                HumanMouse.move_to(release, 0, 0)
                HumanMouse.click()
                time.sleep(0.1)
                release_yes = HumanMouse.locate_on_screen("photos/breed/release_yes.png")
                HumanMouse.move_to(release_yes, 0, 0)
                HumanMouse.click()
            
            time.sleep(1)


bh = BreedHelper()
bh.main(["ew", "hp", "ed"])