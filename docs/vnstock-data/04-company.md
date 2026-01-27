# Company - Thông Tin Công Ty, Cổ Đông, Ban Lãnh Đạo

Lớp `Company` cung cấp thông tin chi tiết về các công ty niêm yết tại thị trường chứng khoán Việt Nam.

## Khởi Tạo

```python
from vnstock_data import Company

# Khởi tạo VCI (đơn giản, dễ phân tích)
company = Company(source="vci", symbol="VCB")

# Khởi tạo KBS (tương tự VCI, dùng cho Cloud/Jupyter để tránh chặn IP)
company_kbs = Company(source="kbs", symbol="VCB")
```

**Lưu ý**: VCI và KBS hỗ trợ đầy đủ các phương thức.

## Phương Thức

### overview() - Thông Tin Tổng Quan

```python
df = company.overview()
```

**Thông Tin Các Cột Dữ Liệu (DataFrame)**

| Cột (Column) | Kiểu Dữ Liệu (Dtype) | Mô Tả |
|---|---|---|
| `symbol` | object | Mã cổ phiếu |
| `id` | object | ID công ty |
| `issue_share` | int64 | Số lượng cổ phiếu lưu hành |
| `history` | object | Lịch sử hình thành & phát triển |
| `company_profile` | object | Giới thiệu công ty |
| `icb_name3` | object | Tên ngành cấp 3 (ICB) |
| `icb_name2` | object | Tên ngành cấp 2 (ICB) |
| `icb_name4` | object | Tên ngành cấp 4 (ICB) |
| `financial_ratio_issue_share` | int64 | Số lượng CP dùng tính chỉ số tài chính |
| `charter_capital` | int64 | Vốn điều lệ |

### shareholders() - Cổ Đông Lớn

```python
df = company.shareholders()
```

**Thông Tin Các Cột Dữ Liệu (DataFrame)**

| Cột (Column) | Kiểu Dữ Liệu (Dtype) | Mô Tả |
|---|---|---|
| `id` | object | ID cổ đông |
| `share_holder` | object | Tên cổ đông |
| `quantity` | int64 | Số lượng cổ phần sở hữu |
| `share_own_percent` | float64 | Tỷ lệ sở hữu (ví dụ: 0.15 là 15%) |
| `update_date` | object | Ngày cập nhật dữ liệu |

**Ví dụ output** (3 cổ đông lớn VCB):
```
         share_holder    quantity  share_own_percent update_date
0   Ngân Hàng Nhà Nước Việt Nam  6250338579             0.7480  2025-11-21
1   Mizuho Bank Limited         1253366534             0.1500  2025-11-21
2   Quỹ Đầu tư Chính phủ Singapore (GIC)    84503639             0.0101  2025-10-05
```

### officers() - Ban Lãnh Đạo

```python
df = company.officers(filter_by='working')
```

**Tham số**:
- `filter_by`: `'working'` (đang làm), `'resigned'` (đã nghỉ), `'all'` - Mặc định là `'working'`

**Thông Tin Các Cột Dữ Liệu (DataFrame)**

| Cột (Column) | Kiểu Dữ Liệu (Dtype) | Mô Tả |
|---|---|---|
| `id` | object | ID nhân sự |
| `officer_name` | object | Tên nhân sự |
| `officer_position` | object | Chức vụ đầy đủ |
| `position_short_name` | object | Chức vụ viết tắt |
| `update_date` | object | Ngày cập nhật |
| `officer_own_percent` | float64 | Tỷ lệ sở hữu cổ phần |
| `quantity` | int64 | Số lượng cổ phần sở hữu |

**Ví dụ output** (3 người quản lý VCB):
```
    officer_name                     officer_position update_date  officer_own_percent  quantity
0   Phùng Nguyễn Hải Yến   Phụ trách CBTT/Phó TGĐ  2025-07-30             0.000005     42339
1   Nguyễn Thanh Tùng      Phó Tổng Giám đốc     2025-10-03             0.000003     22324
2   Đào Minh Tuấn           Phó Tổng Giám đốc     2015-09-14             0.000002      5810
```

### subsidiaries() - Công Ty Con

```python
df = company.subsidiaries()
```

**Thông Tin Các Cột Dữ Liệu (DataFrame)**

| Cột (Column) | Kiểu Dữ Liệu (Dtype) | Mô Tả |
|---|---|---|
| `id` | object | ID công ty con |
| `sub_organ_code` | object | Mã tổ chức liên quan |
| `ownership_percent` | float64 | Tỷ lệ sở hữu |
| `organ_name` | object | Tên công ty con/liên kết |
| `type` | object | Loại hình ('công ty con', 'công ty liên kết') |

