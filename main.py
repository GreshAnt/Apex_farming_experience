import time
import pyautogui
import cv2
from PIL import ImageGrab

# 常量配置
SCREENSHOT_PATH = './pic/screenshot.png'
CLICK_DELAY = 1


def capture_screen(x, y, width, height, filepath):
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot.save(filepath)


def get_screenshot(filepath):
    screen_width, screen_height = ImageGrab.grab().size
    capture_screen(0, 0, screen_width, screen_height, filepath)


def get_xy(img_model_path, screenshot_path):
    while True:
        get_screenshot(screenshot_path)
        img = cv2.imread(screenshot_path)
        img_terminal = cv2.imread(img_model_path)
        height, width, channel = img_terminal.shape
        result = cv2.matchTemplate(img, img_terminal, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 定义一个阈值，表示匹配是否成功
        threshold = 0.2

        if min_val < threshold:
            # 如果匹配成功，返回匹配的坐标
            upper_left = min_loc
            lower_right = (upper_left[0] + width, upper_left[1] + height)
            avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))
            return avg


def auto_click(x, y):
    pyautogui.click(x, y, button='left')
    time.sleep(CLICK_DELAY)


def routine(img_model_path, name, screenshot_path):
    avg = get_xy(img_model_path, screenshot_path)
    pyautogui.moveTo(avg[0], avg[1])
    auto_click(avg[0], avg[1])
    print(f'正在点击{name}')


def main(img_model_path, name):
    routine(img_model_path, name, SCREENSHOT_PATH)


if __name__ == "__main__":
    while True:
        main('./pic/ready.png', '准备按钮')
        time.sleep(600)
        pyautogui.press('esc')
        main('./pic/leave_match.png', '离开比赛')
        main('./pic/yes.png', '确定')

        main('./pic/continue.bmp', '继续')
