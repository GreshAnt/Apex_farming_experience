import time
import pyautogui
import cv2
from PIL import ImageGrab
import pydirectinput
import random
import tool

# 常量配置
SCREENSHOT_PATH = './pic/screenshot.png'
CLICK_DELAY = 1
VERBS = \
    {
        "攻击": "auto_click(100, 100)",
        "释放战术技能": "pydirectinput.press('q')",
        "前进": "pydirectinput.press('w')",
        "后退": "pydirectinput.press('s')"
    }
VERB = list(VERBS.keys())


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

        min_val = 1 - min_val
        # 定义一个阈值，表示匹配是否成功
        threshold = 0.6
        print(min_val)

        if min_val > threshold:
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


def get_if(img_model_path, screenshot_path):
    res = False
    for _ in range(3):
        get_screenshot(screenshot_path)
        img = cv2.imread(screenshot_path)
        img_terminal = cv2.imread(img_model_path)
        height, width, channel = img_terminal.shape
        result = cv2.matchTemplate(img, img_terminal, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        min_val = 1 - min_val
        # 定义一个阈值，表示匹配是否成功
        threshold = 0.7
        print(min_val)

        if min_val > threshold:
            res = True


    return res


def main(img_model_path, name):
    routine(img_model_path, name, SCREENSHOT_PATH)


def run_main():
    num = 1
    while True:
        now_time = tool.get_time_dict()
        print(f"现在是{now_time['Hour']}点{now_time['Minute']}分")
        sw = False
        main('./pic/ready.png', '准备按钮')
        while True:
            if get_if('./pic/introchap.png', SCREENSHOT_PATH):
                print('准备跳伞')
                the_time = random.randint(20, 40)
                print(the_time)
                time.sleep(the_time)
                pydirectinput.click()
                print('跳伞成功')
                break
            time.sleep(0.2)



        # while not sw:
        #    exec(VERBS[random.choice(VERB)])
        #    time.sleep(9)
        #    for _ in range(0, 10):
        #        if get_if('./pic/sw.png', SCREENSHOT_PATH):
        #            sw = True
        #            break
        #    time.sleep(0.1)
            

        # for _ in range(1, 36):
        #     now_verb = random.choice(VERB)
        #     exec(VERBS[now_verb])
        #     print(f'总共35轮, 正在执行第{_}轮, 操作为{now_verb}')
        #     time.sleep(5)
            
        i = 1

        while True:

            if get_if('./pic/eliminated.png',SCREENSHOT_PATH):
                pydirectinput.press('esc')
                main('./pic/leave_match.png', '离开比赛')
                main('./pic/yes.png', '确定')
                break


            else:
                now_verb = random.choice(VERB)
                exec(VERBS[now_verb])
                print(f'正在执行第{i}轮, 操作为{now_verb}')
                i += 1
                time.sleep(5)
                continue





        # while True:
        #    if get_if('./pic/continue.png', SCREENSHOT_PATH):
        #        break
        time.sleep(8)
        for _ in range(0, 10):
            pydirectinput.press('space')
        print(f'>第{num}局结束，开始下一局\n ------------')
        num += 1



if __name__ == "__main__":
    run_main()
