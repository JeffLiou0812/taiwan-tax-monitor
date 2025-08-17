# database_manager.py - 稅務資料庫管理系統
import sqlite3
import json
import os
from datetime import datetime

class TaxDatabaseManager:
    def __init__(self):
        self.base_path = r"C:\Users\fengy\TaxMonitor\TaxMonitor"
        self.db_path = os.path.join(self.base_path, "data", "tax_monitor.db")
        self.init_database()
        
    def init_database(self):
        """初始化資料庫"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 建立函釋表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tax_rulings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ruling_number TEXT,
                title TEXT,
                content TEXT,
                source TEXT,
                issue_date DATE,
                scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                url TEXT,
                UNIQUE(ruling_number)
            )
        ''')
        
        # 建立新聞表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tax_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                source TEXT,
                publish_date DATE,
                scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                url TEXT
            )
        ''')
        
        # 建立變更追蹤表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS change_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT,
                record_id INTEGER,
                change_type TEXT,
                change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✓ 資料庫初始化完成")
        
    def insert_ruling(self, ruling_data):
        """插入函釋資料"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO tax_rulings 
                (ruling_number, title, content, source, issue_date, url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                ruling_data.get('ruling_number'),
                ruling_data.get('title'),
                ruling_data.get('content'),
                ruling_data.get('source'),
                ruling_data.get('issue_date'),
                ruling_data.get('url')
            ))
            
            conn.commit()
            print(f"✓ 已儲存函釋: {ruling_data.get('ruling_number', 'Unknown')}")
            
        except Exception as e:
            print(f"✗ 儲存失敗: {e}")
            
        finally:
            conn.close()
    
    def get_statistics(self):
        """取得統計資料"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # 函釋總數
        cursor.execute("SELECT COUNT(*) FROM tax_rulings")
        stats['total_rulings'] = cursor.fetchone()[0]
        
        # 新聞總數
        cursor.execute("SELECT COUNT(*) FROM tax_news")
        stats['total_news'] = cursor.fetchone()[0]
        
        # 最新函釋日期
        cursor.execute("SELECT MAX(scraped_date) FROM tax_rulings")
        result = cursor.fetchone()[0]
        stats['last_update'] = result if result else "尚無資料"
        
        conn.close()
        return stats
    
    def search_rulings(self, keyword):
        """搜尋函釋"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ruling_number, title, issue_date 
            FROM tax_rulings 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY issue_date DESC
            LIMIT 10
        ''', (f'%{keyword}%', f'%{keyword}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def generate_report(self):
        """生成報告"""
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("稅務資料庫統計報告")
        print("="*60)
        print(f"函釋總數: {stats['total_rulings']}")
        print(f"新聞總數: {stats['total_news']}")
        print(f"最後更新: {stats['last_update']}")
        print("="*60)
        
        return stats

if __name__ == "__main__":
    db = TaxDatabaseManager()
    
    # 測試插入資料
    test_ruling = {
        'ruling_number': '台財稅字第11300000000號',
        'title': '測試函釋標題',
        'content': '測試內容',
        'source': '財政部',
        'issue_date': '2024-08-17',
        'url': 'https://example.com'
    }
    
    db.insert_ruling(test_ruling)
    
    # 生成報告
    db.generate_report()
    
    # 測試搜尋
    results = db.search_rulings("測試")
    if results:
        print("\n搜尋結果:")
        for r in results:
            print(f"- {r[0]}: {r[1]}")