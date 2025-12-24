#!/usr/bin/env python3
"""
勞動基準法 JSON 匯入腳本
將結構化的法規 JSON 批次匯入 KM 文件管理系統
"""
import sys
import os
import json
from datetime import datetime

# 加入專案根目錄
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.document_service import DocumentService


def import_labor_law_json(json_path: str):
    """匯入勞基法 JSON 檔案"""
    
    print("=" * 60)
    print("勞動基準法 批次匯入程式")
    print("=" * 60)
    
    # 讀取 JSON
    print(f"\n📂 讀取 JSON 檔案: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        law_data = json.load(f)
    
    print(f"   法規名稱: {law_data['law_name']}")
    print(f"   版本: {law_data['version']}")
    print(f"   條文數量: {len(law_data['articles'])} 條")
    
    # 建立服務
    service = DocumentService()
    
    # 統計
    success_count = 0
    skip_count = 0
    error_count = 0
    
    print("\n📝 開始匯入條文...\n")
    
    for article in law_data["articles"]:
        article_id = article["article_id"]
        doc_code = f"LAW-LSA-{article_id.replace('第', '').replace('條', '').zfill(3)}"
        title = f"勞基法 {article_id} {article['title']}"
        
        # 建立條文內容檔案
        content = f"""勞動基準法
{article['chapter']}

{article_id}（{article['title']}）

{article['content']}

---
來源：{law_data['source']}
版本：{law_data['version']}
"""
        
        # 寫入暫存檔
        temp_file = f"/tmp/{doc_code}.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        # 準備 metadata
        metadata = {
            "law_name": law_data["law_name"],
            "law_version": law_data["version"],
            "effective_date": law_data["effective_date"],
            "chapter": article["chapter"],
            "article_id": article_id,
            "article_title": article["title"],
            "keywords": article.get("keywords", []),
            "importance": article.get("importance", "medium"),
            "source": law_data["source"]
        }
        
        # 加入條文特有資料
        for key in ["definitions", "contract_types", "working_hours", 
                    "overtime_limits", "rest_days", "annual_leave",
                    "age_restrictions", "night_work", "voluntary_retirement",
                    "mandatory_retirement", "compensation_types", 
                    "current_minimum_wage", "principles", "holiday_types"]:
            if key in article:
                metadata[key] = article[key]
        
        try:
            # 檢查是否已存在
            existing = service.get_by_doc_code(doc_code)
            if existing:
                print(f"   ⏭️  {doc_code} 已存在，略過")
                skip_count += 1
            else:
                # 上傳文件
                service.upload_document(
                    file_path=temp_file,
                    doc_code=doc_code,
                    title=title,
                    department="人力資源部",
                    category="規章",
                    uploaded_by="system_import",
                    metadata=metadata,
                    description=f"勞動基準法 {article_id} 自動匯入"
                )
                print(f"   ✅ {doc_code}: {title}")
                success_count += 1
                
        except Exception as e:
            print(f"   ❌ {doc_code} 匯入失敗: {e}")
            error_count += 1
        
        # 清理暫存檔
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    # 匯入總表文件
    print("\n📚 匯入法規總表...")
    
    # 建立總表檔案
    summary_content = f"""勞動基準法 總覽
{'='*50}

法規名稱：{law_data['law_name']}
英文名稱：{law_data['law_name_en']}
版本：{law_data['version']}
生效日期：{law_data['effective_date']}
來源：{law_data['source']}

總章數：{law_data['metadata']['total_chapters']} 章
總條數：{law_data['metadata']['total_articles']} 條
主管機關：{law_data['metadata']['authority']}

{'='*50}
已收錄條文：
"""
    for article in law_data["articles"]:
        summary_content += f"\n• {article['article_id']} {article['title']}"
    
    summary_content += f"""

{'='*50}
最後更新：{law_data['last_updated']}
"""
    
    summary_file = "/tmp/LAW-LSA-000.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    try:
        existing = service.get_by_doc_code("LAW-LSA-000")
        if existing:
            print("   ⏭️  LAW-LSA-000 總表已存在，略過")
            skip_count += 1
        else:
            service.upload_document(
                file_path=summary_file,
                doc_code="LAW-LSA-000",
                title="勞動基準法 總覽",
                department="人力資源部",
                category="規章",
                uploaded_by="system_import",
                metadata={
                    "law_name": law_data["law_name"],
                    "law_version": law_data["version"],
                    "keywords": law_data["metadata"]["keywords"],
                    "total_chapters": law_data["metadata"]["total_chapters"],
                    "total_articles": law_data["metadata"]["total_articles"],
                    "authority": law_data["metadata"]["authority"],
                    "source": law_data["source"],
                    "is_summary": True
                },
                description="勞動基準法總覽文件"
            )
            print("   ✅ LAW-LSA-000: 勞動基準法 總覽")
            success_count += 1
    except Exception as e:
        print(f"   ❌ 總表匯入失敗: {e}")
        error_count += 1
    
    os.remove(summary_file)
    
    # 結果統計
    print("\n" + "=" * 60)
    print("📊 匯入結果統計")
    print("=" * 60)
    print(f"   ✅ 成功匯入: {success_count} 筆")
    print(f"   ⏭️  略過（已存在）: {skip_count} 筆")
    print(f"   ❌ 失敗: {error_count} 筆")
    print("=" * 60)
    
    # 顯示系統統計
    print("\n📊 系統統計:")
    stats = service.get_statistics()
    print(f"   總文件數: {stats['total_documents']}")
    print(f"   總版本數: {stats['total_versions']}")
    
    return success_count, skip_count, error_count


if __name__ == "__main__":
    # 預設 JSON 路徑
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "勞動基準法.json"
    )
    
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    
    if not os.path.exists(json_path):
        print(f"❌ 找不到檔案: {json_path}")
        sys.exit(1)
    
    import_labor_law_json(json_path)
