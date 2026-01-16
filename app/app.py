import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


@st.cache_data
def load_data():
    df = pd.read_csv("data/model_output.csv")
    return df

df = load_data()

st.set_page_config(
    page_title="Macro Indicators & Market Direction",
    layout="wide"
)

st.title("📊 Macro Indicators & Market Direction Dashboard")

st.markdown("""
This dashboard analyses how macroeconomic indicators such as inflation,
interest rates, unemployment, and market volatility relate to
equity market direction.  

The predictions are generated using a logistic regression model trained
on historical data.
""")


latest = df.iloc[-1]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("VIX (Volatility)", f"{latest['vix']:.2f}")

with col2:
    st.metric("Unemployment Rate", f"{latest['unemployment']:.1f}")

with col3:
    st.metric(
        "Predicted Market Direction",
        "UP 📈" if latest["predicted_prob_up"] > 0.5 else "DOWN 📉"
    )
    
st.subheader("📈 Model Confidence")

st.progress(float(latest["predicted_prob_up"]))

st.write(
    f"**Probability that the market goes UP next month:** "
    f"{latest['predicted_prob_up']:.2%}"
)

# Volatility vs returns

st.subheader("📉 Volatility vs SPY Monthly Returns")

fig, ax = plt.subplots()
ax.scatter(df["vix"], df["spy_return"], alpha=0.4)
ax.set_xlabel("VIX (Market Volatility)")
ax.set_ylabel("SPY Monthly Return")

st.pyplot(fig)

# Time-series view

st.subheader("📅 Predicted Market Direction Over Time")

st.line_chart(
    df.set_index("month")[["predicted_prob_up"]]
)