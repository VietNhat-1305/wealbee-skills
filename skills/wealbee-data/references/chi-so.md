# Cách tính chỉ số trong wealbee.py

Mọi tỷ số dưới đây do script tính từ số liệu BCTC, không phải số Wealbee công bố. Khi đưa vào báo cáo, ghi cách tính một lần.

## Tăng trưởng

- `quarter_growth_pct` = quý này / cùng quý năm trước − 1. `ytd_growth_pct` = luỹ kế / luỹ kế cùng kỳ − 1.
- **Để trống** khi thiếu số, kỳ so sánh bằng 0 hoặc lỗ, hay khi kỳ này lỗ. Lý do: "tăng 300%" từ một khoản lỗ không có nghĩa. Khi trống, mô tả bằng chữ: "chuyển từ lỗ 120 tỷ sang lãi 80 tỷ".
- Phân biệt % với **điểm phần trăm**: biên từ 20% lên 22% là tăng 2 điểm phần trăm, không phải tăng 2%.

## Biên lợi nhuận (chỉ doanh nghiệp thường)

- `gross_margin_quarter_pct` = lợi nhuận gộp / doanh thu thuần, riêng quý.
- `net_margin_quarter_pct` = lợi nhuận sau thuế / doanh thu thuần, riêng quý.
- Ngân hàng, chứng khoán, bảo hiểm không tính biên theo cách này vì mẫu BCTC khác.

## ROE, ROA

- Bình quân = (đầu năm + cuối kỳ) / 2. Đây là xấp xỉ số dư bình quân trong kỳ; ghi rõ khi viết.
- `roe_ytd_pct`: có `equity_parent` thì = lợi nhuận sau thuế của cổ đông công ty mẹ luỹ kế / bình quân vốn chủ của cổ đông công ty mẹ; không có thì = lợi nhuận sau thuế luỹ kế / bình quân tổng vốn chủ. `roe_basis` ghi cách đã dùng.
- `roa_ytd_pct` = lợi nhuận sau thuế luỹ kế / bình quân tổng tài sản.
- `_annualized_pct` = `_ytd_pct` × 12 / `months_ytd`. Quy năm giả định các quý còn lại giống các quý đã qua; nói rõ điều này, nhất là với doanh nghiệp có mùa vụ.

## Đòn bẩy

- `liabilities_to_equity` = nợ phải trả / tổng vốn chủ cuối kỳ. `borrowings_to_equity` = vay / vốn chủ. Thiếu số thì để trống, không coi là 0.
- Ngân hàng có nợ/vốn chủ khoảng 8–13 lần là bình thường của mô hình (tiền gửi là nợ); không so trực tiếp với doanh nghiệp thường.

## Trung vị cùng loại hình (benchmark)

- Tính trên mọi BCTC cùng `industry_type` và cùng kỳ, mặc định chỉ BCTC `verified`.
- Trả `n`, `p25`, `median`, `p75`; với một mã thì thêm `company` và `company_percentile` (% BCTC có giá trị nhỏ hơn hoặc bằng).
- `corporate` gồm mọi ngành, nên trung vị là mốc chung, không phải trung vị ngành. Viết "so với trung vị khoảng 900 doanh nghiệp thường đã kiểm chứng", không viết "so với ngành".
- `company_percentile` chỉ để định vị số liệu. Không biến nó thành xếp hạng nên mua.

## Xu hướng theo quý (trend)

- Số riêng từng quý. Các quý năm trước lấy từ cột cùng kỳ của BCTC năm sau, có thể đã điều chỉnh hồi tố so với BCTC gốc của chính quý đó.
- So với quý trước (`qoq`) chịu ảnh hưởng mùa vụ; so với cùng kỳ (`yoy`) thường có ý nghĩa hơn.
- Chênh lệch biên hay ROE giữa hai kỳ (điểm phần trăm) tính từ số chưa làm tròn rồi mới làm tròn 1 chữ số.
