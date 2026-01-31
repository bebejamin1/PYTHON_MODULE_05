#! /bin/python3.10

from abc import ABC, abstractmethod
from typing import Any, List

# super()
# try/except
# ABC (Abstract Base Class) @abstractmethod
# typing (Any, List, Dict, Union, Optional)
#  Classe de base : DataProcessor
# NumericProcessor(), TextProcessor(), LogProcessor()
# process() Process the data and return result string
# validate() Validate if data is appropriate for this processor
# stream_processor() Format the output string
# Polymorphic Behavior: Same method calls, different specialized behaviors

# =============================================================================
# ========================== Methods / Class ==================================
# =============================================================================


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return ("Output: " + result)


class NumericProcessor(DataProcessor):
    pass


class TextProcessor(DataProcessor):
    print()


class LogProcessor(DataProcessor):
    print()


# =============================================================================
# ========================== STREAM PROCESSOR =================================
# =============================================================================


def stream_processor() -> None:
    print("Initializing Numeric Processor...")
    data = [1, 2, 3, 4, 5]
    print(f"Processing data: {data}")
    string = NumericProcessor().process(data)
    if (NumericProcessor().validate(data) is True):
        print("Validation: Numeric data verified")
    print(NumericProcessor().format_output(string))


# =============================================================================
# ================================= MAIN ======================================
# =============================================================================


if __name__ == "__main__":
    print(" CODE NEXUS - DATA PROCESSOR FOUNDATION ".center(79, "=") + "\n")
    stream_processor()
    print("\n" + "Foundation systems online. "
          "Nexus ready for advanced streams.")
