# 台灣雨量警報系統

## 簡介
這個專案是一個自動化的台灣雨量警報系統，用於從公開資料源抓取雨量數據，當雨量達到特定標準時，分析並發送警報到LINE Notify。
台灣交通部中央氣象署-降雨量10分鐘資料：https://www.cwa.gov.tw/V8/C/P/Rainfall/Rainfall_10Min_County.html
## 功能特色
- 自動抓取台灣各地雨量站的雨量數據。
- 分析雨量數據，根據設定的警報標準生成警報。
- 每小時整點時，系統將發送一次整體雨量狀況的總結。
- 採用智能過濾邏輯，避免在短時間內發送過多訊息。

## 雨量警報判定標準
本系統根據以下標準判定是否發送雨量警報：
1. 超大豪雨警報：24小時累積雨量達500mm以上。
2. 大豪雨警報：24小時累積雨量達350mm以上。
3. 大豪雨警報(短延時)：3小時累積雨量達200mm以上。
4. 豪雨警報：24小時累積雨量達200mm以上。
5. 豪雨警報(短延時)：3小時累積雨量達100mm以上。
6. 大雨警報：24小時累積雨量達80mm以上。
7. 大雨警報(短延時)：每小時雨量達40mm以上。
8. 短時強降雨：每10分鐘雨量達10mm以上，且每小時雨量達30mm以上(2條件必須同時滿足)。

## 抓資料的頻率
系統每5分鐘自動抓取一次雨量數據，以確保數據的即時性和準確性。

## 整點總結訊息
每當時鐘指向整點時，系統將自動生成並發送一條包含過去一小時內所有警報概況的總結訊息，幫助使用者快速獲得雨量狀況的整體了解。

## 避免訊息過多的邏輯
為了避免在極端天氣條件下發送過多訊息，系統設計了以下幾點智能過濾邏輯：
- 如果同一行政區在短時間內有多個雨量站符合警報條件，系統只會選擇最嚴重或降雨量最多的警報進行發送。
- 系統將對同一行政區在一定時間內的警報發送進行限制，以避免重複發送相似的警報訊息。

## 安裝指南
...

## 使用說明
1. 設定您的LINE Notify Token到環境變數：
   export LINE_NOTIFY_TOKEN='您的Token'
2. 執行主程式：
   python main.py

## 貢獻指南
歡迎各種形式的貢獻，包括提出新功能、報告bug、提交Pull Request等。

## 聯絡資訊
如有任何問題，請透過GitHub Issues與我們聯絡。




# Taiwan Rainfall Alert System
# Introduction
This project is an automated Taiwan rainfall alert system designed to fetch rainfall data from public data sources and analyze it to send alerts through LINE Notify when the rainfall reaches specific criteria.
Taiwan Central Weather Bureau - Rainfall Data (10-minute intervals): https://www.cwa.gov.tw/V8/C/P/Rainfall/Rainfall_10Min_County.html

## Features
- Automatically retrieves rainfall data from various stations across Taiwan.
- Analyzes rainfall data and generates alerts based on predefined criteria.
- Sends a summary of the overall rainfall situation at the top of every hour.
- Employs smart filtering logic to avoid sending too many messages in a short period.

## Rainfall Alert Criteria
The system decides whether to send a rainfall alert based on the following criteria:
1. Extremely heavy rain warning: The cumulative rainfall in 24 hours reaches more than 500mm.
2. Heavy rain warning: The cumulative rainfall in 24 hours reaches more than 350mm.
3. Heavy rain warning (short delay): The accumulated rainfall in 3 hours reaches more than 200mm.
4. Heavy rain warning: The cumulative rainfall in 24 hours reaches more than 200mm.
5. Heavy rain warning (short delay): The cumulative rainfall reaches more than 100mm in 3 hours.
6. Heavy rain warning: The cumulative rainfall in 24 hours reaches more than 80mm.
7. Heavy rain warning (short delay): rainfall reaches more than 40mm per hour.
8. Short-term heavy rainfall: the rainfall reaches more than 10mm every 10 minutes, and the rainfall reaches more than 30mm per hour (the two conditions must be met at the same time).

## Data Fetching Frequency
The system automatically fetches rainfall data every 5 minutes to ensure data timeliness and accuracy.

## Hourly Summary Message
At every hour, the system automatically generates and sends a message summarizing all the alerts within the past hour to help users quickly understand the overall rainfall situation.

## Logic to Avoid Excessive Messages
To avoid sending too many messages during extreme weather conditions, the system incorporates the following smart filtering logic:
- If multiple rainfall stations in the same administrative area meet the alert criteria within a short period, the system will only select the most severe or highest rainfall alert for notification.
- The system will limit the frequency of alerts sent for the same administrative area within a certain time frame to avoid sending repetitive alert messages.

## Installation Guide
...

## Instructions for Use
Set your LINE Notify Token in the environment variables:
export LINE_NOTIFY_TOKEN='Your Token'
Execute the main program:
python main.py

## Contribution Guide
Contributions of all kinds are welcome, including new features, bug reports, and pull requests.

## Contact Information
For any questions, please contact us through GitHub Issues.
