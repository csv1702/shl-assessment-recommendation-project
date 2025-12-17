import pandas as pd
from pathlib import Path

DATASET_PATH = Path("data/given/Gen_AI Dataset.xlsx")

def load_given_dataset():
    if not DATASET_PATH.exists():
        raise FileNotFoundError("Gen_AI Dataset.xlsx not found in data/given/")

    df = pd.read_excel(DATASET_PATH)
    df.columns = [c.strip().lower() for c in df.columns]

    return df


if __name__ == "__main__":
    df = load_given_dataset()

    print("Dataset shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nSample rows:")
    print(df.head(5))
