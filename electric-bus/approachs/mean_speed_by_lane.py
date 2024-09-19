from scripts.approach import Approach, ApproachScore
from os import listdir, makedirs, path
import pandas as pd
from typing import List
from tqdm import tqdm


class MeanSpeedByLane(Approach):
    """
    A approach que calcula o score com base na velocidade média dos veículos em cada via.
    """

    def __init__(self) -> None:
        super().__init__()

    def get_emission_files(self, dir: str) -> List[str]:
        """Filtra os arquivos em um diretório que terminam com '.emission.csv'.

        Args:
            diretorio (str): O caminho para o diretório a ser pesquisado.

        Returns:
            Uma lista com os nomes dos arquivos filtrados.
        """

        def filter_emssion_files(f):
            return str(f).endswith(".emission.csv")

        return list(filter(filter_emssion_files, listdir(dir)))

    def run(self):
        print(f"Running traffic approach with {self.simFolderInput}")
        if path.isfile(self.scoreOutput):
            print(f"Score file already exists in {self.scoreOutput}")
            return
        self.emission_files = self.get_emission_files(self.simFolderInput)
        self.emission_dfs = [
            pd.read_csv(f"{self.simFolderInput}/{file}", sep=";")
            for file in self.emission_files
        ]
        self.flow_input_df = pd.read_csv(self.flowInput, sep=";")
        # Check is the cache file exists
        try:
            self.score_df = pd.read_csv(self.scoreOutput, sep=";")
        except Exception:
            # If not, run the approach and save the result
            self.score_df = self.approach(self.emission_dfs, self.flow_input_df)
            self.score_df = self.score_df.sort_values("score", ascending=False)
            makedirs(self.outputFolder, exist_ok=True)
            self.score_df.to_csv(self.scoreOutput, sep=";", index=False)

    def approach(
        self, emissions_dfs: List[pd.DataFrame], flow_input_df: pd.DataFrame
    ) -> ApproachScore:
        score_df = None
        for e_df in tqdm(emissions_dfs, desc="Running approach on emissions"):
            if score_df is None:
                score_df = self._approach(e_df, flow_input_df)
                continue
            score_df["score"] += self._approach(e_df, flow_input_df)["score"]
        score_df["score"] /= len(emissions_dfs)
        return score_df

    def _approach(
        self, emissions_df: pd.DataFrame, base_flow_df: pd.DataFrame
    ) -> ApproachScore:
        flow_ids = base_flow_df["flow_id"].dropna().unique()
        emissions_df["flow_id"] = emissions_df["vehicle_route"].apply(
            lambda x: self.vehicle_route2flow_id(x, flow_ids)
        )
        # Compute the traffic score
        emissions_df["speed_mean"] = emissions_df.groupby(
            ["timestep_time", "vehicle_lane"]
        )["vehicle_speed"].transform("mean")
        # for t in tqdm(emissions_df["timestep_time"].unique(), desc="Runing approach on timesteps_time"):
        #     t_df = emissions_df[emissions_df["timestep_time"] == t]
        #     for lane in t_df["vehicle_lane"].unique():
        #         t_l_df = t_df[t_df["vehicle_lane"] == lane]
        #         speed_mean = t_l_df["vehicle_speed"].mean()
        #         emissions_df.loc[t_l_df.index, "speed_mean"] = speed_mean
        final_score = emissions_df.groupby("flow_id").apply(
            lambda x: x["speed_mean"].mean() * -1
        )
        return final_score.rename("score").reset_index()


if __name__ == "__main__":
    mean_speed_by_lane = MeanSpeedByLane()
    mean_speed_by_lane.run()
