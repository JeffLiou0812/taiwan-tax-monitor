# check_ready.py - 檢查系統是否準備好
import sys

print("檢查稅務爬蟲系統...")
print("-" * 40)

required = {
    'requests': '網頁下載',
    'bs4': '網頁解析', 
    'pandas': '資料處理',
    'jieba': '中文分詞',
    'chardet': '編碼偵測'
}

all_ready = True
for module, purpose in required.items():
    try:
        __import__(module)
        print(f"✓ {module:15} - {purpose}")
    except ImportError:
        print(f"✗ {module:15} - {purpose} [需要安裝]")
        all_ready = False

print("-" * 40)
if all_ready:
    print("✅ 系統準備完成！可以開始爬蟲了")
else:
    print("❌ 請先安裝缺少的套件")