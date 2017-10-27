from collections import namedtuple
from modules.deco.constants import DecoConstants


class DecoAlgorithm(DecoConstants):
    # Gas structures

    Gas = namedtuple("Gas", "FrN2 FrO2 FrHe")

    Gases = [Gas(0.79, 0.21, 0)]

    DecoStop = namedtuple("DecoStop", "Depth Time")

    GasNames = {'Air': 0}

    # Dive Parameters

    DecentRate = 30
    AccentRate = -18
    currentGasIndex = 0

    Depth = 1
    MaxDepth = 1
    TissueAccentCeiling = []
    AccentCeiling = 0
    LimitingTissueIndex = 0

    GFHigh = 0.8
    GFLow = 0.3

    # Gas Parameters

    ppN2 = 0.79
    ppO2 = 0.21
    ppHe = 0

    NitrogenLoading = []
    HeliumLoading = []
    TotalLoading = []

    # Environmental Parameters
    AmbientPressure = 1
    ppWaterVapor = 0

    def create_gas(self, fr_o2, fr_he):
        fr_n2 = 1 - fr_o2 - fr_he
        self.Gases.append(self.Gas(fr_n2, fr_o2, fr_he))
        gas_name = str(fr_o2 * 100) + '/' + str(fr_he * 100)
        self.GasNames[gas_name] = len(self.Gases) - 1
