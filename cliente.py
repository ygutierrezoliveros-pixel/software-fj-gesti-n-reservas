"""Entidad de cliente y validación de sus datos."""

import re

from base import EntidadBase
from excepciones import ErrorCliente


class Cliente(EntidadBase):
    """Representa un cliente con identificación y datos de contacto."""

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        telefono: str,
    ) -> None:
        self.set_identificacion(identificacion)
        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ErrorCliente(f"El {campo} debe ser un texto no vacío.")
        return valor.strip()

    def get_identificacion(self) -> str:
        return self.__identificacion

    def set_identificacion(self, identificacion: str) -> None:
        valor = self._validar_texto(identificacion, "identificación")
        self.__identificacion = valor

    def get_nombre(self) -> str:
        return self.__nombre

    def set_nombre(self, nombre: str) -> None:
        valor = self._validar_texto(nombre, "nombre")
        self.__nombre = valor

    def get_correo(self) -> str:
        return self.__correo

    def set_correo(self, correo: str) -> None:
        valor = self._validar_texto(correo, "correo")
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor) is None:
            raise ErrorCliente("El correo electrónico no tiene un formato válido.")
        self.__correo = valor

    def get_telefono(self) -> str:
        return self.__telefono

    def set_telefono(self, telefono: str) -> None:
        valor = self._validar_texto(telefono, "teléfono")
        digitos = re.sub(r"\D", "", valor)
        if (
            re.fullmatch(r"\+?[\d\s()-]+", valor) is None
            or not 7 <= len(digitos) <= 15
        ):
            raise ErrorCliente(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )
        self.__telefono = valor

    def validar(self) -> None:
        self._validar_texto(self.__identificacion, "identificación")
        self._validar_texto(self.__nombre, "nombre")
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", self.__correo) is None:
            raise ErrorCliente("El correo electrónico no tiene un formato válido.")
        digitos = re.sub(r"\D", "", self.__telefono)
        if (
            re.fullmatch(r"\+?[\d\s()-]+", self.__telefono) is None
            or not 7 <= len(digitos) <= 15
        ):
            raise ErrorCliente(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "identificacion": self.__identificacion,
            "nombre": self.__nombre,
            "correo": self.__correo,
            "telefono": self.__telefono,
        }
