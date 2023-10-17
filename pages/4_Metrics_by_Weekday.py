import streamlit as st
import pandas as pd
import datetime as dt

WEEKDAY_TO_ISO_INDEX = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}

WEEKDAY_TO_WEEKDAY_NUM_AND_NAME = {
    "Monday": "1) Monday",
    "Tuesday": "2) Tuesday",
    "Wednesday": "3) Wednesday",
    "Thursday": "4) Thursday",
    "Friday": "5) Friday",
    "Saturday": "6) Saturday",
    "Sunday": "7) Sunday"
}

if "df" in st.session_state:
    st.title("Metrics by Weekday")

    days = sorted(st.session_state.df.Date.tolist())
    first_day = min(days)
    last_day = max(days)
    days_slider = st.select_slider(
        "Select the days to include in the analysis",
        days,
        value=(first_day, last_day)
    )

    df_by_weekday = st.session_state.df.loc[
        (st.session_state.df["Date"] >= days_slider[0]) & (st.session_state.df["Date"] <= days_slider[1])].groupby("Day of Week")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Avg. Sleep Duration")
        avg_sleep_by_weekday = df_by_weekday["Asleep duration (min)"].mean().reset_index()
        avg_sleep_by_weekday["Weekday"] = avg_sleep_by_weekday["Day of Week"].apply(lambda x: WEEKDAY_TO_WEEKDAY_NUM_AND_NAME[x])
        st.bar_chart(avg_sleep_by_weekday, x="Weekday", y="Asleep duration (min)")

    with col2:
        st.write("### Avg. Sleep Consistency")
        avg_sleep_consistency_by_weekday = df_by_weekday["Sleep consistency %"].mean().reset_index()
        avg_sleep_consistency_by_weekday["Weekday"] = avg_sleep_consistency_by_weekday["Day of Week"].apply(lambda x: WEEKDAY_TO_WEEKDAY_NUM_AND_NAME[x])
        st.bar_chart(avg_sleep_consistency_by_weekday, x="Weekday", y="Sleep consistency %")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Avg. HRV")
        avg_hrv_by_weekday = df_by_weekday["Heart rate variability (ms)"].mean().reset_index()
        avg_hrv_by_weekday["Weekday"] = avg_hrv_by_weekday["Day of Week"].apply(lambda x: WEEKDAY_TO_WEEKDAY_NUM_AND_NAME[x])
        st.bar_chart(avg_hrv_by_weekday, x="Weekday", y="Heart rate variability (ms)")

    with col2:
        st.write("### Avg. RHR")
        avg_rhr_by_weekday = df_by_weekday["Resting heart rate (bpm)"].mean().reset_index()
        avg_rhr_by_weekday["Weekday"] = avg_rhr_by_weekday["Day of Week"].apply(lambda x: WEEKDAY_TO_WEEKDAY_NUM_AND_NAME[x])
        st.bar_chart(avg_rhr_by_weekday, x="Weekday", y="Resting heart rate (bpm)")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Avg. Skin Temperature")
        avg_skin_temp_by_weekday = df_by_weekday["Skin temp (celsius)"].mean().reset_index()
        avg_skin_temp_by_weekday["Weekday"] = avg_skin_temp_by_weekday["Day of Week"].apply(lambda x: WEEKDAY_TO_WEEKDAY_NUM_AND_NAME[x])
        st.bar_chart(avg_skin_temp_by_weekday, x="Weekday", y="Skin temp (celsius)")

    with col2:
        st.write("### Avg. Recovery")
        avg_recovery_by_weekday = df_by_weekday["Recovery score %"].mean().reset_index()
        avg_recovery_by_weekday["Weekday"] = avg_recovery_by_weekday["Day of Week"].apply(lambda x: WEEKDAY_TO_WEEKDAY_NUM_AND_NAME[x])
        st.bar_chart(avg_recovery_by_weekday, x="Weekday", y="Recovery score %")

else:
    st.warning("No data to analyze yet. Please upload your WHOOP export in the Home tab.", icon="📁")