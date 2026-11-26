---
name: wealbee-data
description: Foundation skill for Wealbee Data API (data.wealbee.com), the verified quarterly financial statements (BCTC), source PDFs, multi-outlet news and change events of companies listed on HOSE, HNX and UPCOM. Covers API key setup, the bundled `wealbee.py` command line (summary, compare, trend, benchmark, news, events, filings, glossary) and the shared rules every Wealbee skill follows (field meanings, how ROE and growth are computed, Vietnamese securities-law limits, citation style). Use it whenever the user wants raw Wealbee numbers, a quick data lookup ("doanh thu quý 3 của FPT là bao nhiêu", "tra BCTC HPG", "Wealbee API trả gì"), asks how to set up or test a Wealbee API key, or when another wealbee-* skill points here. Also use it before writing any Vietnamese stock analysis that should rest on real filed numbers instead of memory.
---

# Wealbee Data: nền tảng cho bộ skill phân tích đầu tư

Wealbee Data API cung cấp số liệu báo cáo tài chính (BCTC) quý của doanh nghiệp niêm yết Việt Nam, đã chuẩn hoá và kiểm bằng code, có đường dẫn tới đúng file PDF gốc; cùng tin tức gom cụm từ nhiều báo và luồng sự kiện khi dữ liệu thay đổi. Mọi skill `wealbee-*` lấy số qua skill này, nên đọc kỹ phần quy tắc trước khi viết bất cứ thứ gì cho người đọc.

## Cài khoá (một lần)

1. Lấy khoá tại https://wealbee.com/developers (khoá `wb_live_…`; khoá thử `wb_test_…` trỏ vào dữ liệu sandbox).
2. Đặt khoá bằng một trong hai cách, không dán khoá vào chat hay file kết quả:
   - biến môi trường `WEALBEE_API_KEY`;
   - dòng `WEALBEE_API_KEY=wb_live_...` trong `~/.config/wealbee/.env`.
3. Kiểm tra: `python3 scripts/wealbee.py account` trả gói, hạn mức mỗi phút và `days_left`. Còn dưới 14 ngày thì nhắc người dùng gia hạn.

Thiếu khoá thì script trả `{"error": "Chưa có khoá Wealbee..."}`. Khi đó dừng lại và hướng dẫn người dùng 3 bước trên, đừng đoán số.

## Lệnh

Gọi bằng đường dẫn tuyệt đối: `python3 <thư mục skill wealbee-data>/scripts/wealbee.py <lệnh>` (các skill khác ghép `<thư mục skill đó>/../wealbee-data/scripts/wealbee.py`). Lệnh chạy ở thư mục làm việc của người dùng, nên kết quả ghi ra đó. Kết quả là JSON trên stdout; lỗi là `{"error": ...}`, mã thoát 1. Python 3.9 trở lên, không cần cài thư viện.

