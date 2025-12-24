"""
KM Document Management System - Configuration Settings
"""
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Settings:
    """系統設定類別"""
    
    # MongoDB 連線設定
    mongo_host: str = field(default_factory=lambda: os.getenv("MONGO_HOST", "localhost"))
    mongo_port: int = field(default_factory=lambda: int(os.getenv("MONGO_PORT", "27017")))
    mongo_username: Optional[str] = field(default_factory=lambda: os.getenv("MONGO_USERNAME"))
    mongo_password: Optional[str] = field(default_factory=lambda: os.getenv("MONGO_PASSWORD"))
    
    # 資料庫名稱
    database_name: str = field(default_factory=lambda: os.getenv("MONGO_DATABASE", "km_system"))
    
    # Collection 名稱
    documents_collection: str = "documents"
    
    @property
    def connection_string(self) -> str:
        """產生 MongoDB 連線字串"""
        if self.mongo_username and self.mongo_password:
            return f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/"
        return f"mongodb://{self.mongo_host}:{self.mongo_port}/"


# 全域設定實例
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """取得設定實例（單例模式）"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
