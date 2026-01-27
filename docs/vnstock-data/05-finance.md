# Finance - Báo Cáo Tài Chính, Chỉ Số, Kế Hoạch

Lớp `Finance` cung cấp dữ liệu báo cáo tài chính, chỉ số tài chính và kế hoạch kinh doanh.

## Khởi Tạo

```python
from vnstock_data import Finance

# KBS (mặc định, cấu trúc báo cáo chuẩn, dùng cho Cloud/Jupyter để tránh chặn IP)
fin_kbs = Finance(source="kbs", symbol="VCB", period="year")

# VCI (đơn giản, dễ phân tích)
fin = Finance(source="vci", symbol="VCB", period="year")

# MAS (chi tiết, Excel-style)
fin_mas = Finance(source="mas", symbol="VCB", period="year")
```

**Tham số**:
- `source`: `"kbs"`, `"vci"`, hoặc `"mas"`
- `symbol`: Mã cổ phiếu
- `period`: `"year"` (báo cáo năm) hoặc `"quarter"` (báo cáo quý)

## Phương Thức VCI & KBS (Cấu trúc giống nhau)

*Lưu ý: Nguồn KBS có các phương thức tương tự VCI tuy nhiên cấu các báo cáo được trình bày có tính phân cấp - tương thích với dạng báo cáo truyền thống, nguồn này được bổ sung để thay thế VCI khi chạy trên môi trường Cloud.*

### balance_sheet() - Bảng Cân Đối Kế Toán

```python
df = fin.balance_sheet(lang="vi")
```

**Tham số**:
- `lang`: `'vi'` (Tiếng Việt) hoặc `'en'` (Tiếng Anh) - Mặc định là `'vi'`

**Thông Tin Cấu Trúc Dữ Liệu (Quan Trọng)**
Cấu trúc dữ liệu trả về khác nhau tuỳ thuộc vào nguồn dữ liệu (`source`).

**1. Nguồn VCI (Dạng Wide)**
- Dữ liệu được trải phẳng, mỗi dòng là một kỳ báo cáo.
- **Cột**: `report_period`, `ticker` và các khoản mục tài chính (ví dụ: `Total Assets`, `Owner's Equity`).
- **Thích hợp**: Phân tích theo chuỗi thời gian (time-series) cho một mã.

| Cột (Column) | Kiểu Dữ Liệu | Mô Tả |
|---|---|---|
| `ticker` | object | Mã cổ phiếu |
| `report_period` | object | Kỳ báo cáo |
| `Cash and precious metals` | float64 | Tiền và kim loại quý |
| `TOTAL ASSETS` | float64 | Tổng tài sản |
| `OWNER'S EQUITY` | float64 | Vốn chủ sở hữu |
| ... | ... | (Hàng trăm cột khoản mục khác) |

**2. Nguồn KBS/MAS (Dạng Report)**
- Dữ liệu trình bày giống báo cáo tài chính truyền thống.
- **Cột**: `item` (tên khoản mục), `item_id` (mã khoản mục), và các cột năm/quý (ví dụ `2024`, `2023`).
- **Thích hợp**: Xem chi tiết báo cáo tại một thời điểm hoặc so sánh nhanh các năm.

| Cột (Column) | Kiểu Dữ Liệu | Mô Tả |
|---|---|---|
| `item` | object | Tên khoản mục (ví dụ: "Tổng tài sản") |
| `item_id` | object | Mã định danh khoản mục |
| `2024` | float64 | Giá trị năm 2024 |
| `2023` | float64 | Giá trị năm 2023 |
| ... | ... | Các năm quá khứ khác |

### income_statement() - Báo Cáo Kết Quả Kinh Doanh

```python
df = fin.income_statement(lang="vi")
```

**Thông Tin Cấu Trúc Dữ Liệu**

**1. Nguồn VCI**: Dạng Wide (Mỗi dòng là 1 kỳ)
| Cột | Mô Tả |
|---|---|
| `ticker`, `report_period` | Thông tin chung |
| `Total Operating Income` | Tổng thu nhập hoạt động |
| `Net profit/(loss) after tax` | Lợi nhuận sau thuế |
| `EPS basic (VND)` | EPS cơ bản |
| ... | ... |

**2. Nguồn KBS/MAS**: Dạng Report (Các năm là cột)
| Cột | Mô Tả |
|---|---|
| `item` | Tên khoản mục (VD: "Lợi nhuận sau thuế") |
| `2024`, `2023`, ... | Giá trị theo từng năm/quý |

### cash_flow() - Báo Cáo Lưu Chuyển Tiền Tệ

```python
df = fin.cash_flow(lang="vi")
```

**Thông Tin Cấu Trúc Dữ Liệu**

**1. Nguồn VCI**:
| Cột | Mô Tả |
|---|---|
| `ticker`, `report_period` | Thông tin chung |
| `Net cash from operating activities` | Lưu chuyển tiền từ HĐKD |
| `Net cash from investing activities` | Lưu chuyển tiền từ HĐĐT |
| `Net cash from financing activities` | Lưu chuyển tiền từ HĐTC |
| `Cash and cash equivalents at end` | Tiền & tương đương tiền cuối kỳ |

