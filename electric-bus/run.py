import subprocess
import argparse
import os


class SimulationRunner(object):
    """
    docstring
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Run bus replacement approach."
        )

        self.parser.add_argument(
            "--approach",
            type=str,
            help="Name of the approach to run",
        )
        self.parser.add_argument(
            "--per", default=0.25, type=float, help="Percentage of flow to replace"
        )

        self.args = self.parser.parse_args()
        self.approach = self.args.approach
        self.per = self.args.per
        self.perFolder = str(int(self.per * 100))
        self.simFolderInput = "./electric-bus/outputs/default/"
        self.flowInput = "./electric-bus/outputs/default/flow.csv"
        self.scoreOutput = f"./electric-bus/outputs/{self.approach}/scoreOutput.csv"
        self.flowXmlInput = "./electric-bus/outputs/default/flow.xml"
        self.flowXmlOutput = (
            f"./electric-bus/outputs/{self.approach}/{self.perFolder}per/flow.xml"
        )
        self.outputFolder = (
            f"./electric-bus/outputs/{self.approach}/{self.perFolder}per/"
        )
        self.sumocfg = "./scenario/InTAS_full_poly.sumocfg"

    def run(self):
        subprocess.run(
            [
                "python",
                f"./electric-bus/approachs/{self.approach}.py",
                "--simFolderInput",
                self.simFolderInput,
                "--flowInput",
                self.flowInput,
                "--scoreOutput",
                self.scoreOutput,
                "--outputFolder",
                self.outputFolder,
            ]
        )

        subprocess.run(
            [
                "python",
                "./electric-bus/approachs/scripts/replace_flow.py",
                "--scoreInput",
                self.scoreOutput,
                "--flowInput",
                self.flowXmlInput,
                "--flowOutput",
                self.flowXmlOutput,
                "--outputFolder",
                self.outputFolder,
                "--per",
                str(self.per),
            ]
        )

        subprocess.run(
            [
                "python",
                "./electric-bus/approachs/scripts/run_simulation.py",
                "--flowInput",
                self.flowXmlOutput,
                "--outputFolder",
                self.outputFolder,
                "--sumocfg",
                self.sumocfg,
                "--N",
                "10",
                "--xml2csv",
                "True",
            ]
        )


if __name__ == "__main__":
    simulation_runner = SimulationRunner()
    simulation_runner.run()

