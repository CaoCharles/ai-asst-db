"""
KM Document Management System - Document Service
實作所有文件相關的業務邏輯
"""
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId

from db.connection import get_db_connection, MongoDBConnection
from models.document import Document, Version, DocumentStatus


class DocumentService:
    """文件操作服務類別"""
    
    def __init__(self, connection: Optional[MongoDBConnection] = None):
        self.conn = connection or get_db_connection()
    
    # ============================================================
    # F-001: 文件上傳
    # ============================================================
    def upload_document(
        self,
        file_path: str,
        doc_code: str,
        title: str,
        department: str,
        category: str,
        uploaded_by: str,
        metadata: Optional[Dict[str, Any]] = None,
        description: str = "初版"
    ) -> Document:
        """
        上傳新文件
        
        Args:
            file_path: 檔案路徑
            doc_code: 文件編號（唯一）
            title: 文件標題
            department: 所屬部門
            category: 分類
            uploaded_by: 上傳者
            metadata: 彈性 Metadata
            description: 版本說明
        
        Returns:
            Document: 新建立的文件物件
        """
        # 檢查文件編號是否已存在
        if self.get_by_doc_code(doc_code):
            raise ValueError(f"文件編號 {doc_code} 已存在")
        
        # 讀取檔案
        file_name = os.path.basename(file_path)
        file_type = file_name.split(".")[-1].lower()
        
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_size = len(file_data)
            file_id = self.conn.fs.put(file_data, filename=file_name)
        
        # 建立版本
        version = Version(
            version=1,
            file_name=file_name,
            file_type=file_type,
            file_id=file_id,
            file_size=file_size,
            uploaded_by=uploaded_by,
            uploaded_at=datetime.now(),
            description=description
        )
        
        # 建立文件
        doc = Document(
            doc_code=doc_code,
            title=title,
            department=department,
            category=category,
            status=DocumentStatus.ACTIVE.value,
            current_version=1,
            versions=[version],
            metadata=metadata or {},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # 儲存到資料庫
        result = self.conn.documents.insert_one(doc.to_dict())
        doc._id = result.inserted_id
        
        print(f"✓ 文件上傳成功: {doc_code} - {title}")
        return doc
    
    # ============================================================
    # F-002: 版本控管
    # ============================================================
    def upload_new_version(
        self,
        doc_code: str,
        file_path: str,
        uploaded_by: str,
        description: str = ""
    ) -> Document:
        """
        上傳新版本
        
        Args:
            doc_code: 文件編號
            file_path: 新版本檔案路徑
            uploaded_by: 上傳者
            description: 版本說明/變更摘要
        
        Returns:
            Document: 更新後的文件物件
        """
        # 取得現有文件
        doc = self.get_by_doc_code(doc_code)
        if not doc:
            raise ValueError(f"找不到文件: {doc_code}")
        
        # 計算新版本號
        new_version_num = doc.current_version + 1
        
        # 讀取檔案
        file_name = os.path.basename(file_path)
        file_type = file_name.split(".")[-1].lower()
        
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_size = len(file_data)
            file_id = self.conn.fs.put(file_data, filename=file_name)
        
        # 建立新版本
        new_version = Version(
            version=new_version_num,
            file_name=file_name,
            file_type=file_type,
            file_id=file_id,
            file_size=file_size,
            uploaded_by=uploaded_by,
            uploaded_at=datetime.now(),
            description=description
        )
        
        # 更新資料庫
        self.conn.documents.update_one(
            {"doc_code": doc_code},
            {
                "$set": {
                    "current_version": new_version_num,
                    "updated_at": datetime.now()
                },
                "$push": {
                    "versions": new_version.to_dict()
                }
            }
        )
        
        print(f"✓ 新版本上傳成功: {doc_code} v{new_version_num}")
        return self.get_by_doc_code(doc_code)
    
    # ============================================================
    # F-003: Metadata 管理
    # ============================================================
    def update_metadata(
        self,
        doc_code: str,
        metadata: Dict[str, Any],
        merge: bool = True
    ) -> Document:
        """
        更新 Metadata
        
        Args:
            doc_code: 文件編號
            metadata: 新的 Metadata
            merge: 是否合併現有 Metadata（False 則完全覆蓋）
        
        Returns:
            Document: 更新後的文件物件
        """
        doc = self.get_by_doc_code(doc_code)
        if not doc:
            raise ValueError(f"找不到文件: {doc_code}")
        
        if merge:
            # 合併現有 Metadata
            new_metadata = {**doc.metadata, **metadata}
        else:
            new_metadata = metadata
        
        self.conn.documents.update_one(
            {"doc_code": doc_code},
            {
                "$set": {
                    "metadata": new_metadata,
                    "updated_at": datetime.now()
                }
            }
        )
        
        print(f"✓ Metadata 更新成功: {doc_code}")
        return self.get_by_doc_code(doc_code)
    
    # ============================================================
    # F-004: 文件查詢
    # ============================================================
    def search(
        self,
        department: Optional[str] = None,
        category: Optional[str] = None,
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        include_archived: bool = False
    ) -> List[Document]:
        """
        搜尋文件
        
        Args:
            department: 部門篩選
            category: 分類篩選
            keyword: 關鍵字搜尋（標題或 metadata.keywords）
            status: 狀態篩選
            include_archived: 是否包含已歸檔文件
        
        Returns:
            List[Document]: 符合條件的文件列表
        """
        query: Dict[str, Any] = {}
        
        # 狀態篩選
        if status:
            query["status"] = status
        elif not include_archived:
            query["status"] = {"$ne": DocumentStatus.ARCHIVED.value}
        
        # 部門篩選
        if department:
            query["department"] = department
        
        # 分類篩選
        if category:
            query["category"] = category
        
        # 關鍵字搜尋
        if keyword:
            query["$or"] = [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"metadata.keywords": keyword},
                {"doc_code": {"$regex": keyword, "$options": "i"}}
            ]
        
        # 執行查詢
        results = self.conn.documents.find(query).sort("updated_at", -1)
        return [Document.from_dict(doc) for doc in results]
    
    def get_by_doc_code(self, doc_code: str) -> Optional[Document]:
        """根據文件編號取得文件"""
        doc = self.conn.documents.find_one({"doc_code": doc_code})
        if doc:
            return Document.from_dict(doc)
        return None
    
    def get_all(self, include_archived: bool = False) -> List[Document]:
        """取得所有文件"""
        return self.search(include_archived=include_archived)
    
    # ============================================================
    # F-005: 版本歷史
    # ============================================================
    def get_version_history(self, doc_code: str) -> List[Version]:
        """
        取得文件版本歷史
        
        Args:
            doc_code: 文件編號
        
        Returns:
            List[Version]: 版本歷史列表
        """
        doc = self.get_by_doc_code(doc_code)
        if not doc:
            raise ValueError(f"找不到文件: {doc_code}")
        
        return doc.versions
    
    def get_version(self, doc_code: str, version_num: int) -> Optional[Version]:
        """取得指定版本"""
        doc = self.get_by_doc_code(doc_code)
        if not doc:
            return None
        return doc.get_version(version_num)
    
    # ============================================================
    # F-006: 文件下載
    # ============================================================
    def download_file(
        self,
        doc_code: str,
        version_num: Optional[int] = None,
        save_path: Optional[str] = None
    ) -> str:
        """
        下載文件
        
        Args:
            doc_code: 文件編號
            version_num: 版本號（預設為最新版本）
            save_path: 儲存路徑（預設為當前目錄）
        
        Returns:
            str: 儲存的檔案路徑
        """
        doc = self.get_by_doc_code(doc_code)
        if not doc:
            raise ValueError(f"找不到文件: {doc_code}")
        
        # 取得版本
        if version_num:
            version = doc.get_version(version_num)
            if not version:
                raise ValueError(f"找不到版本: {doc_code} v{version_num}")
        else:
            version = doc.get_latest_version()
            if not version:
                raise ValueError(f"文件沒有任何版本: {doc_code}")
        
        # 從 GridFS 讀取檔案
        file_data = self.conn.fs.get(version.file_id).read()
        
        # 決定儲存路徑
        if save_path:
            file_path = save_path
        else:
            file_path = version.file_name
        
        # 寫入檔案
        with open(file_path, "wb") as f:
            f.write(file_data)
        
        print(f"✓ 檔案下載成功: {file_path}")
        return file_path
    
    # ============================================================
    # F-007: 文件歸檔
    # ============================================================
    def archive_document(self, doc_code: str) -> Document:
        """
        歸檔文件
        
        Args:
            doc_code: 文件編號
        
        Returns:
            Document: 更新後的文件物件
        """
        doc = self.get_by_doc_code(doc_code)
        if not doc:
            raise ValueError(f"找不到文件: {doc_code}")
        
        if doc.status == DocumentStatus.ARCHIVED.value:
            print(f"! 文件已經是歸檔狀態: {doc_code}")
            return doc
        
        self.conn.documents.update_one(
            {"doc_code": doc_code},
            {
                "$set": {
                    "status": DocumentStatus.ARCHIVED.value,
                    "updated_at": datetime.now()
                }
            }
        )
        
        print(f"✓ 文件已歸檔: {doc_code}")
        return self.get_by_doc_code(doc_code)
    
    def restore_document(self, doc_code: str) -> Document:
        """
        恢復歸檔文件
        
        Args:
            doc_code: 文件編號
        
        Returns:
            Document: 更新後的文件物件
        """
        doc = self.get_by_doc_code(doc_code)
        if not doc:
            raise ValueError(f"找不到文件: {doc_code}")
        
        self.conn.documents.update_one(
            {"doc_code": doc_code},
            {
                "$set": {
                    "status": DocumentStatus.ACTIVE.value,
                    "updated_at": datetime.now()
                }
            }
        )
        
        print(f"✓ 文件已恢復: {doc_code}")
        return self.get_by_doc_code(doc_code)
    
    # ============================================================
    # 額外工具方法
    # ============================================================
    def delete_document(self, doc_code: str, delete_files: bool = True) -> bool:
        """
        刪除文件（慎用）
        
        Args:
            doc_code: 文件編號
            delete_files: 是否同時刪除 GridFS 中的檔案
        
        Returns:
            bool: 是否成功刪除
        """
        doc = self.get_by_doc_code(doc_code)
        if not doc:
            return False
        
        # 刪除 GridFS 檔案
        if delete_files:
            for version in doc.versions:
                try:
                    self.conn.fs.delete(version.file_id)
                except Exception:
                    pass
        
        # 刪除文件記錄
        self.conn.documents.delete_one({"doc_code": doc_code})
        print(f"✓ 文件已刪除: {doc_code}")
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """取得統計資訊"""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_documents": {"$sum": 1},
                    "total_versions": {"$sum": {"$size": "$versions"}},
                    "by_department": {
                        "$push": "$department"
                    },
                    "by_category": {
                        "$push": "$category"
                    },
                    "by_status": {
                        "$push": "$status"
                    }
                }
            }
        ]
        
        results = list(self.conn.documents.aggregate(pipeline))
        
        if not results:
            return {
                "total_documents": 0,
                "total_versions": 0,
                "by_department": {},
                "by_category": {},
                "by_status": {}
            }
        
        result = results[0]
        
        # 計算各分類統計
        def count_items(items):
            counts = {}
            for item in items:
                counts[item] = counts.get(item, 0) + 1
            return counts
        
        return {
            "total_documents": result["total_documents"],
            "total_versions": result["total_versions"],
            "by_department": count_items(result["by_department"]),
            "by_category": count_items(result["by_category"]),
            "by_status": count_items(result["by_status"])
        }
