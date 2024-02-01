from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime

def get_last_update_time(driver):
    """
    從網頁中獲取最後更新時間。
    """
    try:
        datetime_element = driver.find_element(By.ID, "Datatime")
        datetime_str = datetime_element.text.split('：')[-1].strip()
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logging.error(f"獲取更新時間時出錯: {e}")
        return None

def fetch_rainfall_data(driver):
    """
    從網頁中抓取雨量資料。
    """
    try:
        wait = WebDriverWait(driver, 10)
        table_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sortTable"]')))
        table_html = table_element.get_attribute('outerHTML')

        soup = BeautifulSoup(table_html, 'html.parser')
        table = soup.find('table')
        headers = [th.text.strip() for th in table.find_all('th')][:11]
        rows = table.find('tbody').find_all('tr')
        data = [[ele.text.strip() for ele in row.find_all(['td', 'th'])] for row in rows]

        df = pd.DataFrame(data, columns=headers)
        df.replace({"-": 0, "X": float('nan')}, inplace=True)
        df[headers[2:]] = df[headers[2:]].apply(pd.to_numeric, errors='coerce').fillna(0)
        return df
    except TimeoutException:
        logging.error("網頁載入超時，嘗試重新載入...")
        return None
