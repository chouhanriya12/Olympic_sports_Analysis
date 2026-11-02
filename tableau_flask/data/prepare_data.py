"""
Olympic Data Preparation Script
================================
This script downloads a sample Olympic dataset, cleans it,
computes statistics, and saves the cleaned CSV.

Run this once before starting the Flask app:
    python data/prepare_data.py
"""

import os
import json
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# 1. Load dataset
# ─────────────────────────────────────────────
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_CSV = os.path.join(DATA_DIR, "olympics_raw.csv")
CLEAN_CSV = os.path.join(DATA_DIR, "olympics.csv")
STATS_JSON = os.path.join(DATA_DIR, "stats.json")

def load_data():
    """Load the raw CSV. If not present, create a representative sample."""
    if os.path.exists(RAW_CSV):
        print(f"Loading existing raw file: {RAW_CSV}")
        df = pd.read_csv(RAW_CSV)
    elif os.path.exists(CLEAN_CSV):
        print(f"Loading existing cleaned file: {CLEAN_CSV}")
        df = pd.read_csv(CLEAN_CSV)
    else:
        print("No dataset found — generating built-in sample dataset …")
        df = generate_sample_dataset()
    return df


def generate_sample_dataset():
    """
    Generate a representative Olympic dataset that mirrors the
    Kaggle '120 years of Olympic history: athletes and results' schema.

    Columns: ID, Name, Sex, Age, Height, Weight, Team, NOC,
             Games, Year, Season, City, Sport, Event, Medal
    """
    np.random.seed(42)

    countries = {
        "USA": "United States", "RUS": "Russia", "GER": "Germany",
        "GBR": "Great Britain", "FRA": "France", "CHN": "China",
        "AUS": "Australia", "ITA": "Italy", "JPN": "Japan",
        "KOR": "South Korea", "NED": "Netherlands", "CAN": "Canada",
        "SWE": "Sweden", "HUN": "Hungary", "NOR": "Norway",
        "FIN": "Finland", "DEN": "Denmark", "POL": "Poland",
        "BRA": "Brazil", "CUB": "Cuba", "ROM": "Romania",
        "BUL": "Bulgaria", "CZE": "Czech Republic", "KEN": "Kenya",
        "ETH": "Ethiopia", "JAM": "Jamaica", "ESP": "Spain",
        "ARG": "Argentina", "UKR": "Ukraine", "BLR": "Belarus",
    }

    sports = {
        "Athletics": ["100m Men", "200m Men", "400m Men", "800m Men",
                      "100m Women", "200m Women", "400m Women",
                      "Marathon Men", "Marathon Women", "Long Jump Men",
                      "High Jump Women", "Triple Jump Men"],
        "Swimming": ["100m Freestyle Men", "200m Freestyle Men",
                     "100m Freestyle Women", "200m Backstroke Men",
                     "100m Breaststroke Women", "200m Butterfly Men"],
        "Gymnastics": ["Floor Exercise Men", "Vault Women",
                       "Horizontal Bar Men", "Balance Beam Women",
                       "Rings Men", "Uneven Bars Women"],
        "Cycling": ["Road Race Men", "Track Sprint Men",
                    "Time Trial Women", "Mountain Bike Men"],
        "Rowing": ["Single Sculls Men", "Double Sculls Women",
                   "Four Men", "Eight Women"],
        "Boxing": ["Heavyweight Men", "Middleweight Men",
                   "Lightweight Women", "Flyweight Men"],
        "Wrestling": ["Freestyle 65kg Men", "Greco-Roman 85kg Men",
                      "Freestyle 50kg Women"],
        "Shooting": ["10m Air Rifle Men", "25m Pistol Women",
                     "Trap Men", "Skeet Women"],
        "Judo": ["60kg Men", "70kg Women", "100kg Men", "+78kg Women"],
        "Fencing": ["Foil Individual Men", "Epee Individual Women",
                    "Sabre Team Men"],
        "Weightlifting": ["56kg Men", "69kg Men", "75kg Women"],
        "Taekwondo": ["58kg Men", "67kg Women"],
        "Volleyball": ["Indoor Men", "Beach Women"],
        "Basketball": ["Men", "Women"],
        "Football": ["Men", "Women"],
        "Tennis": ["Singles Men", "Singles Women", "Doubles Mixed"],
        "Hockey": ["Men", "Women"],
        "Handball": ["Men", "Women"],
        "Canoe Sprint": ["K1 1000m Men", "C1 500m Women"],
        "Triathlon": ["Men", "Women"],
    }

    years = list(range(1896, 2022, 4))
    summer_cities = {
        1896: "Athens", 1900: "Paris", 1904: "St. Louis",
        1908: "London", 1912: "Stockholm", 1920: "Antwerp",
        1924: "Paris", 1928: "Amsterdam", 1932: "Los Angeles",
        1936: "Berlin", 1948: "London", 1952: "Helsinki",
        1956: "Melbourne", 1960: "Rome", 1964: "Tokyo",
        1968: "Mexico City", 1972: "Munich", 1976: "Montreal",
        1980: "Moscow", 1984: "Los Angeles", 1988: "Seoul",
        1992: "Barcelona", 1996: "Atlanta", 2000: "Sydney",
        2004: "Athens", 2008: "Beijing", 2012: "London",
        2016: "Rio de Janeiro", 2020: "Tokyo",
    }
    # Remove war years
    years = [y for y in years if y not in [1916, 1940, 1944]]

    records = []
    athlete_id = 1

    for year in years:
        city = summer_cities.get(year, "Unknown")
        games = f"{year} Summer"

        # Women not participating until 1900; limited events until 1960
        female_ratio = 0.0 if year < 1900 else min(0.5, (year - 1896) / 250)

        for sport, events in sports.items():
            # Some sports added later
            if sport in ["Basketball", "Football", "Volleyball"] and year < 1936:
                continue
            if sport in ["Taekwondo", "Triathlon"] and year < 2000:
                continue
            if sport in ["Canoe Sprint"] and year < 1936:
                continue

            for event in events:
                is_women = "Women" in event or "women" in event

                # Choose competing nations (weighted by historical strength)
                n_nations = min(len(countries), max(3, int(len(countries) * (year - 1890) / 130)))
                noc_list = list(countries.keys())
                chosen = np.random.choice(noc_list, size=n_nations, replace=False)

                # Medal winners
                medals = ["Gold", "Silver", "Bronze"]
                medal_nocs = np.random.choice(chosen, size=3, replace=False)

                for i, noc in enumerate(chosen):
                    n_athletes = np.random.randint(1, 8)
                    sex = "F" if is_women else "M"
                    if not is_women and np.random.random() < female_ratio * 0.3:
                        sex = "F"

                    for _ in range(n_athletes):
                        age = int(np.random.normal(26, 4))
                        age = max(15, min(55, age))
                        medal = None
                        if noc == medal_nocs[0]:
                            medal = "Gold"
                        elif noc == medal_nocs[1]:
                            medal = "Silver"
                        elif noc == medal_nocs[2]:
                            medal = "Bronze"

                        records.append({
                            "ID": athlete_id,
                            "Name": f"Athlete_{athlete_id}",
                            "Sex": sex,
                            "Age": age,
                            "Team": countries[noc],
                            "NOC": noc,
                            "Games": games,
                            "Year": year,
                            "Season": "Summer",
                            "City": city,
                            "Sport": sport,
                            "Event": event,
                            "Medal": medal,
                        })
                        athlete_id += 1

    df = pd.DataFrame(records)
    print(f"  Generated {len(df):,} athlete-event records across {len(years)} Games")
    return df


