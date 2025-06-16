import pyautogui
import time


class HumanMouse:
    @staticmethod
    def move_to(loc, x_off=0, y_off=0):
        pyautogui.moveTo(loc, duration=0.1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveRel(x_off, y_off, duration=0.1, tween=pyautogui.easeInOutQuad)

    @staticmethod
    def random_move(x=0, y=0):
        pyautogui.moveRel(x, y, duration=0.1, tween=pyautogui.easeInOutQuad)

    @staticmethod
    def click():
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(0.3)
        HumanMouse.random_move()
