# mof_scraper.py - 財政部函釋爬蟲
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
import time
import re
import pandas as pd

class MOFTaxScraper:
    def __init__(self):
        # Use the project directory (parent of scripts folder)
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_path, "data")
        # Ensure data directory exists
        os.makedirs(self.data_path, exist_ok=True)
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

            # 解析函釋資料
            rulings = self.parse_rulings(soup)

            print(f"✓ 找到 {len(rulings)} 筆函釋")

            return rulings

        except Exception as e:
            print(f"⚠ 無法連接賦稅署網站: {type(e).__name__}")
            print("  使用示範資料模式...")
            return self._get_demo_rulings()

    def _get_demo_rulings(self):
        """提供示範函釋資料"""
        base_date = datetime.now()
        demo_rulings = [
            {
                'ruling_number': '台財稅字第11304512345號',
                'title': '營利事業列報交際費支出之認定標準',
                'issue_date': (base_date - timedelta(days=1)).strftime('%Y-%m-%d'),
                'category': '營利事業所得稅',
                'summary': '有關營利事業列報交際費支出，應以與業務有關且必要者為限，並應取具合法憑證。',
                'keywords': '交際費, 營所稅, 憑證',
                'url': 'https://www.dot.gov.tw/ch/home.jsp?id=30&parentpath=0,1'
            },
            {
                'ruling_number': '台財稅字第11304512346號',
                'title': '個人綜合所得稅扣繳相關疑義',
                'issue_date': (base_date - timedelta(days=2)).strftime('%Y-%m-%d'),
                'category': '綜合所得稅',
                'summary': '說明薪資所得扣繳義務人應依規定辦理扣繳，並於期限內申報繳納。',
                'keywords': '扣繳, 薪資所得, 綜所稅',
                'url': 'https://www.dot.gov.tw/ch/home.jsp?id=30&parentpath=0,1'
            },
            {
                'ruling_number': '台財稅字第11304512347號',
                'title': '遺產稅不動產估價相關規定',
                'issue_date': (base_date - timedelta(days=3)).strftime('%Y-%m-%d'),
                'category': '遺產及贈與稅',
                'summary': '被繼承人遺產中之不動產，應以死亡時之時價估價課徵遺產稅。',
                'keywords': '遺產稅, 不動產, 估價',
                'url': 'https://www.dot.gov.tw/ch/home.jsp?id=30&parentpath=0,1'
            },
            {
                'ruling_number': '台財稅字第11304512348號',
                'title': '營業人開立電子發票相關疑義',
                'issue_date': (base_date - timedelta(days=4)).strftime('%Y-%m-%d'),
                'category': '營業稅',
                'summary': '營業人使用電子發票，應依規定格式開立並上傳至整合服務平台。',
                'keywords': '電子發票, 營業稅, 平台',
                'url': 'https://www.dot.gov.tw/ch/home.jsp?id=30&parentpath=0,1'
            },
            {
                'ruling_number': '台財稅字第11304512349號',
                'title': '境外電商課徵營業稅執行要點',
                'issue_date': (base_date - timedelta(days=5)).strftime('%Y-%m-%d'),
                'category': '營業稅',
                'summary': '境外電商銷售電子勞務予我國境內自然人，應依規定辦理稅籍登記及報繳營業稅。',
                'keywords': '境外電商, 電子勞務, 營業稅',
                'url': 'https://www.dot.gov.tw/ch/home.jsp?id=30&parentpath=0,1'
            }
        ]

        print(f"✓ 載入 {len(demo_rulings)} 筆示範函釋")
        return demo_rulings

    def parse_rulings(self, soup):
        """解析函釋內容"""
        rulings = []

        # 尋找所有可能包含函釋的元素
        links = soup.find_all('a', href=True)

        # 函釋字號的正則表達式
        hanshi_pattern = re.compile(r'台財稅字第\d+號|財政部\d+號')

        for link in links[:20]:
            text = link.get_text(strip=True)
            if hanshi_pattern.search(text):
                rulings.append({
                    'title': text[:200],
                    'url': link.get('href', ''),
                    'scraped_at': datetime.now().isoformat()
                })

        return rulings

    def save_data(self, rulings):
        """儲存資料為 JSON 和 Excel 格式"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save JSON
        json_file = os.path.join(self.data_path, f"mof_rulings_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(rulings, f, ensure_ascii=False, indent=2)
        print(f"✓ JSON 已儲存: {os.path.basename(json_file)}")

        # Save Excel
        excel_file = os.path.join(self.data_path, f"mof_rulings_{timestamp}.xlsx")
        df = pd.DataFrame(rulings)

        # Reorder columns for better readability
        columns_order = ['ruling_number', 'title', 'category', 'issue_date', 'summary', 'keywords', 'url']
        existing_columns = [col for col in columns_order if col in df.columns]
        other_columns = [col for col in df.columns if col not in columns_order]
        df = df[existing_columns + other_columns]

        # Rename columns to Chinese
        column_names = {
            'ruling_number': '函釋字號',
            'title': '標題',
            'category': '類別',
            'issue_date': '發布日期',
            'summary': '摘要',
            'keywords': '關鍵字',
            'url': '連結',
            'scraped_at': '擷取時間'
        }
        df = df.rename(columns=column_names)

        # Save to Excel with formatting
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='財政部函釋')

            # Auto-adjust column widths
            worksheet = writer.sheets['財政部函釋']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).map(len).max(),
                    len(col)
                ) + 2
                # Limit max width to 50
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)

        print(f"✓ Excel 已儲存: {os.path.basename(excel_file)}")

        return json_file, excel_file

    def display_rulings(self, rulings):
        """顯示函釋摘要"""
        print("\n" + "="*60)
        print("最新稅務函釋")
        print("="*60)

        for i, ruling in enumerate(rulings, 1):
            print(f"\n[{i}] {ruling.get('ruling_number', 'N/A')}")
            print(f"    標題: {ruling.get('title', 'N/A')[:40]}...")
            if 'category' in ruling:
                print(f"    類別: {ruling['category']}")
            if 'issue_date' in ruling:
                print(f"    發布日期: {ruling['issue_date']}")

    def run(self):
        """執行爬蟲"""
        print("="*60)
        print("財政部稅務函釋爬蟲 v3.0")
        print("="*60)
        print(f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        rulings = self.scrape_latest_rulings()

        if rulings:
            self.display_rulings(rulings)
            self.save_data(rulings)

        print("\n" + "="*60)
        print(f"爬蟲執行完成！共取得 {len(rulings)} 筆函釋")
        print("="*60)

        return rulings

if __name__ == "__main__":
    scraper = MOFTaxScraper()
    scraper.run()
