#utilized chatGPT
from steam import steam

class rankine():
    """
    The rankine class analyzes a Rankine cycle by calculating efficiency,
    turbine work, pump work, and heat added based on steam properties.
    """

    def __init__(self, p_low=8, p_high=8000, t_high=None, name='Rankine Cycle'):
        """
        Initialize Rankine cycle parameters.

        :param p_low: Low cycle pressure (condenser) in kPa
        :param p_high: High cycle pressure (boiler) in kPa
        :param t_high: Optional turbine inlet temperature in °C (superheated)
        :param name: Descriptive name of the Rankine cycle
        """
        self.p_low = p_low
        self.p_high = p_high
        self.t_high = t_high
        self.name = name
        self.efficiency = None
        self.turbine_work = 0
        self.pump_work = 0
        self.heat_added = 0
        self.state1 = None
        self.state2 = None
        self.state3 = None
        self.state4 = None

    def calc_efficiency(self):
        """
        Calculates Rankine cycle efficiency by determining thermodynamic
        states around the cycle.

        :return: Efficiency as a percentage
        """
        # State 1: Turbine Inlet (saturated or superheated vapor)
        if self.t_high is None:
            self.state1 = steam(self.p_high, x=1, name='Turbine Inlet')
        else:
            self.state1 = steam(self.p_high, T=self.t_high, name='Turbine Inlet')

        # State 2: Turbine Exit (isentropic expansion)
        self.state2 = steam(pressure=self.p_low, s=self.state1.s, name='Turbine Exit')

        # State 3: Pump Inlet (saturated liquid)
        self.state3 = steam(pressure=self.p_low, x=0, name='Pump Inlet')

        # State 4: Pump Exit (isentropic compression, approximated as compressed liquid)
        self.state4 = steam(pressure=self.p_high, s=self.state3.s, name='Pump Exit')
        self.state4.h = self.state3.h + self.state3.v * (self.p_high - self.p_low)
        self.state4.region = 'Compressed Liquid'  # explicitly set region to compressed liquid
        self.state4.T = None  # explicitly indicate no valid temperature

        # Calculate turbine work, pump work, and heat added
        self.turbine_work = self.state1.h - self.state2.h
        self.pump_work = self.state4.h - self.state3.h
        self.heat_added = self.state1.h - self.state4.h

        # Efficiency calculation
        self.efficiency = 100.0 * (self.turbine_work - self.pump_work) / self.heat_added
        return self.efficiency

    def print_summary(self):
        """
        Prints a detailed summary of the Rankine cycle including efficiency
        and state properties.
        """
        if self.efficiency is None:
            self.calc_efficiency()

        print(f'\n--- Rankine Cycle Summary ({self.name}) ---')
        print(f'Efficiency: {self.efficiency:.3f}%')
        print(f'Turbine Work: {self.turbine_work:.2f} kJ/kg')
        print(f'Pump Work: {self.pump_work:.2f} kJ/kg')
        print(f'Heat Added: {self.heat_added:.2f} kJ/kg')
        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()


def main():
    saturated_cycle = rankine(p_low=8, p_high=8000, name='Saturated Rankine Cycle')
    saturated_cycle.calc_efficiency()
    saturated_cycle.print_summary()

    superheated_cycle = rankine(p_low=8, p_high=8000,
                                t_high=1.7 * saturated_cycle.state1.T,
                                name='Superheated Rankine Cycle')
    superheated_cycle.calc_efficiency()
    superheated_cycle.print_summary()


if __name__ == '__main__':
    main()