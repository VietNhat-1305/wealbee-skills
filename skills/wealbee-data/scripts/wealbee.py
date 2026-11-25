#!/usr/bin/env python3
"""wealbee.py: dòng lệnh gọn cho Wealbee Data API, dùng chung cho mọi skill trong wealbee-skills. Chỉ đọc dữ liệu.

Khoá API: biến môi trường WEALBEE_API_KEY, hoặc dòng ``WEALBEE_API_KEY=wb_live_...`` trong ``~/.config/wealbee/.env``.
Lấy khoá tại https://wealbee.com/developers. Script không in khoá và không ghi khoá vào kết quả.

    python3 wealbee.py account                          # gói, hạn mức, số ngày còn lại của khoá
    python3 wealbee.py search vinamilk                  # tìm mã theo tên, không cần dấu
    python3 wealbee.py summary VNM [--period Q3/2026]   # tóm tắt BCTC (tỷ đồng), tăng trưởng, biên, ROE, ROA, nguồn
    python3 wealbee.py compare VCB BID CTG [--period 2026Q3]
    python3 wealbee.py trend VNM                        # chuỗi theo quý, gồm quý năm trước
    python3 wealbee.py benchmark --ticker VNM           # trung vị, tứ phân vị cùng loại hình và kỳ
    python3 wealbee.py benchmark --industry bank --period 2026Q3
    python3 wealbee.py news --ticker HPG --days 7       # tin tổng hợp nhiều báo
    python3 wealbee.py news-detail <id>                 # phân tích đồng thuận / khác biệt giữa các báo
    python3 wealbee.py events --ticker HPG --since 2026-11-01
    python3 wealbee.py statement HPG.2026Q3 [--as-of 2026-11-01T00:00:00+07:00]
    python3 wealbee.py versions HPG.2026Q3
    python3 wealbee.py filings --ticker HPG
    python3 wealbee.py glossary ROE                     # từ điển Wealbee, không cần khoá

Kết quả là JSON (UTF-8) trên stdout. Lỗi in JSON ``{"error": ...}`` và thoát với mã 1.
Kỳ nhận nhiều cách viết: 2026Q3, Q3/2026, quý 3/2026, 9T/2026.
Chạy được với Python 3.9 trở lên, chỉ dùng thư viện chuẩn.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

PHIEN_BAN = "0.1.0"
API = os.environ.get("WEALBEE_API_BASE", "https://data.wealbee.com/v1").rstrip("/")
TU_DIEN_URL = "https://wealbee.com/api/glossary"
UA = f"wealbee-skills/{PHIEN_BAN} (+https://github.com/VietNhat-1305/wealbee-skills)"
TY = 1_000_000_000
VN = timezone(timedelta(hours=7))
DEM = Path(os.environ.get("WEALBEE_CACHE_DIR", Path.home() / ".cache" / "wealbee-skills"))


class LoiWealbee(Exception):
    pass


# ---------------------------------------------------------------- khoá và gọi API

def _khoa() -> str:
    k = os.environ.get("WEALBEE_API_KEY", "").strip()
    if k:
        return k
    f = Path.home() / ".config" / "wealbee" / ".env"
    if f.exists():
        for dong in f.read_text(encoding="utf-8").splitlines():
            if dong.strip().startswith("WEALBEE_API_KEY="):
                return dong.split("=", 1)[1].strip().strip('"').strip("'")
    raise LoiWealbee("Chưa có khoá Wealbee. Đặt biến môi trường WEALBEE_API_KEY hoặc ghi WEALBEE_API_KEY=... vào "
                     "~/.config/wealbee/.env. Lấy khoá tại https://wealbee.com/developers.")


def _loi(ma: int, than: bytes) -> LoiWealbee:
    try:
        p = json.loads(than.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        p = {}
    chi_tiet = (p.get("detail") or p.get("title") or "").rstrip(".")
    goi_y = {401: " Khoá sai hoặc đã bị thu hồi.", 403: " Gói hiện tại không có quyền với dữ liệu này.",
             404: " Không tìm thấy; kiểm tra lại mã, kỳ hoặc id.", 429: " Vượt giới hạn tốc độ của gói; thử lại sau ít giây."}
    rid = f" (request_id {p['request_id']})" if p.get("request_id") else ""
    return LoiWealbee(f"Wealbee API trả {ma} {p.get('code') or ''}: {chi_tiet}.{goi_y.get(ma, '')}{rid}".replace("  ", " "))


def api(duong_dan: str, params: dict | None = None) -> Any:
    q = {k: ("true" if v is True else "false" if v is False else v) for k, v in (params or {}).items() if v not in (None, "")}
    url = f"{API}{duong_dan}" + (f"?{urllib.parse.urlencode(q)}" if q else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {_khoa()}", "User-Agent": UA,
                                               "Accept": "application/json"})
    for lan in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            than = e.read()
            if e.code == 429 and lan < 3:
                try:
                    cho = float(e.headers.get("retry-after") or 1)
                except ValueError:
                    cho = 1.0
                time.sleep(min(max(cho, 0.5), 5.0))
                continue
            raise _loi(e.code, than) from None
        except (urllib.error.URLError, TimeoutError) as e:
            if lan < 3:
                time.sleep(lan)
                continue
            raise LoiWealbee(f"Không kết nối được Wealbee API: {type(e).__name__}") from None
    raise LoiWealbee("Không gọi được Wealbee API sau 3 lần thử")


def tat_ca(duong_dan: str, params: dict, toi_da: int = 4000) -> list[dict]:
    """Gom mọi trang (next_cursor) của một danh sách."""
    out, con = [], None
    while len(out) < toi_da:
        d = api(duong_dan, {**params, "limit": 100, "cursor": con})
        out += d.get("data") or []
        con = d.get("next_cursor")
        if not con:
            break
    return out


# ---------------------------------------------------------------- chuẩn hoá đầu vào

def bo_dau(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower().strip()


def chuan_ky(ky: str | None) -> str | None:
    """2026Q3, 2026-Q3, Q3/2026, Q3 2026, quý 3/2026, 3/2026, 9T/2026 -> 2026Q3."""
    if ky is None or not str(ky).strip():
        return None
    x = re.sub(r"\s+", "", bo_dau(str(ky))).upper().replace("QUY", "Q")
    for mau in (r"(?P<y>\d{4})[-_/.]?Q(?P<q>[1-4])", r"Q(?P<q>[1-4])[-_/.]?(?P<y>\d{4})", r"(?P<q>[1-4])[-_/.](?P<y>\d{4})"):
        m = re.fullmatch(mau, x)
        if m:
            return f"{m['y']}Q{m['q']}"
    m = re.fullmatch(r"(?P<t>3|6|9|12)T[-_/.]?(?P<y>\d{4})", x)
    if m:
        return f"{m['y']}Q{int(m['t']) // 3}"
    raise LoiWealbee(f"Kỳ '{ky}' không hợp lệ. Viết dạng 2026Q3 (hoặc Q3/2026, quý 3/2026).")


def chuan_id(sid: str) -> str:
    """hpg.q3/2026 -> HPG.2026Q3"""
    if "." not in (sid or ""):
        raise LoiWealbee(f"Id BCTC '{sid}' không hợp lệ. Viết dạng MÃ.KỲ, VD FPT.2026Q3.")
    ma, ky = sid.strip().split(".", 1)
    return f"{ma.strip().upper()}.{chuan_ky(ky)}"


# ---------------------------------------------------------------- tóm tắt BCTC

def ty(v):
    return None if v is None else round(v / TY, 1)


def tang(moi, cu):
    """% thay đổi; để trống khi thiếu số, kỳ so sánh bằng 0 hoặc lỗ, hay khi đổi dấu."""
    if moi is None or cu is None or cu <= 0 or moi < 0:
        return None
    return round((moi / cu - 1) * 100, 1)


def ty_le(tu, mau):
    if tu is None or not mau:
        return None
    return round(tu / mau * 100, 1)


def tom_tat(s: dict) -> dict:
    kq, cd, lc = s.get("income_statement") or {}, s.get("balance_sheet") or {}, s.get("cash_flow") or {}

    def dong_kq(k):
        x = kq.get(k) or {}
        return {"quarter": ty(x.get("quarter")), "quarter_prior_year": ty(x.get("quarter_prior_year")),
                "quarter_growth_pct": tang(x.get("quarter"), x.get("quarter_prior_year")),
                "ytd": ty(x.get("ytd")), "ytd_prior_year": ty(x.get("ytd_prior_year")),
                "ytd_growth_pct": tang(x.get("ytd"), x.get("ytd_prior_year"))}

    def dong_cd(k):
        x = cd.get(k) or {}
        return {"end_of_period": ty(x.get("end_of_period")), "start_of_year": ty(x.get("start_of_year"))}

    def bq(x):
        """Bình quân đầu năm và cuối kỳ (xấp xỉ số dư bình quân trong kỳ)."""
        a, b = (x or {}).get("start_of_year"), (x or {}).get("end_of_period")
        return None if a is None or b is None or a + b <= 0 else (a + b) / 2

    thang = s.get("months_ytd") or 0
    von_me = cd.get("equity_parent") if (cd.get("equity_parent") or {}).get("end_of_period") is not None else None
    roe_ytd = (ty_le((kq.get("net_profit_parent") or {}).get("ytd"), bq(von_me)) if von_me
               else ty_le((kq.get("net_profit") or {}).get("ytd"), bq(cd.get("equity"))))
    roa_ytd = ty_le((kq.get("net_profit") or {}).get("ytd"), bq(cd.get("total_assets")))
    von = (cd.get("equity") or {}).get("end_of_period")
    no, vay = (cd.get("total_liabilities") or {}).get("end_of_period"), (cd.get("borrowings") or {}).get("end_of_period")
    chi_so = {"liabilities_to_equity": None if not von or no is None else round(no / von, 2),
              "borrowings_to_equity": None if not von or vay is None else round(vay / von, 2),
              "roe_ytd_pct": roe_ytd, "roe_annualized_pct": None if roe_ytd is None or not thang else round(roe_ytd * 12 / thang, 1),
              "roe_basis": "net_profit_parent / equity_parent" if von_me else "net_profit / equity (chưa có vốn chủ công ty mẹ)",
              "roa_ytd_pct": roa_ytd, "roa_annualized_pct": None if roa_ytd is None or not thang else round(roa_ytd * 12 / thang, 1)}
    if s.get("industry_type") == "corporate":
        dt = (kq.get("revenue") or {}).get("quarter")
        chi_so["gross_margin_quarter_pct"] = ty_le((kq.get("gross_profit") or {}).get("quarter"), dt)
        chi_so["net_margin_quarter_pct"] = ty_le((kq.get("net_profit") or {}).get("quarter"), dt)
    kiem = s.get("checks") or []
    pv = s.get("provenance") or {}
    kq_gon = {k: dong_kq(k) for k in ("revenue", "gross_profit", "net_profit", "net_profit_parent") if k in kq}
    cd_gon = {k: dong_cd(k) for k in ("total_assets", "total_liabilities", "borrowings", "equity", "equity_parent",
                                      "non_controlling_interest") if k in cd}
    return {
        "ticker": s.get("ticker"), "statement_id": s.get("id"), "period": s.get("period"), "period_label": s.get("period_label"),
        "months_ytd": s.get("months_ytd"), "scope": s.get("scope"), "industry_type": s.get("industry_type"),
        "status": s.get("status"), "review_reasons": s.get("review_reasons") or [], "version": s.get("version"),
        "health_score": s.get("health_score"), "unit": "tỷ đồng",
        "income_statement": {k: v for k, v in kq_gon.items() if v["quarter"] is not None or v["ytd"] is not None},
        "balance_sheet": {k: v for k, v in cd_gon.items() if v["end_of_period"] is not None or v["start_of_year"] is not None},
        "cash_flow": {k: {"ytd": ty((lc.get(k) or {}).get("ytd")), "ytd_prior_year": ty((lc.get(k) or {}).get("ytd_prior_year"))}
                      for k in ("operating", "investing", "financing", "net_change") if k in lc},
        "missing_fields": [k for k, v in {**kq_gon, **cd_gon}.items() if all(x is None for x in v.values())],
        "ratios": chi_so,
        "checks": {"passed": sum(1 for c in kiem if c.get("status") == "passed"), "total": len(kiem),
                   "not_passed": [c.get("code") for c in kiem if c.get("status") != "passed"]},
        "derived_fields": [d.get("path") for d in s.get("derived") or []],
        "source": {"document_url": pv.get("document_url"), "file_sha256": pv.get("file_sha256"), "pages": pv.get("pages"),
                   "ir_url": pv.get("ir_url"), "detected_at": pv.get("detected_at"), "updated_at": pv.get("updated_at")},
        "notes": "Tỷ đồng, làm tròn 1 chữ số. Tăng trưởng để trống khi kỳ so sánh lỗ, bằng 0 hoặc đổi dấu. ROE = lợi nhuận "
                 "luỹ kế / bình quân vốn chủ (đầu năm, cuối kỳ), xem roe_basis; '_annualized' nhân 12 / months_ytd. "
                 "missing_fields là chỉ tiêu Data API chưa có, không phải bằng 0.",
    }


def lay_bctc(ma: str, ky: str | None) -> dict:
    ma, ky = ma.strip().upper(), chuan_ky(ky)
    return api(f"/statements/{ma}.{ky}", {"view": "full"}) if ky else api(f"/companies/{ma}/statements/latest", {"view": "full"})


def mot_ban_moi_ky(ds: list[dict]) -> dict[str, dict]:
    """Mỗi (mã, kỳ) giữ 1 BCTC: ưu tiên hợp nhất, rồi phiên bản mới nhất."""
    out: dict[str, dict] = {}
    for s in ds:
        k = f"{s.get('ticker')}.{s.get('period')}"
        cu, diem = out.get(k), (s.get("scope") == "consolidated", s.get("version") or 0)
        if cu is None or diem > (cu.get("scope") == "consolidated", cu.get("version") or 0):
            out[k] = s
    return out


def ky_truoc(ky: str, buoc: int) -> str:
    n = int(ky[:4]) * 4 + int(ky[-1]) - 1 - buoc
    return f"{n // 4}Q{n % 4 + 1}"


def phan_vi(xs: list[float], p: float) -> float | None:
    if not xs:
        return None
    xs = sorted(xs)
    i = (len(xs) - 1) * p
    a, b = int(i), min(int(i) + 1, len(xs) - 1)
    return round(xs[a] + (xs[b] - xs[a]) * (i - a), 2)


# ---------------------------------------------------------------- lệnh

def lenh_account(a):
    d = api("/me")
    d.pop("key_prefix", None)
    d.pop("tenant", None)            # tên chủ tài khoản: không đưa vào báo cáo
    han = (d.get("entitlements") or {}).get("valid_until")
    if han:
        d["days_left"] = (datetime.fromisoformat(han) - datetime.now(VN)).days
        if d["days_left"] < 14:
            d["warning"] = f"Khoá còn {d['days_left']} ngày (hết hạn {han[:10]})."
    return d


def lenh_search(a):
    return api("/companies", {"q": " ".join(a.query), "exchange": a.exchange, "industry_type": a.industry, "limit": a.limit})


def lenh_summary(a):
    return tom_tat(lay_bctc(a.ticker, a.period))


def lenh_compare(a):
    ds = list(dict.fromkeys(t.strip().upper() for t in a.tickers if t.strip()))[:10]
    if len(ds) < 2:
        raise LoiWealbee("Cần 2–10 mã để so sánh.")

    def mot(t):
        try:
            g = tom_tat(lay_bctc(t, a.period))
        except LoiWealbee as e:
            return {"ticker": t, "error": str(e)}
        kq = g["income_statement"]
        return {"ticker": t, "period": g["period"], "status": g["status"], "industry_type": g["industry_type"],
                "revenue_quarter": (kq.get("revenue") or {}).get("quarter"),
                "revenue_growth_pct": (kq.get("revenue") or {}).get("quarter_growth_pct"),
                "net_profit_parent_quarter": (kq.get("net_profit_parent") or {}).get("quarter"),
                "net_profit_parent_growth_pct": (kq.get("net_profit_parent") or {}).get("quarter_growth_pct"),
                "net_profit_parent_ytd": (kq.get("net_profit_parent") or {}).get("ytd"),
                **g["ratios"], "health_score": (g.get("health_score") or {}).get("value"),
                "missing_fields": g["missing_fields"], "document_url": g["source"]["document_url"]}
    with ThreadPoolExecutor(5) as ex:
        hang = list(ex.map(mot, ds))
    return {"unit": "tỷ đồng", "companies": hang,
            "notes": "Tăng trưởng so với cùng kỳ năm trước. Không chỉ định period thì mỗi mã lấy kỳ mới nhất của mã đó."}


def lenh_trend(a):
    t = a.ticker.strip().upper()
    theo_ky = {s["period"]: s for s in mot_ban_moi_ky(tat_ca("/statements", {"ticker": t, "view": "full"})).values()}
    if not theo_ky:
        raise LoiWealbee(f"Chưa có BCTC nào của {t}.")

    def q(s, k, cot="quarter"):
        return ((s.get("income_statement") or {}).get(k) or {}).get(cot)

    hang: dict[str, dict] = {}
    for ky, s in sorted(theo_ky.items()):
        thuong = s.get("industry_type") == "corporate"
        for p, cot, nguon in ((ky, "quarter", "statement"), (ky_truoc(ky, 4), "quarter_prior_year", f"cột cùng kỳ trong BCTC {ky}")):
            if p in hang or (cot != "quarter" and p in theo_ky):
                continue
            dt, lg, ln = q(s, "revenue", cot), q(s, "gross_profit", cot), q(s, "net_profit_parent", cot)
            hang[p] = {"period": p, "source": nguon, "status": s.get("status"), "revenue": ty(dt), "net_profit_parent": ty(ln),
                       "gross_margin_pct": ty_le(lg, dt) if thuong else None, "net_margin_pct": ty_le(ln, dt) if thuong else None,
                       "equity_parent_end": ty(((s.get("balance_sheet") or {}).get("equity_parent") or {}).get("end_of_period"))
                       if cot == "quarter" else None,
                       "document_url": (s.get("provenance") or {}).get("document_url")}
    for ky, h in hang.items():
        for k in ("revenue", "net_profit_parent"):
            nt, qt = hang.get(ky_truoc(ky, 4)), hang.get(ky_truoc(ky, 1))
            h[f"{k}_yoy_pct"] = tang(h[k], nt[k]) if nt else None
            h[f"{k}_qoq_pct"] = tang(h[k], qt[k]) if qt else None
    return {"ticker": t, "unit": "tỷ đồng", "industry_type": next(iter(theo_ky.values())).get("industry_type"),
            "quarters": [hang[k] for k in sorted(hang)],
            "notes": "Số riêng từng quý. Quý có source khác 'statement' lấy từ cột cùng kỳ của BCTC năm sau (có thể đã điều chỉnh hồi tố)."}


CHI_SO = {
    "revenue_growth_pct": ("Tăng trưởng doanh thu quý so với cùng kỳ (%)", lambda g: (g["income_statement"].get("revenue") or {}).get("quarter_growth_pct")),
    "net_profit_parent_growth_pct": ("Tăng trưởng lợi nhuận công ty mẹ quý so với cùng kỳ (%)",
                                     lambda g: (g["income_statement"].get("net_profit_parent") or {}).get("quarter_growth_pct")),
    "gross_margin_quarter_pct": ("Biên lợi nhuận gộp quý (%)", lambda g: g["ratios"].get("gross_margin_quarter_pct")),
    "net_margin_quarter_pct": ("Biên lợi nhuận ròng quý (%)", lambda g: g["ratios"].get("net_margin_quarter_pct")),
    "roe_annualized_pct": ("ROE quy năm (%)", lambda g: g["ratios"].get("roe_annualized_pct")),
    "roa_annualized_pct": ("ROA quy năm (%)", lambda g: g["ratios"].get("roa_annualized_pct")),
    "liabilities_to_equity": ("Nợ phải trả / vốn chủ (lần)", lambda g: g["ratios"].get("liabilities_to_equity")),
}


def _bctc_ky(ky: str, loai: str, chi_kiem_chung: bool) -> list[dict]:
    """Mọi BCTC của một loại hình trong một kỳ; đệm 6 giờ trong ~/.cache/wealbee-skills."""
    f = DEM / f"bctc-{ky}-{loai}-{'verified' if chi_kiem_chung else 'all'}.json"
    if f.exists() and time.time() - f.stat().st_mtime < 6 * 3600:
        return json.loads(f.read_text(encoding="utf-8"))
    ds = list(mot_ban_moi_ky(tat_ca("/statements", {"period": ky, "industry_type": loai, "view": "full",
                                                    "status": "verified" if chi_kiem_chung else None})).values())
    try:
        DEM.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(ds, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    return ds


def lenh_benchmark(a):
    ky, loai, rieng = chuan_ky(a.period), a.industry, None
    if a.ticker:
        rieng = tom_tat(lay_bctc(a.ticker, ky))
        ky, loai = rieng["period"], rieng["industry_type"]
    if not ky or not loai:
        raise LoiWealbee("Cần --ticker, hoặc cả --industry và --period.")
    ds = [tom_tat(s) for s in _bctc_ky(ky, loai, not a.all_statuses)]
    ket = {}
    for k, (ten, lay) in CHI_SO.items():
        xs = [v for v in (lay(g) for g in ds) if isinstance(v, (int, float))]
        if len(xs) < 5:
            continue
        muc = {"label": ten, "n": len(xs), "p25": phan_vi(xs, 0.25), "median": phan_vi(xs, 0.5), "p75": phan_vi(xs, 0.75)}
        if rieng is not None and isinstance(lay(rieng), (int, float)):
            v = lay(rieng)
            muc.update(company=v, company_percentile=round(sum(1 for x in xs if x <= v) / len(xs) * 100))
        ket[k] = muc
    return {"period": ky, "industry_type": loai, "statements": len(ds), "verified_only": not a.all_statuses,
            **({"ticker": rieng["ticker"], "company_status": rieng["status"]} if rieng else {}), "metrics": ket,
            "notes": "Loại hình theo Data API (corporate, bank, securities, insurance). 'corporate' gồm mọi ngành, nên trung vị chỉ là "
                     "mốc chung. company_percentile = % BCTC có giá trị nhỏ hơn hoặc bằng số của mã; chỉ để định vị, không phải xếp hạng."}


def lenh_news(a):
    tu = a.since or ((datetime.now(VN) - timedelta(days=a.days)).isoformat(timespec="seconds") if a.days else None)
    return api("/news", {"ticker": a.ticker, "category": a.category, "published_since": tu, "limit": a.limit})


def lenh_news_detail(a):
    return api(f"/news/{a.news_id.strip()}")


def lenh_events(a):
    return api("/events", {"type": a.types, "ticker": a.ticker, "created_since": a.since, "limit": a.limit})


def lenh_statement(a):
    return api(f"/statements/{chuan_id(a.statement_id)}", {"as_of": a.as_of, "view": "full"})


def lenh_versions(a):
    sid = chuan_id(a.statement_id)
    return api(f"/statements/{sid}/versions/{a.version}", {"view": "full"}) if a.version else api(f"/statements/{sid}/versions")


def lenh_filings(a):
    return api("/filings", {"ticker": a.ticker, "period": chuan_ky(a.period), "status": a.status, "limit": a.limit})


def lenh_glossary(a):
    """Tra từ điển Wealbee (công khai, không cần khoá); đệm 24 giờ."""
    f = DEM / "glossary.json"
    if f.exists() and time.time() - f.stat().st_mtime < 24 * 3600:
        ds = json.loads(f.read_text(encoding="utf-8"))
    else:
        req = urllib.request.Request(TU_DIEN_URL, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                j = json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            raise LoiWealbee(f"Không tải được từ điển Wealbee: {type(e).__name__}") from None
        ds = j if isinstance(j, list) else (j.get("items") or j.get("terms") or j.get("data") or [])
        try:
            DEM.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps(ds, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass
    q = bo_dau(" ".join(a.term))

    def diem(t):
        ten = [bo_dau(t.get("term") or ""), bo_dau(t.get("en") or "")] + [bo_dau(x) for x in t.get("aliases") or []]
        return 3 if q in ten else 2 if any(x.startswith(q) for x in ten) else 1 if any(q in x for x in ten) else 0

    hop = sorted((t for t in ds if diem(t)), key=lambda t: -diem(t))[:5]
    return {"query": " ".join(a.term), "matches": [{k: t.get(k) for k in ("term", "en", "topic", "definition", "example", "aliases",
                                                                           "related")} for t in hop],
            "page_url_pattern": "https://wealbee.com/tu-dien/<thuật-ngữ-không-dấu>", "note": None if hop else "Không thấy trong từ điển."}


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)
    sub.add_parser("account").set_defaults(f=lenh_account)
    p = sub.add_parser("search"); p.add_argument("query", nargs="+"); p.add_argument("--exchange", choices=["HOSE", "HNX", "UPCOM"])
    p.add_argument("--industry", choices=["corporate", "bank", "securities", "insurance"]); p.add_argument("--limit", type=int, default=20)
    p.set_defaults(f=lenh_search)
    p = sub.add_parser("summary"); p.add_argument("ticker"); p.add_argument("--period"); p.set_defaults(f=lenh_summary)
    p = sub.add_parser("compare"); p.add_argument("tickers", nargs="+"); p.add_argument("--period"); p.set_defaults(f=lenh_compare)
    p = sub.add_parser("trend"); p.add_argument("ticker"); p.set_defaults(f=lenh_trend)
    p = sub.add_parser("benchmark"); p.add_argument("--ticker"); p.add_argument("--period")
    p.add_argument("--industry", choices=["corporate", "bank", "securities", "insurance"])
    p.add_argument("--all-statuses", action="store_true", help="tính cả BCTC needs_review"); p.set_defaults(f=lenh_benchmark)
    p = sub.add_parser("news"); p.add_argument("--ticker"); p.add_argument("--days", type=int); p.add_argument("--since")
    p.add_argument("--category", choices=["company", "industry", "macro", "market", "commodity", "other"])
    p.add_argument("--limit", type=int, default=20); p.set_defaults(f=lenh_news)
    p = sub.add_parser("news-detail"); p.add_argument("news_id"); p.set_defaults(f=lenh_news_detail)
    p = sub.add_parser("events"); p.add_argument("--ticker"); p.add_argument("--since"); p.add_argument("--types")
    p.add_argument("--limit", type=int, default=20); p.set_defaults(f=lenh_events)
    p = sub.add_parser("statement"); p.add_argument("statement_id"); p.add_argument("--as-of"); p.set_defaults(f=lenh_statement)
    p = sub.add_parser("versions"); p.add_argument("statement_id"); p.add_argument("--version", type=int); p.set_defaults(f=lenh_versions)
    p = sub.add_parser("filings"); p.add_argument("--ticker"); p.add_argument("--period")
    p.add_argument("--status", choices=["processing", "in_review", "published", "superseded"]); p.add_argument("--limit", type=int, default=20)
    p.set_defaults(f=lenh_filings)
    p = sub.add_parser("glossary"); p.add_argument("term", nargs="+"); p.set_defaults(f=lenh_glossary)
    a = ap.parse_args(argv)
    try:
        kq = a.f(a)
    except LoiWealbee as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 1
    print(json.dumps(kq, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
