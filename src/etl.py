import os
import pandas as pd

from src.cleaning import clean_firms_data
from src.features import create_features


def run_pipeline(raw_dir="data/raw", processed_dir="data/processed"):
    os.makedirs(processed_dir, exist_ok=True)

    modis = pd.read_csv(f"{raw_dir}/modis_archive.csv")
    viirs = pd.read_csv(f"{raw_dir}/viirs_archive.csv")

    modis = create_features(clean_firms_data(modis, "MODIS"))
    viirs = create_features(clean_firms_data(viirs, "VIIRS"))

    combined = pd.concat([modis, viirs], ignore_index=True)

    out_path = f"{processed_dir}/combined_clean.parquet"
    combined.to_parquet(out_path, index=False)

    print(f"Proceso terminado. MODIS={modis.shape}, VIIRS={viirs.shape}, COMBINED={combined.shape}")
    return combined


if __name__ == "__main__":
    run_pipeline()