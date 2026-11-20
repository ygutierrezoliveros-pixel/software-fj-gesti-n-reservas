"""Servicio de asesoría especializada."""

from servicio import Servicio


class AsesoriaEspecializada(Servicio):
    """Asesoría cobrada por hora, con tarifa_base como tarifa por hora."""

    def __init__(
        self,
        identificador: str,
        especialidad: str,
        tarifa_por_hora: float,
        disponibilidad: bool = True,
    ) -> None:
        especialidad_validada = self._validar_texto(
            especialidad, "especialidad"
        )
        super().__init__(
            identificador,
            especialidad_validada,
            tarifa_por_hora,
            disponibilidad,
        )
        self._especialidad = especialidad_validada

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @property
    def tarifa_por_hora(self) -> float:
        return self.tarifa_base

    def validar_parametros(self) -> None:
        super().validar_parametros()
        self._validar_texto(self._especialidad, "especialidad")

    def calcular_costo(
        self,
        duracion: float,
        *,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        return super().calcular_costo(
            duracion,
            impuesto=impuesto,
            descuento=descuento,
        )

    def describir(self) -> str:
        return (
            f"Asesoría especializada en {self.especialidad} "
            f"(tarifa por hora: {self.tarifa_por_hora:.2f})."
        )

    def to_dict(self) -> dict[str, object]:
        return {
            **super().to_dict(),
            "especialidad": self.especialidad,
            "tarifa_por_hora": self.tarifa_por_hora,
        }
