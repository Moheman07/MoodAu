from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import string
import time
import logging

# إعداد السجلات
logging.basicConfig(filename='logs/errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_random_string(length):
    """توليد سلسلة عشوائية من أحرف وأرقام"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def handle_popup(driver):
    """التعامل مع النوافذ المنبثقة"""
    original_window = driver.current_window_handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            driver.close()
    driver.switch_to.window(original_window)

def main():
    # إعداد المتصفح
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # تشغيل بدون واجهة
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # المرحلة 1: إنشاء المستخدم
        driver.get('https://moodtv.xyz/create.php')
        
        # توليد اسم مستخدم وكلمة مرور
        username = f"user_{generate_random_string(8)}"
        password = generate_random_string(12)
        
        # إدخال البيانات
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
        driver.find_element(By.ID, 'get_user_button').click()  # زر "Get User"
        
        # المرحلة 2: التعامل مع الإعلانات (3 تكرارات)
        for _ in range(3):
            # انتظار عداد 20 ثانية
            WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.ID, 'next_button')))
            
            # التعامل مع إعلان منبثق
            handle_popup(driver)
            
            # إغلاق فيديو (زر X)
            try:
                driver.find_element(By.CLASS_NAME, 'close_video').click()
            except:
                pass  # تجاهل إذا لم يظهر
            
            # النقر على زر Skip
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'skip_button'))).click()
            
            # النقر على زر Next الأزرق
            driver.find_element(By.ID, 'next_button').click()
            
            # انتظار شريط التحميل (~5 ثواني)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'next_button_second')))
            
            # النقر على زر Next الثاني
            driver.find_element(By.ID, 'next_button_second').click()
        
        # المرحلة 3: صفحات المتابعة (3 تكرارات)
        for _ in range(3):
            # انتظار عداد 5 ثواني
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'continue_button')))
            # النقر على زر متابعة
            driver.find_element(By.ID, 'continue_button').click()
            
            # التعامل مع صفحة الإعلان الثابتة
            try:
                # العودة إلى الصفحة السابقة
                driver.back()
                # انتظار زر متابعة مرة أخرى
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'continue_button')))
                driver.find_element(By.ID, 'continue_button').click()
            except:
                logging.warning("فشل التعامل مع صفحة الإعلان الثابتة، يتم المتابعة")
        
        # المرحلة 4: نسخ رابط M3U
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'copy_m3u_button'))).click()
        m3u_link = driver.find_element(By.ID, 'm3u_link').get_attribute('data-clipboard-text')
        
        # حفظ الرابط في ملف
        with open('output/playlist.m3u', 'w') as f:
            f.write(m3u_link)
        
        print(f"تم حفظ رابط M3U: {m3u_link}")
    
    except Exception as e:
        logging.error(f"خطأ: {str(e)}")
        print(f"حدث خطأ، تحقق من logs/errors.log")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
