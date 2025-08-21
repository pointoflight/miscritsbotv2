import tkinter as tk
import threading
import time

def show_region(region, duration=2, color="red", width=3):
    """
    Draws a rectangle overlay on the screen for debugging.
    :param region: (x, y, width, height)
    :param duration: seconds to show
    :param color: rectangle outline color
    :param width: line thickness
    """
    x, y, w, h = region

    def _draw():
        root = tk.Tk()
        root.overrideredirect(True)  # no borders
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.3)  # transparent background
        root.geometry(f"{w}x{h}+{x}+{y}")

        canvas = tk.Canvas(root, width=w, height=h, highlightthickness=0)
        canvas.pack()
        canvas.create_rectangle(0, 0, w, h, outline=color, width=width)

        # Close after duration
        root.after(int(duration * 1000), root.destroy)
        root.mainloop()

    # Run overlay in separate thread so it doesn’t block main program
    threading.Thread(target=_draw, daemon=True).start()


# Example usage
center = (534, 588)
# region = (center[0] - 125, center[1] - 40, 60, 55)  # trial-error region
region = (409, 750, 60, 55)
print("Showing region for debugging...")
show_region(region, duration=2)
time.sleep(2.5)  # wait so you can see it before script ends
