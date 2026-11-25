---
name: wealbee-watchlist
description: Monitors a watchlist of Vietnamese tickers for what changed since a given time using Wealbee's change-event stream. New or restated financial statements (with what changed and why), withdrawn statements, and new or updated multi-outlet news, grouped per ticker into a short "what's new" brief. Use it when the user keeps a list of stocks and asks "có gì mới về VNM, HPG, FPT từ hôm qua", "danh mục của tôi tuần này có tin gì", "mã nào vừa ra BCTC", "BCTC nào bị sửa", "what changed for my watchlist since Monday", or wants a recurring morning check. It reports changes only and does not rate the holdings.
---
> Ví dụ đầu ra: chạy `wealbee-watchlist` với vài mã và một mốc thời gian, kết quả có khuôn như mục Đầu ra.

# Theo dõi thay đổi của danh mục

Người giữ danh mục cần biết "từ lần xem trước có gì mới". Luồng sự kiện của Wealbee ghi lại mỗi lần BCTC mới, BCTC được sửa hay bị rút, và tin mới. Skill này gom các sự kiện đó theo từng mã thành một bản tin ngắn.

## Chuẩn bị

- Khoá Wealbee (xem `../wealbee-data/SKILL.md`). `W` = `python3 <thư mục skill này>/../wealbee-data/scripts/wealbee.py` (ghép từ đường dẫn tuyệt đối của thư mục skill, vì lệnh chạy ở thư mục làm việc của người dùng).
- Người dùng cho: danh sách mã (tối đa khoảng 30), mốc thời gian (mặc định 24 giờ trước; viết dạng RFC 3339 có múi giờ +07:00).
- Lưu danh sách lần đầu vào `watchlist.txt` (mỗi dòng một mã) trong thư mục làm việc để lần sau dùng lại, nếu người dùng đồng ý.

## Quy trình

1. **Sự kiện.** Với từng mã: `W events --ticker <MÃ> --since <mốc> --limit 50`.
2. **BCTC mới hoặc được sửa** (`statement.updated`): `W summary <MÃ> --period <kỳ>`; có phiên bản trước thì `W versions <MÃ>.<kỳ>` để nêu thay đổi và lý do.
3. **BCTC bị rút** (`statement.withdrawn`): ghi kỳ và thời điểm; số của kỳ đó không còn dùng được cho tới khi có bản mới.
4. **Tin** (`news.published`, `news.updated`): `W news --ticker <MÃ> --since <mốc>`; tin nhiều nguồn thì `W news-detail <id>`.
5. **Viết** `WATCH.md`. Mã không có gì mới gom vào một dòng cuối. Lưu JSON vào `evidence/`.

## Đầu ra

```
wealbee-watchlist-<yyyymmdd-hhmm>/
├── WATCH.md
└── evidence/ (events-<MÃ>.json …)
```

Khuôn `WATCH.md`:

```markdown
# Danh mục <n> mã: <số mã có thay đổi> mã có thay đổi từ <mốc>

## <MÃ>
- **BCTC <kỳ> mới / được sửa (phiên bản <n>):** <lợi nhuận công ty mẹ, so với cùng kỳ; sửa gì, lý do> [S1]
- **Tin:** <tiêu đề> (<số nguồn> nguồn, <ngày>)

(lặp cho mã có thay đổi)

Không có thay đổi: <MÃ>, <MÃ>, …

Số liệu: Wealbee Data API, kiểm lúc <hh:mm dd/mm/yyyy>. Thông tin tham khảo, không phải khuyến nghị đầu tư.
```

## Mẹo

- Muốn chạy mỗi sáng: gợi ý người dùng đặt lịch (cron, launchd, hoặc tính năng lịch của Claude) gọi skill này với mốc là lần chạy trước.
- Không viết "nên bán", "nên giữ" cho mã có tin xấu; chỉ nêu điều đã xảy ra và điều cần kiểm.
