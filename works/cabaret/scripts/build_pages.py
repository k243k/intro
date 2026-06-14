#!/usr/bin/env python3
"""CLUB AURORA サンプルHP — 残りページ一括生成スクリプト.

ヘッダー/フッター/SNSレールを共通テンプレートから差し込み、全ページの体裁を統一する。
TOP/CAST/SYSTEM/ACCESS は手書き済みのため対象外。
"""
from __future__ import annotations

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent

# 主要ナビ項目（label, href）
NAV = [
    ("HOME", "index.html"),
    ("ABOUT", "index.html#about"),
    ("CAST", "cast.html"),
    ("SYSTEM", "system.html"),
    ("GALLERY", "gallery.html"),
    ("NEWS", "news.html"),
    ("ACCESS", "access.html"),
    ("RECRUIT", "recruit.html"),
]

IG = ('<svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.9.07 1.17.05 1.8.25 2.23.42.56.22.96.48 '
      '1.38.9.42.42.68.82.9 1.38.17.42.37 1.06.42 2.23.06 1.3.07 1.69.07 4.9s0 3.6-.07 4.9c-.05 '
      '1.17-.25 1.8-.42 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.17-1.06.37-2.23.42-1.3.06'
      '-1.69.07-4.9.07s-3.6 0-4.9-.07c-1.17-.05-1.8-.25-2.23-.42a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 '
      '1-.9-1.38c-.17-.42-.37-1.06-.42-2.23-.06-1.3-.07-1.69-.07-4.9s.01-3.6.07-4.9c.05-1.17.25-1.8.42'
      '-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.17 1.06-.37 2.23-.42 1.3-.06 1.69-.07 '
      '4.9-.07Zm0 1.8c-3.15 0-3.5.01-4.74.07-.9.04-1.38.19-1.7.32-.43.16-.73.36-1.06.69-.33.33-.53.63'
      '-.69 1.06-.13.32-.28.8-.32 1.7C3.43 9.08 3.42 9.42 3.42 12s.01 2.92.07 4.16c.04.9.19 1.38.32 '
      '1.7.16.43.36.73.69 1.06.33.33.63.53 1.06.69.32.13.8.28 1.7.32 1.24.06 1.59.07 4.74.07s3.5-.01 '
      '4.74-.07c.9-.04 1.38-.19 1.7-.32.43-.16.73-.36 1.06-.69.33-.33.53-.63.69-1.06.13-.32.28-.8.32'
      '-1.7.06-1.24.07-1.58.07-4.16s-.01-2.92-.07-4.16c-.04-.9-.19-1.38-.32-1.7a2.85 2.85 0 0 0-.69'
      '-1.06 2.85 2.85 0 0 0-1.06-.69c-.32-.13-.8-.28-1.7-.32C15.5 4.01 15.15 4 12 4Zm0 3.06A4.94 '
      '4.94 0 1 1 12 17a4.94 4.94 0 0 1 0-9.88Zm0 1.8a3.14 3.14 0 1 0 0 6.28 3.14 3.14 0 0 0 0-6.28Zm'
      '5.15-.95a1.15 1.15 0 1 1-2.3 0 1.15 1.15 0 0 1 2.3 0Z"/></svg>')
XICO = ('<svg viewBox="0 0 24 24"><path d="M17.53 3h3.05l-6.67 7.62L21.75 21h-6.13l-4.8-6.28L5.3 21H2.25l'
        '7.13-8.15L2 3h6.28l4.34 5.74L17.53 3Zm-1.07 16.2h1.69L7.62 4.7H5.8l10.66 14.5Z"/></svg>')
LINEICO = ('<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 5.64 2 10.13c0 4.02 3.55 7.39 8.35 8.03.32.07.77'
           '.21.88.49.1.25.06.64.03.9l-.14.85c-.04.25-.2.98.86.53s5.7-3.36 7.78-5.75C21.13 13.45 22 11.9 '
           '22 10.13 22 5.64 17.52 2 12 2Z"/></svg>')


