import pandas as pd


def yearly_summary(df):
    yearly = (
        df.groupby(["sensor", "year"])
        .agg(
            fires=("year", "size"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean"),
            pct_with_confidence=("confidence_level", lambda x: x.notna().mean())
        )
        .reset_index()
        .sort_values(["sensor", "year"])
    )

    return yearly


def monthly_summary(df):
    monthly = (
        df.groupby(["sensor", "month", "month_name"])
        .agg(
            fires=("month", "size"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean")
        )
        .reset_index()
        .sort_values(["sensor", "month"])
    )

    return monthly


def sensor_summary(df):
    summary = (
        df.groupby("sensor")
        .agg(
            total_fires=("sensor", "size"),
            min_year=("year", "min"),
            max_year=("year", "max"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean")
        )
        .reset_index()
    )

    return summary


def daynight_summary(df):
    dn = (
        df.groupby(["sensor", "daynight"])
        .agg(
            fires=("daynight", "size"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean")
        )
        .reset_index()
        .sort_values(["sensor", "daynight"])
    )

    return dn


def frp_level_summary(df):
    frp = (
        df.groupby(["sensor", "frp_level"])
        .agg(
            fires=("frp_level", "size"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean")
        )
        .reset_index()
        .sort_values(["sensor", "fires"], ascending=[True, False])
    )

    return frp