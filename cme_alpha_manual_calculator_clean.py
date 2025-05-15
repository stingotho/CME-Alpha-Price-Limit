
import streamlit as st
from datetime import datetime
import pytz

st.set_page_config(page_title="CME + Alpha Manual Calculator", layout="centered")

st.title("📉 CME + Alpha Futures Manual Limit Calculator")
st.markdown("Paste a reference price and calculate **Alpha upper/lower limits (±5%)**.")

# CME Reference Links
with st.expander("📘 CME References"):
    st.markdown("- [CME Price Limit Guide](https://www.cmegroup.com/trading/price-limits.html#equityIndex)")
    st.markdown("- [Alpha Futures Trading Rule](https://help.alpha-futures.com/en/articles/9806068-price-limit-trading)")

# Manual refresh clock
if st.button("🔁 Refresh Clock"):
    st.rerun()

# Clock
ct = pytz.timezone("America/Chicago")
now_ct = datetime.now(ct)
current_time = now_ct.strftime("%H:%M:%S")
st.markdown(f"### 🕒 Current Time (CT): `{current_time}`")

# New York Session status (8:30 a.m. to 2:25 p.m. CT)
ny_start = now_ct.replace(hour=8, minute=30, second=0, microsecond=0)
ny_end = now_ct.replace(hour=14, minute=25, second=0, microsecond=0)
if ny_start <= now_ct <= ny_end:
    st.success("🟢 New York Session Active - Upside limit lifted")
else:
    st.error("🔴 Outside New York Session - Upside capped")

st.markdown("---")

st.markdown("### 📝 Paste CME Contract & Reference Price")

col1, col2 = st.columns(2)
with col1:
    contract_name = st.text_input("Contract Name", placeholder="e.g., E-mini Nasdaq-100 Futures")
with col2:
    reference_price_input = st.text_input("Reference Price", placeholder="e.g., 18556.00")

calculate = st.button("📊 Calculate Alpha Limits")

if calculate and reference_price_input:
    try:
        reference_price = float(reference_price_input)
        alpha_upper = reference_price * 1.05
        alpha_lower = reference_price * 0.95

        st.markdown(f"### ✅ Alpha Upper (5%): `{alpha_upper:,.2f}`", unsafe_allow_html=True)
        st.markdown(f"### ✅ Alpha Lower (5%): `{alpha_lower:,.2f}`", unsafe_allow_html=True)

        st.markdown("### 🧠 Formula Reference")
        st.code("""
Alpha Upper = Reference Price × 1.05
Alpha Lower = Reference Price × 0.95
        """, language="python")
    except ValueError:
        st.error("Please enter a valid number for the reference price.")
elif calculate:
    st.warning("Please enter a reference price before calculating.")
