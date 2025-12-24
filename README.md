# 📚 KM 文件管理系統

企業級知識管理（Knowledge Management）文件管理平台，基於 MongoDB + GridFS + Python 架構，提供文件上傳、版本控管、Metadata 管理及智能搜尋功能。

## ✨ 功能特色

| 功能 | 說明 |
|------|------|
| 📤 **文件上傳** | 支援 docx、pptx、pdf、txt、json 等多種格式 |
| 🔄 **版本控管** | 自動遞增版號，完整保留歷史版本 |
| 🏷️ **Metadata 管理** | 彈性自定義欄位，適應不同部門需求 |
| 🔍 **智能搜尋** | 依部門、分類、關鍵字快速篩選 |
| 📥 **文件下載** | 支援下載任意歷史版本 |
| 🗃️ **文件歸檔** | 過期文件歸檔管理 |
| 🤖 **AI 條款切分** | 將法規文件切分成條款級別 chunks |
| 🔗 **GraphRAG 支援** | 每個 chunk 包含關鍵字、實體、相關條款 |

## 🛠️ 技術架構

```
┌─────────────────────────────────────────────────┐
│                  KM 文件管理系統                   │
├─────────────────────────────────────────────────┤
│   CLI / Jupyter Notebook / Python 程式整合        │
├─────────────────────────────────────────────────┤
│              DocumentService                     │
│   (文件上傳/版本控管/搜尋/下載/歸檔)               │
├─────────────────────────────────────────────────┤
│     MongoDB Connection     │     GridFS         │
│       (Metadata 存儲)       │   (檔案存儲)        │
├─────────────────────────────────────────────────┤
│               MongoDB 7.0                        │
└─────────────────────────────────────────────────┘
```

| 項目 | 技術 | 版本 |
|------|------|------|
| 資料庫 | MongoDB | 7.0 Community Edition |
| 檔案存儲 | GridFS | MongoDB 內建 |
| 程式語言 | Python | 3.9+ |
| 套件管理 | uv | 最新版 |
| 資料庫驅動 | pymongo | 4.6+ |

## 📁 專案結構

```
ai-asst-db/
├── README.md                 # 本文件
├── pyproject.toml            # 專案設定與依賴管理 (uv)
├── uv.lock                   # 依賴鎖定檔
├── .gitignore                # Git 忽略設定
├── cli.py                    # 命令列介面
├── config/
│   ├── __init__.py
│   └── settings.py           # 系統設定
├── db/
│   ├── __init__.py
│   └── connection.py         # MongoDB 連線管理
├── models/
│   ├── __init__.py
│   └── document.py           # 文件資料模型
├── services/
│   ├── __init__.py
│   └── document_service.py   # 文件操作服務
├── scripts/
│   ├── init_db.py            # 資料庫初始化腳本
│   └── import_labor_law.py   # 勞動基準法匯入腳本
├── data/
│   ├── manifest.json         # 📋 文件清單（主索引）
│   ├── raw/                  # 📂 原始檔案
│   │   └── 勞動基準法.json
│   └── processed/            # 🤖 AI 處理後的 chunks
│       └── 勞動基準法_chunks.json
├── examples/
│   └── usage_example.py      # 使用範例
└── notebooks/
    ├── tutorial.ipynb        # Jupyter 基礎教學
    └── document_workflow.ipynb  # 📚 文件工作流程實作
```

## 🚀 快速開始

### 1. 安裝 MongoDB

#### macOS (推薦使用 Homebrew)
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

