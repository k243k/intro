"""CLUB AURORA（名古屋・高級ラウンジ）HPサンプル用 実写風AI画像一括生成.

FLUX.1-dev fp8（Win RTX 5080 / port 8188）でシネマティックな高級キャバクラ
画像を生成する。プロンプトは自然言語（FLUX系の鉄則）。CFG=1.0 / FluxGuidance
で制御。

出力: 02_Projects/cabaret-club-hp/images/
  - hero.png      16:9 ヒーロー（美女3名）
  - cast-01.jpg / cast-02.jpg / cast-03.jpg  キャストポートレート 3:4
  - lounge.jpg    店内VIPルーム（人物なし）横長
"""

from __future__ import annotations

import json
import logging
import time
import urllib.error
import urllib.request
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

COMFYUI_URL = "http://100.76.244.62:8188"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "images"

# all-in-one fp8 checkpoint（CLIP-L + T5 + VAE + UNET 同梱）
CHECKPOINT = "FLUX1\\flux1-dev-fp8.safetensors"

# 共通の雰囲気記述（高級感・黒×ゴールド×ワインレッド・シネマティック）
AMBIENCE = (
    "luxurious upscale Japanese hostess lounge in Nagoya at night, "
    "opulent dark interior with black and gold accents and deep wine-red velvet drapes, "
    "glittering crystal chandelier casting warm golden light, "
    "moody cinematic lighting with warm gold key light and seductive wine-red rim light, "
    "deep shadows, bokeh of champagne bottles and glasses, "
    "shot on cinema camera, 35mm, shallow depth of field, photorealistic, "
    "rich film grain, elegant and glamorous atmosphere, high-end editorial photography"
)

NEG = (
    "cartoon, anime, illustration, painting, 3d render, cgi, "
    "deformed, disfigured, bad anatomy, bad hands, extra fingers, "
    "lowres, blurry face, watermark, text, signature, child, underage"
)


def _build_jobs() -> list[dict]:
    """生成ジョブ定義リストを返す."""
    return [
        {
            "name": "hero",
            "ext": "png",
            "width": 1344,
            "height": 768,  # 16:9 相当（FLUX推奨の64倍数）
            "seed": 71010,
            "prompt": (
                "cinematic wide editorial photograph, three glamorous beautiful "
                "japanese women in their twenties wearing elegant evening gowns, "
                "positioned on the right side of the frame, "
                "the woman on the left in a wine-red satin gown, "
                "the central woman in a shimmering gold gown raising a champagne glass with a confident smile, "
                "the woman on the right in a sleek dark navy gown, "
                "all with sophisticated hair and refined makeup, classy and alluring, "
                "the left portion of the frame is dark and empty negative space for text overlay, "
                + AMBIENCE
            ),
        },
        {
            "name": "cast-01",
            "ext": "jpg",
            "width": 768,
            "height": 1024,  # 3:4
            "seed": 22001,
            "prompt": (
                "vertical portrait photograph of an elegant beautiful japanese woman "
                "in her mid twenties, long flowing dark hair, wearing a deep wine-red "
                "off-shoulder evening gown, refined sophisticated makeup, "
                "gentle alluring gaze toward camera, classy and sensual, "
                "standing in a luxury lounge, " + AMBIENCE
            ),
        },
        {
            "name": "cast-02",
            "ext": "jpg",
            "width": 768,
            "height": 1024,
            "seed": 22002,
            "prompt": (
                "vertical portrait photograph of a gorgeous beautiful japanese woman "
                "in her twenties, elegant updo hairstyle, wearing a shimmering gold "
                "sequin evening dress, glamorous makeup, soft confident smile, "
                "holding a champagne glass, upscale and seductive, "
                "in a luxury lounge, " + AMBIENCE
            ),
        },
        {
            "name": "cast-03",
            "ext": "jpg",
            "width": 768,
            "height": 1024,
            "seed": 22003,
            "prompt": (
                "vertical portrait photograph of a stunning beautiful japanese woman "
                "in her twenties, sleek straight black hair, wearing an elegant "
                "black evening gown with subtle gold jewelry, sultry sophisticated "
                "expression, mature and classy, leaning gracefully, "
                "in a luxury lounge, " + AMBIENCE
            ),
        },
        {
            "name": "lounge",
            "ext": "jpg",
            "width": 1216,
            "height": 832,  # 横長 約3:2
            "seed": 33007,
            "prompt": (
                "interior architectural photograph of an empty luxurious VIP room "
                "in an upscale Japanese hostess club, no people, "
                "plush black and wine-red leather sofas, polished dark wood low table "
                "with champagne bottles and crystal glasses, glittering crystal chandelier, "
                "warm golden indirect lighting, gold trim accents, mirrored walls, "
                + AMBIENCE
            ),
        },
    ]


