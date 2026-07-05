import pandas as pd


def create_features(df):
    """
    Crea variables nuevas a partir de la fecha, hora e intensidad.
    Esto nos sirve para el análisis y las visualizaciones.
    """

    df = df.copy()

    df["acq_date"] = pd.to_datetime(df["acq_date"], errors="coerce")

    df["year"] = df["acq_date"].dt.year
    df["month"] = df["acq_date"].dt.month
    df["quarter"] = df["acq_date"].dt.quarter
    df["day_of_year"] = df["acq_date"].dt.dayofyear
    df["month_name"] = df["acq_date"].dt.month_name()

    df["hour"] = pd.to_numeric(df["acq_time"], errors="coerce") // 100

    df["time_slot"] = pd.cut(
        df["hour"],
        bins=[-1, 5, 11, 17, 23],
        labels=["night", "morning", "afternoon", "evening"]
    )

    # Clasificación de FRP (NaN se mantiene como NaN, no como "High")
    df["frp_level"] = pd.cut(
        df["frp"],
        bins=[-float("inf"), 5, 20, float("inf")],
        labels=["Low", "Medium", "High"]
    )

    # Clasificación de brightness (mismo criterio)
    df["brightness_level"] = pd.cut(
        df["brightness"],
        bins=[-float("inf"), 320, 340, float("inf")],
        labels=["Low", "Medium", "High"]
    )

    return df