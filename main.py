import time
from datetime import datetime, timedelta
import os
import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from data_fetcher import get_last_update_time, fetch_rainfall_data, save_data_to_csv
from alert_checker import check_rainfall_alerts
from notifier import send_line_notify
from logger import setup_logging

def is_whole_hour(time):
    """檢查給定時間是否為整點"""
    return time.minute == 0 and time.second == 0

def main():
    setup_logging()
    url = 'https://www.cwa.gov.tw/V8/C/P/Rainfall/Rainfall_10Min_County.html'
    token = os.getenv("LINE_NOTIFY_TOKEN")  # 環境變量中獲取 LINE Notify Token

    last_alert_time = {}
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(60)

    last_datetime = None  # 記錄上一次資料更新時間
    normal_check_interval = timedelta(minutes=5)  # 正常檢查間隔
    fast_check_interval = timedelta(minutes=1)  # 加速檢查間隔
    next_check_time = datetime.now()

    try:
        while True:
            current_time = datetime.now().replace(microsecond=0)

            if current_time >= next_check_time:
                driver.get(url)
                current_datetime = get_last_update_time(driver)

                if current_datetime and (last_datetime is None or current_datetime != last_datetime):
                    df = fetch_rainfall_data(driver)
                    if df is not None:
                        filename = current_datetime.strftime('%Y-%m-%d-%H%M') + '_RainfallData.csv'
                        save_data_to_csv(df, filename)
                        last_datetime = current_datetime

                        # 檢查雨量警報並發送 LINE 訊息
                        if is_whole_hour(current_datetime):
                            alert_message, last_alert_time = check_rainfall_alerts(df, last_datetime, last_alert_time)
                            response_status = send_line_notify(alert_message, token)
                            logging.info(f"LINE Notify message sent with status: {response_status}")

                    # 資料已更新，恢復正常檢查間隔
                    next_check_time = current_time + normal_check_interval
                else:
                    # 資料未更新，使用加速檢查間隔
                    next_check_time = current_time + fast_check_interval

                time.sleep(60)  # 等待一分鐘後再次檢查

    except WebDriverException as e:
        logging.error(f"Error accessing website: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
