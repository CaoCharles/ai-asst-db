#!/usr/bin/env python3
"""
KM 文件管理系統使用範例
展示各項功能的基本操作
"""
import sys
import os

# 加入專案根目錄
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.document_service import DocumentService


def main():
    """主程式：展示系統功能"""
    
    print("=" * 60)
    print("KM 文件管理系統使用範例")
    print("=" * 60)
    
    # 建立服務實例
    service = DocumentService()
    
    # ========================================
    # 1. 建立測試文件
    # ========================================
    print("\n📝 1. 建立測試文件...")
    
    test_file = "example_doc.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("這是一份測試文件\n")
        f.write("用於展示 KM 文件管理系統功能\n")
    
    # ========================================
    # 2. 上傳文件
    # ========================================
    print("\n📤 2. 上傳文件...")
    
    try:
        doc = service.upload_document(
            file_path=test_file,
            doc_code="DEMO-001",
            title="系統功能展示文件",
            department="IT部門",
            category="訓練教材",
            uploaded_by="demo_user",
            metadata={
                "keywords": ["展示", "範例", "教學"],
                "owner": "系統管理員"
            },
            description="初版 - 功能展示用"
        )
        print(f"   ✓ 文件已上傳: {doc.doc_code}")
    except ValueError as e:
        print(f"   ! {e}")
        doc = service.get_by_doc_code("DEMO-001")
    
    # ========================================
    # 3. 上傳新版本
    # ========================================
    print("\n🔄 3. 上傳新版本...")
    
    # 建立新版本檔案
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("這是一份測試文件（修訂版）\n")
        f.write("用於展示 KM 文件管理系統功能\n")
        f.write("新增：版本控管說明\n")
    
    doc = service.upload_new_version(
        doc_code="DEMO-001",
        file_path=test_file,
        uploaded_by="demo_user",
        description="第二版 - 新增版本控管說明"
    )
    print(f"   ✓ 新版本已上傳: v{doc.current_version}")
    
    # ========================================
    # 4. 更新 Metadata
    # ========================================
    print("\n🏷️ 4. 更新 Metadata...")
    
    doc = service.update_metadata(
        doc_code="DEMO-001",
        metadata={
            "review_cycle": "每季",
            "last_reviewed": "2024-12-01"
        }
    )
    print(f"   ✓ Metadata 已更新")
    print(f"   當前 Metadata: {doc.metadata}")
    
    # ========================================
    # 5. 搜尋文件
    # ========================================
    print("\n🔍 5. 搜尋文件...")
    
    # 依部門搜尋
    results = service.search(department="IT部門")
    print(f"   IT部門文件: {len(results)} 筆")
    
    # 關鍵字搜尋
    results = service.search(keyword="展示")
    print(f"   關鍵字「展示」: {len(results)} 筆")
    
    # ========================================
    # 6. 查看版本歷史
    # ========================================
    print("\n📜 6. 版本歷史...")
    
    versions = service.get_version_history("DEMO-001")
    for v in versions:
        print(f"   v{v.version}: {v.description} (by {v.uploaded_by})")
    
    # ========================================
    # 7. 下載文件
    # ========================================
    print("\n📥 7. 下載文件...")
    
    downloaded_file = service.download_file(
        doc_code="DEMO-001",
        save_path="downloaded_demo.txt"
    )
    print(f"   ✓ 已下載至: {downloaded_file}")
    
    # 讀取並顯示內容
    with open(downloaded_file, "r", encoding="utf-8") as f:
        print(f"   內容預覽:\n{f.read()}")
    
    # ========================================
    # 8. 統計資訊
    # ========================================
    print("\n📊 8. 統計資訊...")
    
    stats = service.get_statistics()
    print(f"   總文件數: {stats['total_documents']}")
    print(f"   總版本數: {stats['total_versions']}")
    
    # ========================================
    # 清理
    # ========================================
    print("\n🧹 清理測試檔案...")
    os.remove(test_file)
    os.remove(downloaded_file)
    
    # 詢問是否刪除測試文件
    # service.delete_document("DEMO-001")
    
    print("\n" + "=" * 60)
    print("✅ 範例執行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
