import streamlit as st
import pandas as pd
import datetime as dt


def build_monthly_overview(df: pd.DataFrame) -> pd.DataFrame:
    monthly_overview = df.groupby("year_month")[
        ["Heart rate variability (ms)", "Asleep duration (min)", "Resting heart rate (bpm)", "Sleep consistency %",
         "Skin temp (celsius)"]].mean().reset_index()
    monthly_overview["Month"] = monthly_overview["year_month"].astype(str)
    monthly_overview.set_index("Month", inplace=True)
    monthly_overview["Avg. Asleep Duration (h)"] = monthly_overview["Asleep duration (min)"].apply(
        lambda x: dt.time(hour=int(x // 60), minute=int(x % 60)))
    monthly_overview.rename(
        columns={"Heart rate variability (ms)": "Avg. HRV", "Resting heart rate (bpm)": "Avg. RHR",
                 "Sleep consistency %": "Avg. Sleep Consistency (%)",
                 "Skin temp (celsius)": "Avg. Skin temp (celsius)"},
        inplace=True)
    monthly_overview["Avg. HRV"] = monthly_overview["Avg. HRV"].apply(lambda x: round(x, 1))
    monthly_overview["Avg. RHR"] = monthly_overview["Avg. RHR"].apply(lambda x: round(x, 1))
    monthly_overview["Avg. Skin temp (celsius)"] = monthly_overview["Avg. Skin temp (celsius)"].apply(
        lambda x: round(x, 1))
    monthly_overview["Avg. Sleep Consistency (%)"] = monthly_overview["Avg. Sleep Consistency (%)"].apply(
        lambda x: round(x, 1))
    monthly_overview = monthly_overview[
        ['Avg. RHR', 'Avg. HRV', 'Avg. Asleep Duration (h)', 'Avg. Sleep Consistency (%)', "Avg. Skin temp (celsius)"]]
    return monthly_overview


if "df" in st.session_state:
    st.title("Monthly Metrics")
    monthly_overview = build_monthly_overview(st.session_state.df)

    Months = monthly_overview.index.tolist()
    months_slider = st.select_slider(
        "Select the months to display",
        Months,
        value=(Months[0], Months[-1])
    )

    st.write("### Overview by Month")
    monthly_overview = monthly_overview.loc[months_slider[0]:months_slider[1]]
    st.write(monthly_overview.transpose())

    df_monthly = st.session_state.df.loc[(st.session_state.df["year_month"] >= months_slider[0]) & (
                st.session_state.df["year_month"] <= months_slider[1])].groupby("year_month")

    st.write("### Sleep Duration by Month")
    avg_sleep_by_month = df_monthly[
        "Asleep duration (min)"].mean().reset_index()
    avg_sleep_by_month["Asleep duration (h)"] = avg_sleep_by_month["Asleep duration (min)"] / 60
    st.bar_chart(avg_sleep_by_month, x="year_month", y="Asleep duration (h)")
    st.write("### Sleep Consistency by Month")
    avg_sleep_consistency_by_month = df_monthly[
        "Sleep consistency %"].mean().reset_index()
    st.bar_chart(avg_sleep_consistency_by_month, x="year_month", y="Sleep consistency %")
    st.write("### HRV by Month")
    avg_hrv_by_month = df_monthly["Heart rate variability (ms)"].mean().reset_index()
    st.bar_chart(avg_hrv_by_month, x="year_month", y="Heart rate variability (ms)")
    st.write("### RHR by Month")
    avg_rhr_by_month = df_monthly["Resting heart rate (bpm)"].mean().reset_index()
    st.bar_chart(avg_rhr_by_month, x="year_month", y="Resting heart rate (bpm)")
    st.write("### Skin Temperature by Month")
    avg_temperature_by_month = df_monthly["Skin temp (celsius)"].mean().reset_index()
    st.bar_chart(avg_temperature_by_month, x="year_month", y="Skin temp (celsius)")

    st.write("## Share of Good, Bad, and Okay Nights")
    night_counts_by_score = df_monthly["Night Score"].value_counts().unstack()
    night_counts_by_score.fillna(0, inplace=True)
    night_counts_by_score["Total"] = night_counts_by_score.sum(axis=1)
    for ix, score in enumerate(["Good", "Okay", "Bad"]):
        night_counts_by_score["{}) Share of {} Nights".format(ix + 1, score)] = night_counts_by_score[score] / \
                                                                                night_counts_by_score["Total"]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("### Good Nights (7+ hours)")
        st.bar_chart(night_counts_by_score.reset_index(), x="year_month", y="1) Share of Good Nights")
    with col2:
        st.write("### Okay Nights (6-7h hours)")
        st.bar_chart(night_counts_by_score.reset_index(), x="year_month", y="2) Share of Okay Nights")
    with col3:
        st.write("### Bad Nights (<6 hours)")
        st.bar_chart(night_counts_by_score.reset_index(), x="year_month", y="3) Share of Bad Nights")
else:
    st.warning("No data to analyze yet. Please upload your WHOOP export in the Home tab.", icon="📁")
