# CLUB AURORA — 高級キャバクラ サンプルHP

掲載用サンプル。**黒 × ゴールド × ワインレッド / 高級ラウンジ / 大人の非日常**。
参考画像のピンクネオン・アイドル構図・星モチーフは不使用（設計書方針）。

- 架空店名: CLUB AURORA / エリア: 名古屋・錦
- フォント: Cormorant Garamond（英字セリフ）＋ Shippori Mincho B1（和文明朝）
- モーション: GSAP不要のCSS＋IntersectionObserver。HEROはロードアニメ、以降はスクロールreveal
- 完全静的（HTML/CSS/JS）。CMS化を想定した構造（キャスト・出勤・料金・ニュース等を差し替え前提）

## ページ構成（13枚）

| ページ | ファイル | 区分 |
|---|---|---|
| TOP | index.html | 必須 |
| CAST一覧 | cast.html | 必須 |
| CAST詳細 | cast-detail.html | 必須 |
| SYSTEM（料金表） | system.html | 必須 |
| SCHEDULE（出勤） | schedule.html | 重要 |
| GALLERY | gallery.html | 重要 |
| NEWS一覧 / 詳細 | news.html / news-detail.html | 重要 |
| ACCESS | access.html | 必須 |
| RESERVE（予約フォーム） | reserve.html | 必須 |
| RECRUIT（求人） | recruit.html | 重要 |
| プライバシー / 特商法 | privacy.html / legal.html | 法務 |

## 画像

`images/` 配下（ComfyUI / FLUX.1-dev で生成、実写風・成人女性・統一トーン）:
- `hero.png` 1344×768 … HERO合成（美女3名・シャンデリア・ワインレッド）
- `cast-01〜03.jpg` 768×1024 … キャストポートレート
- `lounge.jpg` 1216×832 … VIPルーム内観

画像は `js/main.js` が存在チェックして差し込む。未生成でもCSSプレースホルダーで崩れない。

## 構成
```
index.html / cast.html / system.html / access.html …（手書き）
css/style.css            … 全スタイル（デザイントークン＋各ページ）
js/main.js               … ヘッダー追従・モバイルメニュー・reveal・画像差込
scripts/build_pages.py   … 残りページの一括生成（ヘッダー/フッター統一）
images/                  … AI生成画像
```

## 法務表示（設計書 第8章）
- 全ページフッターに「20歳未満入店不可／18歳未満立入不可／20歳未満飲酒禁止／無断転載禁止」を明記
- 料金はSYSTEMページに税込で表形式表示（風営法・明朗会計の方針）

## プレビュー
```bash
open index.html      # ブラウザで開く
```
※本サイトは掲載用デザインサンプル。店名・住所・電話・キャスト等はすべて架空。
