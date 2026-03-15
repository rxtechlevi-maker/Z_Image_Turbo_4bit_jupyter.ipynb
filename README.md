## Web 觸發圖片輸出範例

這個專案示範如何把原本 notebook 內的圖片生成流程，改成由網頁觸發。

---

## 你問的重點：怎麼部署？可以用 Google Colab 嗎？

可以，用 **Google Colab** 很適合快速 demo。

下面給你兩種常見做法：

1. **Colab（快速展示、臨時網址）** ✅ 推薦先用這個
2. **本機 / 雲端 VM（長時間穩定跑）** ✅ 正式上線再用這個

---

## 方案 A：Google Colab 部署（推薦先試）

> 適合：你要快速測試「用網頁觸發輸出圖片」

### 1) 在 Colab 安裝套件

```bash
!pip install fastapi uvicorn jinja2 python-multipart pillow pyngrok
```

### 2) 上傳專案檔案到 Colab

最簡單是把目前資料夾上傳到 `/content/`，例如放到：

`/content/Z_Image_Turbo_4bit_jupyter.ipynb/`

### 3) 啟動 API + 產生公開網址

在 Colab 新增一格 Python：

```python
import os
import threading
import uvicorn
from pyngrok import ngrok

PROJECT_DIR = "/content/Z_Image_Turbo_4bit_jupyter.ipynb"
os.chdir(PROJECT_DIR)

# 啟動 FastAPI（背景執行）
def run_api():
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)

thread = threading.Thread(target=run_api, daemon=True)
thread.start()

# 建立 ngrok 對外網址
public_url = ngrok.connect(8000).public_url
print("Web URL:", public_url)
```

打開印出的 `Web URL` 就能看到控制頁面，送出 prompt 後會觸發 `/generate`。

### 4) Colab 使用注意事項

- Colab runtime 重啟後，網址會變、檔案可能要重掛載。
- `outputs/` 是暫存資料，重啟後可能清掉。
- 若你要持久保存圖片，建議把 `outputs/` 改存到 Google Drive。

---

## 方案 B：本機 / 雲端 VM 部署

> 適合：比較穩定、可長時間運行

### 1) 安裝依賴

```bash
pip install -r requirements.txt
```

### 2) 啟動服務

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 3) 開啟頁面

- 本機：`http://localhost:8000`
- 雲端 VM：`http://<你的主機IP>:8000`

---

## 架構
### 啟動

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

打開 `http://localhost:8000`。

### 架構

- `app.py`：提供網頁與 `/generate` API。
- `image_service.py`：圖片生成邏輯（目前為示範，可替換成你 notebook 的模型呼叫）。
- `templates/index.html` + `static/app.js`：前端控制台。
- `outputs/<job_id>/result.png`：每次生成建立一個臨時工作資料夾。

---

## 對接你的 notebook 程式
### 對接你的 notebook 程式

把 `image_service.py` 的 `generate_image_job` 內容，替換成你原本的程式碼。
只要最後輸出圖片檔到 `job_dir / "result.png"`，前端就能直接顯示。
