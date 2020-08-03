#! usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime
import clr
import cmsmodel
import json
import sys

def main():

    description = construct_description()
    model = create_model(description)
    config = set_configuration()
    solver = create_solver(config, model)
    start = datetime.now()
    trajectories, taus = solve_once(solver, config["duration"])
    finish = datetime.now()
    print(f"Solver took {finish-start} seconds for {len(taus)} timesteps.")

    return


TOTAL_POPULATION = 10000
INITIAL_SUSCEPTIBLE = TOTAL_POPULATION * 5 // 80    # Up to 5 y.o. with "max" age 80
INITIAL_INFECTIOUS = 10
INITIAL_RECOVERED = TOTAL_POPULATION - (INITIAL_SUSCEPTIBLE + INITIAL_INFECTIOUS)


def construct_description():

    description = cmsmodel.CmsModel("polio")

    description.add_species("S",  INITIAL_SUSCEPTIBLE, observe=True)
    description.add_species("I",  INITIAL_INFECTIOUS,  observe=True)
    description.add_species("R",  INITIAL_RECOVERED,   observe=True)
    description.add_species("CI", 0, observe=True)  # Count of Infections
    description.add_species("CP", 0, observe=True)  # Count of Paralysis

    Ki = 1.05/30/(5/80)     # R0 1.05, 30 day mean infectious duration, in under 5 population
    # Ki = 1.05/30            # R0 1.05, 30 day mean infectious duration
    Kp = 1/200              # ratio of paralytic cases
    Kin = (1-Kp)*Ki         # non-paralytic cases
    Kip = Kp*Ki             # paralytic cases
    Kr = 1/30               # recover, 30 day mean infectious duration

    description.add_parameter("Kin", Kin)
    description.add_parameter("Kip", Kip)
    description.add_parameter("Kr", Kr)

    description.add_reaction("infection", ["S"], ["I", "CI"], "(/ (* Kin S I) (+ S I R))")
    description.add_reaction("paralysis", ["S"], ["I", "CI", "CP"], "(/ (* Kip S I) (+ S I R))")
    description.add_reaction("recovery",  ["I"], ["R"], "(* Kr I)")

    return description


def create_model(description):

    from compartments.emodl import EmodlLoader
    model = EmodlLoader.LoadEMODLModel(str(description))

    return model


def set_configuration():

    from compartments import Configuration as cfg
    config = {
        "solver": "SSA",
        "runs": 1,
        "duration": 365,
        "samples": 365,
        "prng_seed": datetime.now().microsecond
    }
    cfg.CurrentConfiguration = cfg.ConfigurationFromString(json.dumps(config))

    return config


def create_solver(config, model):

    from compartments.emod.utils import SolverFactory as factory
    solver = factory.CreateSolver(config["solver"], model, config["runs"], config["duration"], config["samples"])

    return solver


def solve_once(solver, duration):

    solver.StartRealization()
    species = {population: [population.Count] for population in solver.model.Species}
    taus = [0]

    susceptible = get_species_by_name(solver, "S")
    recovered = get_species_by_name(solver, "R")
    cp = get_species_by_name(solver, "CP")

    while solver.CurrentTime < duration:
        new_tau = solver.CalculateProposedTau(sys.float_info.max)
        solver.CurrentTime = new_tau
        if new_tau < duration:
            solver.ExecuteReactions()
            record_species(solver, species)
            taus.append(new_tau)
            if check_paralysis(species, cp, new_tau):
                print(f"Detected paralytic case at time {new_tau}.")
                vaccinations = int(0.2 * susceptible.Count)
                susceptible.Count -= vaccinations
                recovered.Count += vaccinations

    return species, taus


def get_species_by_name(solver, name):

    return [population for population in solver.model.Species if population.Name == name][0]


def check_paralysis(species: dict, cp, tau: float):

    counts = species[cp]
    return counts[-1] > counts[-2]


def record_species(solver, species: dict):

    for s, c in species.items():
        c.append(s.Count)

    return


if __name__ == "__main__":

    parser = ArgumentParser()
    # The default value here will work if the .NET assembly "compartments" is in the PYTHONPATH.
    # If you are using the pycms docker container, this will be the case. Note that the default value
    # doesn't have ".exe" at the end of it.
    parser.add_argument("-c", "--compartments", default="compartments", help="Specify full path to compartments.exe")

    args = parser.parse_args()

    clr.AddReference(args.compartments)

    main()
