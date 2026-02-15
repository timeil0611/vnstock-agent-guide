from vnstock import Quote
import pandas as pd

def fetch_index_2026(index_symbol="^VNI", interval="1D"):
    """
    抓取越南股市指数 2026 年数据
    
    参数:
        index_symbol: "^VNI" (VN-Index), "^HNX" (HNX-Index), 
                     "VN30", "VNMID", "VNSML" 等
        interval: "1D" (日线), "1H" (小时线), "5m" (5分钟线)
    """
    try:
        # 初始化 Quote API
        quote = Quote(symbol=index_symbol, source="KBS")
        
        # 获取 2026 年数据
        df = quote.history(
            start="2026-01-01",
            end="2026-12-31",
            interval=interval
        )
        
        print(f"✅ 成功获取 {index_symbol} 数据：{len(df)} 条记录")
        print("\n前 5 条数据:")
        print(df[['time', 'open', 'high', 'low', 'close', 'volume']].head())
        
        return df
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    # 获取 VN-Index 2026 年日线数据
    vn_index = fetch_index_2026("^VNI", "1D")
    
    # 获取 HNX-Index 数据
    hnx_index = fetch_index_2026("^HNX", "1D")
    
    # 获取 VN30 数据
    vn30 = fetch_index_2026("VN30", "1D")