"""Abstract base class for library resources."""

from abc import ABC, abstractmethod


class LibraryResource(ABC):
    """Base abstract class for any resource in the library."""

    def __init__(self, resource_id, title):
        self._resource_id = resource_id
        self._title = title

    @property
    def resource_id(self):
        return self._resource_id

    @property
    def title(self):
        return self._title

    @abstractmethod
    def get_info(self):
        """Return information about the resource."""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._resource_id}, title='{self._title}')"

    def __eq__(self, other):
        if isinstance(other, LibraryResource):
            return self.resource_id == other.resource_id
        return False