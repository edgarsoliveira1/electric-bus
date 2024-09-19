import argparse

from pandas import DataFrame, isnull


class ApproachScore(DataFrame):
    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):
        super().__init__(data, index, columns, dtype, copy)

        # Verifica se as colunas obrigatórias estão presentes
        if not all(col in self.columns for col in ["flow_id", "score"]):
            raise ValueError("O DataFrame deve ter as colunas 'flow_id' e 'score'.")

    @property
    def flow_id(self):
        return self["flow_id"]

    @property
    def score(self):
        return self["score"]


class Approach(object):
    """
        É uma interface abstrata para os métodos de abordagem para gerar pontuações para cada fluxo de onibus em um conjunto de simulações de tráfego, geradas com o SUMO. Onde, as abordagens ambicionam encontrar os fluxos de ônibus que mais impactam na emissão de poluentes.
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Run bus replacement approach."
        )

        self.parser.add_argument(
            "--simFolderInput",
            type=str,
            help="Folder with the base simulation/emission files",
        )
        self.parser.add_argument(
            "--flowInput", type=str, help="File with the base flow"
        )
        self.parser.add_argument(
            "--scoreOutput",
            type=str,
            help="File with the score, 'flow_id' and 'score' columns",
        )
        self.parser.add_argument(
            "--outputFolder",
            type=str,
            help="folder to save the output files",
        )

        self.args = self.parser.parse_args()
        self.simFolderInput = self.args.simFolderInput
        self.flowInput = self.args.flowInput
        self.scoreOutput = self.args.scoreOutput
        self.outputFolder = self.args.outputFolder

    def run(self):
        pass

    def approach(
        self, emissions_df: DataFrame, base_flow_df: DataFrame
    ) -> ApproachScore:
        pass

    def vehicle_route2flow_id(self, vehicle_route:str, flow_id:str) -> str:
        if isnull(vehicle_route):
            return None
        for id in flow_id:
            if id in vehicle_route:
                return id
        raise ValueError("No route found for vehicle_route: {}".format(vehicle_route))