def header(active: str) -> str:
    items = "\n".join(
        f'      <li><a href="{href}"{" class=\"active\"" if label == active else ""}>{label}</a></li>'
        for label, href in NAV
    )
    return f"""<header class="site-header" id="siteHeader">
  <a href="index.html" class="logo"><span class="club">CLUB</span><span class="mark gold-text">AURORA</span></a>
  <nav class="main-nav" id="mainNav" aria-label="メインメニュー">
    <ul>
{items}
    </ul>
  </nav>
  <a href="reserve.html" class="nav-reserve">RESERVE<small>ご予約</small></a>
  <button class="nav-toggle" id="navToggle" aria-label="メニューを開く"><span></span><span></span><span></span></button>
</header>

<aside class="social-rail">
  <a href="#" aria-label="Instagram">{IG}</a>
  <a href="#" aria-label="X">{XICO}</a>
  <a href="#" class="line" aria-label="LINE">{LINEICO}</a>
</aside>"""


FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__top">
      <a href="index.html" class="logo"><span class="club">CLUB</span><span class="mark gold-text">AURORA</span></a>
      <nav class="footer-nav" aria-label="フッターメニュー">
        <a href="cast.html">CAST</a><a href="system.html">SYSTEM</a><a href="gallery.html">GALLERY</a>
        <a href="news.html">NEWS</a><a href="access.html">ACCESS</a><a href="recruit.html">RECRUIT</a><a href="reserve.html">RESERVE</a>
      </nav>
    </div>
    <div class="legal">
      <span class="age">20歳未満の方の入店はお断りしております</span>
      <p>18歳未満の方は営業所内に立ち入ることができません。20歳未満の方への酒類の提供は法律で禁止されています。掲載写真・文章の無断転載を禁じます。</p>
    </div>
    <div class="legal" style="border-top:none;padding-top:.6rem">
      <nav class="footer-nav" style="gap:1rem"><a href="privacy.html">プライバシーポリシー</a><a href="legal.html">特定商取引法に基づく表記</a></nav>
      <p class="copy">© 2026 CLUB AURORA — Sample Site</p>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
</body>
</html>"""


def page(slug: str, title: str, desc: str, active: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="css/style.css">
</head>
<body data-page="{slug}">

{header(active)}

<main>
{body}
</main>

{FOOTER}
"""


def page_hero(eyebrow: str, en: str, jp: str, crumb: str) -> str:
    return f"""  <section class="page-hero">
    <div class="page-hero__in">
      <span class="eyebrow">{eyebrow}</span>
      <h1 class="gold-text">{en}<span class="jp">{jp}</span></h1>
      <p class="breadcrumb"><a href="index.html">HOME</a> &nbsp;/&nbsp; <span>{crumb}</span></p>
    </div>
  </section>"""


# ---------------------------------------------------------------- RESERVE
reserve_body = page_hero("Reservation", "RESERVE", "ご予約", "RESERVE") + """
  <section class="section">
    <div class="wrap">
      <div class="reserve-grid">
        <div class="reserve-quick" data-reveal>
          <h3 class="rsv-h">お急ぎの方へ</h3>
          <p class="rsv-p">お電話・LINEなら、その場でスタッフが空席状況をご案内します。当日のご予約も歓迎いたします。</p>
          <a href="tel:0521234567" class="btn-gold" style="width:100%;justify-content:center;margin-bottom:1rem">
            <span class="ar">&#9742;</span> 052-123-4567</a>
          <a href="#" class="btn-line" style="width:100%"> LINEで予約・相談する</a>
          <p class="rsv-note">受付時間 20:00 - LAST / 日曜定休</p>
        </div>

        <form class="reserve-form" data-reveal data-d="1" onsubmit="return false;">
          <h3 class="rsv-h">予約フォーム</h3>
          <div class="field"><label>お名前 <i>必須</i></label><input type="text" placeholder="山田 太郎" required></div>
          <div class="field"><label>電話番号 <i>必須</i></label><input type="tel" placeholder="090-0000-0000" required></div>
          <div class="field"><label>メールアドレス</label><input type="email" placeholder="example@mail.com"></div>
          <div class="field-row">
            <div class="field"><label>ご来店日 <i>必須</i></label><input type="date" required></div>
            <div class="field"><label>ご来店時間</label>
              <select><option>20:00</option><option>21:00</option><option>22:00</option><option>23:00</option><option>24:00以降</option></select></div>
          </div>
          <div class="field-row">
            <div class="field"><label>人数</label>
              <select><option>1名</option><option>2名</option><option>3名</option><option>4名</option><option>5名以上</option></select></div>
            <div class="field"><label>ご指名</label><input type="text" placeholder="キャスト名（任意）"></div>
          </div>
          <div class="field"><label>ご要望</label><textarea rows="3" placeholder="VIPルーム希望・記念日 など"></textarea></div>
          <button class="btn-gold" type="submit" style="width:100%;justify-content:center">予約を送信する<span class="ar">&rarr;</span></button>
          <p class="rsv-note">※本ページはデザインサンプルです。送信は実際には行われません。</p>
        </form>
      </div>
    </div>
  </section>"""

