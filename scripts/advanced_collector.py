# advanced_collector.py - 進階稅務資料收集系統
import requests
from bs4 import BeautifulSoup
import feedparser
import json
import os
from datetime import datetime
from database_manager import TaxDatabaseManager

class AdvancedTaxCollector:
    def __init__(self):
        self.base_path = r"C:\Users\fengy\TaxMonitor\TaxMonitor"
        self.db = TaxDatabaseManager()
        
        # 多元化資料源策略
        self.rss_feeds = {
            '財政部RSS': 'https://www.mof.gov.tw/RSS/Rss.ashx?Type=News',
            '賦稅署RSS': 'https://www.dot.gov.tw/RSS.xml'
        }
        
        # API端點（若可用）
        self.api_endpoints = {
            '全國法規資料庫': 'https://law.moj.gov.tw/api/v1/laws',
            '政府資料開放平台': 'https://data.gov.tw/api/v2/rest/datastore'
        }
        
    def collect_rss_feeds(self):
        """RSS訂閱源收集策略"""
        all_items = []
        
        for source, url in self.rss_feeds.items():
            print(f"\n處理RSS源: {source}")
            try:
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:10]:
                    item = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', ''),
                        'source': source,
                        'type': 'RSS'
                    }
                    all_items.append(item)
                    
                    # 檢查是否為函釋
                    if any(keyword in entry.title for keyword in ['函釋', '解釋', '令']):
                        self.process_ruling(item)
                        
                print(f"✓ 從 {source} 收集 {len(feed.entries)} 項")
                
            except Exception as e:
                print(f"✗ RSS處理失敗: {e}")
                
        return all_items
    
    def process_ruling(self, item):
        """處理潛在的函釋資料"""
        ruling_data = {
            'ruling_number': self.extract_ruling_number(item['title']),
            'title': item['title'],
            'content': item.get('summary', ''),
            'source': item['source'],
            'issue_date': item.get('published', ''),
            'url': item.get('link', '')
        }
        
        if ruling_data['ruling_number']:
            self.db.insert_ruling(ruling_data)
    
    def extract_ruling_number(self, text):
        """提取函釋字號"""
        import re
        patterns = [
            r'台財稅字第\d+號',
            r'財政部\d+號',
            r'\d{10,12}號'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        return None
    
    def generate_collection_report(self, data):
        """生成收集報告"""
        report = {
            'collection_time': datetime.now().isoformat(),
            'total_items': len(data),
            'sources': list(set(item['source'] for item in data)),
            'types': list(set(item.get('type', 'Unknown') for item in data))
        }
        
        # 儲存報告
        report_file = os.path.join(
            self.base_path, 'data', 
            f'collection_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n報告已生成: {os.path.basename(report_file)}")
        return report
    
    def run_advanced_collection(self):
        """執行進階收集流程"""
        print("="*60)
        print("進階稅務資料收集系統 v3.0")
        print("="*60)
        
        # 1. RSS收集
        rss_data = self.collect_rss_feeds()
        
        # 2. 生成報告
        report = self.generate_collection_report(rss_data)
        
        # 3. 資料庫統計
        self.db.generate_report()
        
        return report

if __name__ == "__main__":
    collector = AdvancedTaxCollector()
    collector.run_advanced_collection()