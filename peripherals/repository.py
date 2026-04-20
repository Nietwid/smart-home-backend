from typing import Optional
from peripherals.models import Peripherals


class PeripheralRepository:

    def get_by_id_with_device(self, pk: int) -> Optional[Peripherals]:
        return Peripherals.objects.filter(pk=pk).prefetch_related("device").first()


peripheral_repository = PeripheralRepository()