# ---------------------------------------------------------------- CAST DETAIL
cast_detail_body = """  <section class="cast-detail">
    <div class="wrap">
      <p class="breadcrumb" style="margin-bottom:2rem"><a href="index.html">HOME</a> &nbsp;/&nbsp; <a href="cast.html">CAST</a> &nbsp;/&nbsp; <span>玲奈</span></p>
      <div class="cd-grid">
        <div class="cd-photo" data-reveal>
          <div class="cd-main" style="background-image:url('images/cast-01.jpg')"></div>
          <div class="cd-thumbs">
            <span style="background-image:url('images/cast-01.jpg')"></span>
            <span style="background-image:url('images/cast-02.jpg')"></span>
            <span style="background-image:url('images/cast-03.jpg')"></span>
          </div>
        </div>
        <div class="cd-info" data-reveal data-d="1">
          <span class="cd-role">Platinum Cast</span>
          <h1 class="cd-name gold-text">玲奈 <small>Rena</small></h1>
          <p class="cd-status on">本日出勤</p>
          <dl class="cd-profile">
            <div><dt>誕生日</dt><dd>10月14日</dd></div>
            <div><dt>星座</dt><dd>てんびん座</dd></div>
            <div><dt>趣味</dt><dd>映画鑑賞・ワイン</dd></div>
            <div><dt>好きなお酒</dt><dd>シャンパン / 赤ワイン</dd></div>
            <div><dt>チャームポイント</dt><dd>笑顔と聞き上手</dd></div>
          </dl>
          <p class="cd-comment">「はじめまして、玲奈です。お仕事終わりのひとときを、心からおもてなしいたします。ゆっくりお話ししましょう。」</p>
          <div class="cd-cta">
            <a href="reserve.html" class="btn-gold">玲奈を指名予約<span class="ar">&rarr;</span></a>
            <a href="#" class="cd-sns" aria-label="Instagram">""" + IG + """</a>
            <a href="#" class="cd-sns" aria-label="X">""" + XICO + """</a>
          </div>
        </div>
      </div>
    </div>
  </section>"""

# ---------------------------------------------------------------- SCHEDULE
def sched_cell(name: str, en: str, status: str) -> str:
    cls = "on" if status == "出勤" else ("off" if status == "休" else "")
    return f'<div class="sc-cell {cls}"><span class="sc-name">{name}</span><span class="sc-en">{en}</span><span class="sc-st">{status}</span></div>'

cast_roster = [("玲奈", "Rena"), ("美咲", "Misaki"), ("彩花", "Ayaka"), ("凛", "Rin"),
               ("沙耶", "Saya"), ("麗", "Urara"), ("ひな", "Hina"), ("琴音", "Kotone")]