**Ví dụ output** (3 công ty con của VCB):
```
    sub_organ_code  ownership_percent                                     organ_name        type
0       2646966              0.875    Công ty Chuyển tiền Vietcombank      công ty con
1       TB                 1.000    Ngân hàng Thương mại TNHH MTV...     công ty con
2       VCB198             0.700    Công ty TNHH Cao Ốc Vietcombank 198  công ty con
```

### events() - Sự Kiện Công Ty

```python
df = company.events()
```

**Thông Tin Các Cột Dữ Liệu (DataFrame)**

| Cột (Column) | Kiểu Dữ Liệu (Dtype) | Mô Tả |
|---|---|---|
| `id` | object | ID sự kiện |
| `event_title` | object | Tiêu đề sự kiện (Tiếng Việt) |
| `en__event_title` | object | Tiêu đề sự kiện (English) |
| `public_date` | object | Ngày công bố |
| `issue_date` | object | Ngày thực hiện/thanh toán |
| `source_url` | object | Link nguồn tin |
| `event_list_code` | object | Mã loại sự kiện |
| `ratio` | float64 | Tỷ lệ thực hiện (nếu có) |
| `value` | float64 | Giá trị (tiền/cổ phiếu) |
| `record_date` | object | Ngày đăng ký cuối cùng |
| `exright_date` | object | Ngày giao dịch không hưởng quyền |
| `event_list_name` | object | Tên loại sự kiện |
| `en__event_list_name` | object | Tên loại sự kiện (English) |

### news() - Tin Tức

```python
df = company.news()
```

**Thông Tin Các Cột Dữ Liệu (DataFrame)**

| Cột (Column) | Kiểu Dữ Liệu (Dtype) | Mô Tả |
|---|---|---|
| `id` | object | ID tin tức |
| `news_title` | object | Tiêu đề tin |
| `news_sub_title` | object | Phụ đề |
| `friendly_sub_title` | object | Tiêu đề thân thiện URL |
| `news_image_url` | object | URL ảnh minh họa |
| `news_source_link` | object | Link gốc |
| `created_at` | object | Thời gian tạo |
| `public_date` | int64 | Thời gian công bố (timestamp) |
| `updated_at` | object | Thời gian cập nhật |
| `lang_code` | object | Ngôn ngữ ('vi', 'en') |
| `news_id` | object | Mã tin |
| `news_short_content` | object | Tóm tắt nội dung |
| `news_full_content` | object | Nội dung đầy đủ (HTML) |
| `close_price` | int64 | Giá đóng cửa phiên liên quan |
| `ref_price` | int64 | Giá tham chiếu |
| `floor` | int64 | Giá sàn |
| `ceiling` | int64 | Giá trần |
| `price_change_pct` | float64 | % Thay đổi giá |

### reports() - Báo Cáo Phân Tích

```python
df = company.reports()
```

**Thông Tin Các Cột Dữ Liệu (DataFrame)**

| Cột (Column) | Kiểu Dữ Liệu (Dtype) | Mô Tả |
|---|---|---|
| `date` | object | Ngày báo cáo |
| `description` | object | Mô tả chi tiết |
| `link` | object | Link tải báo cáo (PDF) |
| `name` | object | Tên báo cáo |

### trading_stats() - Thống Kê Giao Dịch

```python
df = company.trading_stats()
```

**Thông Tin Các Cột Dữ Liệu (DataFrame)**

| Cột (Column) | Kiểu Dữ Liệu (Dtype) | Mô Tả |
|---|---|---|
| `symbol` | object | Mã cổ phiếu |
| `exchange` | object | Sàn giao dịch |
| `ev` | int64 | Giá trị doanh nghiệp (Enterprise Value) |
| `ceiling` | int64 | Giá trần |
| `floor` | int64 | Giá sàn |
| `ref_price` | int64 | Giá tham chiếu |
| `open` | int64 | Giá mở cửa |
| `match_price` | int64 | Giá khớp lệnh hiện tại |
| `close_price` | int64 | Giá đóng cửa |
| `price_change` | int64 | Thay đổi giá (số tuyệt đối) |
| `price_change_pct` | float64 | % Thay đổi giá |
| `high` | int64 | Giá cao nhất |
| `low` | int64 | Giá thấp nhất |
| `total_volume` | int64 | Tổng khối lượng giao dịch |
| `high_price_1y` | int64 | Giá cao nhất 52 tuần |
| `low_price_1y` | int64 | Giá thấp nhất 52 tuần |
| `pct_low_change_1y` | float64 | % Thay đổi so với đáy 1 năm |
| `pct_high_change_1y` | float64 | % Thay đổi so với đỉnh 1 năm |
| `foreign_volume` | int64 | Khối lượng NN mua bán khớp lệnh |
| `foreign_room` | int64 | Tổng Room NN |
| `avg_match_volume_2w` | int64 | KLGD trung bình 2 tuần (10 phiên) |
| `foreign_holding_room` | int64 | Room NN còn lại |
| `current_holding_ratio` | float64 | Tỷ lệ sở hữu NN hiện tại |
| `max_holding_ratio` | float64 | Tỷ lệ sở hữu NN tối đa |