**2. Nguồn KBS/MAS**:
| Cột | Mô Tả |
|---|---|
| `item` | Tên khoản mục (VD: "Lưu chuyển tiền từ HĐKD") |
| `2024`, `2023`, ... | Giá trị theo từng năm/quý |

### ratio() - Chỉ Số Tài Chính

```python
df = fin.ratio(lang="vi")
```

**Thông Tin Cấu Trúc Dữ Liệu**

**1. Nguồn VCI (Rất chi tiết)**:
Trả về DataFrame ~40-50 chỉ số quan trọng đã tính toán sẵn.
- **Định giá**: `P/E`, `P/B`, `P/S`, `EV/EBITDA`
- **Hiệu quả**: `ROE (%)`, `ROA (%)`, `ROIC`
- **Thanh khoản**: `Current Ratio`, `Quick Ratio`, `Cash Ratio`
- **Biên lợi nhuận**: `Gross Margin (%)`, `Net Profit Margin (%)`
- **Tăng trưởng**: `Loans Growth (%)`, `Deposit Growth (%)` (ngành bank)

**2. Nguồn KBS/MAS**:
Tương tự cấu trúc Report của KBS, với các chỉ số là dòng (`item`), các năm là cột.

### note() - Thuyết Minh BCTC Chi Tiết

```python
df = fin.note(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 307 cột (shape: 43, 307)
- Các thuyết minh chi tiết về từng khoản mục trong báo cáo
- Phân loại cho vay theo loại khách hàng, ngành, etc.
- Kiểu dữ liệu: float64, object

## Phương Thức MAS

**Lưu ý**: MAS có cấu trúc dữ liệu khác VCI - Cột chi tiết, định dạng giống Excel tải về từ website.

```python
fin_mas = Finance(source="mas", symbol="VCB", period="year")
df_bs = fin_mas.balance_sheet(lang="vi")      # 79 cột, 13 năm
df_ic = fin_mas.income_statement(lang="vi")   # 26 cột, 13 năm
df_cf = fin_mas.cash_flow(lang="vi")          # 52 cột, 13 năm
df_ratio = fin_mas.ratio(lang="vi")           # 8 cột, 13 năm
df_plan = fin_mas.annual_plan(lang="vi")      # 3 cột, 6 năm

