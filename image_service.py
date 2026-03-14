from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageDraw


def generate_image_job(prompt: str, width: int, height: int, base_output_dir: Path) -> dict:
    """
    建立臨時工作頁（job 資料夾）並輸出圖片。

    你可以把這裡替換成原 notebook 的核心生成邏輯，
    保留輸入(prompt/尺寸)與輸出(image_url)格式即可。
    """
    job_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid4().hex[:8]
    job_dir = base_output_dir / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (width, height), color=(24, 28, 36))
    draw = ImageDraw.Draw(image)

    title = "Web Trigger Demo"
    content = f"Prompt: {prompt[:160]}"
    draw.text((24, 24), title, fill=(255, 255, 255))
    draw.text((24, 72), content, fill=(180, 220, 255))

    output_path = job_dir / "result.png"
    image.save(output_path)

    return {
        "job_id": job_id,
        "image_url": f"/outputs/{job_id}/result.png",
        "prompt": prompt,
        "width": width,
        "height": height,
    }
