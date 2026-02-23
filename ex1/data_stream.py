#!/usr/bin/env python3
# ########################################################################### #
#                                                                             #
#                                                          :::      ::::::::  #
#   data_stream.py                                       :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/02/23 10:26:53 by bbeaurai            #+#    #+#            #
#   Updated: 2026/02/23 10:27:56 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


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

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

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

    def process_batch(self, data_batch: List[Any]) -> str:

        try:
            if (isinstance(data_batch, List) is False):
                raise Exception("🎯​ data is not a list, data type -> "
                                f"{type(data_batch)}")
            data_f = self.filter_data(data_batch)
            if (len(data_f) <= 0):
                raise Exception("🎯​ data is empty, no valid data found")

            self.avg_t = [float(data[1]) for data in data_f
                          if (data[0] == "temp")]
            self.sensor_report += len(data_f)

        except (Exception, ValueError) as e:
            print(e)
            return ("0 reading")
        else:
            return (f"{self.sensor_report} readings")

    def filter_data(self, data_batch: List[Union[tuple, str]],
                    criteria: Optional[str] = None) -> List[tuple]:

        filtered_data = [data for data in data_batch
                         if (isinstance(data, tuple) is True
                             and data[0] in ["temp", "humidity", "presure"])]

        if (criteria == "High-priority"):
            for data in filtered_data:
                if ((data[0] == "temp" and (data[1] < -15 or data[1] > 35))
                    or (data[0] == "humidity"
                        and (data[1] < 10 or data[1] > 90))
                    or (data[0] == "presure"
                        and (data[1] < 1005 or data[1] > 1025))):
                    return (data)
        return (filtered_data)

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
        self.net_sell = []
        self.net_buy = []

    def process_batch(self, data_batch: List[Any]) -> str:

        try:
            if (isinstance(data_batch, List) is False):
                raise Exception("🎯​ data is not a list, data type -> "
                                f"{type(data_batch)}")
            data_f = self.filter_data(data_batch)
            if (len(data_f) <= 0):
                raise Exception("🎯​ data is empty, no valid data found")

            self.net_sell = [int(data[1]) for data in data_f
                             if (data[0] == "sell")]
            self.net_buy = [int(data[1]) for data in data_f
                            if (data[0] == "buy")]
            self.trans_operation += len(self.net_sell) + len(self.net_buy)

        except (Exception, ValueError) as e:
            print(e)
            return ("0 operation")
        else:
            return (f"{self.trans_operation} operations")

    def filter_data(self, data_batch: List[Union[tuple, str]],
                    criteria: Optional[str] = None) -> List[tuple]:

        filtered_data = [data for data in data_batch
                         if (isinstance(data, tuple) is True
                             and data[0] in ["sell", "buy"])]

        if (criteria == "High-priority"):
            for data in filtered_data:
                if ((data[0] == "sell" and (data[1] < 0))
                    or (data[0] == "buy"
                        and (data[1] < 0))):
                    return (data)
        return (filtered_data)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"net flow:": (sum(self.net_buy) - sum(self.net_sell))}


# =============================================================================
# ============================ EventStream ====================================
# =============================== Child =======================================


class EventStream(DataStream):
    def __init__(self, stream_id: str, type: str):
        super().__init__(stream_id, type)

        self.nbr_event = 0
        self.error_detect = 0

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

    def filter_data(self, data_batch: List[Union[tuple, str]],
                    criteria: Optional[str] = None) -> List[str]:

        filtered_data = [data for data in data_batch
                         if (isinstance(data, str) is True
                             and data in ["login", "logout", "error"])]

        if (criteria == "High-priority"):
            for data in filtered_data:
                if (data == "error"):
                    return (data)
        return (filtered_data)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return (f"{self.error_detect} error detected")


# ============================= No Parent =====================================
# ========================== StreamProcessor ==================================
# =============================================================================


class StreamProcessor():

    def process_batch(self, data_batch: List[Any],
                      streams: List[object]) -> None:
        for stream in streams:
            result = stream.process_batch(data_batch)
            print(f"- {stream.type} data: {result} processed")

    def process_batch_filtered(self, data_batch: List[Any],
                               streams: List[Any],
                               criteria: str) -> Dict[str, int]:
        liste = []
        for stream in streams:
            liste.append(len(stream.filter_data(data_batch, criteria)))

        return {key.type: value for key, value in zip(streams, liste)}


# =============================================================================
# ============================ DATA STREAM ====================================
# =============================================================================


def data_stream() -> None:

    data_batch = [
                ("temp", 22.5), ("humidity", 65), ("presure", 1013),
                ("buy", 100), ("sell", 150), ("buy", 75),
                "login", "error", "logout"
                ]

    data_batch2 = [
                ("temp", 22.5), ("humidity", 65),
                ("buy", 100), ("sell", 150), ("buy", 75), ("sell", 35),
                "login", "error", "logout"
                ]

    data_batch3 = [
                ("temp", -500), ("humidity", 20000), ("presure", 1013),
                ("buy", 100), ("sell", 150000000), ("buy", 75),
                "login", "error", "logout"
                ]

    stream_type = [
                   SensorStream("SENSOR_002", "Sensor"),
                   TransactionStream("TRANS_002", "Transaction"),
                   EventStream("EVENT_001", "Event")
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
                 " processed, net flow: +"
                 f"{trans_stream.get_stats()['net flow:']} units")

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

    print("\n" + " Polymorphic Stream Processing ".center(79, "="))
    print("Processing mixed stream types through unified interface..." + "\n")

    print("Batch 1 Results:")
    StreamProcessor().process_batch(data_batch2, stream_type)

    print("\n" + "Stream filtering active: High-priority data only")
    filtered_result = StreamProcessor().process_batch_filtered(data_batch3,
                                                               stream_type,
                                                               "High-priority")
    print(f"Filtered results: {filtered_result['Sensor']} "
          f"critical sensor alerts, {filtered_result['Transaction']}"
          " large transaction")


# =============================================================================
# =============================== MAIN ========================================
# =============================================================================


if __name__ == "__main__":
    print(" CODE NEXUS - POLYMORPHIC STREAM SYSTEM ".center(79, "=") + "\n")

    data_stream()

    print("\n" + "All streams processed successfully. "
                 "Nexus throughput optimal.")
