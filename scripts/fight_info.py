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
        # inverted_scaled.show()
        text = pytesseract.image_to_string(inverted_scaled, config=custom_config)
        return text

    def get_tier(self):
        tiers = [
            ("A+", "photos/tiers/A+.png"),
            ("A", "photos/tiers/A.png"),
            ("S+", "photos/tiers/S+.png"),
            ("S", "photos/tiers/S.png"),
            ("B+", "photos/tiers/B+.png")
            # ("B", "photos/tiers/B.png"),
            # ("C+", "photos/tiers/C+.png"),
            # ("C", "photos/tiers/C.png"),
            # ("D+", "photos/tiers/D+.png"),
            # ("D", "photos/tiers/D.png"),
            # ("F+", "photos/tiers/F+.png"),
            # ("F", "photos/tiers/F.png")
        ]

        for tier_name, template_path in tiers:
            if self.locate_on_screen(template_path, confidence=0.8):
                return tier_name

        return "N"

    def get_capture_chance(self):
        _, chance = self.get_capture_chance_and_crit_name(name=False)
        return chance

    def get_crit_name(self):
        crit_name, _ = self.get_capture_chance_and_crit_name(chance=False)
        return crit_name
    
    def get_capture_chance_and_crit_name(self, name=True, chance=True, hp=True):
        loc = self.locate_on_screen("photos/fight/common/capture.png", confidence=0.8)
        critter_name = "--"
        capture_chance = "0"
        crit_hp = "100"

        if loc:
            if name:
                crit_name = (loc[0] + 250, loc[1] - 90, loc[0] + 370, loc[1] - 72)
                crit_name_image = ImageGrab.grab(bbox=crit_name)
                crit_name_config = r'--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                critter_name = self.detect_text(crit_name_image, crit_name_config)

            if chance:
                cc = (loc[0] - 25, loc[1] + 17, loc[0] + 28, loc[1] + 37)
                cc_image = ImageGrab.grab(bbox=cc)
                capture_chance_config = r'--psm 7 -c tessedit_char_whitelist=0123456789%'
                capture_chance = self.detect_text(cc_image, capture_chance_config)
                capture_chance = capture_chance.strip().rstrip('%')
                if not capture_chance:
                    capture_chance = "0"

            if hp:
                cc = (loc[0] - 270, loc[1] - 65, loc[0] - 200, loc[1] - 50)
                hp_image = ImageGrab.grab(bbox=cc)
                hp_config = r'--psm 7 -c tessedit_char_whitelist=0123456789/'
                crit_hp = self.detect_text(hp_image, hp_config)
                crit_hp = crit_hp.split('/')[0]
                if not crit_hp:
                    crit_hp = "0"


            return ''.join(critter_name.split()), capture_chance, crit_hp
        
        print("not found capture!")
        return ''.join(critter_name.split()), capture_chance, crit_hp

