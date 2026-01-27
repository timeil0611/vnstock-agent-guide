# Trading - Dữ Liệu Giao Dịch, Bảng Giá, Thống Kê

Lớp `Trading` cung cấp dữ liệu giao dịch chi tiết, bảng giá, thống kê giao dịch nước ngoài và tự doanh.

## Khởi Tạo

```python
from vnstock_data import Trading

# VCI: Dữ liệu từ bảng giá giao dịch
trading_vci = Trading(source="vci", symbol="VCB")

# KBS: Dữ liệu tương đương VCI, dùng cho Cloud
trading_kbs = Trading(source="kbs", symbol="VCB")

# CafeF: Dữ liệu có thể không đầy đủ và ổn định, sử dụng làm nguồn bổ sung
trading_cafef = Trading(source="cafef", symbol="VCB")
```

**Lưu ý**: VCI/KBS và CafeF có một số method (phương thức) khác nhau.

## Phương Thức VCI & KBS

### price_board() - Bảng Giá Realtime

Truy xuất thông tin bảng giá realtime của các mã chứng khoán từ nguồn dữ liệu VCI.

**Tham số**:
- `symbols_list` (List[str]): Danh sách các mã chứng khoán cần lấy dữ liệu (bắt buộc)
- `flatten_columns` (bool, optional): Có phẳng hóa cột MultiIndex hay không (mặc định: False)
- `separator` (str, optional): Ký tự phân cách khi phẳng hóa cột (mặc định: '_')
- `drop_levels` (int|List[int], optional): Các level cần xóa khi phẳng hóa (mặc định: None)
- `to_df` (bool, optional): Trả về DataFrame hay raw data (mặc định: True)
- `show_log` (bool, optional): Hiển thị log chi tiết (mặc định: False)

```python
df = trading_vci.price_board(
    symbols_list=['VCB', 'ACB', 'TCB'],
    flatten_columns=True,
    drop_levels=[0]
)
```

**Trả về**: DataFrame với ~70 cột
- **Cột thông tin cơ bản**: `symbol`, `exchange` (HOSE/HNX/UPCOM)
- **Cột giá**: `match_price`, `ceiling_price`, `floor_price`, `reference_price`, `open_price`, `highest_price`, `lowest_price`, `average_price`
- **Cột khối lượng**: `accumulated_volume`, `match_volume`, `total_volume`, `total_buy_trade_volume`, `total_sell_trade_volume`
- **Cột giá trị**: `accumulated_value`, `match_value`, `total_value`, `total_buy_trade_value`, `total_sell_trade_value`
- **Cột nước ngoài**: `foreign_buy_volume`, `foreign_sell_volume`, `foreign_buy_value`, `foreign_sell_value`, `foreign_net_volume`, `foreign_net_value`
- **Cột lệnh**: `bid_1_price`, `bid_1_volume`, `bid_2_price`, `bid_2_volume`, `bid_3_price`, `bid_3_volume`, `ask_1_price`, `ask_1_volume`, `ask_2_price`, `ask_2_volume`, `ask_3_price`, `ask_3_volume`
- **Cột khác**: `trading_status`, `total_room`, `current_room`, `trading_date`

**Kiểu dữ liệu**:
- float64: Giá (`match_price`, `ceiling_price`, `floor_price`, v.v.), khối lượng trung bình
- int64: Khối lượng, giá trị
- object: `symbol`, `exchange`, `trading_status`

**Ví dụ** (3 mã VCB, ACB, TCB):
```
  symbol exchange  match_price  ceiling_price  floor_price  ... bid_1_price bid_1_volume ask_1_price ask_1_volume
0    VCB     HOSE        57500          61500        53500  ...       57200        50000       57300        43000
1    ACB     HOSE        24000          25650        22350  ...       23850       250000       23900       137300
2    TCB     HOSE        33200          35500        30900  ...       33300       100000       33350        69500
```

### price_history() - Lịch Sử Giá

Truy xuất lịch sử giá của mã chứng khoán theo các khoảng thời gian khác nhau (ngày, tuần, tháng, quý, năm).

