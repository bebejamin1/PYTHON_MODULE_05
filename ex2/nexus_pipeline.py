#! /bin/python3.10

from abc import ABC, abstractmethod
from typing import Any, Dict, Union, Protocol
# import time

# super() try/except
# ABC avec @abstractmethod et Protocol pour le duck typing
# pipeline

# =============================================================================
# ========================= Methods / Class ===================================
# =============================================================================

# ============================= Parent ========================================
# ======================== ProcessingPipeline =================================
# =============================================================================
# stages: List[Stages]


class ProcessingPipeline(ABC):
    def __init__(self, pipeline_id: str) -> None:

        self.pipeline_id = pipeline_id
        self.stages = []

    @abstractmethod
    def process(self, data: Any) -> Union[str, Any]:
        pass

    def add_stage() -> None:
        pass


# ============================= Child =========================================
# ========================== JSONAdapter ======================================
# =============================================================================


class JSONAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id)

    def process(self, data: Any) -> Union[str, Any]:
        pass


# ============================= Child =========================================
# ========================== CSVAdapter =======================================
# =============================================================================


class CSVAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id)

    def process(self, data: Any) -> Union[str, Any]:
        pass


# ============================= Child =========================================
# ========================= StreamAdapter =====================================
# =============================================================================


class StreamAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id)

    def process(self, data: Any) -> Union[str, Any]:
        pass


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
        pass


# ============================= Child =========================================
# ======================== TransformStage =====================================
# =============================================================================


class TransformStage():

    def process(self, data: Any) -> Dict:
        pass


# ============================= Child =========================================
# ========================== OutputStage ======================================
# =============================================================================


class OutputStage():

    def process(self, data: Any) -> str:
        pass


# =========================== No Parent =======================================
# ========================== NexusManager =====================================
# =============================================================================


class NexusManager():
    def __init__(self):
        self.pipelines = []

    def add_pipeline() -> None:
        pass

    def proces_data() -> None:
        pass

# =============================================================================
# =============================== main ========================================
# =============================================================================


def nexus_pipeline():
    pass

# =============================================================================
# =============================== main ========================================
# =============================================================================


if __name__ == "__main__":
    print(" CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ".center(79, "="))
    nexus_pipeline()
    print("Nexus Integration complete. All systems operational.")
