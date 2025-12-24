"""
KM Document Management System - Document Models
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from bson import ObjectId


class DocumentStatus(str, Enum):
    """文件狀態"""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"


class DocumentCategory(str, Enum):
    """文件分類"""
    REGULATION = "規章"
    SOP = "SOP"
    POLICY = "辦法"
    TRAINING = "訓練教材"


@dataclass
class Version:
    """版本資料結構"""
    version: int
    file_name: str
    file_type: str
    file_id: ObjectId
    file_size: int
    uploaded_by: str
    uploaded_at: datetime
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            "version": self.version,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "file_id": self.file_id,
            "file_size": self.file_size,
            "uploaded_by": self.uploaded_by,
            "uploaded_at": self.uploaded_at,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Version":
        """從字典建立"""
        return cls(
            version=data["version"],
            file_name=data["file_name"],
            file_type=data["file_type"],
            file_id=data["file_id"],
            file_size=data["file_size"],
            uploaded_by=data["uploaded_by"],
            uploaded_at=data["uploaded_at"],
            description=data.get("description", "")
        )


@dataclass
class Document:
    """文件資料結構"""
    doc_code: str
    title: str
    department: str
    category: str
    status: str = DocumentStatus.ACTIVE.value
    current_version: int = 1
    versions: List[Version] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典（用於儲存到 MongoDB）"""
        doc = {
            "doc_code": self.doc_code,
            "title": self.title,
            "department": self.department,
            "category": self.category,
            "status": self.status,
            "current_version": self.current_version,
            "versions": [v.to_dict() if isinstance(v, Version) else v for v in self.versions],
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if self._id:
            doc["_id"] = self._id
        return doc
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """從字典建立"""
        versions = [
            Version.from_dict(v) if isinstance(v, dict) else v 
            for v in data.get("versions", [])
        ]
        return cls(
            _id=data.get("_id"),
            doc_code=data["doc_code"],
            title=data["title"],
            department=data["department"],
            category=data["category"],
            status=data.get("status", DocumentStatus.ACTIVE.value),
            current_version=data.get("current_version", 1),
            versions=versions,
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", datetime.now()),
            updated_at=data.get("updated_at", datetime.now())
        )
    
    def get_latest_version(self) -> Optional[Version]:
        """取得最新版本"""
        if self.versions:
            return self.versions[-1]
        return None
    
    def get_version(self, version_num: int) -> Optional[Version]:
        """取得指定版本"""
        for v in self.versions:
            if v.version == version_num:
                return v
        return None
