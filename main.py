import streamlit as st
import pandas as pd
import datetime as dt

st.set_page_config(layout="wide")
st.title("📈 Deeper WHOOP Analytics")
st.caption("Go beyond the basic analytics in the WHOOP app.")

st.write("## 1) Get your data export from WHOOP")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("1a) Go to the 'More' tab & click on 'App Settings'")
    st.image("screenshots/IMG_3300.jpg")
with col2:
    st.write("1b) Click on 'Data Export'")
    st.image("screenshots/IMG_3301.jpg")
with col3:
    st.write("1c) Click on 'Create Export'")
    st.image("screenshots/IMG_3302.PNG")

st.write("Within a few minutes, you will receive an email with a zip file. Unpack the file and upload 2 of the csv files below.")

st.write("## 2) Upload your WHOOP export")
sleeps_file = st.file_uploader("Choose your sleeps.csv file")
physiological_cycles_file = st.file_uploader("Choose your physiological_cycles.csv file")


def get_night_score(sleep_duration_in_minutes: int) -> str:
    if sleep_duration_in_minutes < 6 * 60:
        return "Bad"
    elif sleep_duration_in_minutes < 7 * 60:
        return "Okay"
    else:
        return "Good"


def get_granular_night_score(sleep_duration_in_minutes: int) -> str:
    if sleep_duration_in_minutes < 4 * 60:
        return "Terrible"
    elif sleep_duration_in_minutes < 5 * 60:
        return "Very Bad"
    elif sleep_duration_in_minutes < 6 * 60:
        return "Bad"
    elif sleep_duration_in_minutes < 7 * 60:
        return "Okay"
    elif sleep_duration_in_minutes < 8 * 60:
        return "Good"
    else:
        return "Great"


MONTHS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

ISO_WEEKDAYS = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}


def remove_naps(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["Nap"] == False]


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


if sleeps_file is not None and physiological_cycles_file is not None:
    physiological_cycles_df = pd.read_csv(physiological_cycles_file)

    df = pd.read_csv(sleeps_file)
    df = df.loc[df['Asleep duration (min)'].notna()]
    df = remove_naps(df)
    df["date_dt"] = df["Wake onset"].apply(lambda x: dt.datetime.strptime(x[:10], '%Y-%m-%d'))

    df = pd.merge(df, physiological_cycles_df, on="Wake onset", how="left", suffixes=("", "_y"))

    df["Night Score"] = df["Asleep duration (min)"].apply(get_night_score)
    df["Granular Night Score"] = df["Asleep duration (min)"].apply(get_granular_night_score)
    df["weekday_num"] = df.date_dt.apply(lambda x: x.isoweekday())
    df["Day of Week"] = df["weekday_num"].apply(lambda x: ISO_WEEKDAYS[x])
    df["month_num"] = df.date_dt.apply(lambda x: x.month)
    df["Month"] = df.month_num.apply(lambda x: MONTHS[x])
    df["Year"] = df.date_dt.apply(lambda x: x.year)
    df["year_month"] = df.apply(
        lambda x: "{}-{}".format(x["Year"], x["month_num"]) if x["month_num"] >= 10 else "{}-0{}".format(x["Year"], x[
            "month_num"]), axis=1)
    df["Asleep Duration (h)"] = df["Asleep duration (min)"].apply(
        lambda x: dt.time(hour=int(x // 60), minute=int(x % 60)))

    st.write("## Overview by Year")
    annual_overview = build_annual_overview(df)
    st.write(annual_overview.transpose())


    col1, col2, col3, col4 = st.columns(4)
    annual_overview.reset_index(inplace=True)
    annual_overview["Year"] = annual_overview["Year"].astype(int)
    with col1:
        st.write("### Avg. Sleep Duration")
        st.bar_chart(df.groupby("Year")["Asleep duration (min)"].mean().reset_index(), x="Year",
                     y="Asleep duration (min)")
    with col2:
        st.write("### Avg. Sleep Consistency")
        st.bar_chart(df.groupby("Year")["Sleep consistency %"].mean().reset_index(), x="Year",
                     y="Sleep consistency %")
    with col3:
        st.write("### Avg. HRV")
        st.bar_chart(df.groupby("Year")["Heart rate variability (ms)"].mean().reset_index(), x="Year",
                     y="Heart rate variability (ms)")
    with col4:
        st.write("### Avg. RHR")
        st.bar_chart(df.groupby("Year")["Resting heart rate (bpm)"].mean().reset_index(), x="Year",
                     y="Resting heart rate (bpm)")

    st.write("## Last 30 Days")
    st.bar_chart(df.head(30), x="date_dt", y="Asleep duration (min)")
    st.line_chart(df.head(30), x="date_dt", y="Skin temp (celsius)")

    st.write("## Overview by Month")
    monthly_overview = build_monthly_overview(df)
    st.write(monthly_overview.transpose())

    st.write("### Sleep Duration by Month")
    avg_sleep_by_month = df.groupby("year_month")["Asleep duration (min)"].mean().reset_index()
    avg_sleep_by_month["Asleep duration (h)"] = avg_sleep_by_month["Asleep duration (min)"].apply(
        lambda x: dt.time(hour=int(x // 60), minute=int(x % 60)))
    st.bar_chart(avg_sleep_by_month, x="year_month", y="Asleep duration (min)")

    st.write("### Sleep Consistency by Month")
    avg_sleep_consistency_by_month = df.groupby("year_month")["Sleep consistency %"].mean().reset_index()
    st.line_chart(avg_sleep_consistency_by_month, x="year_month", y="Sleep consistency %")
    st.write("### HRV by Month")
    avg_hrv_by_month = df.groupby("year_month")["Heart rate variability (ms)"].mean().reset_index()
    st.line_chart(avg_hrv_by_month, x="year_month", y="Heart rate variability (ms)")
    st.write("### RHR by Month")
    avg_rhr_by_month = df.groupby("year_month")["Resting heart rate (bpm)"].mean().reset_index()
    st.line_chart(avg_rhr_by_month, x="year_month", y="Resting heart rate (bpm)")
    st.write("### Skin Temperature by Month")
    avg_temperature_by_month = df.groupby("year_month")["Skin temp (celsius)"].mean().reset_index()
    st.line_chart(avg_temperature_by_month, x="year_month", y="Skin temp (celsius)")

    st.write("## Share of Good, Bad, and Okay Nights")
    night_counts_by_score = df.groupby("year_month")["Night Score"].value_counts().unstack()
    night_counts_by_score.fillna(0, inplace=True)
    night_counts_by_score["Total"] = night_counts_by_score.sum(axis=1)
    for ix, score in enumerate(["Good", "Okay", "Bad"]):
        night_counts_by_score["{}) Share of {} Nights".format(ix+1, score)] = night_counts_by_score[score] / night_counts_by_score["Total"]
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