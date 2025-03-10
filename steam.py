#utilized chatGPT
import numpy as np
from scipy.interpolate import griddata

class steam():
    """
    Class to interpolate and determine steam properties based on saturated and superheated tables.
    """

    def __init__(self, pressure, T=None, x=None, v=None, h=None, s=None, name=''):
        self.p = pressure
        self.T = T
        self.x = x
        self.v = v
        self.h = h
        self.s = s
        self.name = name
        self.region = None
        self.calc()

    def calc(self):
        sat_table = np.loadtxt(r"C:\Users\19182\PycharmProjects\HW6_SP25\Stem_SP25\HW6_3\sat_water_table.txt", skiprows=1)
        super_table = np.loadtxt(r"C:\Users\19182\PycharmProjects\HW6_SP25\Stem_SP25\HW6_3\superheated_water_table.txt", skiprows=1)

        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = sat_table.T
        tcol, hcol, scol, pcol = super_table.T

        Tsat = float(griddata(ps, ts, self.p / 100))
        hf = float(griddata(ps, hfs, self.p / 100))
        hg = float(griddata(ps, hgs, self.p / 100))
        sf = float(griddata(ps, sfs, self.p / 100))
        sg = float(griddata(ps, sgs, self.p / 100))
        vf = float(griddata(ps, vfs, self.p / 100))
        vg = float(griddata(ps, vgs, self.p / 100))

        if self.T is not None:
            if self.T >= Tsat:
                self.region = 'Superheated'
                self.h = float(griddata((pcol, tcol), hcol, (self.p, self.T)))
                self.s = float(griddata((pcol, tcol), scol, (self.p, self.T)))
                self.x = 1.0
            else:
                self.region = 'Saturated'
                self.x = 0
                self.h, self.s, self.v = hf, sf, vf
                self.T = Tsat
        elif self.x is not None:
            self.region = 'Saturated'
            self.T, self.h, self.s, self.v = Tsat, hf + self.x * (hg - hf), sf + self.x * (sg - sf), vf + self.x * (vg - vf)
        elif self.h is not None:
            self.x = (self.h - hf) / (hg - hf)
            self.region = 'Saturated' if 0 <= self.x <= 1 else 'Superheated'
            if self.region == 'Saturated':
                self.T, self.s, self.v = Tsat, sf + self.x * (sg - sf), vf + self.x * (vg - vf)
            else:
                self.T = float(griddata((pcol, hcol), tcol, (self.p, self.h)))
                self.s = float(griddata((pcol, hcol), scol, (self.p, self.h)))
        elif self.s is not None:
            self.x = (self.s - sf) / (sg - sf)
            self.region = 'Saturated' if 0 <= self.x <= 1 else 'Superheated'
            if self.region == 'Saturated':
                self.T, self.h, self.v = Tsat, hf + self.x * (hg - hf), vf + self.x * (vg - vf)
            else:
                self.T = float(griddata((pcol, scol), tcol, (self.p, self.s)))
                self.h = float(griddata((pcol, scol), hcol, (self.p, self.s)))

    def print(self):
        """
        Prints a clear summary of the steam properties.
        """
        print(f'Name: {self.name}')
        print(f'Region: {self.region}')
        print(f'p = {self.p:.2f} kPa')

        # Handle None temperature properly
        if self.T is not None:
            print(f'T = {self.T:.2f} °C')
        else:
            print('T = Not Available')

        print(f'h = {self.h:.2f} kJ/kg')

        if self.s is not None:
            print(f's = {self.s:.4f} kJ/(kg·K)')

        if self.region == 'Saturated':
            print(f'v = {self.v:.6f} m³/kg')
            print(f'x = {self.x:.4f}')

        print()


def main():
    saturated = steam(8000, x=1, name="Saturated Vapor")
    saturated.print()

    superheated = steam(8000, T=500, name="Superheated Vapor")
    superheated.print()


if __name__ == '__main__':
    main()
