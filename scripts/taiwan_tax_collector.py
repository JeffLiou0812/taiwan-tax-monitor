# taiwan_tax_collector.py - 台灣稅務資料收集器（修正版）
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time

class TaiwanTaxCollector:
    def __init__(self):
        self.base_path = r"C:\Users\fengy\TaxMonitor\TaxMonitor"
        self.data_path = os.path.join(self.base_path, "data")
        self.session = requests.Session()
        
    def collect_mof_data(self):
        """收集財政部資料"""
        print("開始收集財政部資料...")
        
        url = "https://www.mof.gov.tw"
        results = []
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 收集所有連結
            links = soup.find_all('a', href=True)
            
            for link in links[:20]:  # 只處理前20個
                text = link.get_text(strip=True)
                if len(text) > 10:
                    results.append({
                        'title': text[:100],
                        'url': link.get('href', ''),
                        'time': datetime.now().isoformat()
                    })
            
            print(f"找到 {len(results)} 個項目")
            
        except Exception as e:
            print(f"錯誤: {e}")
            
        return results
    
    def save_data(self, data):
        """儲存資料"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.data_path, f"tax_data_{timestamp}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"資料已儲存: {os.path.basename(filename)}")
        return filename
    
    def run(self):
        """執行主程式"""
        print("="*50)
        print("台灣稅務資料收集器")
        print("="*50)
        
        # 收集資料
        data = self.collect_mof_data()
        
        # 建立完整結果
        full_results = {
            'scan_time': datetime.now().isoformat(),
            'data': data,
            'count': len(data)
        }
        
        # 儲存
        self.save_data(full_results)
        
        print(f"\n完成！共收集 {len(data)} 筆資料")
        return full_results

if __name__ == "__main__":
    collector = TaiwanTaxCollector()
    collector.run()