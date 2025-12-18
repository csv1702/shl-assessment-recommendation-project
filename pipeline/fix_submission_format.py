import pandas as pd

INPUT_PATH = "submission_predictions.csv"
OUTPUT_PATH = "submission_predictions_final.csv"


def main():
    df = pd.read_csv(INPUT_PATH)

    rows = []

    for _, row in df.iterrows():
        query = row["Query"]
        urls = row["Recommended_Assessments"].split(",")

        for url in urls:
            rows.append({
                "Query": query,
                "Assessment_url": url.strip()
            })

    final_df = pd.DataFrame(rows)
    final_df.to_csv(OUTPUT_PATH, index=False)

    print("✅ Submission file reformatted successfully")
    print(f"Saved as: {OUTPUT_PATH}")
    print(f"Total rows: {len(final_df)}")


if __name__ == "__main__":
    main()
