import time
import numpy as np
import cv2
import random
import win32gui
import win32api
import win32con
from PIL import ImageGrab


def get_window_screenshot(window_rect):
    x, y = window_rect.left, window_rect.top
    width, height = window_rect.width(), window_rect.height()

    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    return screenshot


def get_search_on_image_roi(screenshot, template_path, threshold, roi=None, show_rect=False):
    img_np = np.array(screenshot)

    if roi is not None:
        x_start, y_start, x_end, y_end = roi
        img_np = img_np[y_start:y_end, x_start:x_end]

    template_rgb = cv2.imread(template_path, cv2.IMREAD_COLOR)
    template = cv2.cvtColor(template_rgb, cv2.COLOR_RGB2BGR)

    res = cv2.matchTemplate(img_np, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    match_coordinates = []
    match_mask = np.zeros_like(res, dtype=np.uint8)

    for pt in zip(*loc[::-1]):
        x, y = pt

        roi_match = match_mask[y:y+template.shape[0], x:x+template.shape[1]]
        if np.any(roi_match):
            continue

        bottom_right = (x + template.shape[1], y + template.shape[0])
        match_coordinates.append((pt, bottom_right))

        match_mask[y:y+template.shape[0], x:x+template.shape[1]] = 255

    if roi is not None:
        match_coordinates = [((pt[0] + x_start, pt[1] + y_start), (br[0] + x_start, br[1] + y_start)) for pt, br in match_coordinates]

    if show_rect:
        result_img = img_np.copy()
        for pt1, pt2 in match_coordinates:
            cv2.rectangle(result_img, pt1, pt2, (0, 0, 255), 1)

        cv2.imshow('Result', result_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return match_coordinates


def get_lt_rb_center_point(points_tuple):
    lt, rb = points_tuple

    x = (rb[0] - lt[0]) / 2 + lt[0]
    y = (rb[1] - lt[1]) / 2 + lt[1]
    return (x, y)


def get_img_coords(window, template_path, delay, tries_count, threshold, return_random=False, roi=None, show_rect=False, return_rect=False):
    for i in range(tries_count):
        window_screenshot = get_window_screenshot(window.rectangle())
        data = get_search_on_image_roi(window_screenshot, template_path, threshold, roi=roi, show_rect=show_rect)
        if data is None or len(data) <= 0:
            time.sleep(delay)
            continue
        else:
            if len(data) > 1 and return_random:
                button_points = data[random.randint(0, len(data)-1)]
            else:
                button_points = data[0]
            if return_rect:
                return button_points
            x, y = get_lt_rb_center_point(button_points)
            return (x, y)
        
    return False


def wait_while_img_dissapear(window, template_path, delay, tries_count, threshold, roi=None, show_rect=False):
    for i in range(tries_count):
        if not get_img_coords(window, template_path, 0, 1, threshold, roi=roi, show_rect=show_rect):
            return True
        time.sleep(delay)
    return False


def find_first_image(params_list, wait_time=60, click_first = False):
    lap_time = 0.5 * len(params_list)
    iterations_count = int(wait_time / lap_time) + 1
    if lap_time > wait_time:
        raise Exception("Wait time too small to do at least one lap!")
    for i in range(iterations_count):
        for params in params_list:
            if get_img_coords(*params):
                if click_first:
                    click_on_img(*params)
                return params[1]
    raise Exception("No one image found.")


def click_on_img(window, template_path, delay, tries_count, threshold, roi=None, focus=True, show_rect=False) -> None:
    point = get_img_coords(window, template_path, delay, tries_count, threshold, roi=roi, show_rect=show_rect)
    if point:
        if focus:
            window.set_focus()
        # control_click(int(point[0]), int(point[1]), window.handle)
        window.click_input(coords=(int(point[0]), int(point[1])))
        return True
    return False


def control_click(x, y, handle):
    l_param = win32api.MAKELONG(x, y)

    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)

    win32gui.SendMessage(handle, win32con.WM_SETFOCUS, 0, 0)

    win32gui.SendMessage(handle, win32con.WM_MOUSEMOVE, 0, l_param)
    


    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, l_param)
