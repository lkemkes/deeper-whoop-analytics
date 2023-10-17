import streamlit as st
import pandas as pd
import datetime as dt

if "df" in st.session_state:
    st.title("Daily Metrics")

    days = sorted(st.session_state.df.Date.tolist())
    first_day = min(days)
    last_day = max(days)
    days_slider = st.select_slider(
        "Select the days to display",
        days,
        value=(first_day, last_day)
    )

    df_daily = st.session_state.df.loc[
        (st.session_state.df["Date"] >= days_slider[0]) & (st.session_state.df["Date"] <= days_slider[1])]

    st.write("### Sleep Duration")
    df_daily["Asleep duration (h)"] = df_daily["Asleep duration (min)"] / 60
    st.bar_chart(df_daily, x="date_dt", y="Asleep duration (h)")

    st.write("### Sleep Consistency")
    st.bar_chart(df_daily, x="date_dt", y="Sleep consistency %")

    st.write("### HRV")
    st.bar_chart(df_daily, x="date_dt", y="Heart rate variability (ms)")

    st.write("### RHR")
    st.bar_chart(df_daily, x="date_dt", y="Resting heart rate (bpm)")

    st.write("### Skin Temperature")
    st.bar_chart(df_daily, x="date_dt", y="Skin temp (celsius)")

else:
    st.warning("No data to analyze yet. Please upload your WHOOP export in the Home tab.", icon="📁")
