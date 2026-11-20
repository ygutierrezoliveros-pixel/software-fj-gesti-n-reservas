"""Gestión en memoria de clientes, servicios y reservas."""

from cliente import Cliente
from excepciones import (
    ErrorCliente,
    ErrorClienteDuplicado,
    ErrorReserva,
    ErrorServicio,
)
from reserva import Reserva
from servicio import Servicio


class GestorSoftwareFJ:
    """Mantiene las colecciones del sistema únicamente en memoria."""

    def __init__(self) -> None:
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, cliente: Cliente) -> Cliente:
        if not isinstance(cliente, Cliente):
            raise ErrorCliente("Solo se pueden registrar clientes válidos.")
        cliente.validar()
        identificacion = cliente.get_identificacion()
        if any(
            existente.get_identificacion() == identificacion
            for existente in self.clientes
        ):
            raise ErrorClienteDuplicado(
                f"Ya existe un cliente con identificación '{identificacion}'."
            )
        self.clientes.append(cliente)
        return cliente

    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        if not isinstance(servicio, Servicio):
            raise ErrorServicio("Solo se pueden registrar servicios válidos.")
        servicio.validar_parametros()
        if any(
            existente.identificador == servicio.identificador
            for existente in self.servicios
        ):
            raise ErrorServicio(
                f"Ya existe un servicio con identificador "
                f"'{servicio.identificador}'."
            )
        self.servicios.append(servicio)
        return servicio

    def crear_reserva(
        self,
        identificador: str,
        identificacion_cliente: str,
        identificador_servicio: str,
        duracion: float,
    ) -> Reserva:
        if not isinstance(identificador, str) or not identificador.strip():
            raise ErrorReserva("El identificador debe ser un texto no vacío.")
        identificador_validado = identificador.strip()
        if any(
            existente.identificador == identificador_validado
            for existente in self.reservas
        ):
            raise ErrorReserva(
                f"Ya existe una reserva con identificador "
                f"'{identificador_validado}'."
            )
        cliente = self.buscar_cliente(identificacion_cliente)
        servicio = self.buscar_servicio(identificador_servicio)
        reserva = Reserva(identificador_validado, cliente, servicio, duracion)
        self.reservas.append(reserva)
        return reserva

    def buscar_cliente(self, identificacion: str) -> Cliente:
        for cliente in self.clientes:
            if cliente.get_identificacion() == identificacion:
                return cliente
        raise ErrorCliente(
            f"No se encontró el cliente '{identificacion}'."
        )

    def buscar_servicio(self, identificador: str) -> Servicio:
        for servicio in self.servicios:
            if servicio.identificador == identificador:
                return servicio
        raise ErrorServicio(
            f"No se encontró el servicio '{identificador}'."
        )

    def buscar_reserva(self, identificador: str) -> Reserva:
        for reserva in self.reservas:
            if reserva.identificador == identificador:
                return reserva
        raise ErrorReserva(
            f"No se encontró la reserva '{identificador}'."
        )
