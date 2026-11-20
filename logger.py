"""Registro de eventos y errores del sistema Software FJ.

El archivo de logs se guarda en:
    logs/software_fj.log

Este módulo no almacena clientes, servicios ni reservas.
Solo registra eventos y errores de la aplicación.
"""

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from time import perf_counter

from excepciones import ErrorRegistro


NOMBRE_LOGGER = "software_fj"
CARPETA_LOGS = Path(__file__).resolve().parent / "logs"
ARCHIVO_LOG = CARPETA_LOGS / "software_fj.log"


def configurar_logger() -> logging.Logger:
    """Configura y devuelve el logger compartido de la aplicación."""
    logger = logging.getLogger(NOMBRE_LOGGER)

    if logger.handlers:
        return logger

    try:
        CARPETA_LOGS.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(
            ARCHIVO_LOG,
            mode="a",
            encoding="utf-8",
        )
    except OSError as error:
        raise ErrorRegistro(
            "No se pudo crear o abrir el archivo de logs."
        ) from error

    formato = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formato)
    handler.setLevel(logging.INFO)

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def registrar_evento(mensaje: str) -> None:
    """Guarda un evento informativo en el archivo de logs."""
    configurar_logger().info("%s", mensaje)


def registrar_advertencia(mensaje: str) -> None:
    """Guarda una advertencia en el archivo de logs."""
    configurar_logger().warning("%s", mensaje)


def registrar_error(mensaje: str, error: Exception) -> None:
    """Guarda un error y su traceback asociado."""
    configurar_logger().error(
        "%s | %s: %s",
        mensaje,
        type(error).__name__,
        error,
        exc_info=(type(error), error, error.__traceback__),
    )


@contextmanager
def registrar_operacion(nombre: str) -> Iterator[None]:
    """Supervisa una operación y registra su inicio, resultado y duración."""
    logger = configurar_logger()
    inicio = perf_counter()

    logger.info("Inicio de operación: %s", nombre)

    try:
        yield
    except Exception as error:
        logger.error(
            "Operación fallida: %s | %s: %s",
            nombre,
            type(error).__name__,
            error,
            exc_info=True,
        )
        raise
    else:
        logger.info("Operación completada: %s", nombre)
    finally:
        duracion = perf_counter() - inicio
        logger.info(
            "Fin de operación: %s | Duración: %.4f segundos",
            nombre,
            duracion,
        )


def cerrar_logger() -> None:
    """Vacía y cierra los handlers del logger compartido."""
    logger = logging.getLogger(NOMBRE_LOGGER)

    for handler in logger.handlers[:]:
        try:
            handler.flush()
        finally:
            try:
                handler.close()
            finally:
                logger.removeHandler(handler)


def demostrar_logging() -> None:
    """Ejecuta una demostración del registro de eventos."""
    from excepciones import ErrorValidacion

    try:
        registrar_evento("Inicio de la demostración de Software FJ.")

        with registrar_operacion("Operación de prueba válida"):
            print("La primera operación terminó correctamente.")

        registrar_advertencia(
            "Demostración: se ejecutará una operación inválida."
        )

        try:
            with registrar_operacion("Validar duración de una reserva"):
                duracion = -2
                if duracion <= 0:
                    raise ErrorValidacion(
                        "La duración debe ser mayor que cero."
                    )
        except ErrorValidacion as error:
            print(f"Error controlado: {error}")

        with registrar_operacion("Continuar después del error"):
            print("El programa continúa funcionando.")

        registrar_evento("Fin de la demostración de Software FJ.")

    except ErrorRegistro as error:
        print(f"No fue posible iniciar el registro: {error}")

    finally:
        cerrar_logger()


if __name__ == "__main__":
    demostrar_logging()
