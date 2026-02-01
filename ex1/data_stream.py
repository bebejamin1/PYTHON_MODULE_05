#! /bin/python3.10

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional

# super()
# try/except
# ABC avec @abstractmethod
# isinstance()

# DataStream class abstraite
# SensorStream(stream_id), TransactionStream(stream_id), EventStream(stream_id)

# process_batch(self, ...) - Traite un lot de données <- @abstractmethod
# filter_data(self, ...) - Filtre les données en fonction de critères
# get_stats(self) - Renvoie les statistiques du flux

# StreamProcessor qui gère plusieurs types de flux de manière polymorphe
# Fonctionnalité : traitement par lots, filtrage, pipelines de transformation
# StreamProcessor gere n'importe quel type de flux grâce au polymorphisme


# =============================================================================
# ============================ Methods / Class ================================
# =============================================================================

# =============================== Parent ======================================
# ============================= DataStream ====================================
# =============================================================================


class DataStream(ABC):

    def __init__(self, stream_id: str, type: str):

        self.stream_id = stream_id
        self.type = type

# 🛩️​

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

# 🛩️​

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


# =============================================================================
# ============================ SensorStream ===================================
# =============================== Child =======================================


class SensorStream(DataStream):

    def __init__(self, stream_id: str, type: str):
        super().__init__(stream_id, type)

        self.sensor_report = 0
        self.avg_t = []

# 🛩️​

    def process_batch(self, data_batch: List[Any]) -> str:

        try:
            if (isinstance(data_batch, List) is False):
                raise Exception("🎯​ data is not a list, data type -> "
                                f"{type(data_batch)}")
            data_f = self.filter_data(data_batch)
            if (len(data_f) <= 0):
                raise Exception("🎯​ data is empty, no valid data found")
            for data in data_f:
                float(data[1])
                self.sensor_report += 1
                if (data[0] == "temp"):
                    self.avg_t.append(data[1])
        except (Exception, ValueError) as e:
            print(e)
            return ("0 reading")
        else:
            return (f"{self.sensor_report} readings")

# 🛩️​

    def filter_data(self, data_batch: List[Union[tuple, str]],
                    criteria: Optional[str] = None) -> List[tuple]:
        filtered_data = []
        for data in data_batch:
            if (isinstance(data, tuple) is True
                    and data[0] in ["temp", "humidity", "presure"]):
                filtered_data.append(data)

        if (criteria == "High-priority"):
            for data in filtered_data:
                if ((data[0] == "temp" and (data[1] < -15 or data[1] > 35))
                    or (data[0] == "humidity"
                        and (data[1] < 10 or data[1] > 90))
                    or (data[0] == "presure"
                        and (data[1] < 1005 or data[1] > 1025))):
                    return (data)
        return (filtered_data)

# 🛩️​

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        try:
            return {"average_temperature": sum(self.avg_t) / len(self.avg_t)}
        except ZeroDivisionError as e:
            print(e)
            return {"average_temperature": 0}


# =============================================================================
# ========================= TransactionStream =================================
# =============================== Child =======================================


class TransactionStream(DataStream):
    def __init__(self, stream_id: str, type: str):
        super().__init__(stream_id, type)

        self.trans_operation = 0
        self.net_f = []

# 🛩️​

    def process_batch(self, data_batch: List[Any]) -> str:

        try:
            if (isinstance(data_batch, List) is False):
                raise Exception("🎯​ data is not a list, data type -> "
                                f"{type(data_batch)}")
            data_f = self.filter_data(data_batch)
            if (len(data_f) <= 0):
                raise Exception("🎯​ data is empty, no valid data found")
            for data in data_f:
                int(data[1])
                self.trans_operation += 1
                if (data[0] == "sell"):
                    self.net_f.append(data[1])
                if (data[0] == "buy"):
                    self.net_f.append(-data[1])
        except (Exception, ValueError) as e:
            print(e)
            return ("0 operation")
        else:
            return (f"{self.trans_operation} operations")

# 🛩️​

    def filter_data(self, data_batch: List[Union[tuple, str]],
                    criteria: Optional[str] = None) -> List[tuple]:
        filtered_data = []
        for data in data_batch:
            if (isinstance(data, tuple) is True
                    and data[0] in ["sell", "buy"]):
                filtered_data.append(data)

        if (criteria == "High-priority"):
            for data in filtered_data:
                if ((data[0] == "sell" and (data[1] < 0))
                    or (data[0] == "buy"
                        and (data[1] < 0))):
                    return (data)
        return (filtered_data)