**Tham số**:
- `resolution` (str, optional): Khoảng thời gian dữ liệu - '1D' (ngày), '1W' (tuần), '1M' (tháng), '1Q' (quý), '1Y' (năm) (mặc định: '1D')
- `start` (str, optional): Ngày bắt đầu định dạng YYYY-mm-dd (mặc định: None)
- `end` (str, optional): Ngày kết thúc định dạng YYYY-mm-dd (mặc định: None)
- `get_all` (bool, optional): Bao gồm cả dữ liệu giao dịch nước ngoài (fr_*) hay không (mặc định: False)
- `limit` (int, optional): Số lượng bản ghi tối đa trả về (mặc định: 100)

```python
df = trading_vci.price_history(
    start="2024-01-01",
    end="2024-12-31",
    resolution="1D"
)
```

**Trả về**: DataFrame với ~36 cột (khi `get_all=False`)
- **Cột giá**: `open`, `close`, `high`, `low`, `match_price`, `ceiling_price`, `floor_price`, `reference_price`, `average_price`
- **Cột giá điều chỉnh**: `reference_price_adjusted`, `open_price_adjusted`, `close_price_adjusted`, `highest_price_adjusted`, `lowest_price_adjusted`
- **Cột khối lượng**: `matched_volume`, `deal_volume`, `total_volume`, `total_buy_trade_volume`, `total_sell_trade_volume`, `average_buy_trade_volume`, `average_sell_trade_volume`, `total_net_trade_volume`
- **Cột giá trị**: `matched_value`, `deal_value`, `total_value`
- **Cột thống kê**: `price_change`, `percent_price_change`, `total_buy_trade`, `total_sell_trade`, `total_buy_unmatched_volume`, `total_sell_unmatched_volume`
- **Cột khác**: `trading_date`, `market_cap`, `total_shares`
- **Cột nước ngoài** (khi `get_all=True`): `fr_buy_volume`, `fr_sell_volume`, `fr_net_volume`, `fr_buy_value`, `fr_sell_value`, `fr_net_value`

**Kiểu dữ liệu**:
- float64: Giá, khối lượng, giá trị, phần trăm thay đổi
- int64: Số lượng giao dịch, khối lượng
- datetime64: `trading_date`

**Ví dụ** (VCB, 3 ngày gần nhất):
```
  trading_date   open   high    low  close  match_price  matched_volume  matched_value
0   2024-12-20  92500  93000  92300  92800        92800         1500000   139000000000
1   2024-12-19  93000  93500  92500  92600        92600         1200000   111000000000
2   2024-12-18  92800  93200  92300  93100        93100         1400000   130000000000
```

### summary() - Thống Kê Giao Dịch

Truy xuất thống kê tóm tắt giao dịch của mã chứng khoán.

**Tham số**:
- `resolution` (str, optional): Khoảng thời gian - '1D', '1W', '1M', '1Q', '1Y' (mặc định: '1D')
- `start` (str, optional): Ngày bắt đầu định dạng YYYY-mm-dd (mặc định: None)
- `end` (str, optional): Ngày kết thúc định dạng YYYY-mm-dd (mặc định: None)
- `limit` (int, optional): Số lượng bản ghi tối đa (mặc định: 100)

```python
df = trading_vci.summary(
    start="2024-01-01",
    end="2024-12-31",
    resolution="1D"
)
```

**Trả về**: DataFrame với các cột thống kê giao dịch
- **Cột giá**: `open`, `close`, `high`, `low`, `match_price`, `reference_price`
- **Cột khối lượng**: `matched_volume`, `deal_volume`, `total_volume`
- **Cột giá trị**: `matched_value`, `deal_value`, `total_value`
- **Cột nước ngoài**: `fr_buy_volume`, `fr_sell_volume`, `fr_net_volume`, `fr_buy_value`, `fr_sell_value`, `fr_net_value`
- **Cột khác**: `trading_date`, `price_change`, `percent_price_change`

**Kiểu dữ liệu**: float64 (giá, khối lượng, giá trị), datetime64 (`trading_date`)

### foreign_trade() - Giao Dịch Nước Ngoài

Truy xuất dữ liệu giao dịch nước ngoài của mã chứng khoán.

**Tham số**:
- `resolution` (str, optional): Khoảng thời gian - '1D', '1W', '1M', '1Q', '1Y' (mặc định: '1D')
- `start` (str, optional): Ngày bắt đầu định dạng YYYY-mm-dd (mặc định: None)
- `end` (str, optional): Ngày kết thúc định dạng YYYY-mm-dd (mặc định: None)
- `limit` (int, optional): Số lượng bản ghi tối đa (mặc định: 100)

