import duckdb
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


df = duckdb.read_parquet("data/filtered/df.parquet.gzip")

st.title("Sensor stats")


# Display the dataframe about the sensor
def get_dataframe_sensor(store: str, sensor: float) -> pd.DataFrame:
    query = f"""
    SELECT * FROM df
    WHERE store = '{store}' AND sensor_id = {sensor}
    ORDER BY date"""
    return duckdb.sql(query).df()


# Display column data over time
def plot_data(df: pd.DataFrame, column_name: str, n_weeks: int = 4, avg_month=True):
    title_ = "Daily traffic" if avg_month else "Traffic over the last 4 same days"
    query = f"""
    SELECT * from df
    ORDER BY date DESC
    LIMIT {n_weeks*7}
    """
    n_months_df = duckdb.sql(query).df()
    fig, ax = plt.subplots()
    ax.bar(n_months_df.date.to_numpy()[::-1], n_months_df[column_name].to_numpy()[::-1])
    ax.set(
        xlabel="date",
        ylabel="daily traffic (visitors)",
        title=f"{title_} over the {n_weeks} previous weeks",
    )
    ax.tick_params(axis="x", labelrotation=77)
    st.pyplot(fig)
    return


# Choice of the store, sensor
with st.form("sidebar"):
    with st.sidebar:
        available_stores_df = duckdb.sql(
            "SELECT DISTINCT store, sensor_id from df ORDER BY store, sensor_id"
        ).df()
        store = st.selectbox(
            label="Select a store to display its sensors:",
            # options=available_stores_df.apply(tuple, axis=1),
            options=available_stores_df["store"].unique(),
            placeholder="Pick a store.",
            index=None,
        )
        if store:
            available_sensors_df = duckdb.sql(
                f"SELECT DISTINCT  sensor_id from df WHERE store = '{store}' ORDER BY sensor_id"
            ).df()
            sensor = st.selectbox(
                label="Select a sensor to show its stats:",
                options=available_sensors_df["sensor_id"].unique(),
                placeholder="Pick a sensor.",
                index=None,
            )
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(f"You chose: Store: {store}, sensor: {sensor}.")
            sensor_df = get_dataframe_sensor(store=store, sensor=sensor)

dataframe_tab, daily_traffic, avg_month = st.tabs(
    ["Dataframe", "Daily Traffic Plot", "Moving Average"]
)
with dataframe_tab:
    if submitted:
        st.dataframe(sensor_df)
with daily_traffic:
    n_weeks = st.number_input(
        "Daily traffic over the N previous weeks",
        value=4,
        placeholder="Type a number and submit again",
        min_value=1,
        key="day",
    )
    if submitted:
        st.write(
            "If you want to modify the number of weeks, please modify the above value and submit again."
        )
        plot_data(sensor_df, "daily_traffic", n_weeks)
with avg_month:
    n_week_month = st.number_input(
        "Day traffic moving average over the N previous weeks",
        value=4,
        placeholder="Type a number and submit again",
        min_value=1,
        key="avg",
    )
    if submitted:
        st.write(
            "If you want to modify the number of weeks, please modify the above value and submit again."
        )
        plot_data(sensor_df, "avg_n_weeks", n_week_month)
