## Web 觸發圖片輸出範例

這個專案示範如何把原本 notebook 內的圖片生成流程，改成由網頁觸發。

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

### 對接你的 notebook 程式

把 `image_service.py` 的 `generate_image_job` 內容，替換成你原本的程式碼。
只要最後輸出圖片檔到 `job_dir / "result.png"`，前端就能直接顯示。
