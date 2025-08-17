# 測試爬蟲程式
import os
import json
from datetime import datetime

print("=" * 50)
print("稅務爬蟲測試程式")
print("=" * 50)

# 顯示目前工作目錄
print(f"目前位置: {os.getcwd()}")

# 建立測試資料
test_data = {
    "訊息": "恭喜！爬蟲環境設定成功",
    "時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "使用者": "fengy"
}

# 儲存到data資料夾
save_path = r"C:\Users\fengy\TaxMonitor\TaxMonitor\data\test_result.json"

try:
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 成功儲存測試檔案到: {save_path}")
except Exception as e:
    print(f"\n✗ 儲存失敗: {e}")

print("\n測試完成！")