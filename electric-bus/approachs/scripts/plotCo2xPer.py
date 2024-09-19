import argparse
import os

import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame, concat, read_csv
from tqdm import tqdm


class PlotCo2xPer(object):
    """
    docstring
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Run bus replacement approach."
        )

        self.parser.add_argument(
            "--inputFolder",
            type=str,
            default='./eletric_bus/outputs/',
            help="Folder with approach output files",
        )
        self.parser.add_argument(
            "--outputFolder",
            type=str,
            default='./eletric_bus/results/',
            help="File with approach name, CO2 total and percentage",
        )

        self.args = self.parser.parse_args()
        self.inputFolder = self.args.inputFolder
        self.outputFolder = self.args.outputFolder

    def compute_total_co2_in_folder(self, folder_path: str) -> float:
        all_files = os.listdir(folder_path)
        emission_files = [f for f in all_files if f.endswith("emission.csv")]
        emission_df = [
            read_csv(os.path.join(folder_path, f), sep=";") for f in emission_files
        ]
        df = concat(emission_df)
        return df["vehicle_CO2"].sum()

    def run(self):
        self.inputFolder = self.inputFolder
        approach_co2_per = DataFrame(columns=["approach", "co2", "per"])
        default_total_co2 = self.compute_total_co2_in_folder(
            f"{self.inputFolder}/default/"
        )
        for approach_file in os.listdir(self.inputFolder):
            if approach_file == "default":
                continue
            per_files = [
                f
                for f in os.listdir(f"{self.inputFolder}/{approach_file}")
                if not f.endswith(".csv")
            ]
            for per_file in tqdm(per_files, desc=approach_file):
                total_co2 = self.compute_total_co2_in_folder(
                    f"{self.inputFolder}/{approach_file}/{per_file}"
                )
                approach_co2_per = approach_co2_per.append(
                    {
                        "approach": approach_file,
                        "co2": total_co2,
                        "per": int(per_file[:-3]),
                    },
                    ignore_index=True,
                )
            approach_co2_per = approach_co2_per.append(
                {"approach": approach_file, "co2": default_total_co2, "per": 0},
                ignore_index=True,
            )
            approach_co2_per = approach_co2_per.append(
                {"approach": approach_file, "co2": 0, "per": 100}, ignore_index=True
            )
        approach_co2_per.to_csv(
            f"{self.outputFolder}/approach_co2_per.csv", index=False
        )
        sns.lineplot(data=approach_co2_per, x="per", y="co2", hue="approach")
        plt.savefig(f"{self.outputFolder}/approach_co2_per.png")

if __name__ == "__main__":
    plot_co2_x_per = PlotCo2xPer()
    plot_co2_x_per.run()