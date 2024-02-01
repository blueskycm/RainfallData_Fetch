def check_rainfall_alerts(df, current_datetime):
    """
    檢查是否有雨量站達到警戒標準，並考慮不同時間段的降雨量
    """
    alert_standards = {
        '超大豪雨警報': {'24h': 500},
        '大豪雨警報': {'24h': 350},
        '大豪雨警報(短延時)': {'3h': 200},
        '豪雨警報': {'24h': 200},
        '豪雨警報(短延時)': {'3h': 100},
        '大雨警報': {'24h': 80},
        '大雨警報(短延時)': {'1h': 40},
        '短時強降雨': {'10min': 10, '1h': 30}
    }

    alerts = []
    max_alert_per_region = {}

    for index, row in df.iterrows():
        region = row['行政區']
        station = row['測站名稱']
        try:
            rainfall_data = {
                '10min': float(row['10分鐘']),
                '1h': float(row['1小時']),
                '3h': float(row['3小時']),
                '24h': float(row['24小時'])
            }
        except ValueError:
            continue

        for alert_level, thresholds in alert_standards.items():
            for duration, threshold in thresholds.items():
                if rainfall_data.get(duration, 0) >= threshold:
                    if region not in max_alert_per_region or max_alert_per_region[region][0] < alert_level:
                        max_alert_per_region[region] = (alert_level, station, duration, rainfall_data[duration])
                    break

    for region, (alert_level, station, duration, rainfall) in max_alert_per_region.items():
        if region not in last_alert_time or current_datetime - last_alert_time[region] > timedelta(hours=1):
            alerts.append(f"資料時間 {current_datetime}，{region} {station} 雨量站，已達{alert_level}，目前雨量 {rainfall}mm/{duration}。")
            last_alert_time[region] = current_datetime

    if not alerts:
        alerts.append(f"資料時間 {current_datetime}，目前全區降雨未達警戒標準。")

    return '\n'.join(alerts)
