---
name: wealbee-news-digest
description: Digest of Vietnamese financial news from Wealbee, where each item is one event clustered from many outlets with source counts, official sources, sentiment and Wealbee's analysis of where outlets agree and disagree. Builds a dated brief for a ticker, a category (company, industry, macro, market, commodity) or the whole market over N days, separating announced facts from outlets' opinions. Use it when the user asks "tin về HPG tuần này", "có tin gì mới về ngân hàng", "tóm tắt tin vĩ mô 3 ngày qua", "các báo nói gì về VNM", "news digest for FPT" or wants to know whether a headline is confirmed by several outlets. For financial statements use wealbee-snapshot or wealbee-earnings-review instead.
---
> Ví dụ đầu ra: chạy `wealbee-news-digest` cho một mã hoặc một chủ đề, kết quả có khuôn như mục Đầu ra.

# Điểm tin theo mã hoặc chủ đề

Mỗi tin trong Wealbee là một sự kiện đã gom nhiều bài báo. Skill này biến danh sách đó thành bản tin ngắn: chuyện gì đã xảy ra, bao nhiêu nguồn, có nguồn chính thức không, các báo nói giống và khác nhau ở đâu.

## Chuẩn bị

- Khoá Wealbee (xem `../wealbee-data/SKILL.md`). `W` = `python3 <thư mục skill này>/../wealbee-data/scripts/wealbee.py` (ghép từ đường dẫn tuyệt đối của thư mục skill, vì lệnh chạy ở thư mục làm việc của người dùng).
- Người dùng cho: mã, hoặc chủ đề (`company`, `industry`, `macro`, `market`, `commodity`), và số ngày (mặc định 7).

## Quy trình

1. **Danh sách.** `W news [--ticker <MÃ>] [--category <chủ đề>] --days <N> --limit 50`. Có `next_cursor` mà cần thêm thì gọi lại với `--since` là thời điểm tin cũ nhất đã lấy.
2. **Chọn tin chính.** Sắp theo số nguồn (`source_count`), rồi nguồn chính thức (`official_source_count`). Lấy 5–8 tin.
3. **Đọc sâu.** Với từng tin chính: `W news-detail <id>`. Lấy các bài gốc (tên báo, ngày, link), điểm đồng thuận, điểm khác biệt, số liệu nêu trong tin.
4. **Gắn số liệu nếu có.** Tin về kết quả kinh doanh của một mã: `W summary <MÃ>` để đặt số đã kiểm chứng cạnh số báo đưa; lệch nhau thì ghi rõ cả hai.
5. **Viết** `NEWS.md`; lưu JSON vào `evidence/`.

## Đầu ra

```
wealbee-news-digest-<mã-hoặc-chủ-đề>-<yyyymmdd>/
├── NEWS.md
└── evidence/ (01-news.json, 02-detail-<id>.json …)
```

Khuôn `NEWS.md`:

```markdown
# Tin <mã/chủ đề>, <N> ngày đến <dd/mm/yyyy>: <một câu nêu sự kiện có nhiều nguồn nhất>

<tổng số tin> tin · <tổng số bài gốc> bài từ <số báo> báo

## <Tiêu đề tin 1>
<ngày> · <số nguồn> nguồn, <số nguồn chính thức> chính thức · <đang diễn biến / đã xong>
- **Đã công bố:** <dữ kiện, có số và ngày>
- **Các báo giống nhau:** …
- **Các báo khác nhau:** <báo A nói …, báo B nói …>
- **Chưa rõ:** …
Nguồn: [Báo A](link) · [Báo B](link)

(lặp cho 5–8 tin)

## Các tin khác
| Ngày | Tiêu đề | Số nguồn |

Số liệu: Wealbee Data API (tin gom cụm từ nhiều báo). Thông tin tham khảo, không phải khuyến nghị đầu tư.
```

## Mẹo

- Tách rõ dữ kiện đã công bố với nhận định của báo ("dự kiến", "chuyên gia cho rằng"). Không thêm nhận định của chính mình về tác động lên giá.
- Tin chỉ 1 nguồn và không có nguồn chính thức: ghi "mới có 1 nguồn".
- Sắc thái (`sentiment`) là của bài báo, không phải đánh giá của Wealbee về cổ phiếu.
