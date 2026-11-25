---
name: wealbee-fact-check
description: Fact-checks numbers and claims about Vietnamese listed companies against Wealbee verified financial statements and source PDFs. Takes a sentence, a paragraph, a draft article, a broker note or a social post, extracts every checkable claim (revenue, profit, growth rates, margins, ROE, debt, dates), recomputes it from filed data, and returns a table of Đúng / Sai / Không kiểm được with the corrected figure and the PDF link. Use it whenever the user asks "số này đúng không", "kiểm tra bài viết này", "check lại số liệu trong bài", "VNM lãi 3.000 tỷ quý 3 có đúng không", "verify these earnings numbers", or before publishing any content that quotes company financials. It also catches percentage vs percentage-point errors and wrong comparison periods.
---
> Ví dụ đầu ra: chạy `wealbee-fact-check` với một đoạn văn có số liệu BCTC, kết quả có khuôn như mục Đầu ra.

# Kiểm chứng số liệu và nhận định

Người viết hay sai ở 4 chỗ: nhầm kỳ, nhầm đơn vị, nhầm % với điểm phần trăm, và lấy lợi nhuận sau thuế thay cho lợi nhuận công ty mẹ. Skill này đối chiếu từng khẳng định với số liệu BCTC đã kiểm chứng và file gốc, rồi ghi rõ đúng, sai hay chưa kiểm được.

## Chuẩn bị

- Khoá Wealbee (xem `../wealbee-data/SKILL.md`). `W` = `python3 <thư mục skill này>/../wealbee-data/scripts/wealbee.py` (ghép từ đường dẫn tuyệt đối của thư mục skill, vì lệnh chạy ở thư mục làm việc của người dùng).
- Người dùng cho: văn bản cần kiểm (dán vào hoặc đường dẫn file).
- Đọc `../wealbee-data/references/chi-so.md` để tính lại tăng trưởng và tỷ số đúng cách.

## Quy trình

1. **Tách khẳng định.** Đọc văn bản, liệt kê mọi câu có thể kiểm: số tiền, tỷ lệ, so sánh, ngày, xếp hạng, quan hệ nhân quả có số. Mỗi khẳng định ghi: mã, chỉ tiêu, kỳ, giá trị, đơn vị, câu gốc.
2. **Xác định kỳ và chỉ tiêu.** "Quý 3" mà không ghi năm thì lấy theo ngữ cảnh và ghi giả định. "Lãi" không rõ thì kiểm cả lợi nhuận sau thuế và lợi nhuận công ty mẹ.
3. **Lấy số.** `W summary <MÃ> --period <kỳ>` cho từng (mã, kỳ). Cần dòng chi tiết thì `W statement <MÃ>.<kỳ>`.
4. **Tính lại.** Tăng trưởng, biên, ROE theo `chi-so.md`. Sai số làm tròn ±0,1 tỷ đồng hoặc ±0,1 điểm phần trăm vẫn tính là đúng.
5. **Kết luận từng dòng:** `Đúng` / `Sai` (kèm số đúng) / `Gần đúng` (lệch do làm tròn hoặc khác phạm vi hợp nhất, riêng) / `Không kiểm được` (chỉ tiêu Data API chưa có, kỳ ngoài `coverage`, hoặc không phải số liệu BCTC).
6. **Viết** `FACTCHECK.md`; nếu người dùng đưa file nháp thì thêm `FIXED.md` là bản đã sửa số (chỉ sửa số, giữ nguyên câu chữ khác). Lưu JSON vào `evidence/`.

## Đầu ra

```
wealbee-fact-check-<chủ-đề>-<yyyymmdd>/
├── FACTCHECK.md
├── FIXED.md          (chỉ khi có bản nháp)
└── evidence/ (01-summary-<MÃ>-<kỳ>.json …)
```

Khuôn `FACTCHECK.md`:

```markdown
# Kiểm chứng: <n> khẳng định, <đúng> đúng, <sai> sai, <không kiểm được> chưa kiểm được

| # | Câu gốc | Kết quả | Số theo BCTC | Nguồn |
|---|---|---|---|---|
| 1 | "VNM lãi 3.000 tỷ quý 3/2026" | Sai | Lợi nhuận công ty mẹ quý 3/2026: 2.964,2 tỷ đồng (hợp nhất) | [S1] |

## Lỗi hay gặp trong văn bản này
(nhầm kỳ, nhầm % với điểm phần trăm, nhầm lợi nhuận sau thuế với lợi nhuận công ty mẹ… chỉ nêu lỗi có thật)

## Không kiểm được
(vì sao: chỉ tiêu chưa có, kỳ chưa có, không phải số liệu BCTC)

## Nguồn
Số liệu: Wealbee Data API, lấy ngày <dd/mm/yyyy>.
```

## Mẹo

- Nhận định ("cổ phiếu rẻ", "triển vọng tốt") không phải khẳng định kiểm được bằng BCTC; xếp vào "Không kiểm được" và ghi lý do. Nhận định mang tính khuyến nghị thì nhắc giới hạn trong `../wealbee-data/references/tuan-thu.md`.
- BCTC `needs_review` hay đã có phiên bản mới: ghi rõ số đang dùng là phiên bản nào; số người viết lấy từ phiên bản cũ thì nêu (`W versions`).
- "Tăng 200%" là gấp 3 lần; "từ 20% lên 22%" là tăng 2 điểm phần trăm.
