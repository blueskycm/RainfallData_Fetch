import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
import logging
from data_fetcher import get_last_update_time, fetch_rainfall_data
from alert_checker import check_rainfall_alerts
from notifier import send_line_notify
from logger import setup_logging

def is_whole_hour(time):
    """檢查給定時間是否為整點"""
    return time.minute == 0 and time.second == 0

def main():
    setup_logging()
    url = 'https://www.cwa.gov.tw/V8/C/P/Rainfall/Rainfall_10Min_County.html'
    token = os.getenv("LINE_NOTIFY_TOKEN")  # 請替換為您的LINE Notify Token

    # 初始化檢查間隔和暫停持續時間
    initial_check_interval = 60  # 初始檢查間隔(秒)
    regular_check_interval = 600  # 常規檢查間隔(秒)
    pause_duration = 300  # 暫停持續時間(秒)

    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(60)

    try:
        last_datetime = None
        last_whole_hour_report = None
        data_fetched_count = 0
        next_check_time = datetime.now()

        while True:
            current_time = datetime.now().replace(microsecond=0)

            if current_time >= next_check_time:
                driver.get(url)
                current_datetime = get_last_update_time(driver)

                if current_datetime and (last_datetime is None or current_datetime != last_datetime):
                    df = fetch_rainfall_data(driver)
                    if df is not None:
                        filename = current_datetime.strftime('%Y-%m-%d-%H%M') + '_RainfallData.csv'
                        df.to_csv(filename, index=False, encoding='utf-8-sig')
                        logging.info(f"資料已更新至 {current_datetime}，已存儲為 {filename}。")
                        last_datetime = current_datetime
                        data_fetched_count += 1

                        # 計算下次檢查時間
                        if data_fetched_count >= 2:
                            next_check_time = current_time + timedelta(seconds=regular_check_interval)
                        else:
                            next_check_time = current_time + timedelta(seconds=initial_check_interval)

                        # 檢查雨量警報並發送 LINE 訊息
                        if current_datetime.minute == 0:  # 僅在整點發送訊息
                            alert_message = check_rainfall_alerts(df, last_datetime)
                            response_status = send_line_notify(alert_message, token)
                            logging.info(f"LINE Notify 訊息發送狀態: {response_status}")

            time.sleep(initial_check_interval)

    except WebDriverException as e:
        logging.error(f"訪問網站時出錯: {e}。暫停 {pause_duration} 秒後重試。")
        time.sleep(pause_duration)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()