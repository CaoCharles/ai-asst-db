"""
KM Document Management System - MongoDB Connection Manager
"""
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from gridfs import GridFS

from config.settings import get_settings, Settings


class MongoDBConnection:
    """MongoDB 連線管理類別（單例模式）"""
    
    _instance: Optional["MongoDBConnection"] = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None
    _fs: Optional[GridFS] = None
    
    def __new__(cls, settings: Optional[Settings] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, settings: Optional[Settings] = None):
        if self._client is None:
            self._settings = settings or get_settings()
            self._connect()
    
    def _connect(self) -> None:
        """建立資料庫連線"""
        self._client = MongoClient(self._settings.connection_string)
        self._db = self._client[self._settings.database_name]
        self._fs = GridFS(self._db)
        print(f"✓ 已連線到 MongoDB: {self._settings.database_name}")
    
    @property
    def client(self) -> MongoClient:
        """取得 MongoDB Client"""
        return self._client
    
    @property
    def db(self) -> Database:
        """取得資料庫實例"""
        return self._db
    
    @property
    def fs(self) -> GridFS:
        """取得 GridFS 實例"""
        return self._fs
    
    @property
    def documents(self) -> Collection:
        """取得 documents Collection"""
        return self._db[get_settings().documents_collection]
    
    def close(self) -> None:
        """關閉連線"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            self._fs = None
            MongoDBConnection._instance = None
            print("✓ 已關閉 MongoDB 連線")
    
    def ping(self) -> bool:
        """測試連線狀態"""
        try:
            self._client.admin.command('ping')
            return True
        except Exception:
            return False


# 全域連線實例
_connection: Optional[MongoDBConnection] = None


def get_db_connection(settings: Optional[Settings] = None) -> MongoDBConnection:
    """取得資料庫連線實例"""
    global _connection
    if _connection is None:
        _connection = MongoDBConnection(settings)
    return _connection
