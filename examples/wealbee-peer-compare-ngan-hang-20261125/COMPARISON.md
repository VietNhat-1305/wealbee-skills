# 5 ngân hàng quý 3/2026: lợi nhuận công ty mẹ tăng từ 0,1% đến 44,3% so với cùng kỳ, đòn bẩy chênh gần 3 lần

5 mã (BID, CTG, MBB, TCB, VCB) · BCTC hợp nhất Q3/2026 · số liệu lấy ngày 25/11/2026

> Ví dụ đầu ra của skill `wealbee-peer-compare`, chạy với câu hỏi "so sánh VCB, BID, CTG, MBB, TCB quý 3". Mọi số lấy từ JSON trong `evidence/`; bảng dạng Excel ở `compare.csv`.

## Bảng so sánh

| Mã | Lợi nhuận công ty mẹ Q3 (tỷ đồng) | So với cùng kỳ | Luỹ kế 9 tháng (tỷ đồng) | Tổng tài sản (nghìn tỷ đồng) | ROE quy năm | ROA quy năm | Nợ phải trả / vốn chủ (lần) | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| BID | 8.330,7 | +39,9% | 23.277,7 | 3.493,3 | 16,7% | 0,9% | 16,21 | needs_review |
| CTG | 10.834,8 | +28,2% | 31.491,8 | 2.951,8 | 21,8% | 1,5% | 13,23 | verified |
| MBB | 8.039,5 | +44,3% | 23.784,1 | 1.837,9 | 21,3% | 1,9% | 10,20 | verified |
| TCB | 7.942,9 | +23,7% | 21.964,1 | 1.318,2 | 16,3% | 2,4% | 5,68 | verified |
| VCB | 9.033,3 | +0,1% | 33.032,1 | 2.682,4 | 18,4% | 1,7% | 9,57 | verified |
| *Trung vị 26 BCTC ngân hàng Q3/2026* | | *+10,0%* | | | *16,2%* | *1,4%* | *10,32* | |

Khoảng giữa p25–p75 của 26 BCTC ngân hàng đã kiểm chứng [S6]: tăng trưởng lợi nhuận từ 1,5% đến 29,3%, ROE từ 10,8% đến 19,7%, ROA từ 0,8% đến 1,7%, nợ/vốn chủ từ 8,55 đến 13,2 lần.

Bảng sắp theo chữ cái của mã, không phải thứ hạng. Cả 5 mã cùng cách tính ROE (lợi nhuận sau thuế / bình quân tổng vốn chủ), nên so ROE giữa các mã được.

## Khác biệt đáng chú ý

- **VCB gần như đi ngang so với cùng kỳ, các mã còn lại tăng 23,7–44,3%.** Lý do nằm ở quý 2: lợi nhuận quý 2/2026 của VCB là 14.542,3 tỷ đồng (+64,7%), cao hơn hẳn các quý khác của chính VCB trong dữ liệu (8.702–9.457 tỷ). Tính luỹ kế 9 tháng, lợi nhuận sau thuế VCB vẫn tăng 24,4% [S5]. Quý 2 có khoản thu bất thường nào không? Data API chưa có dòng chi tiết; cần xem BCTC quý 2 của VCB.
- **Đòn bẩy chênh gần 3 lần.** Nợ phải trả / vốn chủ của TCB là 5,68 lần, dưới p25 của nhóm ngân hàng. BID là 16,21 lần, trên p75. Vốn chủ hai ngân hàng gần bằng nhau (197,3 và 203,0 nghìn tỷ đồng), nhưng tổng tài sản của BID lớn gấp 2,65 lần TCB.
- **ROA cao chưa chắc ROE cao.** ROE xấp xỉ ROA nhân với tổng tài sản / vốn chủ. TCB có ROA 2,4%, cao hơn 4 mã còn lại, nhưng tài sản chỉ gấp 6,7 lần vốn chủ nên ROE còn 16,3%. CTG có ROA 1,5% nhưng tài sản gấp 14,2 lần vốn chủ, ROE 21,8%. Hai con đường khác nhau tới cùng mức ROE: sinh lời trên tài sản, hoặc dùng nhiều vốn huy động hơn.
- **Quy mô.** Tổng tài sản từ 1.318,2 nghìn tỷ đồng (TCB) đến 3.493,3 nghìn tỷ đồng (BID); vốn chủ từ 164,1 nghìn tỷ (MBB) đến 253,8 nghìn tỷ (VCB). Lợi nhuận quý 3 của CTG (10.834,8 tỷ) cao hơn VCB (9.033,3 tỷ) dù vốn chủ nhỏ hơn, nhưng luỹ kế 9 tháng thì VCB cao hơn (33.032,1 so với 31.491,8 tỷ).

## Xu hướng 4 quý

