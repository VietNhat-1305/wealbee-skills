# Cách trình bày báo cáo

## Số

- Kiểu Việt Nam: dấu chấm hàng nghìn, dấu phẩy thập phân: `8.559,9 tỷ đồng`, `16,0%`, `0,51 lần`.
- Đơn vị ghi một lần ở tiêu đề cột bảng (`Doanh thu quý (tỷ đồng)`), không lặp trong từng ô.
- Kỳ luôn đi kèm số: "quý 3/2026", "9 tháng 2026 (luỹ kế)", "cuối quý 3/2026".
- Làm tròn như script trả (1 chữ số thập phân cho tỷ đồng và %); không làm tròn thêm khiến số khác bảng gốc.

## Tên

- Lần đầu: tên công ty và mã, dùng tên thường gọi nếu có (`short_name`): "Vinamilk (VNM)". Sau đó dùng mã.
- Thuật ngữ lần đầu: tên tiếng Việt đầy đủ, viết tắt, tên tiếng Anh: "lợi nhuận trên vốn chủ sở hữu (ROE, Return on Equity)". Tra bằng lệnh `glossary`.

## Nguồn

- Gắn nhãn `[S1]`, `[S2]`… ngay sau số liệu; cuối báo cáo liệt kê nguồn: tên file hoặc trang, link `document_url`, ngày lấy.
- BCTC `needs_review`: ghi ngay cạnh số "(BCTC đang chờ Wealbee kiểm chứng lại)".
- Chỉ tiêu `derived` hoặc tỷ số do script tính: ghi "Wealbee tính" hoặc "tính từ BCTC".

## Bố cục

- Câu đầu là kết luận chính bằng số, không mở bằng "Báo cáo này trình bày…".
- Bảng cho số so sánh; gạch đầu dòng cho ý song song; câu dưới 25 từ, đoạn tối đa 3 câu.
- Không dùng tiếng lóng thị trường ("lái", "đu đỉnh", "cá mập", "tím").
- Mỗi báo cáo kết thúc bằng khung cuối trong `tuan-thu.md`.

## Thư mục kết quả

Mỗi skill ghi vào một thư mục `<tên-skill>-<đối-tượng>-<yyyymmdd>/` trong thư mục làm việc hiện tại: một file chính (VD `SNAPSHOT.md`), các file CSV nếu có bảng dài, và `evidence/` chứa JSON thô script trả về để người đọc kiểm lại.
- Viết bằng ngôn ngữ người dùng hỏi; mặc định tiếng Việt. Bản tiếng Anh vẫn giữ số theo kiểu Việt Nam trong bảng nguồn nếu trích nguyên văn, còn phần chữ dùng dấu chấm thập phân (VND bn).
