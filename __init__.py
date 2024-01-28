from datetime import date

from data_quality_monitoring.src.store import Store


def create_data() -> dict:
    """
    Create the available stores in our API
    5 stores, with each 5 sensors
    Each stores has a different number of people coming to it
    As well as different break and malfunction percentages
    (Not realistic, but we keep things simple)
    """

    store_name = ["Nancy", "Paris", "Lille", "Cholet", "Cabourg"]
    store_avg_visit = [3000, 8000, 6000, 2000, 1700]
    store_std_visit = [500, 800, 500, 400, 100]
    perc_malfunction = [0.05, 0.1, 0.08, 0.05, 0.05]
    perc_break = [0.05, 0.08, 0.05, 0.02, 0]

    store_dict = {
        tuple_[0]: Store(*tuple_)
        for tuple_ in zip(
            store_name, store_avg_visit, store_std_visit, perc_break, perc_malfunction
        )
    }

    return store_dict


if __name__ == "__main__":
    print(create_data())