# ─────────────────────────────────────────────
# 2. Clean the data
# ─────────────────────────────────────────────
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n── Cleaning data ──")
    original_len = len(df)

    # Standardise column names
    df.columns = df.columns.str.strip()

    # Keep only Summer Games if Season column exists
    if "Season" in df.columns:
        df = df[df["Season"] == "Summer"].copy()

    # Remove fully duplicate rows
    df.drop_duplicates(inplace=True)

    # Ensure Year is numeric
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df.dropna(subset=["Year"], inplace=True)
    df["Year"] = df["Year"].astype(int)

    # Ensure NOC exists
    if "NOC" not in df.columns and "Team" in df.columns:
        df["NOC"] = df["Team"].str[:3].str.upper()

    # Standardise Medal values
    valid_medals = {"Gold", "Silver", "Bronze"}
    if "Medal" in df.columns:
        df["Medal"] = df["Medal"].where(df["Medal"].isin(valid_medals), other=np.nan)

    # Standardise Sex
    if "Sex" in df.columns:
        df["Sex"] = df["Sex"].str.upper().str.strip()
        df["Sex"] = df["Sex"].map({"M": "M", "F": "F", "MALE": "M", "FEMALE": "F"})

    # Fill missing Age with median per Sex
    if "Age" in df.columns:
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
        median_age = df.groupby("Sex")["Age"].transform("median")
        df["Age"].fillna(median_age, inplace=True)

    # Add helper boolean
    df["HasMedal"] = df["Medal"].notna()

    print(f"  Rows before: {original_len:,}  |  after: {len(df):,}")
    print(f"  Missing Medal (participation records): {df['Medal'].isna().sum():,}")
    print(f"  Medal winners: {df['HasMedal'].sum():,}")
    return df


