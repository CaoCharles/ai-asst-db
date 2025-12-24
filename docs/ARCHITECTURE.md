# 🏗️ 系統架構文件

本文件說明 KM 文件管理系統的整體架構、類別設計、資料流程。

---

## 1. 系統整體架構

```mermaid
graph TB
    subgraph 使用者介面
        A[Jupyter Notebook] --> B[CLI 命令列]
        A --> C[Python API]
    end
    
    subgraph 核心服務層
        D[ManifestManager<br/>文件清單管理]
        E[ChunksManager<br/>條款管理與索引]
        F[DocumentService<br/>文件操作]
    end
    
    subgraph 資料層
        G[(manifest.json<br/>文件清單)]
        H[(raw/<br/>原始檔案)]
        I[(processed/<br/>AI處理後 chunks)]
        J[(MongoDB<br/>未來整合)]
    end
    
    subgraph AI 處理
        K[LLM API<br/>GPT-4/Claude]
        L[條款切分]
        M[關鍵字抽取]
        N[實體識別]
    end
    
    B --> D
    C --> D
    C --> E
    C --> F
    
    D --> G
    F --> H
    E --> I
    
    H --> K
    K --> L --> M --> N --> I
```

---

## 2. 資料處理流程

```mermaid
flowchart LR
    A[📄 原始文件<br/>PDF/DOCX/JSON] --> B[💾 存入 raw/]
    B --> C[📝 更新 manifest.json]
    C --> D[🤖 AI 條款切分]
    D --> E[🏷️ 抽取關鍵字]
    E --> F[🎯 識別實體]
    F --> G[🔗 建立條款關聯]
    G --> H[💾 存入 processed/]
    H --> I[✅ 更新清單狀態]
    I --> J[📊 可供 GraphRAG 檢索]
    
    style A fill:#e1f5fe
    style D fill:#fff3e0
    style J fill:#e8f5e9
```

---

## 3. 類別圖 (UML Class Diagram)

```mermaid
classDiagram
    class ManifestManager {
        -Path manifest_path
        -dict manifest
        +list_documents() List~dict~
        +get_document(doc_id) dict
        +add_document(doc_info)
        +update_document(doc_id, updates)
        +search_by_category(category) List~dict~
        +search_by_keyword(keyword) List~dict~
        -_load_manifest() dict
        -_save_manifest()
    }
    
    class ChunksManager {
        -Path processed_dir
        -dict chunks_cache
        -dict keyword_index
        -dict entity_index
        -dict article_index
        +search_by_keyword(keyword) List~dict~
        +search_by_entity(entity) List~dict~
        +get_article(article_number) dict
        +get_related_articles(article_number) List~dict~
        +get_all_keywords() List~str~
        +get_all_entities() List~str~
        -_build_index()
        -_get_chunk_by_id(chunk_id) dict
    }
    
    class Document {
        +str doc_id
        +str title
        +str category
        +str sub_category
        +str department
        +int current_version
        +str status
        +List~Version~ versions
        +dict metadata
    }
    
    class Chunk {
        +str chunk_id
        +str article_number
        +str chapter
        +str title
        +str content
        +str summary
        +List~str~ keywords
        +List~Entity~ entities
        +List~str~ related_articles
        +dict metadata
    }
    
    class Entity {
        +str type
        +str value
    }
    
    ManifestManager --> Document : 管理
    ChunksManager --> Chunk : 管理
    Document --> Chunk : 1..*
    Chunk --> Entity : 1..*
```

---

## 4. 資料結構

### Document 結構

| 欄位 | 型別 | 說明 |
|------|------|------|
| `doc_id` | string | 文件唯一識別碼，如 LAW-001 |
| `title` | string | 文件標題 |
| `category` | string | 分類（法規、人力資源等） |
| `sub_category` | string | 子分類 |
| `department` | string | 所屬部門 |
| `current_version` | int | 當前版本號 |
| `status` | string | 狀態：active / archived |
| `versions` | array | 版本歷史陣列 |
| `metadata` | object | 關鍵字、生效日期等 |

### Chunk 結構（GraphRAG 格式）

```mermaid
graph LR
    subgraph Chunk 結構
        A[chunk_id<br/>LAW-001-030]
        B[article_number<br/>第30條]
        C[content<br/>條款原文]
        D[summary<br/>摘要]
        E[keywords<br/>關鍵字陣列]
        F[entities<br/>實體陣列]
        G[related_articles<br/>相關條款]
        H[metadata<br/>類型/重要性]
    end
    
    subgraph GraphRAG 用途
        I[節點 ID]
        J[節點標籤]
        K[向量嵌入來源]
        L[摘要檢索]
        M[關鍵字索引]
        N[圖譜節點]
        O[圖譜邊]
        P[過濾排序]
    end
    
    A --> I
    B --> J
    C --> K
    D --> L
    E --> M
    F --> N
    G --> O
    H --> P
```

