# Nhật ký thay đổi

Theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/) và [Semantic Versioning](https://semver.org/lang/vi/).

## [0.2.0] - 2026-11-26

### Thêm
- Skill `wealbee-earnings-reaction`: giá thay đổi bao nhiêu từ lúc công bố BCTC (sau 1, 5, 10, 20 phiên và đến nay), so với chỉ số sàn; backtest nhiều mã, nhiều kỳ theo nhóm tăng trưởng lợi nhuận công ty mẹ, kèm quy tắc chỉ nêu khác biệt đủ chắc.
- Lệnh `prices`, `reaction`, `event-study` trong `wealbee.py`. Giá đóng cửa ngày đã điều chỉnh từ nguồn công khai (VNDirect, dự phòng DNSE) hoặc file CSV riêng.
- Ngày công bố BCTC: lấy ngày sớm nhất giữa ngày doanh nghiệp công bố, lúc Wealbee phát hiện và ngày trong tên file; không có thì ước tính theo hạn luật; ngày muộn hơn hạn được gắn cờ.
- Ví dụ thật: 90 lần công bố BCTC của 30 mã VN30 năm 2026 và VNM từ lúc công bố đến nay. Eval cho skill mới.

## [0.1.1] - 2026-11-26

### Sửa
- ROE, ROA quy năm bị làm tròn hai lần: script làm tròn tỷ lệ luỹ kế rồi mới nhân 12/số tháng, nên có thể lệch 0,1 điểm (VD ROE CTG quý 3/2026 ra 21,7% thay vì 21,8%). Nay quy năm từ số chưa làm tròn. Trung vị và phân vị của lệnh `benchmark` cũng được tính lại.
- Ví dụ VNM và 5 ngân hàng cập nhật theo số đã sửa.

### Thêm
- Tài liệu dữ liệu: link PDF chặn công cụ tự động không có User-Agent; quý cùng kỳ chưa tách lợi nhuận công ty mẹ.

Lỗi làm tròn được chính skill `wealbee-fact-check` phát hiện khi kiểm chứng bài blog trong đợt dùng thử.

## [0.1.0] - 2026-11-26

### Thêm
- `wealbee-data`: skill nền tảng gồm script `wealbee.py` (13 lệnh, chỉ dùng thư viện chuẩn Python 3.9+) và 4 tài liệu tham chiếu: dữ liệu, cách tính chỉ số, tuân thủ pháp lý, cách trình bày.
- 8 skill phân tích: `wealbee-snapshot`, `wealbee-earnings-review`, `wealbee-peer-compare`, `wealbee-benchmark`, `wealbee-news-digest`, `wealbee-fact-check`, `wealbee-explain`, `wealbee-watchlist`.
- Lệnh `benchmark`: trung vị và p25–p75 của mọi BCTC cùng loại hình và kỳ, lưu đệm 6 giờ.
- Ví dụ thật: snapshot VNM và so sánh 5 ngân hàng, quý 3/2026.
- Eval cho `wealbee-snapshot`, `wealbee-fact-check`, `wealbee-peer-compare` theo định dạng `claude plugin eval`.
- Cài bằng plugin Claude Code (`.claude-plugin/`), CI kiểm cấu trúc skill, test script, quét khoá lộ.
