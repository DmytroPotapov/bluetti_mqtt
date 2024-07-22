from typing import List
from ..commands import ReadHoldingRegisters
from .bluetti_device import BluettiDevice
from .struct import DeviceStruct
from enum import Enum, unique


@unique
class ChargingMode(Enum):
    STANDARD = 0
    SILENT = 1
    TURBO = 2


class AC180(BluettiDevice):
    def __init__(self, address: str, sn: str):
        self.struct = DeviceStruct()

        # Power IO
        self.struct.add_uint_field("dc_output_power", 140)
        self.struct.add_uint_field("ac_output_power", 142)
        self.struct.add_uint_field("dc_input_power", 144)
        self.struct.add_uint_field("ac_input_power", 146)

        # Input Details (1100 - 1300)
        self.struct.add_decimal_field("ac_input_voltage", 1314, 1)

        # Controls (2000)
        self.struct.add_bool_field("ac_output_on_switch", 2011)
        self.struct.add_bool_field("dc_output_on_switch", 2012)
        self.struct.add_bool_field(
            "silent_charging_on", 2020
        )  # to be able to choose between normal and silent charging modes
        self.struct.add_enum_field(
            "charging_mode", 2020, ChargingMode
        )  # can't be set from HA, custom switch needed
        self.struct.add_bool_field("power_lifting_on", 2021)

        # Controls (2200)
        self.struct.add_bool_field("grid_enhancement_mode_on", 2225)

        super().__init__(address, 'AC180', sn)

    @property
    def polling_commands(self) -> List[ReadHoldingRegisters]:
            [
                ReadHoldingRegisters(140, 1),
                ReadHoldingRegisters(142, 1),
                ReadHoldingRegisters(144, 1),
                ReadHoldingRegisters(146, 1),
                ReadHoldingRegisters(1314, 1),
                ReadHoldingRegisters(2011, 1),
                ReadHoldingRegisters(2012, 1),
                ReadHoldingRegisters(2020, 1),
                ReadHoldingRegisters(2021, 1),
                ReadHoldingRegisters(2225, 1),
            ]

    @property
    def writable_ranges(self) -> List[range]:
        return  [range(2000, 2022), range(2200, 2226)
