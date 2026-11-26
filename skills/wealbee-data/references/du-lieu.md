# Dữ liệu Wealbee: các trường và ý nghĩa

## Phạm vi

- Doanh nghiệp niêm yết HOSE, HNX, UPCOM. Kỳ quý, viết `2026Q3` (nhãn hiển thị `Q3/2026`). Chưa có kỳ năm.
- Mỗi công ty có `coverage.first_period` và `coverage.latest_period`. Chỉ nói về các kỳ trong khoảng này; kỳ ngoài khoảng là **chưa có dữ liệu**, không phải bằng 0. `latest_period = null`: có trong danh bạ nhưng chưa có BCTC.
- `industry_type`: `corporate` (doanh nghiệp thường), `bank`, `securities`, `insurance`. Chưa có phân ngành chi tiết hơn.

## Một BCTC

- Số tiền nguyên dạng tính bằng **đồng**. Lệnh `summary`, `compare`, `trend`, `benchmark` đã đổi sang **tỷ đồng**.
- `income_statement`, `cash_flow`: `quarter` là riêng quý; `ytd` là luỹ kế từ đầu năm tài chính (`months_ytd` tháng); hậu tố `_prior_year` là cùng kỳ năm trước.
- `balance_sheet`: `end_of_period` cuối kỳ; `start_of_year` đầu năm tài chính.
- Tên trường:

| Trường | Nghĩa |
|---|---|
| `revenue` | Doanh thu thuần |
| `cost_of_sales` | Giá vốn |
| `gross_profit` | Lợi nhuận gộp (ngân hàng, chứng khoán, bảo hiểm: theo mẫu BCTC riêng của ngành, xem `derived`) |
| `net_profit` | Lợi nhuận sau thuế |
| `net_profit_parent` | Lợi nhuận sau thuế của cổ đông công ty mẹ |
| `total_assets` | Tổng tài sản |
| `total_liabilities` | Nợ phải trả |
| `borrowings` | Vay |
| `equity` | Vốn chủ sở hữu (gồm lợi ích cổ đông không kiểm soát) |
| `equity_parent` | Vốn chủ của cổ đông công ty mẹ (chưa có ở mọi BCTC) |
| `non_controlling_interest` | Lợi ích cổ đông không kiểm soát |
| `operating` / `investing` / `financing` | Lưu chuyển tiền từ hoạt động kinh doanh / đầu tư / tài chính |
| `net_change` | Lưu chuyển tiền thuần trong kỳ |

- `scope`: `consolidated` là hợp nhất.
- `status`: `verified` đã qua kiểm chứng; `needs_review` đang chờ xem lại, lý do ở `review_reasons`. Dùng số `needs_review` thì phải nói rõ.
- `checks`: phép kiểm tự động (cân đối tài sản cuối kỳ và đầu năm, cộng lưu chuyển tiền, khớp số tháng luỹ kế, đối chiếu chéo, đọc độc lập lần hai). Phép kiểm không đạt là chỗ cần đọc kỹ thuyết minh.
- `derived`: chỉ tiêu Wealbee tự tính vì BCTC gốc không trình bày sẵn (VD lợi nhuận gộp của công ty chứng khoán). Nói rõ khi dùng.
- `health_score`: điểm sức khoẻ tài chính Wealbee chấm (`value`/`max`); `missing_points` là phần chưa chấm được do thiếu dữ liệu.
- `version`: số lần BCTC được cập nhật. Lịch sử: lệnh `versions`. Số tại một thời điểm quá khứ: `statement … --as-of`.
- `provenance`: `document_url` file PDF gốc; `file_sha256` mã băm; `pages` trang chứa từng bảng; `detected_at` lúc Wealbee phát hiện file; `ir_url` trang quan hệ cổ đông.
- `missing_fields` (do script tính): chỉ tiêu Data API chưa có cho BCTC đó, VD doanh thu của ngân hàng.

## Tin và sự kiện

- Mỗi bản ghi tin là một **sự kiện gộp nhiều bài báo**: `source_count` số bài, `official_source_count` số nguồn chính thức, `sources` danh sách bài gốc, `sentiment` sắc thái, `status` (`developing` là đang diễn biến). Phân tích đồng thuận và khác biệt: lệnh `news-detail`.
- `events`: `statement.updated`, `statement.withdrawn`, `news.published`, `news.updated`.

## Giới hạn đã biết

- Doanh thu của ngân hàng phần lớn để trống; vài ngân hàng có số (VD MBB, TCB) nhưng định nghĩa chưa thống nhất, nên không so doanh thu giữa các ngân hàng. Dùng lợi nhuận, ROE, ROA và tổng tài sản.
- Chuỗi `trend` hiện chưa có quý 4/2025; quý năm 2025 lấy từ cột cùng kỳ của BCTC 2026. Nhiều BCTC quý 1/2026 đang `needs_review`.
- `news --ticker` trả cả tin chỉ nhắc mã trong `tickers`. Tin "về" mã là tin có `primary_ticker` đúng mã; vẫn đọc tiêu đề vì đôi khi mã bị gắn nhầm.
- `net_profit_parent.ytd_prior_year` chưa có, nên tăng trưởng luỹ kế của lợi nhuận công ty mẹ thường trống.
- `equity_parent` chưa có ở mọi BCTC; khi thiếu, ROE tính trên tổng vốn chủ (xem `roe_basis`).
- Vài `document_url` (VD CDN của Vinamilk) trả 403 khi tải không có User-Agent trình duyệt, nhưng mở bình thường trên trình duyệt. Cần đọc PDF thì tải lại với User-Agent trình duyệt, hoặc dùng bản ở `filings` và đối chiếu `file_sha256`. Trong báo cáo vẫn dẫn `document_url`.
- Một số quý năm trước lấy từ cột cùng kỳ chưa tách được lợi nhuận công ty mẹ (ghi chú `parent_profit_not_separated` trong `statement`): khi đó số "công ty mẹ" bằng tổng lợi nhuận sau thuế. Tăng trưởng tính trên quý đó phải ghi rõ, chưa nên trích dẫn.

## Giá cổ phiếu (lệnh prices, reaction, event-study)

- Data API chưa có giá. Script lấy giá đóng cửa ngày từ dữ liệu biểu đồ công khai của VNDirect, dự phòng DNSE. Đây là nguồn không chính thức, có thể đổi hay ngừng bất cứ lúc nào; ghi tên nguồn và ngày lấy trong báo cáo.
- Đơn vị nghìn đồng. Giá đã điều chỉnh cổ tức và chia tách (giá cũ có số lẻ), nên lợi suất đã gồm cổ tức nhưng giá cũ khác giá niêm yết lúc đó.
- Chỉ số sàn theo `exchange` của công ty: HOSE → VNINDEX, HNX → HNXINDEX, UPCOM → UPCOMINDEX.
- Ngày công bố BCTC: `filings.issuer_release_date`, `filings.detected_at` (lúc Wealbee phát hiện, có thể muộn), ngày trong tên file, hoặc hạn luật (20 ngày sau cuối quý, 30 ngày với BCTC hợp nhất). Script lấy ngày sớm nhất có được; hiện nhiều kỳ trước quý 3/2026 chưa có ngày thật.
- Dùng giá riêng: `WEALBEE_PRICE_CSV_DIR=<thư mục>` với file `<MÃ>.csv` hai cột `date,close`. Chọn một nguồn: `WEALBEE_PRICE_SOURCE=vndirect|dnse`.

