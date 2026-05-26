import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 株価変動ランキング（指定期間）")

# --- 入力 ---
symbols_text = st.text_area(
    "銘柄コード（改行区切り）",
    "6758.T\n7974.T\n9984.T\n7203.T"
)

period = st.selectbox(
    "期間を選択",
    ["1mo", "3mo", "6mo", "1y", "2y"]
)

threshold = st.number_input(
    "抽出する変動率（％）の閾値（絶対値）",
    value=10.0
)

symbols = [s.strip() for s in symbols_text.split("\n") if s.strip()]

if st.button("分析する"):
    results = []

    for symbol in symbols:
        try:
            df = yf.download(symbol, period=period, interval="1d", auto_adjust=True)

            if len(df) < 2:
                continue

            start_price = df["Close"].iloc[0]
            end_price = df["Close"].iloc[-1]

            change_pct = (end_price - start_price) / start_price * 100

            results.append({
                "symbol": symbol,
                "start": start_price,
                "end": end_price,
                "change_pct": float(change_pct.iloc[-1])
            })

        except Exception as e:
            st.error(f"{symbol} の取得でエラー: {e}")

    if results:
        df_result = pd.DataFrame(results)
        df_result = df_result.sort_values("change_pct", ascending=False)

        st.subheader("📊 変動率ランキング")
        st.dataframe(df_result)

        # 閾値で抽出
        extracted = df_result[ df_result["change_pct"].abs() >= threshold ]

        st.subheader(f"📌 変動率 ±{threshold}% 以上の銘柄")
        st.dataframe(extracted)

    else:
        st.warning("データが取得できませんでした。")
