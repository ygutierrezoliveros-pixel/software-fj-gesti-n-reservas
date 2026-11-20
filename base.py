"""Contrato abstracto para las entidades del sistema."""

from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Define las operaciones que debe implementar una entidad."""

    @abstractmethod
    def validar(self) -> None:
        """Valida los datos de la entidad."""

    @abstractmethod
    def to_dict(self) -> dict[str, object]:
        """Devuelve la entidad representada como un diccionario."""