days = ["6/9 (月)", "6/10 (火)", "6/11 (水)", "6/12 (木)", "6/13 (金)", "6/14 (土)"]
# 簡易パターン
import_pattern = [
    ["出勤", "出勤", "休", "出勤", "出勤", "出勤"],
    ["出勤", "休", "出勤", "出勤", "出勤", "休"],
    ["休", "出勤", "出勤", "出勤", "出勤", "出勤"],
    ["出勤", "出勤", "出勤", "休", "出勤", "出勤"],
    ["休", "休", "出勤", "出勤", "出勤", "出勤"],
    ["出勤", "出勤", "休", "出勤", "休", "出勤"],
    ["出勤", "出勤", "出勤", "出勤", "出勤", "休"],
    ["休", "出勤", "出勤", "休", "出勤", "出勤"],
]
sched_rows = ""
for (nm, en), pat in zip(cast_roster, import_pattern):
    cells = "".join(
        f'<td class="{"on" if s=="出勤" else "off"}">{s}</td>' for s in pat
    )
    sched_rows += f'<tr><th><span class="sr-name">{nm}</span><span class="sr-en">{en}</span></th>{cells}</tr>\n        '
sched_head = "".join(f"<th>{d}</th>" for d in days)

schedule_body = page_hero("Weekly Schedule", "SCHEDULE", "出勤情報", "SCHEDULE") + f"""
  <section class="section">
    <div class="wrap">
      <div class="section__head"><span class="eyebrow">本日の出勤</span>
        <h2 class="section-title">TODAY<span class="jp">本日出勤キャスト</span></h2></div>
      <div class="cast-grid" style="margin-bottom:4rem">
        <a class="cast-card" href="cast-detail.html" data-reveal>
          <div class="cast-card__img" style="background-image:url('images/cast-01.jpg')"></div>
          <span class="cast-card__status on">出勤中</span>
          <div class="cast-card__body"><span class="cast-card__role">Platinum</span><h3 class="cast-card__name">玲奈 <small>Rena</small></h3></div></a>
        <a class="cast-card" href="cast-detail.html" data-reveal data-d="1">
          <div class="cast-card__img" style="background-image:url('images/cast-02.jpg')"></div>
          <span class="cast-card__status on">出勤中</span>
          <div class="cast-card__body"><span class="cast-card__role">Gold</span><h3 class="cast-card__name">美咲 <small>Misaki</small></h3></div></a>
        <a class="cast-card" href="cast-detail.html" data-reveal data-d="2">
          <div class="cast-card__img" style="background-image:url('images/cast-03.jpg')"></div>
          <span class="cast-card__status on">出勤中</span>
          <div class="cast-card__body"><span class="cast-card__role">Gold</span><h3 class="cast-card__name">彩花 <small>Ayaka</small></h3></div></a>
        <a class="cast-card" href="cast-detail.html" data-reveal data-d="3">
          <div class="cast-card__img" style="background-image:url('images/cast-04.jpg')"></div>
          <span class="cast-card__status on">出勤中</span>
          <div class="cast-card__body"><span class="cast-card__role">Silver</span><h3 class="cast-card__name">凛 <small>Rin</small></h3></div></a>
      </div>

      <div class="section__head"><span class="eyebrow">週間出勤</span>
        <h2 class="section-title">WEEKLY<span class="jp">週間スケジュール</span></h2></div>
      <div class="sched-wrap" data-reveal>
        <table class="sched-table">
          <thead><tr><th>キャスト</th>{sched_head}</tr></thead>
          <tbody>
        {sched_rows}</tbody>
        </table>
      </div>
      <p class="rsv-note" style="text-align:center;margin-top:1.4rem">※スケジュールは変更となる場合がございます。最新情報は店舗までお問い合わせください。</p>
    </div>
  </section>"""