Lợi nhuận công ty mẹ theo quý, tỷ đồng [S6]:

| Mã | Q3/2025 | Q1/2026 | Q2/2026 | Q3/2026 |
|---|---|---|---|---|
| BID | 5.953,0 | 6.800,8 | 8.146,2 | 8.330,7 |
| CTG | 8.448,8 | 8.917,0 | 11.740,1 | 10.834,8 |
| MBB | 5.571,0 | 7.515,5 | 8.229,1 | 8.039,5 |
| TCB | 6.419,3 | 6.671,1 | 7.350,1 | 7.942,9 |
| VCB | 9.020,5 | 9.456,6 | 14.542,3 | 9.033,3 |

Data API chưa có quý 4/2025. TCB và BID tăng liên tiếp qua 3 quý năm 2026. CTG, MBB và VCB có quý 2 cao hơn quý 3. Số Q3/2025 lấy từ cột cùng kỳ của BCTC 2026, có thể đã điều chỉnh hồi tố.

## Lưu ý khi so

- **BID đang `needs_review`.** Có hai lý do: cột cùng kỳ không khớp với BCTC năm trước (`comparative_mismatch`), và có ghi chú khi trích xuất. 9/10 phép kiểm đạt; phép không đạt là tổng lưu chuyển tiền cùng kỳ năm trước. Mức tăng 39,9% dựa trên cột cùng kỳ đó, nên cần đối chiếu báo cáo kết quả kinh doanh ở trang 7 file gốc trước khi trích dẫn [S1].
- **Dòng tiền kinh doanh của ngân hàng không đọc như doanh nghiệp thường.** Lưu chuyển tiền kinh doanh 9 tháng âm ở BID (−42.484,0 tỷ), MBB (−65.264,9 tỷ) và TCB (−8.952,4 tỷ). Ở CTG (+71.619,9 tỷ) và VCB (+81.448,5 tỷ) con số này dương. Với ngân hàng, dòng này biến động theo tiền gửi và cho vay, không phải dấu hiệu lãi "trên giấy".
- **Doanh thu bị bỏ khỏi bảng.** Data API có doanh thu cho MBB và TCB, nhưng chưa có cho BID, CTG, VCB (`missing_fields`). Khái niệm "doanh thu" ngân hàng cũng chưa thống nhất, nên không so.
- **Q1/2026 của cả 5 mã đang `needs_review`.** Số quý 1 trong bảng xu hướng chỉ nên dùng để xem hướng đi, chưa nên trích dẫn.
- Vốn chủ công ty mẹ và lợi ích cổ đông không kiểm soát Data API chưa có cho cả 5 mã.

## Nguồn

- [S1] BID, BCTC hợp nhất Q3/2026: https://bidv.com.vn/wps/wcm/connect/69a3b6bf-9fb3-4ef3-bb61-156cd541bc7d/20261030+-+BID+-+CBTT+BCTC+HN+giua+nien+do+Q3.pdf?MOD=AJPERES&CACHEID=ROOTWORKSPACE-69a3b6bf-9fb3-4ef3-bb61-156cd541bc7d-q6ctCsE (kết quả kinh doanh trang 7)
- [S2] CTG, BCTC hợp nhất Q3/2026: https://investor.vietinbank.vn/documents/20126/1872056/BCTC%20hop%20nhat%20Quy%203.2026.pdf.pdf/705b46cf-4b1f-7981-7487-131330123101?download=true (trang 6)
- [S3] MBB, BCTC hợp nhất Q3/2026: https://cafefnew.mediacdn.vn//Images/Uploaded/DuLieuDownload/BCTC/MBB_202610302020MBB2020Bao20cao20tai20chinh20hop20nhat20Q32026_31102026100340.pdf?v=1793415821716 (trang 6)
- [S4] TCB, BCTC hợp nhất Q3/2026: https://techcombank.com/content/dam/techcombank/public-site/documents/techcombank-vas-bao-cao-tai-chinh-hop-nhat-3q26-scan.pdf (trang 8)
- [S5] VCB, BCTC hợp nhất Q3/2026: https://www.vietcombank.com.vn/-/media/Project/VCB-Sites/VCB/Nha-Dau-tu/Files/BC-dinh-ky/BCTC/2026/20261030---VCB---BCTC-hop-nhat-Q3-2026.pdf?ts=00010101000000 (trang 7)
- [S6] Wealbee Data API, lệnh `compare`, `summary`, `trend`, `benchmark --industry bank --period 2026Q3`, lấy ngày 25/11/2026.

Số liệu: Wealbee Data API, tỷ đồng, làm tròn 1 chữ số. ROE, ROA và trung vị do wealbee-skills tính từ BCTC. Thông tin tham khảo, không phải khuyến nghị đầu tư.