```python
df = trading_vci.foreign_trade(
    start="2024-01-01",
    end="2024-12-31"
)
```

**Trả về**: DataFrame với các cột giao dịch nước ngoài
- **Cột khối lượng**: `fr_buy_volume`, `fr_sell_volume`, `fr_net_volume`
- **Cột giá trị**: `fr_buy_value`, `fr_sell_value`, `fr_net_value`
- **Cột khác**: `trading_date`

**Kiểu dữ liệu**: int64 (khối lượng), float64 (giá trị), datetime64 (`trading_date`)

**Ví dụ** (VCB, 3 ngày gần nhất):
```
  trading_date  fr_buy_volume  fr_sell_volume  fr_net_volume  fr_buy_value  fr_sell_value  fr_net_value
0   2024-12-20        100000         150000       -50000    9300000000    13950000000   -4650000000
1   2024-12-19         80000         120000       -40000    7440000000    11160000000   -3720000000
2   2024-12-18        120000         100000        20000   11160000000     9300000000    1860000000
```

### prop_trade() - Giao Dịch Tự Doanh

Truy xuất dữ liệu giao dịch tự doanh (proprietary trading) của mã chứng khoán.

**Tham số**:
- `resolution` (str, optional): Khoảng thời gian - '1D', '1W', '1M', '1Q', '1Y' (mặc định: '1D')
- `start` (str, optional): Ngày bắt đầu định dạng YYYY-mm-dd (mặc định: None)
- `end` (str, optional): Ngày kết thúc định dạng YYYY-mm-dd (mặc định: None)
- `limit` (int, optional): Số lượng bản ghi tối đa (mặc định: 100)

```python
df = trading_vci.prop_trade(
    start="2024-01-01",
    end="2024-12-31"
)
```

****Thông Tin Các Cột Dữ Liệu**

**1. Nguồn VCI**:
| Cột | Kiểu | Mô Tả |
|---|---|---|
| `trading_date` | datetime64 | Ngày giao dịch |
| `total_buy_trade_volume` | float64 | Tổng KL Tự doanh Mua |
| `total_sell_trade_volume` | float64 | Tổng KL Tự doanh Bán |
| `total_trade_net_volume` | float64 | Tổng KL Ròng |
| `total_match_buy_trade_volume` | float64 | KL Mua (Khớp lệnh) |
| `total_deal_buy_trade_volume` | float64 | KL Mua (Thoả thuận) |

**2. Nguồn CafeF**:
| Cột | Kiểu | Mô Tả |
|---|---|---|
| `prop_buy_volume`, `prop_buy_value` | int64 | KL & GT Mua |
| `prop_sell_volume`, `prop_sell_value` | int64 | KL & GT Bán |

**Ví dụ** (VCB, 3 ngày gần nhất):
```
  trading_date  prop_buy_volume  prop_sell_volume  prop_buy_value  prop_sell_value
0   2024-12-20          200000           180000   18600000000    16740000000
1   2024-12-19          150000           160000   13950000000    14880000000
2   2024-12-18          180000           170000   16740000000    15810000000
```

### insider_deal() - Giao Dịch Nội Bộ

Truy xuất dữ liệu giao dịch nội bộ (insider transactions) của mã chứng khoán.

**Tham số**:
- `limit` (int, optional): Số lượng bản ghi tối đa (mặc định: 100)
- `lang` (str, optional): Ngôn ngữ cột - 'vi' (Tiếng Việt) hoặc 'en' (Tiếng Anh) (mặc định: 'vi')

```python
df = trading_vci.insider_deal(limit=100, lang='vi')
```

****Thông Tin Các Cột Dữ Liệu**

**1. Nguồn VCI**:
| Cột | Kiểu | Mô Tả |
|---|---|---|
| `transaction_man` | object | Tên người giao dịch |
| `position` | object | Chức vụ |
| `relation_name` | object | Mối quan hệ |
| `icb_name` | object | Ngành |
| `real_buy_volume`, `real_sell_volume` | int64 | KL mua/bán thực tế |
| `real_buy_value`, `real_sell_value` | int64 | GT mua/bán thực tế |
| `buy_volume`, `sell_volume` | int64 | KL mua/bán đăng ký |
| `buy_value`, `sell_value` | int64 | GT mua/bán đăng ký |
| `start_date`, `end_date` | datetime64 | Ngày bắt đầu/kết thúc giao dịch |
| `public_date` | datetime64 | Ngày công bố thông tin |

