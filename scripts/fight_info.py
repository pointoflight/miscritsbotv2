import pyautogui
from PIL import ImageGrab, Image, ImageOps, ImageFilter
import pytesseract


class FightInfo:
    def __init__(self, tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def locate_on_screen(self, template_path, confidence=0.8):
        location = pyautogui.locateCenterOnScreen(template_path, confidence=confidence)
        return location

    def detect_text(self, image, custom_config):
        scale = 2
        scaled = image.resize((image.width * scale, image.height * scale))
        gray_scaled = scaled.convert("L")
        sharpened_scaled = gray_scaled.filter(ImageFilter.SHARPEN)
        sharpened_scaled = sharpened_scaled.filter(ImageFilter.SHARPEN)
        sharpened_scaled = sharpened_scaled.filter(ImageFilter.SHARPEN)
        inverted_scaled = ImageOps.invert(sharpened_scaled)
        text = pytesseract.image_to_string(inverted_scaled, config=custom_config)
        return text

    def get_tier(self):
        tiers = [
            ("S+", "photos/tiers/S+.png"),
            ("S", "photos/tiers/S.png"),
            ("A+", "photos/tiers/A+.png"),
            ("A", "photos/tiers/A.png"),
            ("B+", "photos/tiers/B+.png"),
            ("B", "photos/tiers/B.png"),
            ("C+", "photos/tiers/C+.png"),
            ("C", "photos/tiers/C.png"),
            ("D+", "photos/tiers/D+.png"),
            ("D", "photos/tiers/D.png"),
            ("F+", "photos/tiers/F+.png"),
            ("F", "photos/tiers/F.png"),
        ]

        for tier_name, template_path in tiers:
            if self.locate_on_screen(template_path, confidence=0.8):
                return tier_name

        return "NA/F-"

    def get_capture_chance(self):
        loc = self.locate_on_screen("photos/fight/common/capture.png", confidence=0.8)
        if loc:
            cc = (loc[0] - 25, loc[1] + 17, loc[0] + 28, loc[1] + 37)
            cc_image = ImageGrab.grab(bbox=cc)
            capture_chance_config = r'--psm 7 -c tessedit_char_whitelist=0123456789%'
            capture_chance = self.detect_text(cc_image, capture_chance_config)
            return capture_chance

        return None

    def get_crit_name(self):
        loc = self.locate_on_screen("photos/fight/common/capture.png", confidence=0.8)
        if loc:
            print("found capture!")
            crit_name = (loc[0] + 250, loc[1] - 90, loc[0] + 370, loc[1] - 72)
            crit_name_image = ImageGrab.grab(bbox=crit_name)
            crit_name_config = r'--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            critter_name = self.detect_text(crit_name_image, crit_name_config)
            return critter_name
        print("not found capture!")

        return None
