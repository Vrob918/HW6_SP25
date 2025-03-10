#utilized chatGPT
from rankine import rankine

def main():
    # First Rankine Cycle (Saturated Vapor entering turbine)
    saturated_cycle = rankine(p_low=8, p_high=8000, name='Saturated Vapor Cycle')
    saturated_cycle.calc_efficiency()
    saturated_cycle.print_summary()

    # Determine Tsat at p_high for the second cycle
    Tsat_high = saturated_cycle.state1.T
    T_high_superheated = 1.7 * Tsat_high

    # Second Rankine Cycle (Superheated steam entering turbine)
    superheated_cycle = rankine(p_low=8, p_high=8000, t_high=T_high_superheated, name='Superheated Steam Cycle')
    superheated_cycle.calc_efficiency()
    superheated_cycle.print_summary()

if __name__ == "__main__":
    main()