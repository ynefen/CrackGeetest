import random
from pynput import mouse
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from PIL import Image


# from selenium.webdriver.common.action_chains import ActionChains
def Search_notch():
    img = Image.open('1.png')
    img_bak = img
    img = img.convert('L')
    Offset = 45
    frequency = {}
    x_record = []
    for x in range(img.size[0]):
        if x != 0:
            for y in range(img.size[1]):
                if img.getpixel((x - 1, y)) - img.getpixel((x, y)) > 75 and img.getpixel((x - 1, y)) < 250:
                    img_bak.putpixel((x, y), (255, 0, 0, 255))
                    x_record.append(x)
    for y in range(img.size[1]):
        img_bak.putpixel((max(set(x_record), key=x_record.count), y), (255, 0, 0, 255))
    img_bak.save(str(time.time()) + ".png")
    print("xxx", max(set(x_record), key=x_record.count) + Offset)
    return max(set(x_record), key=x_record.count) + Offset


if __name__ == '__main__':
    control = mouse.Controller()  # 获取鼠标的操控对象
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    brower = webdriver.Chrome(options=option)
    brower.set_window_size(1280, 800)
    while True:
        brower.get(r"https://www.geetest.com/show")
        brower.find_element_by_css_selector("[class='tab-item tab-item-1']").click()
        time.sleep(1)
        try:
            brower.find_element_by_class_name("geetest_radar_btn").click()
        except:
            continue
        time.sleep(0.5)
        try:
            brower.find_element_by_css_selector("[class='geetest_slider_button']").click()
        except:
            continue
        brower.get_screenshot_as_file(r".\1.png")
        img = Image.open("./1.png")
        cropped = img.crop((343, 479, 525, 620))  # (left, upper, right, lower)
        cropped.save("./1.png")
        time.sleep(1)
        dot = brower.find_element_by_css_selector("[class='geetest_slider_button']")
        dot_location = brower.get_window_position()  # 根据浏览器窗口位置+偏移算出滑块位置
        dot_location["x"] = dot_location["x"] + 316
        dot_location["y"] = dot_location["y"] + 756
        control.position = (dot_location["x"], dot_location["y"])  # 移动鼠标至滑块
        time.sleep(1.5)
        control.press(mouse.Button.left)
        end = Search_notch()
        max_speed = 17  # 最大速度
        least_speed = 15  # 最小速度
        while end >= 0:
            Moving_distance = random.randint(1, 2)
            end -= Moving_distance  # 循环次数减Less
            if end > 50 and max_speed > 2:  # 加速
                max_speed -= 1
                least_speed -= 1
            if end < 30 and max_speed < 25:
                max_speed += 1
                least_speed += 1
            sleep = random.randint(least_speed, max_speed)  # 设定延迟
            print("max", max_speed, "least", least_speed, "end", end, )
            time.sleep(sleep / 1000)
            control.move(Moving_distance, random.randint(-1, 0))
        control.release(mouse.Button.left)
        time.sleep(1)
    # brower.quit()
