# KM 文件管理系統 - 安裝與啟動指南

## 系統需求

| 項目 | 版本 |
|------|------|
| Python | 3.12+ |
| Node.js | 18+ |
| uv | 最新版 |
| MongoDB | 7.0（可選） |

---

## 快速安裝

### 1. Clone 專案

```bash
git clone https://github.com/CaoCharles/ai-asst-db.git
cd ai-asst-db
```

### 2. 安裝 uv（如果尚未安裝）

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. 建立 Python 虛擬環境並安裝依賴

```bash
# 建立虛擬環境（使用 Python 3.12）
uv venv --python 3.12

# 啟動虛擬環境
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 同步安裝依賴
uv sync
```

### 4. 註冊 Jupyter Kernel（可選）

```bash
uv run python -m ipykernel install --user --name=ai-asst-db --display-name="Python 3.12 (ai-asst-db)"
```

---

## 啟動服務

### 啟動 Jupyter Notebook

```bash
uv run jupyter notebook notebooks/document_workflow.ipynb
```

### 啟動前端開發伺服器

```bash
cd frontend
npm install
npm run dev
```

開啟瀏覽器訪問：http://localhost:5173/

### 啟動 CLI

```bash
uv run python cli.py --help
```

---

## 前端建置與部署

### 建置生產版本

```bash
cd frontend
npm run build
```

### 部署到 GitHub Pages

```bash
# 複製 dist 到 docs
cp -r frontend/dist/* docs/

# 提交並推送
git add .
git commit -m "更新前端"
git push
```

在 GitHub 設定 Pages：
- Settings → Pages → Source: Deploy from a branch
- Branch: main, Folder: /docs

---

## 專案結構

```
ai-asst-db/
├── data/
│   ├── manifest.json          # 文件清單
│   ├── raw/                   # 原始檔案
│   └── processed/             # AI 處理後的 chunks
├── frontend/                  # React 前端
│   ├── src/
│   │   ├── components/        # 元件
│   │   ├── pages/             # 頁面
│   │   └── index.css          # 樣式
│   └── package.json
├── notebooks/
│   └── document_workflow.ipynb # 教學 Notebook
├── docs/                      # GitHub Pages
├── pyproject.toml             # Python 依賴
└── README.md
```

---

## 常見問題

### uv sync 失敗
```bash
# 確認 Python 版本
python --version

# 重新建立虛擬環境
rm -rf .venv
uv venv --python 3.12
uv sync
```

### Jupyter 找不到 kernel
```bash
# 重新註冊
uv run python -m ipykernel install --user --name=ai-asst-db --display-name="Python 3.12 (ai-asst-db)"
```

### 前端 npm install 失敗
```bash
# 清除快取
cd frontend
rm -rf node_modules package-lock.json
npm install
```