# ─────────────────────────────────────────────
# 3. Compute statistics
# ─────────────────────────────────────────────
def compute_stats(df: pd.DataFrame) -> dict:
    print("\n── Computing statistics ──")

    total_athletes = int(df["ID"].nunique()) if "ID" in df.columns else int(len(df))
    total_nations = int(df["NOC"].nunique())
    total_sports = int(df["Sport"].nunique()) if "Sport" in df.columns else 0
    year_range = int(df["Year"].max()) - int(df["Year"].min())
    years_covered = sorted(df["Year"].unique().tolist())

    medal_df = df[df["HasMedal"]]
    gold = int((medal_df["Medal"] == "Gold").sum())
    silver = int((medal_df["Medal"] == "Silver").sum())
    bronze = int((medal_df["Medal"] == "Bronze").sum())
    total_medals = gold + silver + bronze

    male = int((df["Sex"] == "M").sum())
    female = int((df["Sex"] == "F").sum())

    # Top 10 countries by total medals
    top_countries = (
        medal_df.groupby("NOC").size()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_countries.columns = ["NOC", "Medals"]
    top10 = top_countries.to_dict("records")

    # Medals by sport
    medals_by_sport = (
        medal_df.groupby("Sport").size()
        .sort_values(ascending=False)
        .reset_index()
    )
    medals_by_sport.columns = ["Sport", "Medals"]
    sport_list = medals_by_sport.to_dict("records")

    # Medals by year
    medals_by_year = (
        medal_df.groupby("Year").size()
        .reset_index()
    )
    medals_by_year.columns = ["Year", "Medals"]
    year_list = medals_by_year.to_dict("records")

    # Gender participation by year
    gender_year = (
        df.groupby(["Year", "Sex"])
        .size()
        .reset_index(name="Count")
        .pivot(index="Year", columns="Sex", values="Count")
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    gender_list = gender_year.to_dict("records")

    stats = {
        "total_athletes": total_athletes,
        "total_nations": total_nations,
        "total_sports": total_sports,
        "year_range": f"{df['Year'].min()}–{df['Year'].max()}",
        "years_covered": years_covered,
        "gold_medals": gold,
        "silver_medals": silver,
        "bronze_medals": bronze,
        "total_medals": total_medals,
        "male_athletes": male,
        "female_athletes": female,
        "top10_countries": top10,
        "medals_by_sport": sport_list,
        "medals_by_year": year_list,
        "gender_by_year": gender_list,
    }

    for k, v in stats.items():
        if not isinstance(v, (list, dict)):
            print(f"  {k}: {v}")
    return stats


# ─────────────────────────────────────────────
# 4. Save outputs
# ─────────────────────────────────────────────
def save_outputs(df: pd.DataFrame, stats: dict):
    df.to_csv(CLEAN_CSV, index=False)
    print(f"\n  Saved cleaned CSV → {CLEAN_CSV}")

    with open(STATS_JSON, "w") as f:
        json.dump(stats, f, indent=2, default=str)
    print(f"  Saved stats JSON → {STATS_JSON}")


if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    stats = compute_stats(df)
    save_outputs(df, stats)
    print("\n✅ Data preparation complete!")
