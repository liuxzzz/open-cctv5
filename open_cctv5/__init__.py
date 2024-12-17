
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

