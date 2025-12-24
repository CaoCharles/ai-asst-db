#!/usr/bin/env python3
"""
KM Document Management System - Database Initialization Script
建立資料庫與索引
"""
import sys
import os

# 加入專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_db_connection


def init_database():
    """初始化資料庫"""
    print("=" * 50)
    print("KM 文件管理系統 - 資料庫初始化")
    print("=" * 50)
    
    # 建立連線
    conn = get_db_connection()
    
    # 測試連線
    if not conn.ping():
        print("✗ 無法連線到 MongoDB，請確認服務是否已啟動")
        return False
    
    print(f"✓ 成功連線到 MongoDB")
    
    # 建立索引
    print("\n建立索引...")
    
    # doc_code 唯一索引
    conn.documents.create_index("doc_code", unique=True, name="idx_doc_code")
    print("  ✓ doc_code 唯一索引")
    
    # department 索引
    conn.documents.create_index("department", name="idx_department")
    print("  ✓ department 索引")
    
    # category 索引
    conn.documents.create_index("category", name="idx_category")
    print("  ✓ category 索引")
    
    # status 索引
    conn.documents.create_index("status", name="idx_status")
    print("  ✓ status 索引")
    
    # title 全文索引
    conn.documents.create_index([("title", "text")], name="idx_title_text")
    print("  ✓ title 全文索引")
    
    # 複合索引：department + category + status
    conn.documents.create_index(
        [("department", 1), ("category", 1), ("status", 1)],
        name="idx_dept_cat_status"
    )
    print("  ✓ 複合索引 (department, category, status)")
    
    print("\n" + "=" * 50)
    print("✓ 資料庫初始化完成！")
    print("=" * 50)
    
    # 顯示資料庫資訊
    print(f"\n資料庫名稱: {conn.db.name}")
    print(f"Collections: {conn.db.list_collection_names()}")
    print(f"documents 索引: {list(conn.documents.list_indexes())}")
    
    return True


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
