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

# =============================== Parent ======================================
# ============================ DataProcessor ==================================
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


# =============================== Enfant ======================================
# ========================== NumericProcessor =================================
# =============================================================================


class NumericProcessor(DataProcessor):

    def process(self, data: List[int]) -> str:
        if (NumericProcessor().validate(data) is True):
            return (f"Processed {len(data)} numeric values, "
                    f"sum={sum(data)}, vg={sum(data) / len(data)}")
        else:
            return ("🎯​ data was not validate, please verify your input")

# ➡️​

    def validate(self, data: List[int]) -> bool:
        try:
            if (isinstance(data, list) is False):
                raise Exception("🎯​ data is not a list, data type -> "
                                f"{type(data)}")
            if (len(data) == 0):
                raise Exception("🎯​ data is emtpy")
            for number in data:
                int(number)
        except (Exception, ValueError) as e:
            print(e)
            return (False)
        else:
            return (True)

# ➡️​

    def format_output(self, result: str) -> str:
        return super().format_output(result)


# =============================== Enfant ======================================
# =========================== TextProcessor ===================================
# =============================================================================


class TextProcessor(DataProcessor):

    def process(self, data: str) -> str:
        if (TextProcessor().validate(data) is True):
            return (f"Processed text: {len(data)} "
                    f"characters, {len(data.split())} words")

# ➡️​

    def validate(self, data: str) -> bool:
        try:
            if (isinstance(data, str) is False):
                raise Exception("🎯​ data is not a str, data type -> "
                                f"{type(data)}")
            if (len(data) == 0):
                raise Exception("🎯​ data is emtpy")
        except Exception as e:
            print(e)
            return (False)
        else:
            return (True)

# ➡️​

    def format_output(self, result: str) -> str:
        return super().format_output(result)

# =============================== Enfant ======================================
# ============================ LogProcessor ===================================
# =============================================================================


class LogProcessor(DataProcessor):

    def process(self, data: List[int]) -> str:
        print()

# ➡️​

    def validate(self, data: Any) -> bool:
        try:
            if (isinstance(data, list) is False):
                raise Exception("🎯​ data is not a list, data type -> "
                                f"{type(data)}")
            if (len(data) == 0):
                raise Exception("🎯​ data is emtpy")
            for number in data:
                int(number)
        except (Exception, ValueError) as e:
            print(e)
            return (False)
        else:
            return (True)

# ➡️​

    def format_output(self, result: str) -> str:
        return super().format_output(result)


# =============================================================================
# ========================== STREAM PROCESSOR =================================
# =============================================================================


def stream_processor() -> None:

    print("Initializing Numeric Processor...")
    data = [1, 2, 3, 4, 5]
    print(f"Processing data: {data}")

    content = NumericProcessor().process(data)
    if (NumericProcessor().validate(data) is True):
        print("Validation: Numeric data verified")
        print(NumericProcessor().format_output(content))
    else:
        print("Error")

# ☑️​

    print("\n" + "Initializing Text Processor...")
    data = "Hello Nexus World"
    print(f"Processing data: \"{data}\"")

    content = TextProcessor().process(data)
    if (TextProcessor().validate(data) is True):
        print("Validation: Text data verified")
        print(TextProcessor().format_output(content))
    else:
        print("Error")

# ☑️​

    print("\n" + "Initializing Log Processor...")
    data = "ERROR: Connection timeout"
    print(f"Processing data: \"{data}\"")

    content = LogProcessor().process(data)
    if (LogProcessor().validate(data) is True):
        print("Validation: Log entry verified")
        print(LogProcessor().format_output(content))
    else:
        print("Error")

# ☑️​


# =============================================================================
# ================================= MAIN ======================================
# =============================================================================


if __name__ == "__main__":

    print(" CODE NEXUS - DATA PROCESSOR FOUNDATION ".center(79, "=") + "\n")

    stream_processor()

    print("\n" + "Foundation systems online. "
          "Nexus ready for advanced streams.")
