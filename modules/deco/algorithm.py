from collections import namedtuple
from modules.deco.constants import DecoConstants
import math
import copy
from modules.deco.utilities import *

class DecoAlgorithm(DecoConstants):
    # Gas structures

    Gas = namedtuple("Gas", "FrN2 FrO2 FrHe")

    Gases = [Gas(0.79, 0.21, 0)]

    GasNames = {'Air': 0}

    # Deco Structures

    DecoStop = namedtuple("DecoStop", "Depth Time")

    # Dive Parameters

    DecentRate = 30
    AccentRate = -18
    currentGasIndex = 0

    Depth = 1
    MaxDepth = 1
    TissueAccentCeiling = [-math.inf] * 16
    AccentCeiling = -math.inf
    LimitingTissueIndex = 0

    GFHigh = 0.8
    GFLow = 0.3

    # Gas Parameters

    ppN2 = 0.79
    ppO2 = 0.21
    ppHe = 0

    NitrogenLoadings = [0] * 16
    HeliumLoadings = [0] * 16
    TotalLoadings = [0] * 16

    # Environmental Parameters
    AmbientPressure = 1
    ppWaterVapor = 0

    def __init__(self):
        self.NitrogenLoadings = [0] * 16
        self.HeliumLoadings = [0] * 16
        self.TotalLoadings = [0] * 16
        self.TissueAccentCeiling = [-math.inf] * 16

    def create_gas(self, fr_o2, fr_he):
        fr_n2 = 1 - fr_o2 - fr_he
        self.Gases.append(self.Gas(fr_n2, fr_o2, fr_he))
        gas_name = str(fr_o2 * 100) + '/' + str(fr_he * 100)
        self.GasNames[gas_name] = len(self.Gases) - 1

    def set_partial_pressures(self, depth):
        self.AmbientPressure = depth
        self.ppN2 = self.Gases[self.currentGasIndex].FrN2 * (self.AmbientPressure - self.ppWaterVapor)
        self.ppO2 = self.Gases[self.currentGasIndex].FrO2 * (self.AmbientPressure - self.ppWaterVapor)
        self.ppHe = self.Gases[self.currentGasIndex].FrHe * (self.AmbientPressure - self.ppWaterVapor)

    def add_decent(self, depth, decent_rate):
        if depth > self.MaxDepth:
            self.MaxDepth = depth
        delta_depth = depth - self.Depth
        for i in range(16):
            time = delta_depth / decent_rate

            # Calculate Nitrogen
            pp_n2 = self.ppN2
            current_nitrogen_loading = self.NitrogenLoadings[i]
            r_n2 = decent_rate * self.Gases[self.currentGasIndex].FrN2
            k_n2 = math.log(2) / self.buehlmann_N2_halflife[i]

            nitrogen_loading = pp_n2 + r_n2 * (time - (1 / k_n2)) - (pp_n2 - current_nitrogen_loading - (
            r_n2 / k_n2)) * math.exp(-k_n2 * time)

            # Calculate Helium
            pp_he = self.ppHe
            current_helium_loading = self.HeliumLoadings[i]
            r_he = decent_rate * self.Gases[self.currentGasIndex].FrHe
            k_he = math.log(2) / self.buehlmann_He_halflife[i]

            helium_loading = pp_he + r_he * (time - (1 / k_he)) - (pp_he - current_helium_loading - (
            r_he / k_he)) * math.exp(-k_he * time);

            # Final totaling
            self.NitrogenLoadings[i] = nitrogen_loading
            self.HeliumLoadings[i] = helium_loading
            self.TotalLoadings[i] = nitrogen_loading + helium_loading
        self.set_partial_pressures(depth)
        self.Depth = depth

    def add_bottom(self, time):
        for i in range(16):
            # Calculate Nitrogen
            pp_n2 = self.ppN2
            current_nitrogen_loading = self.NitrogenLoadings[i]
            n2_halflife = self.buehlmann_N2_halflife[i]

            nitrogen_loading = current_nitrogen_loading + (pp_n2 - current_nitrogen_loading) * (
            1 - pow(2, -time / n2_halflife))

            # Calculate Helium
            pp_he = self.ppHe
            current_helium_loading = self.HeliumLoadings[i]
            he_halflife = self.buehlmann_He_halflife[i]

            helium_loading = current_helium_loading + (pp_he - current_helium_loading) * (
            1 - pow(2, -time / he_halflife))

            # Final totaling
            self.NitrogenLoadings[i] = nitrogen_loading
            self.HeliumLoadings[i] = helium_loading
            self.TotalLoadings[i] = nitrogen_loading + helium_loading

    def set_pp_water_vapor(self, pp_water_vapor):
        self.ppWaterVapor = pp_water_vapor
        self.set_partial_pressures(self.Depth)

    def get_m_value(self, tissue_index, depth):
        self.set_partial_pressures(depth)
        pp_n2 = self.ppN2
        a_n2 = self.buehlmann_N2_a[tissue_index]
        b_n2 = self.buehlmann_N2_b[tissue_index]

        pp_he = self.ppHe
        a_he = self.buehlmann_He_a[tissue_index]
        b_he = self.buehlmann_He_b[tissue_index]
        try:
            a = ((a_n2 * pp_n2) + (a_he * pp_he)) / (pp_n2 + pp_he)
            b = ((b_n2 * pp_n2) + (b_he * pp_he)) / (pp_n2 + pp_he)
            return (depth / b) + a
        except:
            return -math.inf

    def get_gf_point(self, depth):
        gf_high = self.GFHigh
        gf_low = self.GFLow
        low_depth = self.MaxDepth

        return gf_high - ((gf_high - gf_low) / low_depth) * depth

    def get_ceiling(self):
        self.LimitingTissueIndex = 0
        for i in range(16):
            deco_sim = copy.copy(self)
            current_ceiling = 0
            in_limits = False
            while not in_limits:
                nitrogen_loading = deco_sim.NitrogenLoadings[i]
                helium_loading = deco_sim.HeliumLoadings[i]
                ambient_pressure = deco_sim.AmbientPressure
                max_gf = deco_sim.get_gf_point(current_ceiling)
                theoretical_gf = ((nitrogen_loading + helium_loading) - ambient_pressure) / (
                deco_sim.get_m_value(i, current_ceiling) - ambient_pressure)

                if theoretical_gf < max_gf and theoretical_gf != 0.0:
                    in_limits = True
                else:
                    current_ceiling += 0.1
            self.TissueAccentCeiling[i] = current_ceiling

            if self.TissueAccentCeiling[i] > self.TissueAccentCeiling[self.LimitingTissueIndex]:
                self.LimitingTissueIndex = i

        ceiling = self.TissueAccentCeiling[self.LimitingTissueIndex]
        self.AccentCeiling = ceiling
        return ceiling

    def get_no_deco_time(self):
        no_stop_time = 0
        in_limits = True
        while in_limits:
            deco_sim = copy.deepcopy(self)
            deco_sim.add_bottom(no_stop_time)
            in_limits = deco_sim.get_ceiling() < 1
            no_stop_time += 1
            if no_stop_time > 999:
                return 999
        no_stop_time -= 1
        return no_stop_time

    def get_next_deco_stop(self):
        # Round Deco depth to next multiple of 3 m (return as bar)
        stop_depth = meter_to_bar(math.ceil(bar_to_meter(self.get_ceiling()) / 3) * 3)
        stop_time = 0
        in_limits = False
        while not in_limits:
            stop_time += 1
            deco_sim = copy.deepcopy(self)
            deco_sim.add_decent(stop_depth, -meter_to_bar(self.AccentRate))
            deco_sim.add_bottom(stop_time)
            in_limits = deco_sim.get_ceiling() < stop_depth - 0.3
        return self.DecoStop(stop_depth, stop_time)

    def get_deco_schedule(self):
        schedule = []
        deco_sim = copy.deepcopy(self)
        while deco_sim.get_ceiling() > 1:
            stop = deco_sim.get_next_deco_stop()
            schedule.append(stop)
            deco_sim.add_decent(stop.Depth, -meter_to_bar(self.AccentRate))
            deco_sim.add_bottom(stop.Time)
        return schedule
