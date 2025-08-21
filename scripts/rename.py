import time
import math
from human_mouse import HumanMouse
import pyautogui

# If no rename successfull that means stop program
# dont rename if already has rea/.. names. not needed but can do np
class Rename:
    def __init__(self, stat_image_list, region=(945, 645, 90, 170)) -> None:
        self.region = region
        self.stat_image_list = stat_image_list

    @staticmethod
    def locate_all_on_screen(template_path, min_distance=60, confidence=0.8,
                             exclude_template=None, exclude_box=None):
        """
        Locate all instances of template_path on screen, filter by min_distance,
        and optionally exclude detections if exclude_template is found
        in a box defined relative to the detection center.

        :param template_path: image to locate
        :param min_distance: minimum pixel distance between centers
        :param confidence: match confidence (requires opencv)
        :param exclude_template: optional image path to check for exclusion
        :param exclude_box: (offset_x, offset_y, width, height)
                            region relative to the detection center
        :return: list of center coordinates
        """
        # Step 1: get all matches
        matches = list(pyautogui.locateAllOnScreen(template_path, confidence=confidence))
        centers = [pyautogui.center(match) for match in matches]
        print("centers:", centers)

        # Step 2: filter duplicates by distance
        unique_centers = []
        for match in matches:
            center = pyautogui.center(match)
            if all(math.dist(center, existing) > min_distance for existing in unique_centers):
                unique_centers.append(center)

        print("Unique centers before exclusion:", unique_centers)

        # Step 3: exclusion filter
        if exclude_template and exclude_box:
            offset_x, offset_y, w, h = exclude_box
            filtered_centers = []
            for cx, cy in unique_centers:
                # region relative to center
                region = (cx + offset_x, cy + offset_y, w, h)

                found = pyautogui.locateOnScreen(exclude_template, region=region, confidence=0.9)
                if not found:
                    filtered_centers.append((cx, cy))
                else:
                    print(f"Excluded {cx, cy} because {exclude_template} was found nearby in {region}")

            unique_centers = filtered_centers

        print("Final centers:", unique_centers)
        return unique_centers
    
    def find_all_crits(self):

        a = self.locate_all_on_screen(
            "photos/rename/0xp.png",
            min_distance=15,
            confidence=0.8,
            exclude_template="photos/rename/11.png",
            exclude_box=(-125, -40, 60, 55)
            )
        
        return a

    def find_images(self):
        screenshot = pyautogui.screenshot(region=self.region)

        found_images = []
        found_count = 0

        for image_path in self.stat_image_list:
            location = pyautogui.locate(image_path, screenshot, confidence=0.99)
            if location:
                found_count += 1
                rw_stat = image_path.split('/')[2].split('.')[0]
                rw_stat = "".join(ch for ch in rw_stat if not ch.isdigit())
                rw_stat = rw_stat[1:] if rw_stat else rw_stat
                found_images.append(rw_stat)  # store both image and its location

        return found_count, found_images

    def rename(self, crit):
        HumanMouse.move_to(crit)
        HumanMouse.click()
        time.sleep(0.05) # TODO: optimize
        count, stats = self.find_images()
        if count != 1:
            return False
        settings = HumanMouse.locate_on_screen("photos/rename/settings.png")
        HumanMouse.move_to(settings)
        HumanMouse.click()
        time.sleep(0.05)

        rename_crit = HumanMouse.locate_on_screen(
            "photos/rename/rename_crit.png", confidence=0.99)
        HumanMouse.move_to(rename_crit)
        HumanMouse.click()
        time.sleep(0.1)

        rename = HumanMouse.locate_on_screen(
            "photos/rename/rename.png", confidence=0.9)
        HumanMouse.move_to(rename, 200, 80)
        HumanMouse.click()
        
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")

        # Type new text
        pyautogui.typewrite(stats[0], interval=0.05)

        save = HumanMouse.locate_on_screen(
            "photos/rename/save.png", confidence=0.9)
        HumanMouse.move_to(save)
        HumanMouse.click()
        time.sleep(1.3)

        return True

    def main(self):

        while True:
            crits = self.find_all_crits()
            for crit in crits:
                out = self.rename(crit)
                print("RENAME:", out)

            down = HumanMouse.locate_on_screen(
                "photos/rename/down.png", confidence=0.9)
            HumanMouse.move_to(down)
            HumanMouse.click()
            time.sleep(0.05)


# a = rename.find_all()
image_list = [
    "photos/rename/whp13.png",
    "photos/rename/whp14.png",
    "photos/rename/wea6.png",
    "photos/rename/wea7.png",
    "photos/rename/wpa6.png",
    "photos/rename/wpa7.png",
    "photos/rename/wpd6.png",
    "photos/rename/wpd7.png",
    "photos/rename/wed6.png",
    "photos/rename/wed7.png",

    "photos/rename/rhp13.png",
    "photos/rename/rhp14.png",
    "photos/rename/rea6.png",
    "photos/rename/rea7.png",
    "photos/rename/rpa6.png",
    "photos/rename/rpa7.png",
    "photos/rename/rpd6.png",
    "photos/rename/rpd7.png",
    "photos/rename/red6.png",
    "photos/rename/red7.png",
]

rename = Rename(image_list)
rename.main()
# crits = rename.find_all_crits()
# for crit in crits:
#     HumanMouse.move_to(crit)

# print(crits)
# region = (945, 645, 90, 170)
# count, images = rename.find_images(image_list, region)
# for loc in images:
#     HumanMouse.move_to(loc[1])
#     time.sleep(0.2)

# .strip('/')[2].strip('.')[0]
# images = [image.split('/')[2].split('.')[0] for image in images]
# print(count, images)