# ---------------------------------------------------------------- GALLERY
gallery_imgs = [
    ("images/lounge.jpg", "VIP ROOM", "wide"),
    ("images/cast-01.jpg", "CAST", "tall"),
    ("images/cast-02.jpg", "CHAMPAGNE", "tall"),
    ("images/hero.png", "MAIN FLOOR", "wide"),
    ("images/cast-03.jpg", "CAST", "tall"),
    ("images/lounge.jpg", "INTERIOR", "tall"),
    ("images/hero.png", "NIGHT", "wide"),
    ("images/cast-02.jpg", "PARTY", "tall"),
]
gal_items = ""
for i, (src, cap, shape) in enumerate(gallery_imgs):
    gal_items += (f'        <figure class="gal-item {shape}" data-reveal data-d="{i % 4}">'
                  f'<span class="gal-img" style="background-image:url(\'{src}\')"></span>'
                  f'<figcaption>{cap}</figcaption></figure>\n')

gallery_body = page_hero("Gallery", "GALLERY", "店内ギャラリー", "GALLERY") + f"""
  <section class="section">
    <div class="wrap">
      <p class="sys-intro" data-reveal>シャンデリアの灯りに包まれたメインフロア、特別な夜を約束するVIPルーム。
        CLUB AURORA の世界観をご覧ください。</p>
      <div class="gallery-grid">
{gal_items}      </div>
    </div>
  </section>"""

# ---------------------------------------------------------------- NEWS
news_items = [
    ("2026.06.01", "EVENT", "6月限定イベント「Aurora Champagne Night」開催"),
    ("2026.05.28", "CAST", "新キャスト3名が入店しました"),
    ("2026.05.20", "INFO", "営業時間変更のお知らせ"),
    ("2026.05.15", "RENEWAL", "VIPルームリニューアルオープン"),
    ("2026.05.01", "EVENT", "ゴールデンウィーク特別営業のご案内"),
    ("2026.04.20", "CAMPAIGN", "ご新規様限定 ファーストセット特別ご優待"),
]
news_rows = ""
for date, cat, title in news_items:
    news_rows += (f'        <a class="news-row" href="news-detail.html" data-reveal>'
                  f'<time>{date}</time><span class="news-cat">{cat}</span>'
                  f'<span class="news-title">{title}</span><span class="news-ar">&rarr;</span></a>\n')

news_body = page_hero("News &amp; Event", "NEWS", "お知らせ・イベント", "NEWS") + f"""
  <section class="section">
    <div class="wrap">
      <div class="news-page">
{news_rows}      </div>
    </div>
  </section>"""

# ---------------------------------------------------------------- RECRUIT
recruit_body = page_hero("Recruit", "RECRUIT", "女性求人", "RECRUIT") + """
  <section class="section">
    <div class="wrap">
      <div class="section__head" data-reveal>
        <span class="eyebrow">Join Our Stage</span>
        <h2 class="section-title">あなたらしく、輝ける場所。</h2>
      </div>
      <p class="sys-intro" data-reveal data-d="1">未経験の方も安心。充実した待遇と、あなたのペースに合わせた働き方をご用意しています。
        まずは体験入店から、お気軽にどうぞ。</p>

      <div class="recruit-cards">
        <div class="rc-card" data-reveal><span class="rc-num">01</span><h3>高時給</h3><p class="rc-amt gold-text">時給 3,000円〜</p><p>体験入店時給も保証。頑張りはしっかり評価します。</p></div>
        <div class="rc-card" data-reveal data-d="1"><span class="rc-num">02</span><h3>体験入店歓迎</h3><p class="rc-amt gold-text">日払いOK</p><p>1日だけのお試しも大歓迎。当日全額日払い対応。</p></div>
        <div class="rc-card" data-reveal data-d="2"><span class="rc-num">03</span><h3>自由なシフト</h3><p class="rc-amt gold-text">週1〜・短時間OK</p><p>学業・Wワーク・子育てとの両立も応援します。</p></div>
        <div class="rc-card" data-reveal data-d="3"><span class="rc-num">04</span><h3>安心の環境</h3><p class="rc-amt gold-text">送迎・寮あり</p><p>ノルマなし・自由出勤。スタッフが丁寧にサポートします。</p></div>
      </div>

      <div class="recruit-table" data-reveal>
        <table class="ptable" style="max-width:760px;margin:2.5rem auto 0">
          <tr><th style="text-align:left">募集職種</th><td style="text-align:left;font-family:var(--mincho);font-size:.96rem;color:var(--cream)">フロアキャスト（女性）</td></tr>
          <tr><th style="text-align:left">給与</th><td style="text-align:left;font-family:var(--mincho);font-size:.96rem;color:var(--cream)">時給 3,000円〜＋各種バック</td></tr>
          <tr><th style="text-align:left">勤務時間</th><td style="text-align:left;font-family:var(--mincho);font-size:.96rem;color:var(--cream)">20:00 - LAST の間で応相談</td></tr>
          <tr><th style="text-align:left">資格</th><td style="text-align:left;font-family:var(--mincho);font-size:.96rem;color:var(--cream)">20歳以上の方（高校生不可）</td></tr>
          <tr><th style="text-align:left">待遇</th><td style="text-align:left;font-family:var(--mincho);font-size:.96rem;color:var(--cream)">日払い・送迎・寮完備・体験入店可</td></tr>
        </table>
      </div>

      <div style="text-align:center;margin-top:3rem" data-reveal>
        <a href="#" class="btn-line" style="margin-right:1rem">LINEで応募・質問</a>
        <a href="tel:0521234567" class="btn-gold"><span class="ar">&#9742;</span> 052-123-4567</a>
      </div>
    </div>
  </section>"""

