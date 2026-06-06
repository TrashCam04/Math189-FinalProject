import pandas as pd
from pathlib import Path

RAW_FILE = "../data/US_Accidents_March23.csv"
OUTPUT_FILE = "../data/accidents_200k.csv"

cols = [
    "Severity",
    "State",
    "County",
    "Start_Time",
    "Temperature(F)",
    "Humidity(%)",
    "Visibility(mi)",
    "Wind_Speed(mph)",
    "Precipitation(in)",
    "Weather_Condition",
    "Sunrise_Sunset",
    "Junction",
    "Traffic_Signal",
    "Railway",
    "Crossing",
    "Stop",
    "Roundabout",
]

df = pd.read_csv(RAW_FILE, usecols=cols)

df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors="coerce")

df["Year"] = df["Start_Time"].dt.year
df["Month"] = df["Start_Time"].dt.month
df["Hour"] = df["Start_Time"].dt.hour
df["DayOfWeek"] = df["Start_Time"].dt.dayofweek

df = df.drop(columns=["Start_Time"])

df = df.dropna(subset=["Severity", "State", "County"])

df = df.sample(n=200_000, random_state=42)

df.to_csv(OUTPUT_FILE, index=False)