def submit_and_wait(workflow: dict, timeout: int = 1200) -> tuple[str, str]:
    """ワークフローを送信し、完成画像のファイル名とサブフォルダを返す."""
    data = json.dumps(workflow).encode()
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    pid = json.loads(urllib.request.urlopen(req).read())["prompt_id"]
    logger.info("  送信OK (%s)", pid[:8])
    start = time.time()
    while True:
        if time.time() - start > timeout:
            raise TimeoutError(f"タイムアウト: {pid}")
        try:
            r = urllib.request.urlopen(f"{COMFYUI_URL}/history/{pid}")
            d = json.loads(r.read())
            if d and pid in d:
                status = d[pid].get("status", {}).get("status_str", "")
                if status == "success":
                    for _, out in d[pid].get("outputs", {}).items():
                        if "images" in out:
                            img = out["images"][0]
                            return img["filename"], img.get("subfolder", "")
                elif status == "error":
                    msgs = d[pid].get("status", {}).get("messages", [])
                    raise RuntimeError(f"生成エラー: {msgs}")
        except urllib.error.URLError:
            pass
        time.sleep(3)


def download(filename: str, subfolder: str, dest: Path) -> None:
    """ComfyUI出力(PNG)をローカルに保存する.

    destの拡張子が.jpgの場合はPILでJPEG変換して保存する。
    """
    url = f"{COMFYUI_URL}/view?filename={filename}&type=output"
    if subfolder:
        url += f"&subfolder={subfolder}"
    with urllib.request.urlopen(url) as r:
        raw = r.read()
    if dest.suffix.lower() in (".jpg", ".jpeg"):
        import io

        from PIL import Image

        img = Image.open(io.BytesIO(raw)).convert("RGB")
        img.save(dest, "JPEG", quality=90)
    else:
        dest.write_bytes(raw)
    logger.info("  => %s (%d KB)", dest.name, dest.stat().st_size // 1024)


def build_workflow(job: dict) -> dict:
    """FLUX.1-dev用ワークフローを構築する.

    Args:
        job: 名前・サイズ・seed・promptを含むジョブ定義。

    Returns:
        ComfyUI API形式のワークフロー辞書。
    """
    wf = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": CHECKPOINT},
        },
        "pos": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": job["prompt"], "clip": ["1", 1]},
        },
        "neg": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEG, "clip": ["1", 1]},
        },
        "guidance": {
            "class_type": "FluxGuidance",
            "inputs": {"conditioning": ["pos", 0], "guidance": 3.5},
        },
        "latent": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": job["width"],
                "height": job["height"],
                "batch_size": 1,
            },
        },
        "ksampler": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["guidance", 0],
                "negative": ["neg", 0],
                "latent_image": ["latent", 0],
                "seed": job["seed"],
                "steps": 28,
                "cfg": 1.0,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1.0,
            },
        },
        "decode": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["ksampler", 0], "vae": ["1", 2]},
        },
        "save": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["decode", 0],
                "filename_prefix": f"aurora/{job['name']}",
            },
        },
    }
    return {"prompt": wf}


def main() -> None:
    """全ジョブを順次生成して images/ に保存する."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    jobs = _build_jobs()
    done: list[Path] = []
    for i, job in enumerate(jobs, 1):
        dest = OUTPUT_DIR / f"{job['name']}.{job['ext']}"
        logger.info(
            "[%d/%d] %s (%dx%d, FLUX.1-dev 28steps)",
            i, len(jobs), dest.name, job["width"], job["height"],
        )
        try:
            wf = build_workflow(job)
            fn, subfolder = submit_and_wait(wf)
            download(fn, subfolder, dest)
            done.append(dest)
        except Exception as exc:  # noqa: BLE001
            logger.error("  失敗: %s — %s", dest.name, exc)
    logger.info("\n=== 完了: %d/%d 枚 ===", len(done), len(jobs))
    for p in done:
        logger.info("  %s", p)


if __name__ == "__main__":
    main()
