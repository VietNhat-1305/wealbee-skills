---
name: wealbee-peer-compare
description: Side-by-side comparison of 2 to 10 Vietnamese listed companies from Wealbee verified quarterly statements. Revenue and parent-company profit with growth, margins, ROE/ROA, leverage, health score and verification status, aligned on the same period, placed against the median of their company type, with a CSV for spreadsheets. Use it whenever the user names several tickers or a peer group, such as "so sánh VCB, BID, CTG", "MWG với FRT ai lãi hơn", "so sánh các ngân hàng quốc doanh quý 3", "compare HPG HSG NKG" or "đặt 4 công ty chứng khoán cạnh nhau". It describes differences and never ranks which stock to buy.
---
> Ví dụ đầu ra: [examples/wealbee-peer-compare-ngan-hang-20261125/COMPARISON.md](../../examples/wealbee-peer-compare-ngan-hang-20261125/COMPARISON.md)

# So sánh nhiều doanh nghiệp

Đặt số của 2–10 công ty cạnh nhau trên cùng một kỳ, giải thích khác biệt lớn và đặt cả nhóm cạnh mặt bằng chung. Mục tiêu là người đọc thấy rõ khác nhau ở đâu và vì sao có thể khác, không phải "mã nào tốt hơn".

## Chuẩn bị

- Khoá Wealbee (xem `../wealbee-data/SKILL.md`). `W` = `python3 <thư mục skill này>/../wealbee-data/scripts/wealbee.py` (ghép từ đường dẫn tuyệt đối của thư mục skill, vì lệnh chạy ở thư mục làm việc của người dùng).
- Người dùng cho: danh sách mã (hoặc tên nhóm, VD "ngân hàng quốc doanh" thì xác nhận danh sách trước khi chạy), kỳ (mặc định mới nhất).
- Đọc `../wealbee-data/references/chi-so.md` và `../wealbee-data/references/tuan-thu.md`.

## Quy trình

1. **Chuẩn hoá danh sách.** Tên công ty thì `W search`. Nhiều loại hình lẫn nhau (VD ngân hàng với doanh nghiệp thường) thì báo người dùng: số đọc được nhưng tỷ số không so trực tiếp được.
2. **Lấy số.** `W compare <MÃ…> [--period <kỳ>]`. Không chỉ định kỳ mà các mã khác kỳ: chạy lại với `--period` là kỳ chung mới nhất, và ghi rõ.
3. **Mặt bằng.** Với mỗi loại hình có trong nhóm: `W benchmark --industry <loại> --period <kỳ>`.
4. **Xu hướng (khi nhóm từ 2–5 mã).** `W trend <MÃ>` cho từng mã để thêm cột lợi nhuận công ty mẹ 4 quý gần nhất.
5. **Viết** `COMPARISON.md` và `compare.csv`; lưu JSON vào `evidence/`.

## Đầu ra

```
wealbee-peer-compare-<tên-nhóm-hoặc-các-mã>-<yyyymmdd>/
├── COMPARISON.md
├── compare.csv          (một dòng mỗi mã, cột như bảng chính, số dạng 1234.5 để mở bằng Excel)
└── evidence/ (01-compare.json, 02-benchmark-<loại>.json, 03-trend-<MÃ>.json …)
```

Khuôn `COMPARISON.md`:

```markdown
# <Nhóm> <kỳ>: <kết luận một câu về khác biệt lớn nhất, bằng số>

<n> mã · BCTC <kỳ> · số liệu lấy ngày <dd/mm/yyyy>

## Bảng so sánh
| Mã | Lợi nhuận công ty mẹ quý (tỷ đồng) | So với cùng kỳ | ROE quy năm | ROA quy năm | Nợ phải trả / vốn chủ (lần) | Trạng thái |
(thêm doanh thu, biên gộp, biên ròng nếu là doanh nghiệp thường; dòng cuối: trung vị cùng loại hình)
Sắp theo thứ tự chữ cái của mã, để bảng không đọc thành bảng xếp hạng.

## Khác biệt đáng chú ý
(3–5 gạch đầu dòng: khác ở đâu, lớn bao nhiêu, lý do có thể từ dữ liệu — quy mô, cơ cấu vốn, mùa vụ; lý do không có trong dữ liệu thì viết là câu hỏi)

## Xu hướng 4 quý
(bảng mã × quý, lợi nhuận công ty mẹ)

## Lưu ý khi so
(khác loại hình, khác kỳ, needs_review, missing_fields, ROE khác roe_basis)

## Nguồn
[S1] … một dòng mỗi file BCTC
Thông tin tham khảo, không phải khuyến nghị đầu tư.
```

## Mẹo

- Không đặt tên cột "Hạng", không tô màu "tốt/xấu", không viết "dẫn đầu" hay "kém nhất".
- Ngân hàng: so ROE, ROA, tăng trưởng lợi nhuận, quy mô tổng tài sản; nợ/vốn chủ 8–13 lần là của mô hình ngân hàng.
- Hai mã khác `roe_basis` (một mã có vốn chủ công ty mẹ, một mã không): ghi chú dưới bảng.
- Người dùng hỏi "nên chọn mã nào": làm theo mục cùng tên trong `tuan-thu.md`.
