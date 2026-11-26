# VN30, 90 lần công bố BCTC năm 2026: chưa thấy khác biệt chắc chắn giữa nhóm lãi tăng mạnh và yếu; 20/29 mã công bố quý 3 vào hai ngày cuối hạn

30 mã VN30 × 3 quý (Q1–Q3/2026) · giá đến 26/11/2026 · ngày công bố: 18 ngày thật, 27 từ tên file BCTC, 45 ước tính theo hạn luật (2 ngày muộn hơn hạn, đã gắn cờ)

> Ví dụ đầu ra của skill `wealbee-earnings-reaction`, chạy với câu hỏi "VNM từ lúc ra BCTC đến giờ tăng bao nhiêu, và backtest mỗi lần VN30 công bố BCTC thì giá phản ứng thế nào". Số lấy từ `evidence/`; bảng từng sự kiện ở `events.csv`.

## Vinamilk (VNM): từ lúc công bố đến nay

| Kỳ | Ngày công bố (nguồn) | Lợi nhuận công ty mẹ so với cùng kỳ | 1 phiên | 5 phiên | 20 phiên | Đến nay | Đến nay so với VN-Index |
|---|---|---|---|---|---|---|---|
| Q1/2026 | 30/4 (ước tính theo hạn luật) | +53,0% | 0,0% | 0,0% | −2,8% | −6,6% | +5,5 điểm % |
| Q2/2026 | 30/7 (từ tên file) | +28,0% | −0,5% | −3,6% | +2,1% | −10,0% | −3,4 điểm % |
| Q3/2026 | 30/10, sau 17:00 (doanh nghiệp công bố) | +17,3% | −1,6% | +1,6% | chưa đủ 20 phiên | −3,2% | +3,2 điểm % |

Từ lúc công bố BCTC quý 3/2026 đến 26/11/2026 (18 phiên), giá VNM giảm 3,2%. VN-Index cùng khoảng giảm 6,4%, nên VNM tốt hơn chỉ số 3,2 điểm %. Lợi suất tính từ giá đã điều chỉnh cổ tức, nên đã gồm cổ tức có ngày giao dịch không hưởng quyền trong khoảng này [S2].

Mức tăng lợi nhuận chậm dần qua 3 quý (53,0%, 28,0%, 17,3%), nhưng phản ứng giá không đi theo một hướng rõ ràng. Mẫu 3 lần công bố quá nhỏ để rút ra điều gì về riêng VNM.

## Backtest 30 mã VN30 theo nhóm kết quả

Mỗi ô là chênh lệch trung bình so với chỉ số sàn, trung vị trong ngoặc, đơn vị điểm %.

| Nhóm (lợi nhuận công ty mẹ quý so với cùng kỳ) | Số lần | 1 phiên | 5 phiên | 10 phiên | 20 phiên | % lần vượt chỉ số (5 phiên) |
|---|---|---|---|---|---|---|
| Giảm | 14 | −0,1 (+0,2) | −0,7 (−0,7) | 0,0 (−0,7) | +0,7 (−2,2) | 36% |
| Tăng 0–20% | 27 | −0,1 (−0,1) | −1,0 (−1,8) | −1,2 (−3,1) | −0,4 (−2,1) | 37% |
| Tăng trên 20% | 48 | +0,6 (+0,3) | +0,3 (+0,6) | +0,7 (0,0) | +1,0 (−0,7) | 57% |
| Tất cả | 90 | +0,2 (+0,1) | −0,3 (−0,3) | −0,1 (−0,8) | +0,6 (−1,7) | 47% |

Cột 20 phiên có ít sự kiện hơn (69 lần), vì BCTC quý 3 mới qua 18 phiên. 1 lần công bố không tính được tăng trưởng (lợi nhuận đổi dấu) nằm ngoài các nhóm.

## Điều thấy được

