const form = document.getElementById('gen-form');
const statusEl = document.getElementById('status');
const previewEl = document.getElementById('preview');
const outputLinkEl = document.getElementById('output-link');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  statusEl.textContent = '生成中...';
  previewEl.hidden = true;
  outputLinkEl.textContent = '';

  const data = new FormData(form);
  try {
    const resp = await fetch('/generate', { method: 'POST', body: data });
    const body = await resp.json();

    if (!resp.ok) {
      throw new Error(body.detail || '生成失敗');
    }

    const imgUrl = `${body.image_url}?t=${Date.now()}`;
    previewEl.src = imgUrl;
    previewEl.hidden = false;
    outputLinkEl.innerHTML = `輸出檔案：<code>${body.image_url}</code>（job: <code>${body.job_id}</code>）`;
    statusEl.textContent = '完成';
  } catch (err) {
    statusEl.textContent = `錯誤：${err.message}`;
  }
});
