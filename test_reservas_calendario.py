import unittest
from datetime import datetime

from asesoria import AsesoriaEspecializada
from cliente import Cliente
from excepciones import ErrorReserva
from gestor import GestorSoftwareFJ
from reserva import ModalidadReserva, Reserva
from sala import ReservaSala


class PruebasCalendarioReservas(unittest.TestCase):
    def setUp(self) -> None:
        self.gestor = GestorSoftwareFJ()
        self.gestor.registrar_cliente(
            Cliente("C-1", "Ana Pérez", "ana@example.com", "3001234567")
        )
        self.sala = ReservaSala("S-1", "Lugar campestre", 100, 5)
        self.gestor.registrar_servicio(self.sala)

    def crear_reserva(
        self,
        identificador: str,
        entrada: datetime,
        salida: datetime,
        personas: int,
        *,
        modalidad: ModalidadReserva = ModalidadReserva.POR_HORAS,
        servicio: str = "S-1",
    ) -> Reserva:
        return self.gestor.crear_reserva(
            identificador,
            "C-1",
            servicio,
            fecha_hora_entrada=entrada,
            fecha_hora_salida=salida,
            cantidad_personas=personas,
            modalidad=modalidad,
        )

    def test_calcula_duracion_y_guarda_modalidad_y_horario(self) -> None:
        reserva = self.crear_reserva(
            "R-1",
            datetime(2026, 12, 1, 18),
            datetime(2026, 12, 2, 8),
            4,
            modalidad=ModalidadReserva.NOCHE_COMPLETA,
        )

        self.assertEqual(reserva.duracion, 14)
        self.assertEqual(reserva.modalidad, ModalidadReserva.NOCHE_COMPLETA)
        self.assertEqual(reserva.cantidad_personas, 4)
        self.assertEqual(
            reserva.to_dict()["fecha_hora_salida"],
            "2026-12-02T08:00:00",
        )

    def test_rechaza_exceso_de_aforo_en_horarios_solapados(self) -> None:
        self.crear_reserva(
            "R-1", datetime(2026, 12, 1, 10), datetime(2026, 12, 1, 12), 3
        )
        self.crear_reserva(
            "R-2", datetime(2026, 12, 1, 11), datetime(2026, 12, 1, 13), 2
        )

        with self.assertRaisesRegex(ErrorReserva, "aforo"):
            self.crear_reserva(
                "R-3",
                datetime(2026, 12, 1, 11, 30),
                datetime(2026, 12, 1, 12, 30),
                1,
            )

        self.assertEqual(len(self.gestor.reservas), 2)

    def test_revisa_aforo_cuando_otra_reserva_inicia_mas_tarde(self) -> None:
        self.crear_reserva(
            "R-1", datetime(2026, 12, 1, 11), datetime(2026, 12, 1, 12), 3
        )

        with self.assertRaisesRegex(ErrorReserva, "aforo"):
            self.crear_reserva(
                "R-2",
                datetime(2026, 12, 1, 10),
                datetime(2026, 12, 1, 13),
                3,
            )

    def test_rechaza_personas_por_encima_de_capacidad_de_una_reserva(self) -> None:
        with self.assertRaisesRegex(ErrorReserva, "capacidad"):
            self.crear_reserva(
                "R-1",
                datetime(2026, 12, 1, 10),
                datetime(2026, 12, 1, 12),
                6,
            )

    def test_reserva_cancelada_libera_aforo(self) -> None:
        primera = self.crear_reserva(
            "R-1", datetime(2026, 12, 1, 10), datetime(2026, 12, 1, 12), 5
        )
        primera.cancelar()

        segunda = self.crear_reserva(
            "R-2", datetime(2026, 12, 1, 10), datetime(2026, 12, 1, 12), 5
        )

        self.assertEqual(segunda.cantidad_personas, 5)

    def test_horarios_contiguos_no_se_consideran_solapados(self) -> None:
        self.crear_reserva(
            "R-1", datetime(2026, 12, 1, 10), datetime(2026, 12, 1, 11), 5
        )

        segunda = self.crear_reserva(
            "R-2", datetime(2026, 12, 1, 11), datetime(2026, 12, 1, 12), 5
        )

        self.assertEqual(segunda.cantidad_personas, 5)

    def test_asesoria_personalizada_no_admite_citas_solapadas(self) -> None:
        asesoria = AsesoriaEspecializada("A-1", "Finanzas", 80)
        self.gestor.registrar_servicio(asesoria)
        self.crear_reserva(
            "R-1",
            datetime(2026, 12, 1, 10),
            datetime(2026, 12, 1, 11),
            1,
            servicio="A-1",
        )

        with self.assertRaisesRegex(ErrorReserva, "aforo"):
            self.crear_reserva(
                "R-2",
                datetime(2026, 12, 1, 10, 30),
                datetime(2026, 12, 1, 11, 30),
                1,
                servicio="A-1",
            )

    def test_modalidad_dia_completo_requiere_horario(self) -> None:
        with self.assertRaisesRegex(ErrorReserva, "requieren fecha"):
            self.gestor.crear_reserva(
                "R-1",
                "C-1",
                "S-1",
                8,
                modalidad=ModalidadReserva.DIA_COMPLETO,
            )

    def test_rechaza_salida_anterior_a_entrada(self) -> None:
        with self.assertRaisesRegex(ErrorReserva, "posterior"):
            self.crear_reserva(
                "R-1",
                datetime(2026, 12, 1, 12),
                datetime(2026, 12, 1, 10),
                1,
            )

    def test_reserva_sin_calendario_conserva_duracion_existente(self) -> None:
        reserva = self.gestor.crear_reserva("R-1", "C-1", "S-1", 2)

        self.assertEqual(reserva.duracion, 2)
        self.assertIsNone(reserva.fecha_hora_entrada)


if __name__ == "__main__":
    unittest.main()
