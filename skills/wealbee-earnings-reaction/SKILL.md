---
name: wealbee-earnings-reaction
description: Measures how a Vietnamese stock's price moved after each quarterly financial statement (BCTC) release, using Wealbee filing dates and public daily prices adjusted for dividends and splits. Gives the return from the last close before the market could react to 1, 5, 10 and 20 sessions later and to today, against the exchange index (VN-Index, HNX-Index, UPCOM-Index). Also backtests releases across many tickers and quarters as a simple event study, grouped by parent-company profit growth, to show what happened after strong and weak results. Use it when the user asks "từ lúc ra BCTC đến giờ VNM tăng bao nhiêu %", "giá phản ứng thế nào sau BCTC quý 3", "backtest mỗi lần công bố BCTC", "cổ phiếu có tăng sau khi báo lãi không", "post-earnings drift Vietnam", or wants insight on price behaviour around earnings. It reports history only and never forecasts prices or says what to buy.
---
> Ví dụ đầu ra: [examples/wealbee-earnings-reaction-vn30-20261126/REACTION.md](../../examples/wealbee-earnings-reaction-vn30-20261126/REACTION.md)

# Phản ứng giá quanh ngày công bố BCTC

Skill trả lời hai câu hỏi bằng số lịch sử. Thứ nhất, từ lúc một mã công bố BCTC đến nay, giá đã đổi bao nhiêu so với chỉ số. Thứ hai, qua nhiều lần công bố của nhiều mã, giá thường phản ứng ra sao sau kết quả tốt và kết quả xấu. Kết quả là thống kê đã xảy ra, không phải dự báo.

## Chuẩn bị

- Khoá Wealbee (xem `../wealbee-data/SKILL.md`). `W` = `python3 <thư mục skill này>/../wealbee-data/scripts/wealbee.py` (ghép từ đường dẫn tuyệt đối của thư mục skill, vì lệnh chạy ở thư mục làm việc của người dùng).
- Giá lấy từ nguồn công khai, không chính thức: VNDirect, dự phòng DNSE. Đây là giá đóng cửa ngày, đơn vị nghìn đồng, đã điều chỉnh cổ tức và chia tách, nên lợi suất đã gồm cổ tức. Người dùng có file giá riêng thì đặt `WEALBEE_PRICE_CSV_DIR=<thư mục>`, mỗi mã một file `<MÃ>.csv` với 2 cột `date,close`.
- Đọc `../wealbee-data/references/tuan-thu.md` trước khi viết phần nhận xét: phần này dễ trượt sang dự báo hay gợi ý chiến lược mua bán.

## Hai lệnh chính

| Câu hỏi | Lệnh |
|---|---|
| Một mã: từ lúc công bố đến nay giá đổi bao nhiêu | `W reaction <MÃ>` (kỳ mới nhất), `--period 2026Q3`, hoặc `--all` cho mọi kỳ có dữ liệu |
| Nhiều mã: backtest phản ứng giá | `W event-study --period 2026Q1 2026Q2 2026Q3 --tickers VNM,FPT,HPG,...` hoặc `--industry corporate --limit 40` (40 doanh nghiệp có tổng tài sản lớn nhất) |

`W prices <MÃ> --from YYYY-MM-DD` xem giá thô khi cần kiểm một phiên cụ thể.

## Quy trình

1. **Phạm vi.** Một mã: mặc định `--all` để thấy mọi lần công bố. Backtest: dùng danh sách người dùng đưa; không có thì hỏi lại, hoặc gợi ý nhóm VN30 hay `--industry corporate --limit 40`, qua mọi kỳ trong `coverage`.
2. **Chạy lệnh**, lưu JSON vào `evidence/`. Backtest 30 mã × 3 kỳ mất vài phút vì phải tải giá từng mã.
3. **Kiểm ngày công bố** (`release.source`). Trường này quyết định độ tin của toàn bộ kết quả:
   - `issuer_release_date`: ngày doanh nghiệp công bố, tin cậy nhất.
   - `detected_at`: lúc Wealbee phát hiện file, có giờ; công bố sau 15:00 thì phiên phản ứng đầu tiên là phiên kế tiếp. Wealbee có thể phát hiện muộn, nên script lấy ngày sớm nhất giữa các nguồn. `release.after_deadline = true` (danh sách `release_after_deadline` trong backtest) là ngày muộn hơn hạn luật: kiểm lại hoặc loại khỏi mẫu, và ghi rõ.
   - `document_url`: ngày đọc từ tên file BCTC, khá tin cậy nhưng vẫn là ước tính.
   - `legal_deadline`: ước tính theo hạn công bố (20 ngày sau cuối quý, 30 ngày với BCTC hợp nhất). Doanh nghiệp có thể công bố sớm hơn vài ngày, nên phản ứng 1 phiên gần như vô nghĩa với nhóm này.
   Ghi tỷ lệ từng loại ngày (`release_date_sources`) trong báo cáo. Phần lớn là ước tính thì nói rõ, và đọc cửa sổ 10–20 phiên thay cho 1 phiên.
