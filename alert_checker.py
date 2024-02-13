import logging
from datetime import datetime, timedelta

def check_rainfall_alerts(df, current_datetime, last_alert_time):
    alert_standards = [
        ('超大豪雨警報', {'24h': 500}),
        ('大豪雨警報', {'24h': 350}),
        ('大豪雨警報(短延時)', {'3h': 200}),
        ('豪雨警報', {'24h': 200}),
        ('豪雨警報(短延時)', {'3h': 100}),
        ('大雨警報', {'24h': 80}),
        ('大雨警報(短延時)', {'1h': 40}),
        ('短時強降雨', {'10min': 10, '1h': 30})  # 需要特殊處理因為有兩個條件
    ]

    alerts = []
    region_alerts = {}

    for index, row in df.iterrows():
        region = row['行政區']
        station = row['測站名稱']
        rainfall_data = {
            '10min': row['10分鐘'],
            '1h': row['1小時'],
            '3h': row['3小時'],
            '24h': row['24小時']
        }

        station_alerts = []
        for alert_level, thresholds in alert_standards:
            meets_criteria = False
            for duration, threshold in thresholds.items():
                if duration in rainfall_data and rainfall_data[duration] >= threshold:
                    meets_criteria = True
                    station_alerts.append((alert_level, station, rainfall_data[duration], duration))
                    break  # 只要滿足一個條件即可
            
            if meets_criteria:
                # 確保短時強降雨的特殊條件
                if alert_level == '短時強降雨' and not (rainfall_data['10min'] >= thresholds['10min'] and rainfall_data['1h'] >= thresholds['1h']):
                    station_alerts.pop()

        if station_alerts:
            region_alerts.setdefault(region, []).extend(station_alerts)

    for region, alerts_list in region_alerts.items():
        most_severe_alert = max(alerts_list, key=lambda x: (alert_standards.index((x[0], {x[3]: x[2]})), x[2]))
        if region not in last_alert_time or current_datetime - last_alert_time[region] > timedelta(hours=1):
            alert_message = f"資料時間 {current_datetime}，{region} {most_severe_alert[1]} 雨量站，已達{most_severe_alert[0]}，目前雨量 {most_severe_alert[2]}mm/{most_severe_alert[3]}。"
            alerts.append(alert_message)
            last_alert_time[region] = current_datetime
            logging.info(f"Sending Alert: {alert_message}")
        alerts_list.remove(most_severe_alert)
        for alert in alerts_list:
            logging.info(f"Detected but not sent: {region} {alert[1]} - {alert[0]} with {alert[2]}mm/{alert[3]} at {current_datetime}.")

    if not alerts:
        no_alert_message = f"資料時間 {current_datetime}，目前全區降雨未達警戒標準。"
        alerts.append(no_alert_message)
        logging.info(no_alert_message)

    return alerts, last_alert_time
