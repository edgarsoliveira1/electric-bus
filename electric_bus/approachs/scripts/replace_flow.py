import xml.etree.ElementTree as ET
from os import makedirs
import pandas as pd
import argparse


class ReplaceFlow(object):
    """
        É um script que recebe um arquivo (xml) com os fluxos de ônibus e um arquivo (csv) com os scores de cada fluxo de ônibus, e substitui os fluxos de ônibus com os maiores scores por ônibus elétricos.
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Replace gas bus by eletric ones in a flow (xml) file."
        )
        self.parser.add_argument(
            "--scoreInput",
            type=str,
            help="File (csv) with the 'flow_id' and 'score' columns",
        )
        self.parser.add_argument(
            "--flowInput",
            type=str,
            help="File (xml) with the base flow, flow_ids to be replaced by electric buses",
        )
        self.parser.add_argument(
            "--flowOutput",
            type=str,
            help="File (xml) with the result flow, flow_ids replaced by electric buses",
        )
        self.parser.add_argument(
            "--outputFolder",
            type=str,
            help="folder to save the output files",
        )
        self.parser.add_argument(
            "--per",
            type=float,
            default=0.25,
            help="Percentage of flow_ids to be replaced by electric buses",
        )

        self.args = self.parser.parse_args()
        self.scoreInput = self.args.scoreInput
        self.flowInput = self.args.flowInput
        self.flowOutput = self.args.flowOutput
        self.outputFolder = self.args.outputFolder
        self.per = self.args.per
        self.score_df = pd.read_csv(self.scoreInput, sep=";").sort_values(
            by="score", ascending=False
        )

    def run(self):
        score_len = len(self.score_df)
        replace_ids = self.score_df.head(int(score_len * self.per))["flow_id"].tolist()
        # Read the scores file
        tree = ET.parse(self.flowInput)
        root = tree.getroot()
        # Modify the XML file
        for flow in root.iter("flow"):
            if flow.get("id") in replace_ids:
                flow.attrib["type"] = "ElectricBus"

        makedirs(self.outputFolder, exist_ok=True)
        tree.write(self.flowOutput)


if __name__ == "__main__":
    replacer = ReplaceFlow()
    replacer.run()