4. **Đọc kết quả một mã.** Lập bảng kỳ × cửa sổ: lợi suất của mã, của chỉ số, chênh lệch (`excess_pct`). Đặt cạnh tăng trưởng lợi nhuận công ty mẹ của kỳ đó (`net_profit_parent_yoy_pct`). Muốn thêm bối cảnh thì chạy `W summary <MÃ> --period <kỳ>` và `W news --ticker <MÃ> --since <ngày công bố>`.
5. **Đọc backtest.** Bảng nhóm × cửa sổ, mỗi ô có số sự kiện, chênh lệch trung bình, trung vị, % số lần vượt chỉ số. Chỉ nêu một khác biệt giữa các nhóm khi:
   - mỗi nhóm có từ 10 sự kiện;
   - trung bình và trung vị cùng chiều. Ngược chiều nghĩa là vài sự kiện cực đoan kéo trung bình; tìm chúng trong `events` và nêu tên;
   - khác biệt lặp lại ở ít nhất 2 cửa sổ hoặc 2 kỳ. Kiểm từng kỳ bằng cách chạy riêng từng `--period`.
   Không đạt 3 điều trên thì viết là "chưa thấy khác biệt rõ trên mẫu này".
6. **Viết** `REACTION.md` theo khuôn bên dưới.

## Đầu ra

```
wealbee-earnings-reaction-<mã-hoặc-nhóm>-<yyyymmdd>/
├── REACTION.md
├── events.csv          (backtest: một dòng mỗi lần công bố)
└── evidence/ (reaction-<MÃ>.json, event-study.json …)
```

Khuôn `REACTION.md`:

```markdown
# <Mã/nhóm>: <một câu kết quả chính bằng số, VD "sau 20 phiên, nhóm lãi tăng trên 20% vượt VN-Index trung bình 2,1 điểm %">

<phạm vi: n lần công bố, mã, kỳ> · giá đến <dd/mm/yyyy> · ngày công bố: <a> ngày thật, <b> từ tên file, <c> ước tính theo hạn luật

## Từ lúc công bố đến nay          (khi có một mã)
| Kỳ | Ngày công bố (nguồn) | Lợi nhuận công ty mẹ so với cùng kỳ | 1 phiên | 5 phiên | 20 phiên | Đến nay | Đến nay so với chỉ số |

## Backtest theo nhóm kết quả      (khi có nhiều mã)
| Nhóm | Số lần | 1 phiên | 5 phiên | 10 phiên | 20 phiên | % lần vượt chỉ số (20 phiên) |
(mỗi ô: chênh lệch trung bình so với chỉ số, trung vị trong ngoặc)

## Điều thấy được
(2–4 ý, mỗi ý có số và cỡ mẫu, chỉ nêu khác biệt đạt điều kiện ở bước 5; các sự kiện cực đoan nêu tên)

## Giới hạn
(cỡ mẫu, số ngày công bố ước tính, nguồn giá không chính thức, chưa điều chỉnh rủi ro/beta, không xét kỳ vọng thị trường trước ngày công bố)

## Nguồn
Ngày công bố và số liệu BCTC: Wealbee Data API, lấy ngày <dd/mm/yyyy>. Giá: <nguồn>, đã điều chỉnh cổ tức. Thống kê lịch sử, không dự báo giá, không phải khuyến nghị đầu tư.
```

## Đọc số cho đúng

- Lợi suất tính từ giá đóng cửa ngay trước phiên đầu tiên thị trường phản ứng được. Đó là giá đã điều chỉnh, nên có thể khác giá niêm yết cũ người dùng nhớ.
- `excess_pct` là lợi suất mã trừ lợi suất chỉ số sàn cùng khoảng. Chỉ số này chưa điều chỉnh rủi ro: cổ phiếu biến động mạnh sẽ có chênh lệch lớn theo cả hai chiều.
- Thị trường có thể đã biết trước một phần kết quả, qua BCTC công ty mẹ, ước tính hay buổi gặp nhà đầu tư. Phản ứng nhỏ không có nghĩa thị trường không quan tâm.
- Các cửa sổ chồng lên nhau theo thời gian khi nhiều mã công bố cùng tuần, nên các sự kiện không độc lập. Một phiên thị trường chung giảm mạnh có thể kéo cả nhóm.

## Không viết

- "Mua sau khi BCTC tăng trưởng trên 20% sẽ lãi X%", "chiến lược", "tín hiệu mua", hay bất kỳ câu nào biến thống kê thành gợi ý giao dịch. Luật Chứng khoán coi khuyến nghị là tư vấn đầu tư, cần giấy phép.
- Câu dự báo: "giá sẽ", "dự kiến tăng". Viết: "trong 27 lần công bố của nhóm này trên mẫu, sau 20 phiên giá trung bình vượt VN-Index 1,8 điểm %; trung vị 0,9 điểm %".