#### Windows
1. 下載 [MongoDB Community Server](https://www.mongodb.com/try/download/community)
2. 選擇 Version: 7.0, Platform: Windows, Package: msi
3. 執行安裝，勾選 "Install MongoDB as a Service"

#### Linux (Ubuntu)
```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
  sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
http://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 2. 驗證 MongoDB 安裝
```bash
mongosh
```

### 3. 安裝 Python 依賴

使用 [uv](https://docs.astral.sh/uv/) 管理依賴：

```bash
# 安裝 uv（如果尚未安裝）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步依賴
cd ai-asst-db
uv sync
```

### 4. 初始化資料庫
```bash
uv run python scripts/init_db.py
```

### 5. 在 Jupyter 中使用

虛擬環境已註冊為 Jupyter kernel：

```bash
# 啟動 Jupyter
uv run jupyter notebook

# 選擇 kernel: "Python (ai-asst-db)"
```

## 💻 使用方式

### 方式一：命令列介面 (CLI)

#### 上傳新文件
```bash
uv run python cli.py upload \
  -f document.pdf \
  -c HR-001 \
  -t "員工請假辦法" \
  -d 人力資源部 \
  -cat 辦法 \
  -u admin \
  -k "請假,事假,年假" \
  -desc "初版"
```

#### 上傳新版本
```bash
uv run python cli.py version -c HR-001 -f document_v2.pdf -u admin -desc "更新請假天數"
```

#### 列出所有文件
```bash
uv run python cli.py list
```

#### 搜尋文件
```bash
# 依部門
uv run python cli.py list -d 人力資源部

# 依分類
uv run python cli.py list -cat SOP

# 關鍵字搜尋
uv run python cli.py list -k 請假
```

#### 查看文件詳情
```bash
uv run python cli.py info -c HR-001
```

#### 下載文件
```bash
# 下載最新版本
uv run python cli.py download -c HR-001

# 下載指定版本
uv run python cli.py download -c HR-001 -v 1 -o ./downloads/
```

#### 歸檔/恢復文件
```bash
uv run python cli.py archive -c HR-001
uv run python cli.py restore -c HR-001
```

#### 查看統計
```bash
uv run python cli.py stats
```

### 方式二：Python 程式整合

```python
from services.document_service import DocumentService

# 建立服務實例
service = DocumentService()

# 上傳文件
doc = service.upload_document(
    file_path="document.pdf",
    doc_code="HR-001",
    title="員工請假辦法",
    department="人力資源部",
    category="辦法",
    uploaded_by="admin",
    metadata={
        "keywords": ["請假", "事假", "年假"],
        "owner": "人資經理",
        "effective_date": "2024-01-01"
    }
)

# 上傳新版本
doc = service.upload_new_version(
    doc_code="HR-001",
    file_path="document_v2.pdf",
    uploaded_by="admin",
    description="更新請假天數規定"
)

# 搜尋文件
results = service.search(department="人力資源部", keyword="請假")

# 下載文件
file_path = service.download_file("HR-001", version_num=2)

# 更新 Metadata
service.update_metadata("HR-001", {"review_cycle": "每年一次"})

# 歸檔文件
service.archive_document("HR-001")
```

### 方式三：Jupyter Notebook 互動教學

```bash
uv run jupyter notebook notebooks/tutorial.ipynb
```

提供完整的互動式教學，包含：
- 環境設定
- MongoDB 連線
- 文件上傳與版本控管
- Metadata 管理
- 搜尋與下載
- 統計報表

## 🔄 文件管理工作流程

### 資料夾結構

```
data/
├── manifest.json          # 📋 文件清單（主索引）
├── raw/                   # 📂 原始檔案
│   └── 勞動基準法.json
└── processed/             # 🤖 AI 處理後的 chunks
    └── 勞動基準法_chunks.json
```

### 工作流程圖

```
📄 上傳原始文件 → 💾 存入 raw/ → 📝 更新 manifest.json
                                        ↓
                                 🤖 AI 條款切分
                                        ↓
                             🏷️ 抽取關鍵字/實體
                                        ↓
                              🔗 建立條款關聯
                                        ↓
                             💾 存入 processed/
                                        ↓
                           📊 可供 GraphRAG 檢索
```

### manifest.json 文件清單格式

```json
{
  "documents": [
    {
      "doc_id": "LAW-001",
      "title": "勞動基準法",
      "category": "法規",
      "sub_category": "勞動法規",
      "current_version": 1,
      "versions": [
        {
          "version": 1,
          "raw_path": "raw/勞動基準法.json",
          "processed_path": "processed/勞動基準法_chunks.json",
          "ai_processed": true,
          "chunk_count": 15
        }
      ],
      "metadata": {
        "keywords": ["勞基法", "勞動", "工時", "工資"]
      }
    }
  ]
}
```

### AI 處理後的 Chunks 格式（GraphRAG 支援）

每個條款切分成獨立的 chunk，包含完整的 metadata 和關鍵字：

```json
{
  "chunk_id": "LAW-001-030",
  "article_number": "第30條",
  "chapter": "第四章 工作時間、休息、休假",
  "title": "正常工作時間",
  "content": "勞工正常工作時間，每日不得超過八小時...",
  "summary": "規定正常工時上限：每日8小時、每週40小時",
  "keywords": ["正常工時", "每日八小時", "每週四十小時"],
  "entities": [
    {"type": "數值規定", "value": "每日8小時"},
    {"type": "數值規定", "value": "每週40小時"}
  ],
  "related_articles": ["第30-1條", "第32條", "第36條"],
  "metadata": {
    "article_type": "工時規定",
    "importance": "high",
    "common_questions": ["一天可以工作幾小時", "法定工時是多少"]
  }
}
```

### GraphRAG 結構說明

| 欄位 | 說明 | GraphRAG 用途 |
|------|------|---------------|
| `chunk_id` | 唯一識別碼 | 節點 ID |
| `article_number` | 條款編號 | 節點標籤 |
| `content` | 條款原文 | 向量嵌入來源 |
| `keywords` | 關鍵字陣列 | 圖譜邊的標籤 |
| `entities` | 實體抽取 | 圖譜節點 |
| `related_articles` | 相關條款 | 圖譜邊（關聯） |

### Jupyter Notebook 實作

```bash
uv run jupyter notebook notebooks/document_workflow.ipynb
```

完整的實作教學，包含：
- 讀取文件清單（Manifest）
- Chunks 管理與索引建立
- 關鍵字搜尋
- 實體搜尋
- 相關條款查詢（Graph Traversal）
- 模擬 AI 處理流程


## 📊 資料庫結構

### documents Collection

| 欄位 | 型別 | 說明 |
|------|------|------|
| `_id` | ObjectId | MongoDB 自動產生 |
| `doc_code` | String | 文件編號（唯一），如 HR-001 |
| `title` | String | 文件標題 |
| `category` | String | 分類：規章、SOP、辦法、訓練教材 |
| `department` | String | 所屬部門 |
| `status` | String | 狀態：active / archived / draft |
| `current_version` | Integer | 當前版本號 |
| `versions` | Array | 版本歷史陣列 |
| `metadata` | Object | 彈性 Metadata |
| `created_at` | DateTime | 建立時間 |
| `updated_at` | DateTime | 最後更新時間 |

### versions 陣列結構

| 欄位 | 型別 | 說明 |
|------|------|------|
| `version` | Integer | 版本號 |
| `file_name` | String | 原始檔案名稱 |
| `file_type` | String | 檔案類型：docx / pptx / pdf / txt |
| `file_id` | ObjectId | GridFS 檔案 ID |
| `file_size` | Integer | 檔案大小（bytes） |
| `uploaded_by` | String | 上傳者 |
| `uploaded_at` | DateTime | 上傳時間 |
| `description` | String | 版本說明 |

### metadata 彈性欄位

| 欄位 | 說明 |
|------|------|
| `effective_date` | 生效日期 |
| `expiry_date` | 到期日期 |
| `keywords` | 關鍵字陣列 |
| `related_docs` | 相關文件編號 |
| `owner` | 文件負責人 |
| `review_cycle` | 審核週期 |

## 🏷️ 文件分類代碼

| 分類 | 代碼前綴 | 範例 |
|------|----------|------|
| 人力資源 | HR- | HR-001, HR-002 |
| 業務部門 | BIZ- | BIZ-001, BIZ-002 |
| 訓練教材 | TRN- | TRN-001, TRN-002 |
| 法遵合規 | CMP- | CMP-001, CMP-002 |
| SOP 手冊 | SOP- | SOP-001, SOP-002 |

## ⚙️ 環境變數設定

可透過環境變數客製化連線設定：

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `MONGO_HOST` | localhost | MongoDB 主機 |
| `MONGO_PORT` | 27017 | MongoDB 埠號 |
| `MONGO_USERNAME` | - | 認證使用者名稱 |
| `MONGO_PASSWORD` | - | 認證密碼 |
| `MONGO_DATABASE` | km_system | 資料庫名稱 |

建立 `.env` 檔案：
```env
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DATABASE=km_system
```

## 📋 常用指令

### uv 套件管理
```bash
uv sync                     # 同步依賴
uv add <package>            # 新增套件
uv remove <package>         # 移除套件
uv run python <script>      # 執行腳本
uv run jupyter notebook     # 啟動 Jupyter
```

### MongoDB 服務管理
```bash
# macOS
brew services start mongodb-community@7.0   # 啟動
brew services stop mongodb-community@7.0    # 停止

# Linux
sudo systemctl start mongod                 # 啟動
sudo systemctl stop mongod                  # 停止
```

### MongoDB Shell 操作
```bash
mongosh                                     # 連線 MongoDB
show dbs                                    # 顯示所有資料庫
use km_system                               # 切換資料庫
show collections                            # 顯示 Collections
db.documents.find()                         # 查詢所有文件
db.documents.countDocuments()               # 統計文件數量
```

## 🔧 系統需求

| 項目 | 最低需求 | 建議配置 |
|------|----------|----------|
| CPU | 2 Core | 4 Core |
| 記憶體 | 4 GB | 8 GB |
| 硬碟空間 | 50 GB | 200 GB SSD |
| 作業系統 | Windows 10+ / macOS 11+ / Ubuntu 20.04+ | - |

## 📄 授權條款

MIT License

## 🙋 常見問題

### Q: 如何連線遠端 MongoDB？
設定環境變數 `MONGO_HOST` 指向遠端主機位址。

### Q: 如何啟用認證？
設定 `MONGO_USERNAME` 和 `MONGO_PASSWORD` 環境變數。

### Q: GridFS 檔案儲存在哪裡？
GridFS 會自動在 MongoDB 中建立 `fs.files` 和 `fs.chunks` collections。

### Q: 如何備份資料？
使用 `mongodump` 工具：
```bash
mongodump --db km_system --out ./backup/
```

### Q: 如何還原資料？
使用 `mongorestore` 工具：
```bash
mongorestore --db km_system ./backup/km_system/
```
