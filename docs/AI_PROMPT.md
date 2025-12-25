# AI 提示詞：在新電腦安裝 KM 文件管理系統

請將以下提示詞貼給 AI（Claude/GPT/Gemini），它會幫你完成安裝。

---

## 提示詞

```
我需要在這台電腦上安裝 KM 文件管理系統專案。

專案 GitHub: https://github.com/CaoCharles/ai-asst-db

請幫我依序執行以下步驟：

1. **Clone 專案**
   - git clone https://github.com/CaoCharles/ai-asst-db.git
   - cd ai-asst-db

2. **安裝 uv**（如果尚未安裝）
   - macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
   - 確認安裝: uv --version

3. **建立 Python 虛擬環境**
   - uv venv --python 3.12
   - source .venv/bin/activate
   - uv sync

4. **註冊 Jupyter Kernel**
   - uv run python -m ipykernel install --user --name=ai-asst-db --display-name="Python 3.12 (ai-asst-db)"

5. **安裝前端依賴**
   - cd frontend
   - npm install
   - cd ..

6. **驗證安裝**
   - uv run python cli.py --help
   - 確認沒有錯誤

完成後告訴我結果，並啟動前端開發伺服器：
- cd frontend && npm run dev
- 開啟 http://localhost:5173/
```

---

## 版本資訊

| 項目 | 版本 |
|------|------|
| Python | 3.12 |
| Node.js | 18+ |
| uv | 最新版 |
| React | 19.x |
| Vite | 7.x |

---

## 依賴套件

### Python (pyproject.toml)
- pymongo
- python-dotenv
- tabulate
- colorama
- pytest
- jupyter
- ipykernel

### Node.js (package.json)
- react
- react-dom
- vite
- @vitejs/plugin-react

---

## 快速命令參考

```bash
# 啟動 Jupyter Notebook
uv run jupyter notebook notebooks/document_workflow.ipynb

# 啟動前端開發
cd frontend && npm run dev

# 建置前端
cd frontend && npm run build

# 執行 CLI
uv run python cli.py list
uv run python cli.py stats
```