| 欄位 | 型別 | 說明 | GraphRAG 用途 |
|------|------|------|---------------|
| `chunk_id` | string | 唯一識別碼 | 節點 ID |
| `article_number` | string | 條款編號 | 節點標籤 |
| `chapter` | string | 所屬章節 | 分類 |
| `title` | string | 條款標題 | 顯示用 |
| `content` | string | 條款原文 | 向量嵌入來源 |
| `summary` | string | 摘要 | 快速檢索 |
| `keywords` | array | 關鍵字陣列 | 關鍵字索引 |
| `entities` | array | 實體陣列 | 圖譜節點 |
| `related_articles` | array | 相關條款 | 圖譜邊（關聯） |
| `metadata` | object | 類型、重要性 | 過濾與排序 |

---

## 5. GraphRAG 查詢流程

```mermaid
sequenceDiagram
    participant U as 使用者
    participant CM as ChunksManager
    participant KI as keyword_index
    participant AI as article_index
    participant LLM as LLM API
    
    U->>CM: search_by_keyword("加班")
    CM->>KI: 查詢關鍵字索引
    KI-->>CM: chunk_ids
    CM-->>U: 相關 chunks
    
    U->>CM: get_related_articles("第30條")
    CM->>AI: 查詢條款
    AI-->>CM: chunk + related_articles
    CM->>AI: 遍歷相關條款
    CM-->>U: 所有相關 chunks
    
    U->>LLM: 問題 + 相關 chunks
    LLM-->>U: 生成答案
```

---

## 6. 索引結構

ChunksManager 建立三種索引，加速查詢：

```mermaid
graph TB
    subgraph 索引結構
        A[keyword_index<br/>Dict] --> |"加班" → | B["[LAW-001-032]"]
        A --> |"工時" → | C["[LAW-001-030, LAW-001-032]"]
        
        D[entity_index<br/>Dict] --> |"雇主" → | E["[LAW-001-001, LAW-001-002, ...]"]
        D --> |"每日8小時" → | F["[LAW-001-030]"]
        
        G[article_index<br/>Dict] --> |"第30條" → | H[Chunk 物件]
        G --> |"第32條" → | I[Chunk 物件]
    end
```

| 索引名稱 | 結構 | 說明 |
|----------|------|------|
| `keyword_index` | `keyword → [chunk_ids]` | 關鍵字到 chunks 的映射 |
| `entity_index` | `entity → [chunk_ids]` | 實體到 chunks 的映射 |
| `article_index` | `article_number → chunk` | 條款編號到 chunk 的直接映射 |

---

## 7. 檔案結構

```
ai-asst-db/
├── data/
│   ├── manifest.json              # 文件清單主索引
│   ├── raw/                       # 原始檔案
│   │   └── 勞動基準法.json
│   └── processed/                 # AI 處理後的 chunks
│       └── 勞動基準法_chunks.json
├── notebooks/
│   ├── tutorial.ipynb             # 基礎教學
│   └── document_workflow.ipynb    # 工作流程實作
├── scripts/
│   ├── init_db.py                 # 資料庫初始化
│   └── import_labor_law.py        # 匯入腳本
├── config/
│   └── settings.py                # 系統設定
├── db/
│   └── connection.py              # MongoDB 連線
├── models/
│   └── document.py                # 資料模型
├── services/
│   └── document_service.py        # 文件服務
└── cli.py                         # 命令列介面
```

---

## 8. 未來擴展

```mermaid
graph LR
    subgraph 現有功能
        A[ManifestManager]
        B[ChunksManager]
        C[關鍵字搜尋]
        D[實體搜尋]
        E[相關條款查詢]
    end
    
    subgraph 未來擴展
        F[向量嵌入<br/>Embedding]
        G[語意搜尋<br/>Semantic Search]
        H[知識圖譜<br/>Knowledge Graph]
        I[LangChain/LlamaIndex<br/>整合]
        J[MongoDB<br/>持久化]
        K[Web API<br/>RESTful]
    end
    
    B --> F
    F --> G
    E --> H
    G --> I
    H --> I
    A --> J
    B --> J
    I --> K
```

| 優先順序 | 功能 | 說明 |
|----------|------|------|
| 1 | 向量嵌入 | 使用 OpenAI/Sentence-Transformers 生成 embedding |
| 2 | 語意搜尋 | 基於向量相似度的搜尋 |
| 3 | MongoDB 整合 | 將 JSON 資料遷移至 MongoDB |
| 4 | 知識圖譜 | 使用 Neo4j 建立完整的知識圖譜 |
| 5 | LangChain 整合 | 結合 LLM 建立完整 RAG 系統 |
| 6 | Web API | 提供 RESTful API 供前端使用 |
