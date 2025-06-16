import pyautogui
# import time
# import cv2
# import numpy as np
# import random
# import requests
from PIL import ImageGrab, Image, ImageOps, ImageFilter
import pytesseract
# import easyocr
# import os


# Load templates (screenshots of UI elements)
def locate_on_screen(template_path, confidence=0.8):
    location = pyautogui.locateCenterOnScreen(template_path, confidence=confidence)
    return location


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def detect_text(image, custom_config):
    scale = 2
    scaled = image.resize((image.width * scale, image.height * scale))
    gray_scaled = scaled.convert("L")
    sharpened_scaled = gray_scaled.filter(ImageFilter.SHARPEN)
    sharpened_scaled_2 = sharpened_scaled.filter(ImageFilter.SHARPEN)
    sharpened_scaled_3 = sharpened_scaled_2.filter(ImageFilter.SHARPEN)
    # sharpened_scaled_4 = sharpened_scaled_3.filter(ImageFilter.SHARPEN)
    # sharpened_scaled_4.show()
    inverted_scaled = ImageOps.invert(sharpened_scaled_3)
    # inverted_scaled.show()

    text = pytesseract.image_to_string(inverted_scaled, config=custom_config)
    return text

def get_tier():

    S_tier = locate_on_screen("photos/tiers/S.png", confidence=0.8)
    Sp_tier = locate_on_screen("photos/tiers/S+.png", confidence=0.8)
    A_tier = locate_on_screen("photos/tiers/A.png", confidence=0.8)
    Ap_tier = locate_on_screen("photos/tiers/A+.png", confidence=0.8)
    B_tier = locate_on_screen("photos/tiers/B.png", confidence=0.8)
    Bp_tier = locate_on_screen("photos/tiers/B+.png", confidence=0.8)
    C_tier = locate_on_screen("photos/tiers/C.png", confidence=0.8)
    Cp_tier = locate_on_screen("photos/tiers/C+.png", confidence=0.8)
    D_tier = locate_on_screen("photos/tiers/D.png", confidence=0.8)
    Dp_tier = locate_on_screen("photos/tiers/D+.png", confidence=0.8)
    F_tier = locate_on_screen("photos/tiers/F.png", confidence=0.8)
    Fp_tier = locate_on_screen("photos/tiers/F+.png", confidence=0.8)
    

    if Sp_tier:
        return "S+"
    elif S_tier:
        return "S"
    elif Ap_tier:
        return "A+"
    elif A_tier:
        return "A"
    elif Bp_tier:
        return "B+"
    elif B_tier:
        return "B"
    elif Cp_tier:
        return "C+"
    elif C_tier:
        return "C"
    elif Dp_tier:
        return "D+"
    elif D_tier:
        return "D"
    elif Fp_tier:
        return "F+"
    elif F_tier:
        return "F"
    else:
        return "NA/F-"


def main_loop():
    while True:
        # tier = get_tier()
        # print(tier)

        loc = locate_on_screen("photos/fight/common/capture_big.png", confidence=0.8)
        if loc:
            cc = (loc[0] - 25, loc[1] + 17, loc[0] + 28, loc[1] + 37)  # Example values
            crit_name = (loc[0] + 250, loc[1] - 90, loc[0] + 370, loc[1] - 72)

            cc_image = ImageGrab.grab(bbox=cc)
            crit_name_image = ImageGrab.grab(bbox=crit_name)
            custom_config = r'--psm 7 -c tessedit_char_whitelist=0123456789%'
            print("capture chance: ", detect_text(cc_image, custom_config=custom_config))
            custom_config = r'--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            print("crit name: ", detect_text(crit_name_image, custom_config=custom_config))
            # cc_image.show()
            # crit_name_image.show()
            # print(loc)
            # pyautogui.moveTo(loc, duration=0.1, tween=pyautogui.easeInOutQuad)
            # pyautogui.moveRel(0, -280, duration=0.1, tween=pyautogui.easeInOutQuad)
            return
            

if __name__ == "__main__":
    # time.sleep(1)  # Time to switch to game
    main_loop()
