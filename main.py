"""Simulación de operaciones válidas e inválidas de Software FJ."""

from collections.abc import Callable

from asesoria import AsesoriaEspecializada
from cliente import Cliente
from equipo import AlquilerEquipo
from excepciones import ErrorSoftwareFJ
from gestor import GestorSoftwareFJ
from logger import cerrar_logger, registrar_operacion
from reserva import Reserva
from sala import ReservaSala


def ejecutar_operacion(
    nombre: str,
    accion: Callable[[], object],
) -> bool:
    """Ejecuta una operación aislada y contabiliza errores."""
    try:
        with registrar_operacion(nombre):
            accion()
    except ErrorSoftwareFJ as error:
        print(f"[RECHAZADA] {nombre}: {error}")
        return False
    except Exception as error:
        print(
            f"[ERROR INESPERADO] {nombre}: "
            f"{type(error).__name__}: {error}"
        )
        return False
    print(f"[OK] {nombre}")
    return True


def main() -> None:
    gestor = GestorSoftwareFJ()
    resultados: list[bool] = []
    reservas: dict[str, Reserva] = {}

    sala = ReservaSala("S-1", "Sala Norte", 100.0, 20)
    equipo = AlquilerEquipo("E-1", "Proyector", 50.0, 3)
    asesoria = AsesoriaEspecializada("A-1", "Finanzas", 80.0)
    sala_cerrada = ReservaSala(
        "S-2",
        "Sala cerrada",
        90.0,
        10,
        disponibilidad=False,
    )
    gestor.registrar_servicio(sala_cerrada)

    def registrar_cliente_valido() -> None:
        gestor.registrar_cliente(
            Cliente(
                "C-1",
                "Ana Pérez",
                "ana@example.com",
                "+57 300 1234567",
            )
        )

    def registrar_cliente_invalido() -> None:
        Cliente("C-2", "Cliente de prueba", "correo-invalido", "3001234567")

    def registrar_cliente_duplicado() -> None:
        gestor.registrar_cliente(
            Cliente(
                "C-1",
                "Otro nombre",
                "otro@example.com",
                "3001234567",
            )
        )

    def crear_reserva_valida() -> None:
        reserva = gestor.crear_reserva("R-1", "C-1", "S-1", 2)
        reserva.confirmar()
        reservas["confirmada"] = reserva

    def intentar_reserva_no_disponible() -> None:
        gestor.crear_reserva("R-2", "C-1", "S-2", 1)

    def intentar_reserva_duracion_invalida() -> None:
        gestor.crear_reserva("R-3", "C-1", "S-1", 0)

    def crear_y_cancelar_reserva() -> None:
        reserva = gestor.crear_reserva("R-4", "C-1", "S-1", 1)
        reserva.cancelar()
        reservas["cancelada"] = reserva

    def crear_reserva_asesoria() -> None:
        reserva = gestor.crear_reserva("R-5", "C-1", "A-1", 1.5)
        reserva.confirmar()
        reservas["asesoria"] = reserva

    def confirmar_reserva_cancelada() -> None:
        reservas["cancelada"].confirmar()

    def calcular_costo_con_impuestos() -> None:
        costo = reservas["confirmada"].procesar(
            impuesto=0.19,
            descuento=0.10,
        )
        print(f"Costo calculado con impuesto y descuento: {costo:.2f}")

    def procesar_reserva_asesoria() -> None:
        costo = reservas["asesoria"].procesar()
        print(f"Costo de la asesoría: {costo:.2f}")

    operaciones: list[tuple[str, Callable[[], object]]] = [
        ("Registrar un cliente válido", registrar_cliente_valido),
        ("Rechazar un correo inválido", registrar_cliente_invalido),
        ("Rechazar un cliente duplicado", registrar_cliente_duplicado),
        ("Registrar un servicio de sala", lambda: gestor.registrar_servicio(sala)),
        (
            "Registrar un servicio de equipo",
            lambda: gestor.registrar_servicio(equipo),
        ),
        (
            "Registrar un servicio de asesoría",
            lambda: gestor.registrar_servicio(asesoria),
        ),
        (
            "Rechazar un servicio con tarifa negativa",
            lambda: ReservaSala("S-3", "Sala inválida", -10, 5),
        ),
        ("Crear y confirmar una reserva", crear_reserva_valida),
        ("Rechazar reserva de un servicio no disponible", intentar_reserva_no_disponible),
        ("Rechazar una duración inválida", intentar_reserva_duracion_invalida),
        ("Crear y cancelar una reserva", crear_y_cancelar_reserva),
        ("Rechazar confirmación de reserva cancelada", confirmar_reserva_cancelada),
        ("Crear y confirmar una reserva de asesoría", crear_reserva_asesoria),
        ("Procesar costo con impuesto y descuento", calcular_costo_con_impuestos),
        ("Procesar costo de reserva de asesoría", procesar_reserva_asesoria),
        (
            "Continuar después de errores",
            lambda: gestor.buscar_cliente("C-1").validar(),
        ),
    ]

    try:
        for nombre, accion in operaciones:
            resultados.append(ejecutar_operacion(nombre, accion))
    finally:
        print("\nResumen")
        print(f"Operaciones ejecutadas: {len(resultados)}")
        print(f"Operaciones completadas: {sum(resultados)}")
        print(f"Operaciones rechazadas: {len(resultados) - sum(resultados)}")
        print(f"Clientes en memoria: {len(gestor.clientes)}")
        print(f"Servicios en memoria: {len(gestor.servicios)}")
        print(f"Reservas en memoria: {len(gestor.reservas)}")
        cerrar_logger()


if __name__ == "__main__":
    main()
