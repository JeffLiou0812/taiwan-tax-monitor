# taiwan_tax_scraper.py
# 台灣財政部稅務資料爬蟲
# 作者：fengy
# 日期：2025-08-17

import os
import json
from datetime import datetime

print("=" * 60)
print("台灣稅務資料爬蟲 v1.0")
print("=" * 60)

# 設定資料儲存路徑 (use project directory)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_path, "data")
log_path = os.path.join(base_path, "logs")

# Ensure directories exist
os.makedirs(data_path, exist_ok=True)
os.makedirs(log_path, exist_ok=True)

print(f"\n工作目錄: {os.getcwd()}")
print(f"資料將儲存到: {data_path}")

# 第一步：先測試基本功能
def test_basic_functions():
    print("\n[測試1] 檢查資料夾是否存在...")
    
    if os.path.exists(data_path):
        print(f"✓ data資料夾存在")
    else:
        print(f"✗ data資料夾不存在")
        
    if os.path.exists(log_path):
        print(f"✓ logs資料夾存在")
    else:
        print(f"✗ logs資料夾不存在")

# 第二步：建立測試資料
def create_test_data():
    print("\n[測試2] 建立測試資料...")
    
    test_data = {
        "系統": "稅務爬蟲",
        "版本": "1.0",
        "測試時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "測試狀態": "成功",
        "下一步": "準備連接真實網站"
    }
    
    # 儲存測試資料
    filename = os.path.join(data_path, "taiwan_test.json")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 測試資料已儲存到: taiwan_test.json")
        return True
    except Exception as e:
        print(f"✗ 儲存失敗: {e}")
        return False

# 主程式
if __name__ == "__main__":
    # 執行測試
    test_basic_functions()
    
    # 建立測試資料
    if create_test_data():
        print("\n恭喜！基礎環境測試成功！")
        print("下一步：我們將開始連接真實的稅務網站")
    else:
        print("\n需要解決問題後才能繼續")