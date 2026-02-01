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

# =============================================================================
# ============================ Methods / Class ================================
# =============================================================================


class DataStream(ABC):

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass

# =============================================================================
# ============================= DATA STREAM ===================================
# =============================================================================


def data_stream() -> None:
    print("Initializing Sensor Stream...")


# =============================================================================
# ================================= MAIN ======================================
# =============================================================================


if __name__ == "__main__":
    print(" CODE NEXUS - POLYMORPHIC STREAM SYSTEM ".center(79, "=") + "\n")

    data_stream()

    print("\n" + "All streams processed successfully. Nexus throughput optimal.")
