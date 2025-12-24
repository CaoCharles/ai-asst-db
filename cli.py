#!/usr/bin/env python3
"""
KM Document Management System - Command Line Interface
提供命令列操作文件管理系統
"""
import argparse
import sys
import os
from datetime import datetime

# 加入專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.document_service import DocumentService
from models.document import DocumentCategory

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


def format_size(size_bytes: int) -> str:
    """格式化檔案大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def format_date(dt: datetime) -> str:
    """格式化日期"""
    return dt.strftime("%Y-%m-%d %H:%M")


def print_table(headers, rows):
    """列印表格"""
    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        # 簡易表格輸出
        print(" | ".join(headers))
        print("-" * 80)
        for row in rows:
            print(" | ".join(str(cell) for cell in row))


def cmd_upload(args):
    """上傳文件"""
    service = DocumentService()
    
    metadata = {}
    if args.keywords:
        metadata["keywords"] = args.keywords.split(",")
    if args.owner:
        metadata["owner"] = args.owner
    
    doc = service.upload_document(
        file_path=args.file,
        doc_code=args.code,
        title=args.title,
        department=args.department,
        category=args.category,
        uploaded_by=args.user,
        metadata=metadata,
        description=args.description or "初版"
    )
    
    print(f"\n文件編號: {doc.doc_code}")
    print(f"標題: {doc.title}")
    print(f"部門: {doc.department}")
    print(f"分類: {doc.category}")


def cmd_version(args):
    """上傳新版本"""
    service = DocumentService()
    
    doc = service.upload_new_version(
        doc_code=args.code,
        file_path=args.file,
        uploaded_by=args.user,
        description=args.description or ""
    )
    
    print(f"\n當前版本: v{doc.current_version}")


def cmd_list(args):
    """列出文件"""
    service = DocumentService()
    
    docs = service.search(
        department=args.department,
        category=args.category,
        keyword=args.keyword,
        include_archived=args.archived
    )
    
    if not docs:
        print("沒有找到符合條件的文件")
        return
    
    headers = ["編號", "標題", "部門", "分類", "版本", "狀態", "更新時間"]
    rows = []
    
    for doc in docs:
        rows.append([
            doc.doc_code,
            doc.title[:30] + "..." if len(doc.title) > 30 else doc.title,
            doc.department,
            doc.category,
            f"v{doc.current_version}",
            doc.status,
            format_date(doc.updated_at)
        ])
    
    print(f"\n共找到 {len(docs)} 筆文件:\n")
    print_table(headers, rows)


def cmd_info(args):
    """查看文件詳情"""
    service = DocumentService()
    
    doc = service.get_by_doc_code(args.code)
    if not doc:
        print(f"找不到文件: {args.code}")
        return
    
    print("\n" + "=" * 50)
    print(f"文件編號: {doc.doc_code}")
    print(f"標題: {doc.title}")
    print(f"部門: {doc.department}")
    print(f"分類: {doc.category}")
    print(f"狀態: {doc.status}")
    print(f"當前版本: v{doc.current_version}")
    print(f"建立時間: {format_date(doc.created_at)}")
    print(f"更新時間: {format_date(doc.updated_at)}")
    
    if doc.metadata:
        print(f"\nMetadata:")
        for key, value in doc.metadata.items():
            print(f"  {key}: {value}")
    
    print("\n版本歷史:")
    headers = ["版本", "檔案名稱", "大小", "上傳者", "上傳時間", "說明"]
    rows = []
    
    for v in doc.versions:
        rows.append([
            f"v{v.version}",
            v.file_name,
            format_size(v.file_size),
            v.uploaded_by,
            format_date(v.uploaded_at),
            v.description[:20] + "..." if len(v.description) > 20 else v.description
        ])
    
    print_table(headers, rows)
    print("=" * 50)


def cmd_download(args):
    """下載文件"""
    service = DocumentService()
    
    file_path = service.download_file(
        doc_code=args.code,
        version_num=args.version,
        save_path=args.output
    )
    
    print(f"檔案已儲存至: {file_path}")


def cmd_archive(args):
    """歸檔文件"""
    service = DocumentService()
    service.archive_document(args.code)


def cmd_restore(args):
    """恢復文件"""
    service = DocumentService()
    service.restore_document(args.code)


def cmd_stats(args):
    """顯示統計"""
    service = DocumentService()
    stats = service.get_statistics()
    
    print("\n" + "=" * 50)
    print("KM 文件管理系統統計")
    print("=" * 50)
    print(f"\n總文件數: {stats['total_documents']}")
    print(f"總版本數: {stats['total_versions']}")
    
    if stats['by_department']:
        print("\n依部門統計:")
        for dept, count in stats['by_department'].items():
            print(f"  {dept}: {count}")
    
    if stats['by_category']:
        print("\n依分類統計:")
        for cat, count in stats['by_category'].items():
            print(f"  {cat}: {count}")
    
    if stats['by_status']:
        print("\n依狀態統計:")
        for status, count in stats['by_status'].items():
            print(f"  {status}: {count}")
    
    print("=" * 50)


def cmd_delete(args):
    """刪除文件"""
    service = DocumentService()
    
    if not args.force:
        confirm = input(f"確定要刪除文件 {args.code}？此操作無法復原 (y/N): ")
        if confirm.lower() != 'y':
            print("已取消")
            return
    
    if service.delete_document(args.code):
        print(f"文件 {args.code} 已刪除")
    else:
        print(f"找不到文件: {args.code}")


def main():
    parser = argparse.ArgumentParser(
        description="KM 文件管理系統 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  # 上傳新文件
  python cli.py upload -f doc.pdf -c HR-001 -t "請假規定" -d 人力資源部 -cat 規章 -u admin

  # 上傳新版本
  python cli.py version -c HR-001 -f doc_v2.pdf -u admin -desc "更新請假天數"

  # 列出所有文件
  python cli.py list

  # 搜尋文件
  python cli.py list -d 人力資源部 -k 請假

  # 查看文件詳情
  python cli.py info -c HR-001

  # 下載文件
  python cli.py download -c HR-001 -o ./downloads/

  # 歸檔文件
  python cli.py archive -c HR-001

  # 查看統計
  python cli.py stats
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # upload 命令
    upload_parser = subparsers.add_parser("upload", help="上傳新文件")
    upload_parser.add_argument("-f", "--file", required=True, help="檔案路徑")
    upload_parser.add_argument("-c", "--code", required=True, help="文件編號")
    upload_parser.add_argument("-t", "--title", required=True, help="文件標題")
    upload_parser.add_argument("-d", "--department", required=True, help="所屬部門")
    upload_parser.add_argument("-cat", "--category", required=True, 
                               choices=["規章", "SOP", "辦法", "訓練教材"],
                               help="文件分類")
    upload_parser.add_argument("-u", "--user", required=True, help="上傳者")
    upload_parser.add_argument("-desc", "--description", help="版本說明")
    upload_parser.add_argument("-k", "--keywords", help="關鍵字（逗號分隔）")
    upload_parser.add_argument("-o", "--owner", help="文件負責人")
    upload_parser.set_defaults(func=cmd_upload)
    
    # version 命令
    version_parser = subparsers.add_parser("version", help="上傳新版本")
    version_parser.add_argument("-c", "--code", required=True, help="文件編號")
    version_parser.add_argument("-f", "--file", required=True, help="檔案路徑")
    version_parser.add_argument("-u", "--user", required=True, help="上傳者")
    version_parser.add_argument("-desc", "--description", help="版本說明")
    version_parser.set_defaults(func=cmd_version)
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出文件")
    list_parser.add_argument("-d", "--department", help="部門篩選")
    list_parser.add_argument("-cat", "--category", help="分類篩選")
    list_parser.add_argument("-k", "--keyword", help="關鍵字搜尋")
    list_parser.add_argument("-a", "--archived", action="store_true", help="包含已歸檔文件")
    list_parser.set_defaults(func=cmd_list)
    
    # info 命令
    info_parser = subparsers.add_parser("info", help="查看文件詳情")
    info_parser.add_argument("-c", "--code", required=True, help="文件編號")
    info_parser.set_defaults(func=cmd_info)
    
    # download 命令
    download_parser = subparsers.add_parser("download", help="下載文件")
    download_parser.add_argument("-c", "--code", required=True, help="文件編號")
    download_parser.add_argument("-v", "--version", type=int, help="版本號（預設最新）")
    download_parser.add_argument("-o", "--output", help="輸出路徑")
    download_parser.set_defaults(func=cmd_download)
    
    # archive 命令
    archive_parser = subparsers.add_parser("archive", help="歸檔文件")
    archive_parser.add_argument("-c", "--code", required=True, help="文件編號")
    archive_parser.set_defaults(func=cmd_archive)
    
    # restore 命令
    restore_parser = subparsers.add_parser("restore", help="恢復歸檔文件")
    restore_parser.add_argument("-c", "--code", required=True, help="文件編號")
    restore_parser.set_defaults(func=cmd_restore)
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="顯示統計")
    stats_parser.set_defaults(func=cmd_stats)
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="刪除文件（慎用）")
    delete_parser.add_argument("-c", "--code", required=True, help="文件編號")
    delete_parser.add_argument("-f", "--force", action="store_true", help="強制刪除不確認")
    delete_parser.set_defaults(func=cmd_delete)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
