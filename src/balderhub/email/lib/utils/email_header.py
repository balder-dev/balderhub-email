import dataclasses


@dataclasses.dataclass
class EmailHeader:
    """Represents a single email header consisting of a ``key`` and a ``value`` pair."""
    key: str
    value: str

    def __eq__(self, other):
        """Return ``True`` if ``other`` is an :class:`EmailHeader` with the same key and value."""
        return self.key == other.key and self.value == other.value

    def __hash__(self):
        return hash((self.key, self.value))

    def __str__(self):
        return f"{self.key}: {self.value}"
