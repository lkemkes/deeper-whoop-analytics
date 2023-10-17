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
col1, col2 = st.columns(2)
with col1:
    sleeps_file = st.file_uploader("Choose your sleeps.csv file")
with col2:
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


if sleeps_file is not None and physiological_cycles_file is not None:
    st.balloons()
    physiological_cycles_df = pd.read_csv(physiological_cycles_file)

    df = pd.read_csv(sleeps_file)
    df = df.loc[df['Asleep duration (min)'].notna()]
    df = remove_naps(df)
    df["date_dt"] = df["Wake onset"].apply(lambda x: dt.datetime.strptime(x[:10], '%Y-%m-%d'))
    df["Date"] = df["Wake onset"].apply(lambda x: x[:10])

    df = pd.merge(df, physiological_cycles_df, on="Wake onset", how="left", suffixes=("", "_y"))

    if "df" not in st.session_state:
        st.session_state.df = df

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

    st.session_state.df = df