**2. Nguồn CafeF**:
| Cột | Kiểu | Mô Tả |
|---|---|---|
| `time` | datetime | Ngày giao dịch (Index) |
| `transaction_man` | object | Tên người giao dịch |
| `position` | object | Chức vụ |
| `relation_name` | object | Mối quan hệ |
| `buy_volume`, `sell_volume` | int64 | KL mua/bán |
| `buy_value`, `sell_value` | int64 | GT mua/bán |
| `start_date`, `end_date` | datetime | Ngày bắt đầu/kết thúc giao dịch |

**Ví dụ** (VCB, 3 giao dịch gần nhất):
```
  transaction_man position  real_buy_volume  real_sell_volume public_date
0     Nguyễn Văn A   Giám đốc          10000                0  2024-12-15
1     Trần Thị B    Kế toán              0            5000  2024-12-10
2     Lê Văn C      Trưởng phòng       8000                0  2024-12-05
```

## Phương Thức CafeF

### price_history() - Lịch Sử Giá

```python
df = trading_cafef.price_history(
    start="2024-01-01",
    end="2024-12-31"
)
```

****Thông Tin Các Cột Dữ Liệu**

**1. Nguồn VCI**:
| Cột | Kiểu | Mô Tả |
|---|---|---|
| `trading_date` | datetime64 | Ngày giao dịch |
| `open`, `high`, `low`, `close` | float64 | Giá OHLC |
| `volume`, `value` | float64 | Khối lượng & Giá trị |
| `total_buy_trade`, `total_sell_trade` | float64 | Tổng số lệnh mua/bán (Chỉ VCI có) |
| `foreign_buy_volume_total`... | float64 | Các cột về giao dịch khối ngoại |

**2. Nguồn CafeF**:
| Cột | Kiểu | Mô Tả |
|---|---|---|
| `open`, `high`, `low`, `close` | float64 | Giá OHLC |
| `adjusted_price` | float64 | Giá điều chỉnh |
| `matched_volume`, `matched_value` | int64 | KL & Giá trị khớp lệnh |
| `deal_volume`, `deal_value` | int64 | KL & Giá trị thoả thuận |
| `change_pct` | float64 | % thay đổi giá |
| Index: `time` | datetime | Ngày giao dịch |

**Ví dụ** (3 ngày gần nhất VCB):
```
             open  high   low  close adjusted_price matched_volume matched_value  deal_volume  deal_value
time                                                                                                      
2024-11-29  92.6  93.3  92.5   93.3          61.96      1010500    93955000000        64600    5949660000
2024-11-28  93.1  93.5  92.5   92.6          61.49      1289900   120033000000        99000    9207000000
2024-11-27  92.3  93.2  92.3   92.7          61.56      1048309    97319490000            0             0
```

### order_stats() - Thống Kê Đặt Lệnh

```python
df = trading_cafef.order_stats(
    start="2024-01-01",
    end="2024-12-31"
)
```

Trả về: buy_orders, sell_orders, buy_volume, sell_volume, volume_diff, avg_buy_order_volume, avg_sell_order_volume

### foreign_trade() - Giao Dịch Nước Ngoài

```python
df = trading_cafef.foreign_trade(
    start="2024-01-01",
    end="2024-12-31"
)
```

**Trả về**: DataFrame với 8 cột (shape: N, 8)
- Cột khối lượng: `fr_buy_volume`, `fr_sell_volume`, `fr_net_volume`
- Cột giá trị: `fr_buy_value`, `fr_sell_value`, `fr_net_value`
- Cột khác: `fr_remaining_room` (phòng còn lại), `fr_ownership` (% sở hữu của nước ngoài)
- Kiểu dữ liệu: int64, float64
- Index: `time` (datetime)

**Ví dụ** (3 ngày gần nhất VCB):
```
            fr_buy_volume  fr_sell_volume  fr_net_volume  fr_buy_value  fr_sell_value  fr_net_value  fr_remaining_room  fr_ownership
time                                                                                                                                      
2024-11-29        51400         342600      -291200     4784820000    31851880000   -27067060000          381515749           23.17
2024-11-28        13000         663400      -650400     1211420000    61721750000   -60510330000          381113505           23.18
2024-11-27       160900         453500      -292600    14950780000    42087290000   -27136510000          380404163           23.19
```

### prop_trade() - Giao Dịch Tự Doanh

