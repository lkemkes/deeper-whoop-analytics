import streamlit as st
import pandas as pd
import datetime as dt


def build_annual_overview(df: pd.DataFrame) -> pd.DataFrame:
    annual_overview = df.groupby("Year")[
        ["Heart rate variability (ms)", "Asleep duration (min)", "Resting heart rate (bpm)",
         "Sleep consistency %"]].mean().reset_index()
    annual_overview["Year"] = annual_overview["Year"].astype(str)
    annual_overview.set_index("Year", inplace=True)
    annual_overview["Avg. Asleep Duration (h)"] = annual_overview["Asleep duration (min)"].apply(
        lambda x: dt.time(hour=int(x // 60), minute=int(x % 60)))
    annual_overview.rename(
        columns={"Heart rate variability (ms)": "Avg. HRV", "Resting heart rate (bpm)": "Avg. RHR",
                 "Sleep consistency %": "Avg. Sleep Consistency (%)"},
        inplace=True)
    annual_overview["Avg. HRV"] = annual_overview["Avg. HRV"].apply(lambda x: round(x, 1))
    annual_overview["Avg. RHR"] = annual_overview["Avg. RHR"].apply(lambda x: round(x, 1))
    annual_overview["Avg. Sleep Consistency (%)"] = annual_overview["Avg. Sleep Consistency (%)"].apply(
        lambda x: round(x, 1))
    annual_overview = annual_overview[
        ['Avg. RHR', 'Avg. HRV', 'Avg. Asleep Duration (h)', 'Avg. Sleep Consistency (%)']]
    return annual_overview


if "df" in st.session_state:
    st.title("Annual Metrics")
    annual_overview = build_annual_overview(st.session_state.df)
    st.write(annual_overview.transpose())

    col1, col2 = st.columns(2)
    annual_overview.reset_index(inplace=True)
    annual_overview["Year"] = annual_overview["Year"].astype(int)
    with col1:
        st.write("### Avg. Sleep Duration")
        st.bar_chart(st.session_state.df.groupby("Year")["Asleep duration (min)"].mean().reset_index(), x="Year",
                     y="Asleep duration (min)")
    with col2:
        st.write("### Avg. Sleep Consistency")
        st.bar_chart(st.session_state.df.groupby("Year")["Sleep consistency %"].mean().reset_index(), x="Year",
                     y="Sleep consistency %")

    col1, col2 = st.columns(2)
    with col1:
        st.write("### Avg. HRV")
        st.bar_chart(st.session_state.df.groupby("Year")["Heart rate variability (ms)"].mean().reset_index(), x="Year",
                     y="Heart rate variability (ms)")
    with col2:
        st.write("### Avg. RHR")
        st.bar_chart(st.session_state.df.groupby("Year")["Resting heart rate (bpm)"].mean().reset_index(), x="Year",
                     y="Resting heart rate (bpm)")

else:
    st.warning("No data to analyze yet. Please upload your WHOOP export in the Home tab.", icon="📁")