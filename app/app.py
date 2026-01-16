import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/model_output.csv")
    return df

df = load_data()

# ---------------------------
# Page title
# ---------------------------

st.title("📊 Macro Indicators & Market Direction Dashboard")

st.markdown("""
This dashboard analyses how macroeconomic indicators such as inflation,
interest rates, unemployment, and market volatility relate to
equity market direction.  

The predictions are generated using a logistic regression model trained
on historical data.
""")

# ---------------------------
# Latest metrics
# ---------------------------

latest = df.iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric("VIX (Volatility)", round(latest["vix"], 2))
col2.metric("Unemployment Rate", round(latest["unemployment"], 2))
col3.metric(
    "Predicted Market Direction",
    "UP 📈" if latest["predicted_direction"] == 1 else "DOWN 📉"
)

# ---------------------------
# Prediction confidence
# ---------------------------

st.subheader("📈 Model Confidence")

st.progress(float(latest["predicted_prob_up"]))

st.write(
    f"**Probability that the market goes UP next month:** "
    f"{latest['predicted_prob_up']:.2%}"
)

# ---------------------------
# Volatility vs returns
# ---------------------------

st.subheader("📉 Volatility vs SPY Monthly Returns")

fig, ax = plt.subplots()
ax.scatter(df["vix"], df["spy_return"], alpha=0.4)
ax.set_xlabel("VIX (Market Volatility)")
ax.set_ylabel("SPY Monthly Return")

st.pyplot(fig)

# ---------------------------
# Time-series view
# ---------------------------

st.subheader("📅 Predicted Market Direction Over Time")

st.line_chart(
    df.set_index("month")[["predicted_prob_up"]]
)