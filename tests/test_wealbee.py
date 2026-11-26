"""Test cho skills/wealbee-data/scripts/wealbee.py. Không gọi mạng, không cần khoá.

    python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "wealbee-data" / "scripts" / "wealbee.py"
spec = importlib.util.spec_from_file_location("wealbee", SCRIPT)
wb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wb)

TY = 1_000_000_000


def bctc_vnm() -> dict:
    """BCTC dạng Data API (đơn vị đồng), số lấy từ BCTC hợp nhất Q3/2026 của VNM."""
    def d(q, qp, y, yp):
        return {"quarter": q * TY, "quarter_prior_year": qp * TY, "ytd": y * TY, "ytd_prior_year": None if yp is None else yp * TY}

    return {
        "id": "VNM.2026Q3", "ticker": "VNM", "period": "2026Q3", "period_label": "Q3/2026", "months_ytd": 9,
        "scope": "consolidated", "industry_type": "corporate", "status": "verified", "version": 3,
        "income_statement": {
            "revenue": d(18465.2, 16982.9, 53461.2, 46688.8),
            "gross_profit": d(7636.5, 7070.5, 22736.6, 19269.6),
            "net_profit": d(2962.2, 2510.5, 8604.8, 6586.4),
            "net_profit_parent": d(2964.2, 2526.8, 8559.9, None),
        },
        "balance_sheet": {
            "total_assets": {"end_of_period": 57892.4 * TY, "start_of_year": 53312.4 * TY},
            "total_liabilities": {"end_of_period": 19628.2 * TY, "start_of_year": 18829.4 * TY},
            "borrowings": {"end_of_period": 8482.1 * TY, "start_of_year": 9456.6 * TY},
            "equity": {"end_of_period": 38264.2 * TY, "start_of_year": 34483.0 * TY},
            "equity_parent": {"end_of_period": None, "start_of_year": None},
        },
        "cash_flow": {"operating": {"ytd": 7745.8 * TY, "ytd_prior_year": 7007.8 * TY}},
        "checks": [{"code": "a", "status": "passed"}, {"code": "b", "status": "failed"}],
        "provenance": {"document_url": "https://example.com/vnm.pdf", "pages": {"income_statement": 11}},
    }


class KyVaId(unittest.TestCase):
    def test_cac_cach_viet_ky(self):
        for vao in ("2026Q3", "2026-q3", "Q3/2026", "q3 2026", "quý 3/2026", "Quý 3 2026", "3/2026", "9T/2026", "9t2026"):
            self.assertEqual(wb.chuan_ky(vao), "2026Q3", vao)
        self.assertEqual(wb.chuan_ky("12T/2025"), "2025Q4")
        self.assertIsNone(wb.chuan_ky(None))
        self.assertIsNone(wb.chuan_ky("  "))

    def test_ky_sai(self):
        for vao in ("Q5/2026", "2026", "abc", "13/2026"):
            with self.assertRaises(wb.LoiWealbee):
                wb.chuan_ky(vao)

    def test_id(self):
        self.assertEqual(wb.chuan_id("hpg.q3/2026"), "HPG.2026Q3")
        self.assertEqual(wb.chuan_id(" fpt .2026Q1"), "FPT.2026Q1")
        with self.assertRaises(wb.LoiWealbee):
            wb.chuan_id("HPG2026Q3")

    def test_ky_truoc(self):
        self.assertEqual(wb.ky_truoc("2026Q1", 1), "2025Q4")
        self.assertEqual(wb.ky_truoc("2026Q3", 4), "2025Q3")
        self.assertEqual(wb.ky_truoc("2026Q3", 0), "2026Q3")

    def test_bo_dau(self):
        self.assertEqual(wb.bo_dau("Sữa Việt Nam Đ"), "sua viet nam d")


class TinhSo(unittest.TestCase):
    def test_tang_truong(self):
        self.assertEqual(wb.tang(110, 100), 10.0)
        self.assertIsNone(wb.tang(10, 0))       # kỳ so sánh bằng 0
        self.assertIsNone(wb.tang(10, -5))      # kỳ so sánh lỗ
        self.assertIsNone(wb.tang(-1, 5))       # đổi dấu
        self.assertIsNone(wb.tang(None, 5))

    def test_phan_vi(self):
        xs = [1, 2, 3, 4, 5]
        self.assertEqual(wb.phan_vi(xs, 0.5), 3)
        self.assertEqual(wb.phan_vi(xs, 0.25), 2)
        self.assertEqual(wb.phan_vi([4, 1, 3, 2], 0.5), 2.5)
        self.assertIsNone(wb.phan_vi([], 0.5))

    def test_mot_ban_moi_ky_uu_tien_hop_nhat_roi_phien_ban(self):
        ds = [{"ticker": "A", "period": "2026Q3", "scope": "separate", "version": 9},
              {"ticker": "A", "period": "2026Q3", "scope": "consolidated", "version": 1},
              {"ticker": "A", "period": "2026Q3", "scope": "consolidated", "version": 2}]
        x = wb.mot_ban_moi_ky(ds)["A.2026Q3"]
        self.assertEqual((x["scope"], x["version"]), ("consolidated", 2))


class TomTat(unittest.TestCase):
    def setUp(self):
        self.t = wb.tom_tat(bctc_vnm())

    def test_doi_ty_dong_va_tang_truong(self):
        kq = self.t["income_statement"]
        self.assertEqual(kq["revenue"]["quarter"], 18465.2)
        self.assertEqual(kq["revenue"]["quarter_growth_pct"], 8.7)
        self.assertEqual(kq["net_profit_parent"]["quarter_growth_pct"], 17.3)
        self.assertIsNone(kq["net_profit_parent"]["ytd_growth_pct"])   # thiếu cùng kỳ luỹ kế thì để trống
        self.assertEqual(self.t["unit"], "tỷ đồng")

    def test_ty_so(self):
        r = self.t["ratios"]
        self.assertEqual(r["gross_margin_quarter_pct"], 41.4)
        self.assertEqual(r["net_margin_quarter_pct"], 16.0)
        self.assertEqual(r["liabilities_to_equity"], 0.51)
        self.assertEqual(r["borrowings_to_equity"], 0.22)
        self.assertEqual(r["roe_ytd_pct"], 23.7)
        self.assertEqual(r["roe_annualized_pct"], 31.5)
        self.assertEqual(r["roa_annualized_pct"], 20.6)
        self.assertIn("chưa có vốn chủ công ty mẹ", r["roe_basis"])

    def test_quy_nam_khong_lam_tron_hai_lan(self):
        # CTG Q3/2026: 31.614,8 / bình quân(179.655,0; 207.465,6) = 16,334% -> quy năm 21,78% -> 21,8 (không phải 16,3 x 12/9 = 21,7)
        s = bctc_vnm()
        s["income_statement"]["net_profit"]["ytd"] = 31614.8 * TY
        s["balance_sheet"]["equity"] = {"end_of_period": 207465.6 * TY, "start_of_year": 179655.0 * TY}
        r = wb.tom_tat(s)["ratios"]
        self.assertEqual(r["roe_ytd_pct"], 16.3)
        self.assertEqual(r["roe_annualized_pct"], 21.8)

    def test_roe_dung_von_chu_cong_ty_me_khi_co(self):
        s = bctc_vnm()
        s["balance_sheet"]["equity_parent"] = {"end_of_period": 38000.0 * TY, "start_of_year": 34000.0 * TY}
        r = wb.tom_tat(s)["ratios"]
        self.assertEqual(r["roe_basis"], "net_profit_parent / equity_parent")
        self.assertEqual(r["roe_ytd_pct"], round(8559.9 / 36000.0 * 100, 1))

    def test_truong_thieu_kiem_va_nguon(self):
        self.assertIn("equity_parent", self.t["missing_fields"])
        self.assertEqual(self.t["checks"], {"passed": 1, "total": 2, "not_passed": ["b"]})
        self.assertEqual(self.t["source"]["document_url"], "https://example.com/vnm.pdf")

    def test_ngan_hang_khong_tinh_bien(self):
        s = bctc_vnm()
        s["industry_type"] = "bank"
        self.assertNotIn("gross_margin_quarter_pct", wb.tom_tat(s)["ratios"])


class KhoaVaLoi(unittest.TestCase):
    def test_thieu_khoa(self):
        with tempfile.TemporaryDirectory() as home, mock.patch.dict(os.environ, {"HOME": home, "WEALBEE_API_KEY": ""}):
            with self.assertRaises(wb.LoiWealbee) as e:
                wb._khoa()
            self.assertIn("wealbee.com/developers", str(e.exception))

    def test_doc_khoa_tu_file_env(self):
        with tempfile.TemporaryDirectory() as home, mock.patch.dict(os.environ, {"HOME": home, "WEALBEE_API_KEY": ""}):
            f = Path(home) / ".config" / "wealbee" / ".env"
            f.parent.mkdir(parents=True)
            f.write_text('# ghi chú\nWEALBEE_API_KEY="wb_test_khoa_gia"\n', encoding="utf-8")
            self.assertEqual(wb._khoa(), "wb_test_khoa_gia")

    def test_bien_moi_truong_uu_tien(self):
        with mock.patch.dict(os.environ, {"WEALBEE_API_KEY": " wb_test_tu_env "}):
            self.assertEqual(wb._khoa(), "wb_test_tu_env")

    def test_thong_bao_loi_api(self):
        e = wb._loi(429, json.dumps({"code": "rate_limited", "detail": "Too many requests.", "request_id": "r1"}).encode())
        self.assertIn("429", str(e))
        self.assertIn("thử lại sau", str(e))
        self.assertIn("request_id r1", str(e))
        self.assertIn("404", str(wb._loi(404, b"khong phai json")))


class DongLenh(unittest.TestCase):
    def chay(self, *args, env=None):
        with tempfile.TemporaryDirectory() as home:
            e = {**os.environ, "HOME": home, "WEALBEE_API_KEY": "", **(env or {})}
            return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=e, timeout=60)

    def test_thieu_khoa_tra_json_loi(self):
        r = self.chay("summary", "VNM")
        self.assertEqual(r.returncode, 1)
        self.assertIn("error", json.loads(r.stdout))

    def test_ky_sai_tra_json_loi(self):
        r = self.chay("summary", "VNM", "--period", "Q9/2026", env={"WEALBEE_API_KEY": "wb_test_khoa_gia"})
        self.assertEqual(r.returncode, 1)
        self.assertIn("không hợp lệ", json.loads(r.stdout)["error"])

    def test_help(self):
        r = self.chay("--help")
        self.assertEqual(r.returncode, 0)
        for lenh in ("summary", "compare", "trend", "benchmark", "news", "events", "glossary", "prices", "reaction", "event-study"):
            self.assertIn(lenh, r.stdout)


class PhanUngGia(unittest.TestCase):
    """Ngày công bố, cửa sổ phản ứng giá, nhóm tăng trưởng, giá từ CSV (không gọi mạng)."""
    GIA = [("2026-10-28", 100.0), ("2026-10-29", 101.0), ("2026-10-30", 102.0), ("2026-11-02", 104.0),
           ("2026-11-03", 103.0), ("2026-11-04", 105.0), ("2026-11-05", 106.0), ("2026-11-06", 108.0)]
    CS = [("2026-10-28", 1000.0), ("2026-10-29", 1000.0), ("2026-10-30", 1000.0), ("2026-11-02", 1010.0),
          ("2026-11-03", 1000.0), ("2026-11-04", 1020.0), ("2026-11-05", 1020.0), ("2026-11-06", 1030.0)]

    def test_ngay_uu_tien_filings_va_gio(self):
        f = [{"period": "2026Q3", "issuer_release_date": "2026-10-30", "detected_at": "2026-10-30T17:09:34+07:00"},
             {"period": "2026Q2", "issuer_release_date": "2026-07-01"}]
        cb = wb.ngay_cong_bo("2026Q3", f, [])
        self.assertEqual((cb["date"], cb["time"], cb["source"], cb["estimated"]), ("2026-10-30", "17:09", "issuer_release_date", False))

    def test_lay_ngay_som_nhat_khi_wealbee_phat_hien_muon(self):
        f = [{"period": "2026Q3", "detected_at": "2026-11-25T22:03:00+07:00", "document_url": "https://x/VHM_20261030_BCTC.pdf"}]
        cb = wb.ngay_cong_bo("2026Q3", f, [f[0]["document_url"]])
        self.assertEqual((cb["date"], cb["source"], cb["after_deadline"]), ("2026-10-30", "document_url", False))
        cb = wb.ngay_cong_bo("2026Q3", [f[0]], [])
        self.assertEqual((cb["date"], cb["after_deadline"]), ("2026-11-25", True))

    def test_ngay_tu_ten_file_roi_han_luat(self):
        cb = wb.ngay_cong_bo("2026Q2", [], ["https://x/cms/20260730_VNM_BCTC_Q2.pdf"])
        self.assertEqual((cb["date"], cb["source"], cb["estimated"]), ("2026-07-30", "document_url", True))
        cb = wb.ngay_cong_bo("2026Q2", [], ["https://x/BCTC_20250115.pdf"])        # ngày ngoài khoảng hợp lý: bỏ qua
        self.assertEqual((cb["date"], cb["source"]), ("2026-07-30", "legal_deadline"))
        self.assertEqual(wb.ngay_cong_bo("2026Q4", [], [], hop_nhat=False)["date"], "2027-01-20")

    def test_cong_bo_sau_gio_dong_cua_phan_ung_phien_sau(self):
        r = wb.phan_ung({"date": "2026-10-30", "time": "17:09"}, self.GIA, self.CS, (1, 5))
        self.assertEqual((r["base_date"], r["first_session"]), ("2026-10-30", "2026-11-02"))
        self.assertEqual(r["windows"]["1"]["stock_pct"], round((104 / 102 - 1) * 100, 2))
        self.assertEqual(r["windows"]["1"]["excess_pct"], round((104 / 102 - 1) * 100 - 1.0, 2))
        self.assertEqual(r["windows"]["5"]["date"], "2026-11-06")
        self.assertEqual(r["to_date"]["sessions"], 5)

    def test_cong_bo_trong_phien_va_khong_ro_gio(self):
        r = wb.phan_ung({"date": "2026-10-30", "time": "10:00"}, self.GIA, self.CS, (1,))
        self.assertEqual((r["base_date"], r["first_session"]), ("2026-10-29", "2026-10-30"))
        r = wb.phan_ung({"date": "2026-10-31", "time": None}, self.GIA, self.CS, (1,))   # thứ Bảy, không rõ giờ
        self.assertEqual((r["base_date"], r["first_session"]), ("2026-10-30", "2026-11-02"))
        self.assertIsNone(wb.phan_ung({"date": "2026-11-06", "time": None}, self.GIA, self.CS))   # chưa có phiên sau

    def test_nhom_tang_truong(self):
        self.assertEqual([wb._nhom_tang(v) for v in (-5, 0, 20, 20.1, None)],
                         ["giam", "tang_0_20", "tang_0_20", "tang_tren_20", "khong_tinh_duoc"])

    def test_gia_tu_csv(self):
        from datetime import date
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {"WEALBEE_PRICE_CSV_DIR": d}):
            (Path(d) / "ABC.csv").write_text("date,close\n2026-11-03,10.5\n2026-11-02,10\n2026-12-01,11\n", encoding="utf-8")
            out, nguon = wb.gia("abc", date(2026, 11, 1), date(2026, 11, 30))
            self.assertEqual(out, [("2026-11-02", 10.0), ("2026-11-03", 10.5)])
            self.assertEqual(nguon, "csv:ABC.csv")


if __name__ == "__main__":
    unittest.main()
