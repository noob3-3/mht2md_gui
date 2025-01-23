# Abstract Base Class for Converters
from abc import ABC, abstractmethod
from abc import ABC


class FileConverter(ABC):
    def __init__(self, file_path, output_dir):
        self.file_path = file_path
        self.output_dir = output_dir

    @abstractmethod
    def convert(self, progress_callback):
        pass