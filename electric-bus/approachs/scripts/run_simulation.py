import argparse
import random
import subprocess


class RunSimulation(object):
    """
        Run 'n' SUMO simulations
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Run 'n' SUMO simulations"
        )
        self.parser.add_argument(
            "--flowInput",
            type=str,
            help="File (xml) with bus flow",
        )
        self.parser.add_argument(
            "--outputFolder",
            type=str,
            default="./outputs/",
            help="Folder to save the output files (default: ./output/)",
        )
        self.parser.add_argument(
            "--sumocfg",
            type=str,
            help="File (xml) with the base SUMO configuration",
        )
        self.parser.add_argument(
            "--N",
            type=int,
            default=10,
            help="Number of simulations to run (default: 10)",
        )
        self.parser.add_argument(
            "--xml2csv",
            type=bool,
            default=False,
            help="Convert the output xml files to csv (default: False)",
        )
        

        self.args = self.parser.parse_args()
        self.flowInput = self.args.flowInput
        self.outputFolder = self.args.outputFolder
        self.sumocfg = self.args.sumocfg
        self.N = self.args.N

    def run(self):
        for i in range(self.N):
            print(f"Running simulation {i+1}")
            subprocess.run(
                [
                    "sumo.exe",
                    "-c",
                    self.sumocfg,
                    "-r",
                    self.flowInput,
                    "--emission-output",
                    f"{self.outputFolder}simulation_{i+1}.emission.xml",
                    "--tripinfo-output",
                    f"{self.outputFolder}simulation_{i+1}.tripinfo.xml",
                    "--seed",
                    str(random.randint(0, 99999)),
                ]
            )
            if self.args.xml2csv:
                subprocess.run(
                    [
                        "python",
                        "./eletric_bus/approachs/scripts/xml2csv.py",
                        f"{self.outputFolder}simulation_{i+1}.emission.xml",
                    ]
                )
                subprocess.run(
                    [
                        "python",
                        "./eletric_bus/approachs/scripts/xml2csv.py",
                        f"{self.outputFolder}simulation_{i+1}.tripinfo.xml",
                    ]
                )


if __name__ == "__main__":
    runSimulation = RunSimulation()
    runSimulation.run()