# note() không được implement trong MAS
```

### balance_sheet() - Bảng Cân Đối Kế Toán

```python
df = fin_mas.balance_sheet(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 79 cột, có thể thay đổi theo loại hình doanh nghiệp (shape: 13, 79)
- Dòng: 13 giai đoạn báo cáo năm (2024-2012)
- Cột: Tài sản (cash, tiền gửi NHNN, cho vay, chứng khoán, TSCĐ, etc.), Nợ (tiền gửi khách, vay NHNN, phát hành giấy tờ), Vốn (vốn điều lệ, quỹ, lợi nhuận lũy kế)
- Kiểu dữ liệu: object (period, year_period, các khoản mục), int64 (số tiền - VND)

### income_statement() - Báo Cáo Kết Quả Kinh Doanh

```python
df = fin_mas.income_statement(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 26 cột, có thể thay đổi theo loại hình doanh nghiệp (shape: 13, 26)
- Dòng: 13 giai đoạn năm
- Cột: Thu nhập lãi, chi phí lãi, thu nhập dịch vụ, chi phí dịch vụ, lãi/lỗ các hoạt động, chi phí dự phòng, lợi nhuận trước/sau thuế, lợi nhuận sau thuế của cổ đông, EPS
- Kiểu dữ liệu: object (period, year_period, các khoản mục), int64 (số tiền - VND)

### cash_flow() - Báo Cáo Lưu Chuyển Tiền Tệ

```python
df = fin_mas.cash_flow(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 52 cột, có thể thay đổi theo loại hình doanh nghiệp (shape: 13, 52)
- Dòng: 13 giai đoạn năm
- Cột: Dòng tiền từ hoạt động kinh doanh (chi tiết: lãi, chi phí, dịch vụ, nhân viên), thay đổi tài sản, thay đổi công nợ, hoạt động đầu tư, hoạt động tài chính
- Kiểu dữ liệu: object (period, year_period), int64 (số tiền - VND)

### ratio() - Chỉ Số Tài Chính

```python
df = fin_mas.ratio(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 8 cột, có thể thay đổi theo loại hình doanh nghiệp (shape: 13, 8)
- Cột: `period`, `year_period`, `EPS`, `BVPS`, `P/E`, `P/B`, `Tỷ suất cổ tức`, `Beta`
- Kiểu dữ liệu: object (period, year_period), float64/int64 (chỉ số)

### annual_plan() - Kế Hoạch Kinh Doanh Hàng Năm

```python
df_plan = fin_mas.annual_plan(lang="vi")
```

**Kiểu Dữ Liệu Trả Về**: DataFrame với 3 cột (shape: 6, 3)
- `period`: int64 - Năm kế hoạch
- `Lợi nhuận trước thuế kế hoạch`: object - Giá trị lợi nhuận kế hoạch (hoặc NULL)
- `Tỷ lệ cổ tức (%) kế hoạch`: object - Tỷ lệ cổ tức dự kiến (hoặc NULL)

**Ví dụ**:
```
   period Lợi nhuận trước thuế kế hoạch Tỷ lệ cổ tức (%) kế hoạch
0    2024                          None                      None
1    2023                42973304650000                      None
2    2022                30675680000000                      None
```

## Ví Dụ

```python
from vnstock_data import Finance
import pandas as pd

# VCI: Phân tích đơn giản
fin = Finance(source="vci", symbol="VCB", period="year")

# Lấy BCTC
bs = fin.balance_sheet(lang="vi")
ic = fin.income_statement(lang="vi")
ratio = fin.ratio(lang="vi")

# Phân tích xu hướng
print("Doanh thu qua các năm:")
print(ic[['Năm', 'Doanh thu']].head())

# Tính chỉ số
print("\nChỉ số tài chính:")
print(ratio[['Năm', 'P/E', 'P/B', 'ROE', 'ROA']].head())

# MAS: Dữ liệu chi tiết
fin_mas = Finance(source="mas", symbol="VCB", period="year")
bs_mas = fin_mas.balance_sheet(lang="vi")

# MAS có cấu trúc MultiIndex hoặc cột dài
print(f"\nSố cột MAS: {len(bs_mas.columns)}")
print(f"Số cột VCI: {len(bs.columns)}")
```

## So Sánh VCI vs MAS

| Tiêu Chí | VCI | MAS |
|---|:---:|:---:|
| Ổn định | ✅ | ✅ |
| Số cột | Lớn (28-307) | Vừa (8-79) |
| Kích thước dữ liệu | Lớn | Trung bình |
| Dễ sử dụng | ✅ | ✅ |
| Thuyết minh BCTC | ✅ | ❌ |
| Chỉ tiêu kế hoạch | ❌ | ✅ |
| Định dạng | Làm phẳng cột, rút gọn tiêu chí | Báo cáo chuẩn |
| Thích hợp cho | Phân tích chi tiết | Phân tích theo cấu trúc quan hệ |

**Khuyến Cáo**:
- **VCI**: Phân tích các tiêu chí quan trọng, theo dõi quý, cần thuyết minh BCTC. Báo cáo của ngành đặc thù như tài chính, ngân hàng có thể không giữ nguyên cấu trúc khoản mục gốc.
- **MAS**: Báo cáo theo định dạng tiêu chuẩn giữ nguyên cấu trúc khoản mục báo cáo, kế hoạch năm

## Tham Số Chính

### Khởi Tạo Finance
```python
fin = Finance(source="vci", symbol="VCB", period="year")
```

**Tham số**:
- `source`: `"vci"`, `"kbs"`, `"mas"` - Mặc định là `"kbs"`
- `symbol`: Mã cổ phiếu (ví dụ: `"VCB"`)
- `period`: `"year"` (năm) hoặc `"quarter"` (quý) - Mặc định là `"year"`

### Tham số Method

```python
df = fin.balance_sheet(lang="vi")
```

**Tham số**:
- `lang`: `"vi"` (tiếng Việt) hoặc `"en"` (tiếng Anh) - Mặc định là `"vi"`

## Ma Trận Các Phương Thức Hỗ Trợ

> Thông tin số dòng/cột chỉ mang tính chất tham khảo, có thể thay đổi theo mã cụ thể, thời gian, và đặc thù nhóm phân loại công ty.

| Phương Thức | VCI | KBS | MAS | Ghi Chú |
|---|:---:|:---:|:---:|---|
| balance_sheet | ✅ (đa kỳ) | ✅ | ✅ (13 năm) | MAS theo chuẩn NHNN |
| income_statement | ✅ (đa kỳ) | ✅ | ✅ (13 năm) | MAS theo chuẩn NHNN |
| cash_flow | ✅ (đa kỳ) | ✅ | ✅ (13 năm) | MAS theo chuẩn NHNN |
| ratio | ✅ (đa kỳ) | ✅ | ✅ (13 năm) | MAS chỉ có 6 chỉ số |
| note | ✅ (đa kỳ) | ✅ | ❌ NotImplemented | Chỉ VCI/KBS có |
| annual_plan | ❌ | ❌ | ✅ (6 năm) | MAS only |


## Ví Dụ Phân Tích

```python
from vnstock_data import Finance
import pandas as pd

fin = Finance(source="vci", symbol="VCB", period="year")

# Tính trend doanh thu
ic = fin.income_statement(lang="vi")
ic['revenue_growth'] = ic['Doanh thu'].pct_change()

print("Tăng trưởng doanh thu:")
print(ic[['Năm', 'Doanh thu', 'revenue_growth']])

# Tính lợi nhuận biên
ic['profit_margin'] = ic['Lợi nhuận'] / ic['Doanh thu']

print("\nLợi nhuận biên:")
print(ic[['Năm', 'profit_margin']])

# Lấy ratio
ratio = fin.ratio(lang="vi")
print("\nChỉ số định giá:")
print(ratio[['Năm', 'P/E', 'P/B', 'EPS']].tail(5))
```
