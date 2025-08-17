# mof_scraper.py - 財政部函釋爬蟲
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time
import re

class MOFTaxScraper:
    def __init__(self):
        self.base_path = r"C:\Users\fengy\TaxMonitor\TaxMonitor"
        self.data_path = os.path.join(self.base_path, "data")
        self.session = requests.Session()
        
        # 設定請求標頭
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
        }
        
    def scrape_latest_rulings(self):
        """爬取最新函釋"""
        print("開始爬取財政部最新函釋...")
        
        # 財政部賦稅署函釋查詢網址
        url = "https://www.dot.gov.tw/ch/home.jsp?id=30&parentpath=0,1"
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 擷取頁面標題確認連接成功
            title = soup.find('title')
            if title:
                print(f"✓ 成功連接: {title.text.strip()}")
            
            # 儲存原始HTML供後續分析
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            html_file = os.path.join(self.data_path, f"mof_rulings_{timestamp}.html")
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"✓ HTML已儲存: {os.path.basename(html_file)}")
            
            # 解析函釋資料
            rulings = self.parse_rulings(soup)
            
            # 儲存為JSON
            json_file = os.path.join(self.data_path, f"mof_rulings_{timestamp}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(rulings, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 找到 {len(rulings)} 筆函釋")
            print(f"✓ JSON已儲存: {os.path.basename(json_file)}")
            
            return rulings
            
        except Exception as e:
            print(f"✗ 爬取失敗: {e}")
            return []
    
    def parse_rulings(self, soup):
        """解析函釋內容"""
        rulings = []
        
        # 尋找所有可能包含函釋的元素
        # 這需要根據實際網頁結構調整
        links = soup.find_all('a', href=True)
        
        # 函釋字號的正則表達式
        hanshi_pattern = re.compile(r'台財稅字第\d+號|財政部\d+號')
        
        for link in links[:20]:  # 先處理前20個連結
            text = link.get_text(strip=True)
            if hanshi_pattern.search(text):
                rulings.append({
                    'title': text[:200],
                    'url': link.get('href', ''),
                    'scraped_at': datetime.now().isoformat()
                })
        
        return rulings
    
    def run(self):
        """執行爬蟲"""
        print("="*50)
        print("財政部稅務函釋爬蟲")
        print("="*50)
        
        rulings = self.scrape_latest_rulings()
        
        if rulings:
            print("\n最新函釋摘要:")
            for i, ruling in enumerate(rulings[:3], 1):
                print(f"{i}. {ruling.get('title', 'N/A')[:50]}...")
        
        print("\n爬蟲執行完成！")
        return rulings

if __name__ == "__main__":
    scraper = MOFTaxScraper()
    scraper.run()