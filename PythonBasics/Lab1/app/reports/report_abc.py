"""
Abstract report base class.
"""

from abc import ABC, abstractmethod

class Report(ABC):
    """Abstract report class."""

    @abstractmethod
    def generate(self):
        pass