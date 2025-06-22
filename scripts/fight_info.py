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

        return "NA/F-"

    def get_capture_chance(self):
        _, chance = self.get_capture_chance_and_crit_name(name=False)
        return chance

    def get_crit_name(self):
        crit_name, _ = self.get_capture_chance_and_crit_name(chance=False)
        return crit_name
    
    def get_capture_chance_and_crit_name(self, name=True, chance=True):
        loc = self.locate_on_screen("photos/fight/common/capture.png", confidence=0.8)
        critter_name = "--"
        capture_chance = "0"
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

            return critter_name, capture_chance
        
        print("not found capture!")
        return critter_name, capture_chance
    
    # def get_captured_crit_name_and_rating(self):
    #     loc = self.locate_on_screen("photos/fight/common/congrats.png", confidence=0.8)
    #     critter_name = "--"
    #     rating = "N"
    #     if loc:
    #         crit_name = (loc[0] + 90, loc[1] +75, loc[0] + 305, loc[1] +103)
    #         crit_name_image = ImageGrab.grab(bbox=crit_name)
    #         # crit_name_image.show()
    #         crit_name_config = r'--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #         critter_name = self.detect_text(crit_name_image, crit_name_config)

    #         rating_box = (loc[0] + 90, loc[1] +101, loc[0] + 305, loc[1] +125)
    #         rating_box_image = ImageGrab.grab(bbox=rating_box)
    #         # rating_box_image.show()
    #         scale = 2
    #         scaled = rating_box_image.resize((rating_box_image.width * scale, rating_box_image.height * scale))
    #         gray_scaled = scaled.convert("L")
    #         sharpened_scaled = gray_scaled.filter(ImageFilter.SHARPEN)
    #         sharpened_scaled = sharpened_scaled.filter(ImageFilter.SHARPEN)
    #         sharpened_scaled = sharpened_scaled.filter(ImageFilter.SHARPEN)
    #         inverted_scaled = ImageOps.invert(sharpened_scaled)
    #         rating_config = r'--psm 7 -c tessedit_char_whitelist=RatingABCDFS:+'
    #         inverted_scaled.show()
    #         rating = pytesseract.image_to_string(inverted_scaled, config=rating_config)
            
    #         # rating = pytesseract.image_to_string(rating_box_image, config=rating_config)
            
    #         # rating = self.detect_text(rating_box_image, rating_config)
    #         # import re
    #         # match = re.search(r'Rating:?\s*([ABCDFS]\+?)', rating)
    #         # if match:
    #         #     rating = match.group(1)
    #         #     print("Parsed rating:", rating)
    #         # else:
    #         #     print("Could not detect rating.")

    #         return ''.join(critter_name.split()), rating

    #     print("not found captured crit name image!")
    #     return critter_name