```python
df = trading_cafef.prop_trade(
    start="2024-01-01",
    end="2024-12-31"
)
```

**Trả về**: DataFrame với 4 cột (shape: N, 4)
- `prop_buy_volume`: Khối lượng mua tự doanh (int64)
- `prop_sell_volume`: Khối lượng bán tự doanh (int64)
- `prop_buy_value`: Giá trị mua tự doanh (int64 - VND)
- `prop_sell_value`: Giá trị bán tự doanh (int64 - VND)
- Index: `time` (datetime)

**Ví dụ** (3 ngày gần nhất VCB):
```
            prop_buy_volume  prop_sell_volume  prop_buy_value  prop_sell_value
time                                                                           
2024-11-29          118900           154700    11061620000      14372650000
2024-11-28          139200           188700    12968610000      17546430000
2024-11-27           96900           215800     8994070000      20018910000
```

### insider_deal() - Giao Dịch Nội Bộ

```python
df = trading_cafef.insider_deal(
    start="2024-01-01",
    end="2024-12-31"
)
```

**Trạng thái**: Dữ liệu có sẵn chỉ cho một số cổ phiếu và thời kỳ cụ thể.

### order_stats() - Thống Kê Đặt Lệnh

```python
df = trading_cafef.order_stats(
    start="2024-01-01",
    end="2024-12-31"
)
```

****Thông Tin Các Cột Dữ Liệu (CafeF Only)**

| Cột | Kiểu | Mô Tả |
|---|---|---|
| `buy_orders` | int64 | Số lệnh đặt mua |
| `sell_orders` | int64 | Số lệnh đặt bán |
| `buy_volume` | int64 | Tống khối lượng đặt mua |
| `sell_volume` | int64 | Tổng khối lượng đặt bán |
| `avg_buy_order_volume` | int64 | Trung bình KL/lệnh mua |
| `avg_sell_order_volume` | int64 | Trung bình KL/lệnh bán |
| Index: `time` | datetime | Ngày giao dịch |

**Ví dụ** (3 ngày gần nhất VCB):
```
            buy_orders  sell_orders  buy_volume  sell_volume  volume_diff  avg_buy_order_volume  avg_sell_order_volume
time                                                                                                                     
2024-11-29         869         1047    1715000      2094000      -379000              1974                   2000
2024-11-28        1501         2111    2053600      2610100      -556500              1368                   1236
2024-11-27         762         1190    2230500      1858700       371800              2927                   1562
```

```python
from vnstock_data import Trading

# VCI
trading_vci = Trading(source="vci", symbol="VCB")

# Bảng giá hiện tại
board = trading_vci.price_board(symbols_list=['VCB', 'ACB'])
print("Bảng giá:")
print(board[['symbol', 'match_price', 'total_volume']])

# Lịch sử giao dịch
history = trading_vci.price_history(start="2024-01-01", end="2024-12-31")
print(f"\nLịch sử giao dịch: {len(history)} dòng")

# CafeF
trading_cafef = Trading(source="cafef", symbol="VCB")

# Giao dịch nước ngoài
foreign = trading_cafef.foreign_trade(start="2024-01-01", end="2024-12-31")
print(f"\nGiao dịch nước ngoài:")
print(foreign[['fr_buy_volume', 'fr_sell_volume', 'fr_net_volume']].tail())

# Giao dịch tự doanh
prop = trading_cafef.prop_trade(start="2024-01-01", end="2024-12-31")
print(f"\nGiao dịch tự doanh:")
print(prop[['prop_buy_volume', 'prop_sell_volume']].tail())

# Giao dịch nội bộ
insider = trading_cafef.insider_deal(start="2024-01-01", end="2024-12-31")
print(f"\nGiao dịch nội bộ:")
print(insider[['transaction_man', 'real_buy_volume', 'real_sell_volume']])
```

## So Sánh VCI/KBS vs CafeF

| Dữ Liệu | VCI/KBS | CafeF |
|---|:---:|:---:|
| Giá lịch sử | ✅ | ✅ |
| Bảng giá realtime | ✅ | ❌ |
| Thống kê giao dịch | ✅ | ✅ |
| Nước ngoài | ✅ | ✅ |
| Tự doanh | ✅ | ✅ |
| Nội bộ | ✅ | ✅ |
| Thống kê đặt lệnh | ✅ | ✅ |

## Phân Tích Ví Dụ

