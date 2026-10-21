from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
OUTPUT_PATH = RAW_DIR / "owid_co2_data.csv"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_URL)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Downloaded dataset with {len(df)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