| Lệnh | Trả về | Dùng khi |
|---|---|---|
| `account` | Gói, quyền, hạn mức, số ngày còn lại của khoá | Kiểm tra khoá, giải thích lỗi 403/429 |
| `search <tên hoặc mã>` | Công ty, sàn, loại hình, `coverage` (kỳ BCTC đang có) | Người dùng nói tên công ty thay vì mã |
| `summary <MÃ> [--period Q3/2026]` | Tóm tắt BCTC bằng tỷ đồng: KQKD, CĐKT, LCTT, tăng trưởng, biên, ROE, ROA, phép kiểm, `missing_fields`, nguồn PDF | Mọi câu hỏi về kết quả kinh doanh của một mã |
| `compare <MÃ1> <MÃ2> … [--period]` | 2–10 mã cạnh nhau | So sánh |
| `trend <MÃ>` | Chuỗi theo quý, gồm quý năm trước lấy từ cột cùng kỳ; tăng trưởng so với cùng kỳ và quý trước | "Đang tăng hay giảm", vẽ biểu đồ |
| `benchmark --ticker <MÃ>` hoặc `--industry <loại> --period <kỳ>` | Trung vị, p25, p75 của tăng trưởng, biên, ROE, ROA, nợ/vốn chủ trên mọi BCTC cùng loại hình và kỳ; vị trí phần trăm của mã | Đặt số cạnh mặt bằng, thay cho "mức tốt" theo ý kiến |
| `news [--ticker] [--days N] [--category]` | Tin gom cụm từ nhiều báo, số nguồn, sắc thái | Tin về mã, ngành, thị trường |
| `news-detail <id>` | Bài gốc, điểm đồng thuận và khác biệt giữa các báo | Đọc sâu một tin |
| `events [--ticker] [--since]` | Sự kiện: BCTC mới, được sửa, bị rút; tin mới | "Có gì mới từ hôm qua" |
| `statement <MÃ.KỲ> [--as-of]` | BCTC nguyên dạng (đơn vị đồng), đủ phép kiểm, chỉ tiêu tự tính, nguồn | Cần dòng chi tiết hoặc xem số tại một thời điểm |
| `versions <MÃ.KỲ> [--version N]` | Lịch sử phiên bản và lý do sửa | Số liệu bị sửa, kiểm chứng |
| `filings [--ticker] [--period]` | File BCTC gốc: link, SHA-256, ngày công bố, lúc Wealbee phát hiện | Dẫn nguồn, kiểm file gốc |
| `glossary <thuật ngữ>` | Định nghĩa, tên tiếng Anh, ví dụ, thuật ngữ liên quan (không cần khoá) | Giải thích thuật ngữ |
| `prices <MÃ> [--from] [--to]` | Giá đóng cửa ngày (nghìn đồng, đã điều chỉnh cổ tức, chia tách) từ nguồn công khai | Cần giá cổ phiếu hoặc chỉ số (VNINDEX, HNXINDEX, UPCOMINDEX) |
| `reaction <MÃ> [--period] [--all]` | Ngày công bố BCTC, lợi suất sau 1, 5, 10, 20 phiên và đến nay, so với chỉ số sàn | "Từ lúc ra BCTC đến giờ giá tăng bao nhiêu" |
| `event-study --period … --tickers …` | Backtest nhiều mã, nhiều kỳ: lợi suất vượt chỉ số theo nhóm tăng trưởng lợi nhuận | Phản ứng giá quanh mùa BCTC |

Kỳ nhận `2026Q3`, `Q3/2026`, `quý 3/2026`, `9T/2026`. Đã kết nối Wealbee MCP thì có thể gọi tool tương ứng (`wealbee_statement_summary`, `wealbee_compare_companies`, `wealbee_quarterly_trend`, `wealbee_industry_benchmark`, …) thay cho script; số liệu và cách tính giống nhau.

## Đọc trước khi viết cho người đọc

- `references/du-lieu.md`: ý nghĩa từng trường, trạng thái kiểm chứng, phạm vi kỳ. Đọc khi gặp trường lạ hoặc số trông bất thường.
- `references/chi-so.md`: cách tính tăng trưởng, biên, ROE, ROA, trung vị; khi nào để trống. Đọc trước khi diễn giải bất kỳ tỷ số nào.
- `references/tuan-thu.md`: giới hạn pháp lý khi viết về cổ phiếu ở Việt Nam. Đọc trước khi viết kết luận.
- `references/trinh-bay.md`: cách viết số, dẫn nguồn, khung cuối báo cáo.

## Ba quy tắc không đổi

1. **Chỉ dùng số script trả về.** Thiếu số thì ghi "Data API chưa có", không ước đoán và không lấy số từ trí nhớ. Người đọc dùng số này để ra quyết định tiền bạc.
2. **Mỗi số có kỳ, đơn vị, phạm vi (hợp nhất hay riêng) và link `document_url`.** BCTC `needs_review` phải nói rõ.
3. **Không khuyến nghị mua, bán, nắm giữ, không giá mục tiêu, không dự báo giá.** Luật Chứng khoán coi khuyến nghị là tư vấn đầu tư, cần giấy phép. Mô tả số liệu và đặt cạnh trung vị thì được.