```python
from vnstock_data import Trading

# Phân tích khối ngoại
trading = Trading(source="cafef", symbol="VCB")
foreign = trading.foreign_trade(start="2024-01-01", end="2024-12-31")

# Net volume nước ngoài
foreign['net_pct'] = foreign['fr_net_volume'] / (
    foreign['fr_buy_volume'] + foreign['fr_sell_volume']
)

print("Top ngày mua ròng nước ngoài:")
print(foreign.nlargest(5, 'fr_net_volume')[
    ['fr_buy_volume', 'fr_sell_volume', 'fr_net_volume']
])
```

## Ma Trận Phương Thức Hỗ Trợ

| Phương Thức | VCI | KBS | CafeF |
|---|:---:|:---:|:---:|
| price_board | ✅ (~70 cột) | ✅ | ❌ |
| price_history | ✅ (~36 cột, hỗ trợ 1D/1W/1M/1Q/1Y) | ✅ | ✅ (10 cột) |
| summary | ✅ (thống kê tóm tắt) | ✅ | ❌ |
| foreign_trade | ✅ (6 cột) | ✅ | ✅ (8 cột) |
| prop_trade | ✅ (4 cột) | ✅ | ✅ (4 cột) |
| insider_deal | ✅ (hỗ trợ VI/EN) | ✅ | ⚠️ (hiếm) |
| order_stats | ❌ | ❌ | ✅ (7 cột) |

## Ví Dụ Sử Dụng Toàn Diện

### VCI - Phân Tích Giao Dịch Toàn Diện

```python
from vnstock_data import Trading

# Khởi tạo
trading = Trading(source="vci", symbol="VCB")

# 1. Bảng giá realtime
board = trading.price_board(
    symbols_list=['VCB', 'ACB', 'TCB'],
    flatten_columns=True
)
print("Bảng giá realtime:")
print(board[['symbol', 'match_price', 'bid_1_price', 'ask_1_price', 'accumulated_volume']])

# 2. Lịch sử giá ngày
history = trading.price_history(
    start="2024-01-01",
    end="2024-12-31",
    resolution="1D"
)
print(f"\nLịch sử giá: {len(history)} dòng")
print(history[['trading_date', 'open', 'close', 'high', 'low', 'matched_volume']].head())

# 3. Thống kê giao dịch
summary = trading.summary(
    start="2024-01-01",
    end="2024-12-31",
    resolution="1D"
)
print(f"\nThống kê giao dịch: {len(summary)} dòng")

# 4. Giao dịch nước ngoài
foreign = trading.foreign_trade(
    start="2024-01-01",
    end="2024-12-31"
)
print("\nGiao dịch nước ngoài (3 ngày gần nhất):")
print(foreign[['trading_date', 'fr_buy_volume', 'fr_sell_volume', 'fr_net_volume']].tail(3))

# 5. Giao dịch tự doanh
prop = trading.prop_trade(
    start="2024-01-01",
    end="2024-12-31"
)
print("\nGiao dịch tự doanh (3 ngày gần nhất):")
print(prop[['trading_date', 'prop_buy_volume', 'prop_sell_volume']].tail(3))

# 6. Giao dịch nội bộ
insider = trading.insider_deal(limit=10, lang='vi')
print("\nGiao dịch nội bộ (10 giao dịch gần nhất):")
print(insider[['transaction_man', 'position', 'real_buy_volume', 'real_sell_volume', 'public_date']])
```

### Phân Tích Khối Ngoại

```python
from vnstock_data import Trading
import pandas as pd

trading = Trading(source="vci", symbol="VCB")

# Lấy dữ liệu giao dịch nước ngoài
foreign = trading.foreign_trade(
    start="2024-01-01",
    end="2024-12-31"
)

# Tính toán chỉ số
foreign['net_pct'] = (foreign['fr_net_volume'] / 
    (foreign['fr_buy_volume'] + foreign['fr_sell_volume']) * 100).round(2)

# Top ngày mua ròng
print("Top 5 ngày mua ròng nước ngoài:")
print(foreign.nlargest(5, 'fr_net_volume')[
    ['trading_date', 'fr_buy_volume', 'fr_sell_volume', 'fr_net_volume', 'net_pct']
])

# Top ngày bán ròng
print("\nTop 5 ngày bán ròng nước ngoài:")
print(foreign.nsmallest(5, 'fr_net_volume')[
    ['trading_date', 'fr_buy_volume', 'fr_sell_volume', 'fr_net_volume', 'net_pct']
])
```