- **Gộp cả 90 lần, nhóm lãi tăng trên 20% nhỉnh hơn sau 5 phiên, nhưng chưa đủ chắc.** Trung vị +0,6 điểm % và 57% số lần vượt chỉ số, so với −1,8 điểm % và 37% ở nhóm tăng 0–20%. Tách theo quý thì khác biệt này có ở Q1 (+1,1) và Q2 (+0,6) nhưng đảo chiều ở Q3 (−0,7, 40% vượt chỉ số). Q3 lại là quý có nhiều ngày công bố thật nhất. Chỉ giữ 43 lần có ngày thật hoặc ngày từ tên file thì trung vị nhóm tăng trên 20% sau 5 phiên còn 0,0 điểm %.
- **Ở cửa sổ 20 phiên, trung bình và trung vị ngược chiều ở nhóm giảm và nhóm tăng trên 20%.** Vài sự kiện cực đoan kéo trung bình. BSR Q1/2026 (lợi nhuận gấp gần 21 lần cùng kỳ, do nền thấp) vượt chỉ số 25,6 điểm %. LPB Q1/2026 (lợi nhuận giảm 10,1%) vượt 19,1 điểm %, GAS Q2/2026 vượt 17,7 điểm %. BSR Q2/2026 kém chỉ số 16,3 điểm %, nhưng ngày công bố của lần này bị gắn cờ muộn (xem Giới hạn).
- **Doanh nghiệp dồn công bố vào hạn cuối, sau giờ giao dịch.** Ở quý 3/2026, 20 trong 29 mã công bố vào 29–30/10, riêng ngày 30/10 (hạn công bố BCTC hợp nhất) có 16 mã. Cả 14 lần có giờ phát hiện đều sau 15:00, nên thị trường chỉ phản ứng từ phiên kế tiếp.
- **Giá giảm sau công bố phần lớn đến từ thị trường chung.** Tính đến 26/11, giá trung bình giảm 8,2% kể từ lúc công bố, nhưng chênh lệch so với chỉ số gần 0 (trung vị +0,8 điểm %). VN-Index giảm từ 1.875,84 điểm (28/4) xuống 1.629,68 điểm (26/11).

## Giới hạn

- **Mẫu ngắn.** Data API hiện có BCTC từ quý 1/2026, nên mỗi mã chỉ có 3 lần công bố.
- **Một nửa ngày công bố là ước tính.** 45 trên 90 ngày tính theo hạn luật, gồm toàn bộ quý 1. Doanh nghiệp có thể công bố sớm hơn vài ngày, nên cửa sổ 1 phiên của nhóm này gần như không dùng được.
- **Hai ngày muộn hơn hạn luật.** BSR Q2/2026 (27/10) và VHM Q3/2026 (25/11) có ngày phát hiện của Wealbee muộn hơn nhiều so với hạn. Nhiều khả năng Wealbee phát hiện file chậm, không phải doanh nghiệp công bố muộn. Cần kiểm lại trước khi dùng hai sự kiện này.
- **Cách đo đơn giản.** Chênh lệch là lợi suất mã trừ chỉ số sàn, chưa điều chỉnh rủi ro. Phép đo không xét thị trường đã kỳ vọng gì trước ngày công bố. Nhiều mã công bố cùng tuần nên các sự kiện không độc lập.
- **Nguồn giá không chính thức.** Giá lấy từ dữ liệu biểu đồ công khai của VNDirect, đã điều chỉnh cổ tức và chia tách.

## Nguồn

- [S1] Ngày công bố, kỳ, tăng trưởng lợi nhuận: Wealbee Data API (`filings`, `statements`), lấy ngày 26/11/2026. BCTC quý 3/2026 của VNM: https://d8um25gjecm9v.cloudfront.net/cms/20261030_VNM_BCTC_da_soat_xet_Q3_2026_Hop_nhat_010a30af2b.pdf
- [S2] Giá cổ phiếu và chỉ số: dữ liệu biểu đồ công khai của VNDirect (dchart-api.vndirect.com.vn), giá đóng cửa ngày đã điều chỉnh, lấy ngày 26/11/2026.

Thống kê lịch sử trên mẫu nhỏ, không dự báo giá, không phải khuyến nghị đầu tư.
