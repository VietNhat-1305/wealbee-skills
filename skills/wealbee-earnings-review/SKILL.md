---
name: wealbee-earnings-review
description: Deep read of one quarterly financial statement (BCTC) of a Vietnamese listed company from Wealbee verified data. Walks income statement, balance sheet and cash flow line by line, checks Wealbee's automated reconciliation checks, statement versions and restatements, derived fields and the source PDF pages, then lists the questions a careful reader should verify in the notes. Use it when the user wants to really read one report, such as "đọc BCTC quý 3 của HPG", "phân tích báo cáo tài chính MWG quý này", "BCTC VNM có gì bất thường không", "review FPT Q3 2026 earnings" or "báo cáo tài chính có bị sửa không". Prefer wealbee-snapshot for a quick overview of a ticker and wealbee-peer-compare for several tickers.
---
> Ví dụ đầu ra: chạy `wealbee-earnings-review` cho một mã, kết quả có khuôn như mục Đầu ra.

# Đọc kỹ BCTC một quý

Không dừng ở "lãi tăng bao nhiêu %": đọc cả ba báo cáo, xem số khớp nhau không, xem Wealbee đã kiểm gì và BCTC có bị sửa không, rồi đưa ra danh sách câu hỏi cụ thể kèm trang PDF để người đọc tự kiểm.

## Chuẩn bị

- Khoá Wealbee (xem `../wealbee-data/SKILL.md`). `W` = `python3 <thư mục skill này>/../wealbee-data/scripts/wealbee.py` (ghép từ đường dẫn tuyệt đối của thư mục skill, vì lệnh chạy ở thư mục làm việc của người dùng).
- Người dùng cho: mã, kỳ (mặc định mới nhất).
- Đọc `../wealbee-data/references/du-lieu.md` (nghĩa từng trường, `checks`, `derived`) và `../wealbee-data/references/tuan-thu.md`.

## Quy trình

1. **Tóm tắt.** `W summary <MÃ> [--period <kỳ>]`. Ghi loại hình (mẫu BCTC khác nhau theo loại hình), trạng thái, `review_reasons`, `version`.
2. **Bản đầy đủ.** `W statement <MÃ>.<kỳ>`: lấy `checks` (mã phép kiểm, `difference`, `tolerance`), `derived`, `provenance.pages` (trang PDF của từng bảng), `original_unit`.
3. **Lịch sử sửa.** `W versions <MÃ>.<kỳ>`. Có hơn 1 phiên bản thì xem `reason` và `changes`; cần số trước khi sửa thì `W versions <MÃ>.<kỳ> --version <n>`.
4. **File gốc.** `W filings --ticker <MÃ> --period <kỳ>`: ngày công bố, lúc Wealbee phát hiện, mã băm, có bản thay thế (`superseded`) không.
5. **Bối cảnh.** `W trend <MÃ>` (4–6 quý) và `W benchmark --ticker <MÃ> --period <kỳ>`.
6. **Đọc theo khung bên dưới**, ghi mọi số kèm kỳ và trang PDF. Viết `EARNINGS.md`; lưu JSON của bước 1–5 vào `evidence/`.

## Khung đọc

**Kết quả kinh doanh**
- Doanh thu, lợi nhuận gộp, lợi nhuận sau thuế, lợi nhuận công ty mẹ: quý và luỹ kế, so với cùng kỳ.
- Biên gộp và biên ròng (doanh nghiệp thường): thay đổi bằng điểm phần trăm.
- Lợi nhuận công ty mẹ khác lợi nhuận sau thuế nhiều: phần của cổ đông không kiểm soát lớn, nêu ra.

**Bảng cân đối**
- Tổng tài sản, nợ phải trả, vay, vốn chủ: cuối kỳ so với đầu năm.
- Vay tăng nhanh hơn vốn chủ: đòn bẩy tăng.
- Có `equity_parent` và `non_controlling_interest` thì tách ra.

**Lưu chuyển tiền**
- Tiền từ hoạt động kinh doanh luỹ kế so với lợi nhuận sau thuế luỹ kế. Lãi mà tiền kinh doanh âm là câu hỏi số một.
- Đầu tư và tài chính: đang đầu tư mạnh, trả nợ hay đi vay thêm.

**Độ tin cậy của số**
- Phép kiểm không đạt: tên phép kiểm, chênh lệch, ý nghĩa (xem `du-lieu.md`).
- Chỉ tiêu `derived`: Wealbee tự tính vì BCTC không trình bày sẵn.
- Phiên bản: số đã bị sửa chưa, sửa gì, khi nào.
- `needs_review`: lý do.

## Đầu ra

```
wealbee-earnings-review-<mã>-<kỳ>-<yyyymmdd>/
├── EARNINGS.md
└── evidence/ (01-summary.json, 02-statement.json, 03-versions.json, 04-filings.json, 05-trend.json, 06-benchmark.json)
```

Khuôn `EARNINGS.md`:

```markdown
# BCTC <kỳ> của <Tên> (<MÃ>): <kết luận một câu bằng số>

<loại hình> · <hợp nhất/riêng> · <trạng thái>, phiên bản <n> · công bố <ngày>, Wealbee phát hiện <ngày> · file gốc [S1]

## Kết quả kinh doanh
(bảng: chỉ tiêu · quý · cùng kỳ · thay đổi · luỹ kế · cùng kỳ · thay đổi; 2–3 câu đọc)

## Bảng cân đối
(bảng cuối kỳ · đầu năm · thay đổi; 2 câu đọc)

## Lưu chuyển tiền
(bảng luỹ kế; 1–2 câu: tiền kinh doanh so với lợi nhuận)

## Độ tin cậy của số
(phép kiểm: <đạt>/<tổng>, liệt kê phép không đạt; derived; lịch sử phiên bản; needs_review)

## So với mặt bằng và xu hướng
(3–4 gạch đầu dòng từ trend và benchmark)

## Câu hỏi cần kiểm trong thuyết minh
1. <câu hỏi cụ thể> — xem trang <n> của file gốc [S1]
(3–6 câu, chỉ từ tín hiệu có trong dữ liệu)

## Nguồn
...
Thông tin tham khảo, không phải khuyến nghị đầu tư.
```

## Lưu ý

- Ngân hàng, chứng khoán, bảo hiểm: tên trường giống nhau nhưng khoản mục gốc theo mẫu BCTC của ngành. Nói rõ và dẫn trang gốc khi giải thích.
- Không suy diễn nguyên nhân ("do giá thép tăng") nếu dữ liệu và tin không nói. Thay bằng câu hỏi.
- Kỳ chưa có trong `coverage`: nói chưa có dữ liệu, không lấy số kỳ khác thay vào.
