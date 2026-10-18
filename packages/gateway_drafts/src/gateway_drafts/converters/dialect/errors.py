from __future__ import annotations


class DraftMarkdownError(ValueError):
    """Raised when draft Markdown (or a dialect construct in it) is malformed."""

    def __init__(self, message: str, line: int | None = None) -> None:
        self.message = message
        self.line = line
        super().__init__(self.__str__())

    def __str__(self) -> str:
        if self.line is None:
            return self.message
        return f"line {self.line}: {self.message}"
