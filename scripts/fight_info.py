import pyautogui
from PIL import ImageGrab, Image, ImageOps, ImageFilter
import pytesseract
from human_mouse import HumanMouse

class FightInfo:
    def __init__(self, tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def locate_on_screen(self, template_path, confidence=0.8):
        location = pyautogui.locateCenterOnScreen(template_path, confidence=confidence)
        return location

    def _screenshot_region(self, region):
        """
        Take one screenshot of a region (left, top, width, height).
        Returns PIL image.
        """
        return pyautogui.screenshot(region=region)

    def locate_in_screenshot(self, haystack, template_path, region_offset, confidence=0.8):
        """
        Locate template inside a given PIL image.
        Returns absolute screen coordinates.
        """
        box = pyautogui.locate(template_path, haystack, confidence=confidence)
        if box:
            loc = pyautogui.center(box)
            return (loc[0] + region_offset[0], loc[1] + region_offset[1])
        return None

    def detect_text(self, image, custom_config):
        scale = 2
        scaled = image.resize((image.width * scale, image.height * scale))
        gray_scaled = scaled.convert("L")
        sharpened_scaled = gray_scaled.filter(ImageFilter.SHARPEN)
        sharpened_scaled = sharpened_scaled.filter(ImageFilter.SHARPEN)
        sharpened_scaled = sharpened_scaled.filter(ImageFilter.SHARPEN)
        inverted_scaled = ImageOps.invert(sharpened_scaled)
        # inverted_scaled.show()
        text = pytesseract.image_to_string(inverted_scaled, config=custom_config)
        return text

    def get_tier(self, screenshot, fight_region):
        tiers = [
            ("A+", "photos/tiers/A+.png"),
            ("A", "photos/tiers/A.png"),
            ("S+", "photos/tiers/S+.png"),
            ("S", "photos/tiers/S.png"),
            ("B+", "photos/tiers/B+.png")
        ]

        for tier_name, template_path in tiers:
            loc = self.locate_in_screenshot(screenshot, template_path, 
                                       region_offset=(fight_region[0], 
                                                      fight_region[1]))
            if loc:
                return tier_name

        return "N"
    
    def get_capture_chance_crit_name_tier(self, name=True, chance=True, hp=True, tier=True):
        loc = HumanMouse.locate_on_screen("photos/fight/common/book.png")

        critter_name = "--"
        capture_chance = "0"
        crit_hp = "100"
        crit_tier = 'N'

        if not loc:
            return ''.join(critter_name.split()), capture_chance, crit_hp, crit_tier 

        fight_region = (loc[0] - 270, loc[1] - 40, 700, 170)
        # fight_region = (500, 300, 900, 400)  # adjust to your fight UI box
        screenshot = self._screenshot_region(fight_region)

        # TODO: This loc is not really needed can use book location for offsets.
        loc = self.locate_in_screenshot(screenshot, "photos/fight/common/capture.png", 
                                   region_offset=(fight_region[0], fight_region[1]))

        if loc:
            if tier:
                crit_tier = self.get_tier(screenshot, fight_region)

            if name:
                crit_name = (loc[0] + 250, loc[1] - 90, loc[0] + 370, loc[1] - 72)
                crit_name_image = ImageGrab.grab(bbox=crit_name)
                # crit_name_image.show()
                crit_name_config = r'--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                critter_name = self.detect_text(crit_name_image, crit_name_config)

            if chance:
                cc = (loc[0] - 25, loc[1] + 17, loc[0] + 28, loc[1] + 37)
                cc_image = ImageGrab.grab(bbox=cc)
                # cc_image.show()
                capture_chance_config = r'--psm 7 -c tessedit_char_whitelist=0123456789%'
                capture_chance = self.detect_text(cc_image, capture_chance_config).replace('%', "").replace("\n", "")
                if not capture_chance:
                    capture_chance = "0"

            if hp:
                hp_box = (loc[0] - 270, loc[1] - 65, loc[0] - 200, loc[1] - 50)
                hp_image = ImageGrab.grab(bbox=hp_box)
                hp_config = r'--psm 7 -c tessedit_char_whitelist=0123456789/'
                crit_hp = self.detect_text(hp_image, hp_config).split('/')[0]
                if not crit_hp:
                    crit_hp = "0"

            return ''.join(critter_name.split()), capture_chance, "".join(crit_hp.split()), crit_tier

        print("not found capture!")
        return ''.join(critter_name.split()), capture_chance, crit_hp, crit_tier