### Phân Tích Giao Dịch Tự Doanh

```python
from vnstock_data import Trading

trading = Trading(source="vci", symbol="VCB")

# Lấy dữ liệu tự doanh
prop = trading.prop_trade(
    start="2024-01-01",
    end="2024-12-31"
)

# Tính toán
prop['prop_net_volume'] = prop['prop_buy_volume'] - prop['prop_sell_volume']
prop['prop_net_value'] = prop['prop_buy_value'] - prop['prop_sell_value']

# Phân tích
print("Thống kê giao dịch tự doanh:")
print(f"Tổng mua: {prop['prop_buy_volume'].sum():,} cổ phiếu")
print(f"Tổng bán: {prop['prop_sell_volume'].sum():,} cổ phiếu")
print(f"Net volume: {prop['prop_net_volume'].sum():,} cổ phiếu")
print(f"Net value: {prop['prop_net_value'].sum():,.0f} VND")

# Top ngày mua ròng
print("\nTop 5 ngày mua ròng tự doanh:")
print(prop.nlargest(5, 'prop_net_volume')[
    ['trading_date', 'prop_buy_volume', 'prop_sell_volume', 'prop_net_volume']
])
```

### So Sánh Dữ Liệu VCI vs CafeF

```python
from vnstock_data import Trading
import pandas as pd

# VCI
trading_vci = Trading(source="vci", symbol="VCB")
vci_history = trading_vci.price_history(
    start="2024-12-01",
    end="2024-12-31"
)

# CafeF
trading_cafef = Trading(source="cafef", symbol="VCB")
cafef_history = trading_cafef.price_history(
    start="2024-12-01",
    end="2024-12-31"
)

# So sánh
print("So sánh dữ liệu VCI vs CafeF:")
print(f"VCI: {len(vci_history)} dòng, {vci_history.shape[1]} cột")
print(f"CafeF: {len(cafef_history)} dòng, {cafef_history.shape[1]} cột")

# Cột chung
common_cols = set(vci_history.columns) & set(cafef_history.columns)
print(f"\nCột chung: {len(common_cols)} cột")
print(f"Cột riêng VCI: {len(set(vci_history.columns) - common_cols)} cột")
print(f"Cột riêng CafeF: {len(set(cafef_history.columns) - common_cols)} cột")
```

## Ghi Chú Quan Trọng

### Về Dữ Liệu VCI & KBS
- **Realtime**: `price_board()` cung cấp dữ liệu bảng giá realtime với độ trễ tối thiểu
- **Độ chính xác**: Dữ liệu từ VCI/KBS được cập nhật liên tục và có độ chính xác cao
- **Phạm vi thời gian**: Hỗ trợ lấy dữ liệu từ ngày (1D) đến năm (1Y)
- **Nước ngoài**: Dữ liệu giao dịch nước ngoài được tích hợp trong `price_history()` khi `get_all=True`
- **Tự doanh**: Dữ liệu tự doanh được cung cấp riêng biệt qua `prop_trade()` - hiện tại chỉ có VCI cung cấp.
- **Nội bộ**: Dữ liệu giao dịch nội bộ có thể không đầy đủ cho tất cả mã chứng khoán.
- **Lưu ý**: Dùng KBS khi chạy trên môi trường Cloud (Colab, Kaggle) để tránh chặn IP.

### Về Dữ Liệu CafeF
- **Bổ sung**: CafeF được sử dụng làm nguồn bổ sung khi VCI không có dữ liệu
- **Ổn định**: Dữ liệu có thể không đầy đủ hoặc ổn định như VCI, đôi khi thiếu dữ liệu cho những ngày cụ thể.
- **Nước ngoài**: Cung cấp thông tin chi tiết về phòng ngoại và sở hữu
- **Tự doanh**: Dữ liệu tự doanh được cung cấp riêng biệt
- **Nội bộ**: Dữ liệu giao dịch nội bộ hiếm khi có sẵn

### Xử Lý Lỗi
```python
from vnstock_data import Trading

try:
    trading = Trading(source="vci", symbol="VCB")
    data = trading.price_history(
        start="2024-01-01",
        end="2024-12-31"
    )
except ConnectionError as e:
    print(f"Lỗi kết nối: {e}")
except ValueError as e:
    print(f"Lỗi giá trị: {e}")
```
