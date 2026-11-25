---
name: wealbee-explain
description: Explains a Vietnamese investing or accounting term (ROE, P/B, biên lợi nhuận gộp, nợ vay trên vốn chủ, lưu chuyển tiền kinh doanh, NIM, bảng cân đối kế toán…) using Wealbee's 490-term glossary plus a worked example computed from real filed numbers of listed companies and the market median, so the reader sees what the metric looks like in practice. Use it when the user asks "ROE là gì", "giải thích biên lợi nhuận bằng ví dụ thật", "nợ vay trên vốn chủ bao nhiêu là cao", "what is gross margin with a Vietnamese example", or wants beginner-friendly educational content, a glossary entry or a blog section grounded in real data instead of hypothetical numbers.
---
> Ví dụ đầu ra: chạy `wealbee-explain` cho một thuật ngữ, kết quả có khuôn như mục Đầu ra.

# Giải thích thuật ngữ bằng số thật

Định nghĩa trong sách đúng nhưng khó nhớ. Skill này lấy định nghĩa chuẩn từ từ điển Wealbee, rồi tính ví dụ bằng BCTC thật và đặt cạnh trung vị thị trường, để người mới thấy chỉ số đó trông thế nào ngoài đời.

## Chuẩn bị

- Khoá Wealbee cho phần ví dụ (xem `../wealbee-data/SKILL.md`); phần từ điển không cần khoá. `W` = `python3 <thư mục skill này>/../wealbee-data/scripts/wealbee.py` (ghép từ đường dẫn tuyệt đối của thư mục skill, vì lệnh chạy ở thư mục làm việc của người dùng).
- Người dùng cho: thuật ngữ; tuỳ chọn mã muốn làm ví dụ.

## Quy trình

1. **Định nghĩa.** `W glossary <thuật ngữ>`. Lấy định nghĩa, tên tiếng Anh, tên khác, ví dụ trong từ điển (thường là số giả định), thuật ngữ liên quan. Trang từ điển trên web: `https://wealbee.com/tu-dien/<thuật-ngữ-không-dấu>`.
2. **Chỉ số có trong dữ liệu không?** Script tính được: tăng trưởng doanh thu và lợi nhuận, biên gộp, biên ròng, ROE, ROA, nợ phải trả / vốn chủ, vay / vốn chủ; đọc được trực tiếp: các dòng KQKD, CĐKT, LCTT trong `du-lieu.md`. Thuật ngữ khác (P/E, P/B, cổ tức, NIM…) cần giá cổ phiếu hoặc chỉ tiêu Data API chưa có: dùng ví dụ giả định của từ điển, ghi rõ "giả định", và không bịa số.
3. **Ví dụ thật (khi tính được).** Chọn 2–3 mã khác nhau rõ (VD một doanh nghiệp thường, một ngân hàng) hoặc mã người dùng nêu: `W summary <MÃ>`. Viết phép tính từng bước bằng số tỷ đồng, đúng kỳ.
4. **Mặt bằng.** `W benchmark --industry <loại> --period <kỳ>` để có trung vị và khoảng giữa; giải thích vì sao ngân hàng và doanh nghiệp thường khác nhau ở chỉ số này.
5. **Viết** `EXPLAIN.md`; lưu JSON vào `evidence/`.

## Đầu ra

```
wealbee-explain-<thuật-ngữ>-<yyyymmdd>/
├── EXPLAIN.md
└── evidence/
```

Khuôn `EXPLAIN.md`:

```markdown
# <Thuật ngữ> là gì? <một câu trả lời thẳng>

**<Định nghĩa in đậm, một câu đứng riêng được>** (<tên tiếng Anh>)

## Công thức
(viết bằng chữ, có đơn vị; nêu cách tính bình quân và quy năm nếu có)

## Ví dụ bằng BCTC <kỳ>
(từng bước cho 2–3 mã, số tỷ đồng, nguồn [S1]…)

## Mặt bằng hiện tại
(trung vị và p25–p75 của <n> BCTC cùng loại hình; vì sao khác giữa các loại hình)

## Khi nào chỉ số này dễ hiểu sai
(3–4 gạch đầu dòng: mùa vụ, quy năm, vốn chủ nhỏ hoặc âm, lợi nhuận bất thường…)

## Thuật ngữ liên quan
(từ từ điển, kèm link trang từ điển Wealbee)

## Nguồn
Thông tin tham khảo, không phải khuyến nghị đầu tư.
```

## Mẹo

- Không đưa "mức tốt" theo ý kiến ("ROE trên 15% là tốt"). Đặt cạnh trung vị và giải thích vì sao khác.
- Ví dụ có mã thật không phải lời khen hay chê mã đó; chọn mã để minh hoạ cơ chế và ghi lý do chọn.
- Nội dung dùng làm bài blog: giữ văn phong trong `../wealbee-data/references/trinh-bay.md` (câu dưới 25 từ, đoạn tối đa 3 câu).