### ratio_summary() - Tóm Tắt Chỉ Số Tài Chính

```python
df = company.ratio_summary()
```

**Thông Tin Các Cột Dữ Liệu (DataFrame)**

Một số chỉ số tài chính cơ bản và định giá quan trọng:

| Cột (Column) | Kiểu Dữ Liệu | Mô Tả |
|---|---|---|
| `symbol` | object | Mã cổ phiếu |
| `year_report` | int64 | Năm báo cáo gần nhất |
| `length_report` | int64 | Số kỳ báo cáo |
| `update_date` | int64 | Ngày cập nhật |
| `revenue` | int64 | Doanh thu |
| `revenue_growth` | float64 | Tăng trưởng doanh thu |
| `net_profit` | int64 | Lợi nhuận ròng |
| `net_profit_growth` | float64 | Tăng trưởng lợi nhuận |
| `gross_margin` | int64 | Biên lợi nhuận gộp |
| `net_profit_margin` | float64 | Biên lợi nhuận ròng |
| `roe` | float64 | Return on Equity |
| `roa` | float64 | Return on Assets |
| `roic` | int64 | Return on Invested Capital |
| `pe` | float64 | Price/Earnings |
| `pb` | float64 | Price/Book |
| `ps` | float64 | Price/Sales |
| `pcf` | float64 | Price/Cash Flow |
| `eps` | float64 | Earnings Per Share |
| `eps_ttm` | float64 | EPS Trailing 12 months |
| `current_ratio` | int64 | Tỷ số thanh khoản hiện hành |
| `quick_ratio` | int64 | Tỷ số thanh khoản nhanh |
| `cash_ratio` | int64 | Tỷ số thanh khoản tiền mặt |
| `debt_equity (de)` | float64 | Nợ/Vốn chủ sở hữu |
| `dividend` | int64 | Cổ tức |
| `charter_capital` | int64 | Vốn điều lệ |
| `issue_share` | int64 | Số lượng cổ phiếu |
| ... | ... | (Tổng cộng ~45 cột) |

*Ghi chú: Các cột `dtype=object` (ví dụ `interest_coverage`) có thể chứa giá trị NULL hoặc chuỗi.*

## Ví Dụ

```python
from vnstock_data import Company
import pandas as pd

company = Company(source="vci", symbol="VCB")

# Thông tin công ty
overview = company.overview()
print(f"Công ty: {overview['company_name'].values[0]}")
print(f"Vốn điều lệ: {overview['charter_capital'].values[0]:,.0f}")

# Cổ đông lớn
shareholders = company.shareholders()
print(f"\nTop 5 cổ đông lớn:")
print(shareholders[['share_holder', 'share_own_percent']].head())

# Ban lãnh đạo
officers = company.officers(filter_by='working')
print(f"\nBan lãnh đạo (đang làm):")
print(officers[['officer_name', 'officer_position']].head())

# Sự kiện gần đây
events = company.events().head()
print(f"\nSự kiện gần đây:")
print(events[['event_title', 'public_date']])

# Thống kê giao dịch
stats = company.trading_stats()
print(f"\nThống kê giao dịch:")
print(f"Giá khớp: {stats['match_price'].values[0]}")
print(f"Khối lượng: {stats['total_volume'].values[0]:,.0f}")
```

## Thực hành tốt

1. **Cache dữ liệu công ty**: Thông tin công ty ít thay đổi, hãy cache
2. **Kết hợp với Quote**: Sử dụng Company + Quote để phân tích sâu hơn
3. **Kiểm tra update_date**: Xác nhận dữ liệu có mới nhất không

## Ma Trận Support

| Phương Thức | VCI | KBS |
|---|:---:|:---:|
| overview | ✅ | ✅ |
| shareholders | ✅ | ✅ |
| officers | ✅ | ✅ |
| subsidiaries | ✅ | ✅ |
| events | ✅ | ✅ |
| news | ✅ | ✅ |
| reports | ✅ | ✅ |
| trading_stats | ✅ | ✅ |
| ratio_summary | ✅ | ✅ |

**Khuyến Nghị**: Luôn sử dụng VCI cho Company data.
