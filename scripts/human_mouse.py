import pyautogui
import time
import math

pyautogui.FAILSAFE = False

class HumanMouse:
    @staticmethod
    def move_to(loc, x_off=0, y_off=0):
        pyautogui.moveTo(loc, duration=0.1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveRel(x_off, y_off, duration=0.05, tween=pyautogui.easeInOutQuad)

    @staticmethod
    def random_move(x=0, y=0):
        pyautogui.moveRel(x, y, duration=0.05, tween=pyautogui.easeInOutQuad)

    @staticmethod
    def click():
        pyautogui.mouseDown()
        time.sleep(0.01)
        pyautogui.mouseUp()
        time.sleep(0.05) # TODO: OPTIMIZE, 0.3 seems too much.

    @staticmethod
    def locate_on_screen(template_path, confidence=0.8):
        location = pyautogui.locateCenterOnScreen(template_path, confidence=confidence)
        return location
    
    @staticmethod
    def locate_all_on_screen(template_path, min_distance=60, confidence=0.8):
        # Find all raw matches
        matches = list(pyautogui.locateAllOnScreen(template_path, confidence=confidence))
        centers = [pyautogui.center(match) for match in matches]
        print("centers:", centers)
        # Get centers and filter
        unique_centers = []

        for match in matches:
            center = pyautogui.center(match)
            
            # Check distance to all previously stored centers
            if all(math.dist(center, existing) > min_distance for existing in unique_centers):
                unique_centers.append(center)

        print("!! unique_centers:", unique_centers)
        return unique_centers
    
    @staticmethod
    def smooth_drag(start_pos, offset_x, offset_y):
        """
        Clicks and drags from start_pos by the given offset using tweening for smooth motion.
        """
        x_start, y_start = start_pos
        x_end = x_start + offset_x
        y_end = y_start + offset_y

        pyautogui.moveTo(x_start, y_start, duration=0.01, tween=pyautogui.easeInOutQuad)
        pyautogui.mouseDown()
        time.sleep(0.01)

        pyautogui.moveTo(x_end, y_end, duration=0.01, tween=pyautogui.easeInOutQuad)

        pyautogui.mouseUp()
