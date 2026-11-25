---
name: wealbee-snapshot
description: One-page snapshot of a Vietnamese listed stock from Wealbee verified data. Latest quarterly results in VND billion, growth versus the same quarter last year, margins, ROE/ROA, leverage, a 6-quarter trend, position against the median of all companies of the same type, recent multi-outlet news, and the source PDF for every number. Use it whenever the user asks about one ticker in general terms, such as "phân tích nhanh VNM", "Hoà Phát dạo này thế nào", "tóm tắt cổ phiếu FPT", "snapshot of MWG" or "VCB quý này ra sao", or names a company and wants an overview rather than a deep read of one statement (use wealbee-earnings-review for that) or a side-by-side of several tickers (use wealbee-peer-compare).
---
> Ví dụ đầu ra: [examples/wealbee-snapshot-vnm-20261125/SNAPSHOT.md](../../examples/wealbee-snapshot-vnm-20261125/SNAPSHOT.md)

# Phân tích nhanh một mã

Một trang trả lời "mã này đang thế nào" bằng số đã kiểm chứng: kết quả quý gần nhất, xu hướng, vị trí so với mặt bằng, tin gần đây. Người đọc xem trong 2 phút và biết số nào cần đọc kỹ, không có khuyến nghị mua bán.

## Chuẩn bị

- Khoá Wealbee đã cài (xem `../wealbee-data/SKILL.md`, mục Cài khoá). Lệnh dưới đây viết tắt `W` = `python3 <thư mục skill này>/../wealbee-data/scripts/wealbee.py` (ghép từ đường dẫn tuyệt đối của thư mục skill, vì lệnh chạy ở thư mục làm việc của người dùng).
- Người dùng cho: mã hoặc tên công ty; kỳ (mặc định kỳ mới nhất).
- Đọc `../wealbee-data/references/chi-so.md` và `../wealbee-data/references/tuan-thu.md` trước khi viết phần diễn giải.

## Quy trình

1. **Xác định mã.** Người dùng nói tên (VD "Sữa Việt Nam") thì `W search <tên>`; nhiều kết quả thì hỏi lại. Ghi `short_name` để gọi tên thường dùng, và `coverage` để biết kỳ nào có dữ liệu.
2. **BCTC kỳ cần xem.** `W summary <MÃ> [--period <kỳ>]`. Ghi lại: kỳ, trạng thái (`verified` / `needs_review`), doanh thu và lợi nhuận công ty mẹ quý, tăng trưởng, biên (doanh nghiệp thường), ROE/ROA quy năm và `roe_basis`, nợ/vốn chủ, lưu chuyển tiền kinh doanh luỹ kế, phép kiểm không đạt, `missing_fields`, `document_url`.
3. **Xu hướng.** `W trend <MÃ>`. Lấy 6 quý gần nhất của doanh thu và lợi nhuận công ty mẹ, tăng trưởng so với cùng kỳ. Xác định hướng: tăng đều, giảm đều, hay đảo chiều ở quý nào.
4. **Mặt bằng.** `W benchmark --ticker <MÃ>`. Với mỗi chỉ số có `company_percentile`, ghi trung vị, p25, p75 và vị trí của mã.
5. **Tin gần đây.** `W news --ticker <MÃ> --days 30 --limit 10`. Lệnh này trả cả tin chỉ nhắc mã trong danh sách `tickers`; giữ tin có `primary_ticker` là mã đó hoặc có tên công ty trong tiêu đề, và đọc tiêu đề để loại tin gắn nhầm (VD "VNM" bị gắn cho bài nói về cả thị trường Việt Nam). Chọn tối đa 3 tin nhiều nguồn nhất; tin nào gắn với kết quả kinh doanh thì `W news-detail <id>` để lấy điểm các báo đưa giống và khác nhau.
6. **Viết `SNAPSHOT.md`** theo khuôn bên dưới. Lưu JSON thô của bước 2–5 vào `evidence/`.

## Đầu ra

```
wealbee-snapshot-<mã-thường>-<yyyymmdd>/
├── SNAPSHOT.md
└── evidence/
    ├── 01-summary.json
    ├── 02-trend.json
    ├── 03-benchmark.json
    └── 04-news.json
```

Khuôn `SNAPSHOT.md`:

```markdown
# <Tên thường gọi> (<MÃ>): <một câu kết luận bằng số, VD "lợi nhuận quý 3/2026 tăng 17,3%, biên ròng 16,0%">

<Sàn> · <loại hình> · BCTC <hợp nhất/riêng> <kỳ>, <trạng thái kiểm chứng> · số liệu lấy ngày <dd/mm/yyyy>

## Nhìn nhanh
| Chỉ số | <kỳ> | Cùng kỳ năm trước | Thay đổi | Trung vị cùng loại hình |
(doanh thu, lợi nhuận công ty mẹ, biên gộp, biên ròng, ROE quy năm, ROA quy năm, nợ phải trả / vốn chủ; bỏ dòng không có số)

## Xu hướng 6 quý
(bảng quý · doanh thu · lợi nhuận công ty mẹ · so với cùng kỳ; 1–2 câu đọc xu hướng)

## So với mặt bằng
(2–4 gạch đầu dòng: chỉ số nào nằm trên p75 hoặc dưới p25 của <n> BCTC cùng loại hình; nhắc 'corporate' là mốc chung mọi ngành)

## Điểm cần đọc kỹ
(chỉ các tín hiệu có thật trong dữ liệu: phép kiểm không đạt, dòng tiền kinh doanh âm, lợi nhuận tăng mạnh hơn doanh thu, BCTC needs_review, chỉ tiêu derived, missing_fields; viết như câu hỏi để kiểm, kèm trang PDF nếu có)

## Tin gần đây
(tối đa 3 tin: ngày, tiêu đề, số nguồn, điểm các báo nói khác nhau nếu có)

## Nguồn
[S1] BCTC <kỳ> — <document_url>
[S2] Wealbee Data API, lệnh trend/benchmark/news — lấy ngày <dd/mm/yyyy>

Số liệu: Wealbee Data API. Tỷ số ROE, ROA, trung vị do wealbee-skills tính từ BCTC (cách tính: ...). Thông tin tham khảo, không phải khuyến nghị đầu tư.
```

## Mẹo đọc số

- Lợi nhuận tăng nhanh hơn doanh thu nhiều lần: xem biên gộp có tăng không. Không tăng thì lợi nhuận có thể đến từ thu nhập tài chính hay khoản bất thường; ghi là điểm cần đọc thuyết minh.
- Dòng tiền kinh doanh luỹ kế âm trong khi có lãi: nêu như câu hỏi về phải thu, hàng tồn kho.
- Chênh lệch biên (điểm %) tính từ số chưa làm tròn: 41,36% − 41,63% là −0,3 điểm, không phải 41,4 − 41,6 = −0,2.
- Ngân hàng: không có doanh thu trong dữ liệu; dùng lợi nhuận, ROE, ROA, tổng tài sản. Đừng so nợ/vốn chủ của ngân hàng với doanh nghiệp thường.
- `percentile` cao không có nghĩa là "tốt để mua". Viết "ROE quy năm 31,6%, cao hơn 93% số BCTC doanh nghiệp thường quý này", không viết "ROE vượt trội".
- Người dùng hỏi "có nên mua không": làm theo mục cùng tên trong `../wealbee-data/references/tuan-thu.md`.
