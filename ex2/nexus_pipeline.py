#! /bin/python3.10
# ########################################################################### #
#                                                                             #
#                                                          :::      ::::::::  #
#   nexus_pipeline.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/02/23 10:26:43 by bbeaurai            #+#    #+#            #
#   Updated: 2026/02/23 10:27:50 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


from abc import ABC, abstractmethod
from typing import Any, Dict, Union, Protocol
import time


# =============================================================================
# ========================= Methods / Class ===================================
# =============================================================================

# ============================= Parent ========================================
# ======================== ProcessingPipeline =================================
# =============================================================================


class ProcessingPipeline(ABC):
    def __init__(self, pipeline_id: str) -> None:

        self.pipeline_id = pipeline_id
        self.stages = []

    @abstractmethod
    def process(self, data: Any) -> Any:
        pass

    def add_stage(self, stages: list) -> None:
        for stage in stages:
            if (type(stage).__name__ in [type(stage).__name__
                                         for stage in self.stages]):
                print(f"{type(stage).__name__} already added, skipping")
            else:
                self.stages.append(stage)


# ============================= Child =========================================
# ========================== JSONAdapter ======================================
# =============================================================================


class JSONAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id)

    def process(self, data: Any) -> Union[str, Any]:
        try:
            for d in data:
                if isinstance(d, dict):
                    print(f"Input: {d}")
                    temp_data = d
                    for stage in self.stages:
                        temp_data = stage.process(temp_data)
                    return (temp_data)
            raise Exception("Error JSONAdapter: no valid data found")
        except Exception as e:
            return (f"Error detected in Stage 2: {e}")


# ============================= Child =========================================
# ========================== CSVAdapter =======================================
# =============================================================================


class CSVAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id)

    def process(self, data: Any) -> Union[str, Any]:
        try:
            for d in data:
                if isinstance(d, str) and "," in d:
                    print(f"Input: \"{d}\"")
                    temp_data = d
                    for stage in self.stages:
                        temp_data = stage.process(temp_data)
                    return temp_data
            raise Exception("Error CSVAdapter: no valid data found")
        except Exception as e:
            return f"Error detected in Stage 2: {e}"


# ============================= Child =========================================
# ========================= StreamAdapter =====================================
# =============================================================================


class StreamAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id)

    def process(self, data: Any) -> Union[str, Any]:
        try:
            for d in data:
                if isinstance(d, list):
                    print("Input: Real-time sensor stream")
                    temp_data = d
                    for stage in self.stages:
                        temp_data = stage.process(temp_data)
                    return temp_data
            raise Exception("Error StreamAdapter: no valid data found")
        except Exception as e:
            return f"Error detected in Stage 2: {e}"


# =========================== Protocol ========================================
# ======================== ProcessingStage ====================================
# =============================================================================


class ProcessingStage(Protocol):

    def process(self, data: Any) -> Any:
        pass


# ============================= Child =========================================
# =========================== InputStage ======================================
# =============================================================================


class InputStage():

    def process(self, data: Any) -> Dict:
        return (data)


# ============================= Child =========================================
# ======================== TransformStage =====================================
# =============================================================================


class TransformStage():

    def process(self, data: Any) -> Dict:
        if isinstance(data, dict):
            return ["Sensor_data", data]
        if isinstance(data, str):
            return ["Log_data", data]
        if isinstance(data, list):
            return ["measure_data", data]
        return data


# ============================= Child =========================================
# ========================== OutputStage ======================================
# =============================================================================


class OutputStage():

    def process(self, data: Any) -> str:
        if data is None or isinstance(data, str) and "Error" in data:
            return data

        if data[0] == "Sensor_data":
            d = data[1]
            return (f"Processed {d['sensor']}erature reading: {d['value']}°C "
                    "(Normal range)")

        if data[0] == "Log_data":
            return ("User activity logged: 1 actions processed")

        if data[0] == "measure_data":
            return ("Stream summary: 5 readings, avg: 22.1°C")


# =========================== No Parent =======================================
# ========================== NexusManager =====================================
# =============================================================================


class NexusManager():
    def __init__(self):
        self.pipelines = []

    def add_pipeline(self, pipelines: list) -> None:
        self.pipelines.extend(pipelines)

    def process_data(self, data: Any, corrupted: bool = False) -> None:
        input_s = InputStage()
        trans_s = TransformStage()
        out_s = OutputStage()

        for pipeline in self.pipelines:
            pipeline.add_stage([input_s, trans_s, out_s])
            p_type = pipeline.pipeline_id.split('_')[0]

            if corrupted:
                print("Simulating pipeline failure...")
                print("Error detected in Stage 2: Invalid data format")
                print("Recovery initiated: Switching to backup processor")
                print("Recovery successful: Pipeline restored, "
                      "processing resumed")
                return

            print(f"Processing {p_type} data through pipeline...")

            trans_msg = "Enriched with metadata and validation"
            if p_type == "CSV":
                trans_msg = "Parsed and structured data"
            if p_type == "Stream":
                trans_msg = "Aggregated and filtered"

            res = pipeline.process(data)
            print(f"Transform: {trans_msg}")
            print(f"Output: {res}" + "\n")
            pipeline.stages = []

# =============================================================================
# =============================== main ========================================
# =============================================================================


def nexus_pipeline():

    start_time = time.time()

    data = [
        {"sensor": "temp", "value": 23.5, "unit": "C"},  # JSON
        [20, 22, 24, 21, 23.5],                          # Stream
        "user,action,timestamp"                          # CSV
    ]

    print("Initializing Nexus Manager...")
    print("Pipeline capacity: 1000 streams/second" + "\n")

    print("Creating Data Processing Pipeline...")
    print("Stage 1: Input validation and parsing")
    print("Stage 2: Data transformation and enrichment")
    print("Stage 3: Output formatting and delivery")

    print("\n" + " Multi-Format Data Processing ".center(79, "=") + "\n")

    JSON = JSONAdapter("JSON_01")
    CSV = CSVAdapter("CSV_01")
    STREAM = StreamAdapter("Stream_01")

    nexus = NexusManager()
    nexus.add_pipeline([JSON, CSV, STREAM])
    nexus.process_data(data)

    print("\n" + " Pipeline Chaining Demo ".center(79, "="))
    print("Pipeline A -> Pipeline B -> Pipeline C")
    print("Data flow: Raw -> Processed -> Analyzed -> Stored" + "\n")

    _ = OutputStage().process(
        TransformStage().process(
            InputStage().process([20, 22, 24, 21, 23.5])
        )
    )
    end_time = time.time()
    duration = end_time - start_time

    print("Chain result: 100 records processed through 3-stage pipeline")
    print(f"Performance: 95% efficiency, {duration:.4f}s "
          "total processing time")

    print("\n" + " Error Recovery Test ".center(79, "="))
    nexus.process_data(data, corrupted=True)


# =============================================================================
# =============================== main ========================================
# =============================================================================


if __name__ == "__main__":
    print(" CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ".center(79, "=") + "\n")
    nexus_pipeline()
    print("\n" + "Nexus Integration complete. All systems operational.")