# ---------------------------------------------------------------- PRIVACY / LEGAL
privacy_body = page_hero("Privacy Policy", "PRIVACY", "プライバシーポリシー", "PRIVACY") + """
  <section class="section"><div class="wrap" style="max-width:820px">
    <div class="doc" data-reveal>
      <p>CLUB AURORA（以下「当店」）は、お客様の個人情報を適切に保護することを社会的責務と考え、以下の方針に基づき個人情報を取り扱います。</p>
      <h3>1. 個人情報の利用目的</h3>
      <p>ご予約の確認、サービスのご提供、各種ご連絡、より良いサービス向上のための分析を目的として利用いたします。</p>
      <h3>2. 第三者への提供</h3>
      <p>法令に基づく場合を除き、お客様の同意なく個人情報を第三者に提供することはありません。</p>
      <h3>3. 個人情報の管理</h3>
      <p>取得した個人情報は、不正アクセス・紛失・漏洩等を防止するため、適切な安全管理措置を講じます。</p>
      <h3>4. お問い合わせ</h3>
      <p>個人情報に関するお問い合わせは、052-123-4567 までご連絡ください。</p>
      <p class="rsv-note">※本ページはデザインサンプルです。</p>
    </div>
  </div></section>"""

legal_body = page_hero("Legal", "LEGAL", "特定商取引法に基づく表記", "LEGAL") + """
  <section class="section"><div class="wrap" style="max-width:820px">
    <div class="access-info" data-reveal>
      <div class="row"><dt>店舗名</dt><dd>CLUB AURORA</dd></div>
      <div class="row"><dt>所在地</dt><dd>愛知県名古屋市中区錦3-10-14 ピア錦ビル 6F</dd></div>
      <div class="row"><dt>電話番号</dt><dd>052-123-4567</dd></div>
      <div class="row"><dt>営業時間</dt><dd>20:00 - LAST（日曜定休）</dd></div>
      <div class="row"><dt>料金</dt><dd>SYSTEMページに記載のとおり（すべて税込）</dd></div>
      <div class="row"><dt>お支払い方法</dt><dd>現金 / 各種クレジットカード / QRコード決済</dd></div>
      <div class="row"><dt>許可</dt><dd>風俗営業等の規制及び業務の適正化等に関する法律に基づく許可営業</dd></div>
    </div>
    <p class="rsv-note" style="margin-top:1.4rem">※本ページはデザインサンプルです。記載内容は架空のものです。</p>
  </div></section>"""

