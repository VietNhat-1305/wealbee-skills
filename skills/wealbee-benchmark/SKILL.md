---
name: wealbee-benchmark
description: Earnings-season landscape for one company type and one quarter on Vietnamese exchanges, built from every Wealbee verified statement. Medians and quartiles of revenue growth, profit growth, margins, ROE, ROA and leverage across all banks, securities firms, insurers or ordinary companies; distribution tables; which tickers fall outside the middle half; and where specific tickers sit. Use it when the user asks about the whole market or a sector rather than one stock, such as "mùa BCTC quý 3 ngân hàng thế nào", "trung vị ROE doanh nghiệp niêm yết", "bao nhiêu công ty chứng khoán lãi tăng", "mặt bằng biên lợi nhuận quý này", "earnings season overview Vietnam banks", or needs an objective yardstick instead of an opinion like "ROE 15% là tốt".
---
> Ví dụ đầu ra: chạy `wealbee-benchmark` cho một loại hình và một kỳ, kết quả có khuôn như mục Đầu ra.

# Mặt bằng mùa BCTC theo loại hình

Trả lời "cả nhóm đang thế nào" bằng phân phối số liệu của mọi BCTC đã kiểm chứng: trung vị, khoảng giữa (p25–p75), bao nhiêu công ty tăng trưởng, và các mã cụ thể nằm ở đâu.

## Chuẩn bị

- Khoá Wealbee (xem `../wealbee-data/SKILL.md`). `W` = `python3 <thư mục skill này>/../wealbee-data/scripts/wealbee.py` (ghép từ đường dẫn tuyệt đối của thư mục skill, vì lệnh chạy ở thư mục làm việc của người dùng).
- Người dùng cho: loại hình (`corporate`, `bank`, `securities`, `insurance`) và kỳ; tuỳ chọn vài mã cần đặt vào phân phối.
- Lần đầu mỗi kỳ, `corporate` cần tải khoảng 1.000 BCTC (khoảng 10 lượt gọi API); kết quả đệm 6 giờ trong `~/.cache/wealbee-skills`.

## Quy trình

1. **Phân phối.** `W benchmark --industry <loại> --period <kỳ>`. Mặc định chỉ BCTC `verified`; người dùng muốn tính cả `needs_review` thì thêm `--all-statuses` và ghi rõ.
2. **Danh sách đầy đủ (để đếm và lập bảng).** `W compare` nhận tối đa 10 mã, nên với phân phối cả nhóm, đọc file đệm `~/.cache/wealbee-skills/bctc-<kỳ>-<loại>-verified.json` (danh sách BCTC nguyên dạng) và tính bằng chính hàm `tom_tat` của script:
   ```bash
   python3 -c "import json,sys; sys.path.insert(0,'../wealbee-data/scripts'); import wealbee as w; \
   ds=[w.tom_tat(s) for s in json.load(open('$HOME/.cache/wealbee-skills/bctc-<kỳ>-<loại>-verified.json'))]; \
   print(json.dumps([{'ticker':g['ticker'],**g['ratios'],'np_growth':(g['income_statement'].get('net_profit_parent') or {}).get('quarter_growth_pct')} for g in ds],ensure_ascii=False))" > evidence/02-all.json
   ```
   Từ đó: số công ty có lợi nhuận tăng hay giảm so với cùng kỳ, số công ty lỗ, nhóm ngoài p25–p75 của từng chỉ số.
3. **Các mã người dùng nêu.** `W benchmark --ticker <MÃ> --period <kỳ>` cho từng mã.
4. **Viết** `BENCHMARK.md` và `distribution.csv` (một dòng mỗi BCTC); lưu JSON vào `evidence/`.

## Đầu ra

```
wealbee-benchmark-<loại>-<kỳ>-<yyyymmdd>/
├── BENCHMARK.md
├── distribution.csv
└── evidence/ (01-benchmark.json, 02-all.json, 03-<MÃ>.json …)
```

Khuôn `BENCHMARK.md`:

```markdown
# <Loại hình> <kỳ>: <kết luận một câu, VD "trung vị lợi nhuận tăng 10,0%, 18/26 ngân hàng lãi tăng">

<n> BCTC đã kiểm chứng · số liệu lấy ngày <dd/mm/yyyy>

## Phân phối
| Chỉ số | p25 | Trung vị | p75 | Số BCTC |

## Tăng hay giảm
(số công ty lợi nhuận tăng, giảm, lỗ; so với cùng kỳ)

## Ngoài khoảng giữa
(với 2–3 chỉ số chính: các mã trên p75 và dưới p25, sắp theo mã, kèm giá trị; không gọi là "top" hay "đáng mua")

## Các mã được hỏi
(mỗi mã: giá trị và vị trí phần trăm của từng chỉ số)

## Cách hiểu đúng
(mốc chung cho mọi ngành khi là corporate; quy năm; needs_review bị loại; missing_fields)

## Nguồn
Thông tin tham khảo, không phải khuyến nghị đầu tư.
```

## Mẹo

- Phân phối lệch: dùng trung vị, không dùng trung bình; vài công ty tăng trưởng hàng nghìn % làm trung bình vô nghĩa.
- `corporate` gồm mọi ngành. Người dùng hỏi một ngành cụ thể (VD thép) thì nói rõ Data API chưa phân ngành chi tiết, và gợi ý dùng `wealbee-peer-compare` với danh sách mã của ngành đó.
