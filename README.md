# 为妈妈开发的一个看比赛的小工具 

## 目的
方便妈妈在电脑上看cctv5的直播比赛

## base 
python、windows、Rainmeter

## 需求
在桌面上点击一个图标，以最少的操作步骤体验到一个不错的观赛效果。

## 流程拆解
1. .bat 文件图标会淹没在桌面上茫茫多的图标中，为了方便妈妈快速寻找到她需要点击的图标，调研到windows上有一个 Rainmeter 的工具可以高度自定义图标，实现我的需求。
2. 点击到图标后需要用浏览器打开固定的网址，并且需要将视频处于播放状态，调整到全屏播放，这里用 js 或者 py 去控制一个无头浏览器都能够实现，js 的操作已经比较熟悉了，因此选择了py来练练手。 

实现步骤：
1. 实现一个py脚本，用于控制浏览器的打开、放大、播放等操作。
```

import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def open_cctv5():
    url = 'https://tv.cctv.com/live/cctv5/'
    
    # 初始化Chrome浏览器
    options = webdriver.ChromeOptions()
    options.add_argument('--no-first-run')  # 禁用首次运行界面
    options.add_argument('--no-default-browser-check')  # 禁用默认浏览器检查
    options.add_argument('--disable-infobars')  # 禁用信息栏
    options.add_argument('--start-maximized')  # 启动时最大化窗口
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 禁用"正受到自动测试软件的控制"提示
    options.add_experimental_option('useAutomationExtension', False)  # 禁用自动化扩展
    driver = webdriver.Chrome(options=options)
    
    try:
        # 打开网页
        driver.get(url)
        
        # 等待视频播放器加载
        wait = WebDriverWait(driver, 10)
        
        # 1. 检查视频是否在播放，如果没有则点击播放按钮

        play_pause_button = wait.until(EC.presence_of_element_located((By.ID, "play_or_pause_play_player")))
        button_display = play_pause_button.value_of_css_property('display')

        print("检查视频播放状态",button_display)
        
        if button_display != 'none':
            print("视频处于暂停状态，正在点击播放按钮")
            play_pause_button.click()
        else:
            print("视频已在播放中")
        
        # 2. 调整音量到80%
        # 假设音量控制是0-100的范围
        #TODO

        # 3. 设置全屏
        # player_fullscreen_no_player id 
        fullscreen_button = wait.until(EC.presence_of_element_located((By.ID, "player_fullscreen_no_player")))
        fullscreen_button_display = fullscreen_button.value_of_css_property('display')
        print("检查全屏状态",fullscreen_button_display)

        if fullscreen_button_display != 'none':
            print("视频处于非全屏状态，正在点击全屏按钮")
            fullscreen_button.click()
        else:
            print("视频已在全屏中")
        
        # 保持浏览器窗口打开
        input("按回车键关闭浏览器...")
        
    except TimeoutException:
        print("页面加载超时")
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    open_cctv5()

```

2. 写一个bat 脚本来作为py脚本的启动器
```
@echo off
title CCTV5

:: 检查 Python 是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo Python未安装，请先安装Python
    pause
    exit /b
)

:: 检查 selenium 是否已安装
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo 正在安装 selenium...
    pip install selenium
)

:: 运行脚本
echo open cctv5 ing...
cd /d "%~dp0"
python -c "import sys; sys.path.append('.'); from open_cctv5 import open_cctv5; open_cctv5()"

pause
```

3. 实现一个 Rainmeter 的ini 脚本，链接到 bat 脚本
```
[Rainmeter]
Update=1000

[Metadata]
Name=CCTV5 Launcher
Author=Horizon
Information=Launch CCTV5 Live Stream
Version=1.0
License=Creative Commons Attribution

[MeterBackground]
Meter=Image
ImageName=C:\***\CCTV-5_Logo.png
W=226 
H=128
LeftMouseUpAction=["cmd.exe" "/c" "C:\***\run_cctv5.bat"]
SolidColor=0,0,0,1
ToolTipText=open cctv5 
```

4. 将该脚本嵌入到 Rainmeter 中，测试该效果如下：