news_detail_body = """  <section class="cast-detail" style="padding-top:9rem">
    <div class="wrap" style="max-width:860px">
      <p class="breadcrumb" style="margin-bottom:2rem"><a href="index.html">HOME</a> &nbsp;/&nbsp; <a href="news.html">NEWS</a> &nbsp;/&nbsp; <span>EVENT</span></p>
      <div data-reveal>
        <div style="display:flex;gap:1rem;align-items:center;margin-bottom:1.2rem">
          <time style="font-family:var(--serif);color:var(--gold);letter-spacing:.05em">2026.06.01</time>
          <span class="news-cat">EVENT</span>
        </div>
        <h1 class="section-title" style="font-size:clamp(1.8rem,4vw,2.8rem);margin-bottom:2rem">6月限定イベント<br>「Aurora Champagne Night」開催</h1>
        <div class="cd-main" style="aspect-ratio:16/9;background-image:url('images/hero.png');margin-bottom:2rem"></div>
        <div class="doc">
          <p>日頃の感謝を込めて、6月限定の特別イベント「Aurora Champagne Night」を開催いたします。期間中はシャンパンを特別価格でご用意し、キャスト一同、華やかな一夜を演出いたします。</p>
          <h3>開催期間</h3>
          <p>2026年6月1日（月）〜 6月30日（火）　20:00 - LAST</p>
          <h3>イベント内容</h3>
          <p>・対象シャンパンを特別価格でご提供<br>・ご来店のお客様に記念ノベルティを進呈<br>・週末はキャストによるスペシャルステージを実施</p>
          <p>ご予約はお電話・LINE・予約フォームより承っております。皆さまのご来店を心よりお待ちしております。</p>
        </div>
        <div style="margin-top:2.5rem"><a href="news.html" class="btn-gold"><span class="ar">&larr;</span> 一覧へ戻る</a></div>
      </div>
    </div>
  </section>"""

PAGES = [
    ("news-detail", "6月限定イベント｜NEWS｜CLUB AURORA",
     "CLUB AURORA 6月限定イベント「Aurora Champagne Night」のご案内。", "NEWS", news_detail_body),
    ("reserve", "RESERVE｜ご予約｜CLUB AURORA 名古屋・錦",
     "CLUB AURORA のご予約。電話・LINE・予約フォームから24時間受付。", "RECRUIT", reserve_body),
    ("cast-detail", "玲奈（Rena）｜CAST｜CLUB AURORA",
     "CLUB AURORA 在籍キャスト 玲奈のプロフィール・出勤情報。", "CAST", cast_detail_body),
    ("schedule", "SCHEDULE｜出勤情報｜CLUB AURORA 名古屋・錦",
     "CLUB AURORA 本日の出勤・週間スケジュール。", "CAST", schedule_body),
    ("gallery", "GALLERY｜店内ギャラリー｜CLUB AURORA 名古屋・錦",
     "CLUB AURORA の店内・VIPルーム・雰囲気をご紹介します。", "GALLERY", gallery_body),
    ("news", "NEWS｜お知らせ・イベント｜CLUB AURORA 名古屋・錦",
     "CLUB AURORA の最新イベント・キャンペーン・新人入店情報。", "NEWS", news_body),
    ("recruit", "RECRUIT｜女性求人｜CLUB AURORA 名古屋・錦",
     "CLUB AURORA 女性キャスト求人。高時給・体験入店・日払いOK。", "RECRUIT", recruit_body),
    ("privacy", "プライバシーポリシー｜CLUB AURORA",
     "CLUB AURORA のプライバシーポリシー。", "HOME", privacy_body),
    ("legal", "特定商取引法に基づく表記｜CLUB AURORA",
     "CLUB AURORA 特定商取引法に基づく表記。", "HOME", legal_body),
]


def main() -> None:
    """全ページを生成して書き出す."""
    for slug, title, desc, active, body in PAGES:
        html = page(slug, title, desc, active, body)
        out = ROOT / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        logger.info("生成: %s (%d bytes)", out.name, len(html))
    logger.info("完了: %d ページ", len(PAGES))


if __name__ == "__main__":
    main()