# 🛩️​

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"net flow:": -sum(self.net_f)}


# =============================================================================
# ============================ EventStream ====================================
# =============================== Child =======================================


class EventStream(DataStream):
    def __init__(self, stream_id: str, type: str):
        super().__init__(stream_id, type)

        self.nbr_event = 0
        self.error_detect = 0

# 🛩️​

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            if (isinstance(data_batch, List) is False):
                raise Exception("🎯​ data is not a list, data type -> "
                                f"{type(data_batch)}")
            data_f = self.filter_data(data_batch)
            if (len(data_f) <= 0):
                raise Exception("🎯​ data is empty, no valid data found")
            for data in data_f:
                str(data)
                if (data == "login" or data == "logout"):
                    self.nbr_event += 1
                if (data == "error"):
                    self.nbr_event += 1
                    self.error_detect += 1
        except (Exception, ValueError) as e:
            print(e)
            return ("0 event")
        else:
            return (f"{self.nbr_event} events")

# 🛩️​

    def filter_data(self, data_batch: List[Union[tuple, str]],
                    criteria: Optional[str] = None) -> List[str]:
        filtered_data = []
        for data in data_batch:
            if (isinstance(data, str) is True
                    and data in ["login", "logout", "error"]):
                filtered_data.append(data)

        if (criteria == "High-priority"):
            for data in filtered_data:
                if (data == "error"):
                    return (data)
        return (filtered_data)

# 🛩️​

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return (f"{self.error_detect} error detected")


# ============================= No Parent =====================================
# ========================== StreamProcessor ==================================
# =============================  Miskine ======================================


class StreamProcessor():
    pass

# =============================================================================
# ============================ DATA STREAM ====================================
# =============================================================================


def data_stream() -> None:

    data_batch = [
                ("temp", 22.5), ("humidity", 65), ("presure", 1013),
                ("buy", 100), ("sell", 150), ("buy", 75),
                "login", "error", "logout"
                ]

# 🧺​

    print("Initializing Sensor Stream...")
    sensor_stream = SensorStream("SENSOR_001", "Sensor")
    print(f"Stream ID: {sensor_stream.stream_id}, Type: Environmental Data")
    data_batch_filtered = sensor_stream.filter_data(data_batch)

    data = []
    for n, v in data_batch_filtered:
        data.append(f"{n}:{v}")
    print("Processing sensor batch: [", end="")
    print(*data, sep=", ", end="]")

    print("\n" + f"Sensor analysis: {sensor_stream.process_batch(data_batch)}"
                 " processed, avg temp: "
                 f"{sensor_stream.get_stats()['average_temperature']}°C")

# 🔰​

    print("\n" + "Initializing Transaction Stream...")
    trans_stream = TransactionStream("TRANS_001", "Trans")
    print(f"Stream ID: {trans_stream.stream_id}, Type: Financial Data")
    data_batch_filtered = trans_stream.filter_data(data_batch)

    data = []
    for n, v in data_batch_filtered:
        data.append(f"{n}:{v}")
    print("Processing transaction batch: [", end="")
    print(*data, sep=", ", end="]")
    print("\n" + "Transaction analysis: "
                 f"{trans_stream.process_batch(data_batch)}"
                 " processed, net flow: "
                 f"{trans_stream.get_stats()['net flow:']}")

# 🔰​

    print("\n" + "Initializing Event Stream...")
    event_stream = EventStream("EVENT_001", "Event")
    print(f"Stream ID: {event_stream.stream_id}, Type: System Events")
    data_batch_filtered = event_stream.filter_data(data_batch)

    data = []
    for n in data_batch_filtered:
        data.append(f"{n}")
    print("Processing transaction batch: [", end="")
    print(*data, sep=", ", end="]")
    print("\n" + "Event analysis: "
                 f"{event_stream.process_batch(data_batch)}"
                 " events, "
                 f"{event_stream.get_stats()}")

# 🔰​

    print("\n" + " Polymorphic Stream Processing ".center(79, "=") + "\n")
    print("Processing mixed stream types through unified interface..." + "\n")

    print("Batch 1 Results:")

    print("Stream filtering active: High-priority data only")

# =============================================================================
# =============================== MAIN ========================================
# =============================================================================


if __name__ == "__main__":
    print(" CODE NEXUS - POLYMORPHIC STREAM SYSTEM ".center(79, "=") + "\n")

    data_stream()

    print("\n" + "All streams processed successfully. "
                 "Nexus throughput optimal.")
