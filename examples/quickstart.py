"""Load the AlgoraeOS curated dataset, attach drug and cell line names, and print a short summary.

Requires: pandas  (pip install pandas)
Run:      python examples/quickstart.py            # reads from GitHub
          python examples/quickstart.py --local    # reads ./data when run from a clone
"""
import sys

import pandas as pd

REMOTE = "https://raw.githubusercontent.com/VafaeeLab/AlgoraeOS/main/data/"
base = "data/" if "--local" in sys.argv else REMOTE

data = pd.read_csv(base + "AlgoraeOS_DrugComb_curated_synergy.csv")
drugs = pd.read_csv(base + "drugs.csv").set_index("drugcomb_drug_id")
cells = pd.read_csv(base + "cell_lines.csv").set_index("drugcomb_cell_line_id")

data["drug_1"] = data["drug_row_id"].map(drugs["drug_name"])
data["drug_2"] = data["drug_col_id"].map(drugs["drug_name"])
data["cell_line"] = data["cell_line_id"].map(cells["cell_line_name"])
data["tissue"] = data["cell_line_id"].map(cells["tissue"])

metrics = ["synergy_loewe", "synergy_bliss", "synergy_hsa", "synergy_zip"]

print(f"{len(data):,} combinations | "
      f"{pd.concat([data.drug_row_id, data.drug_col_id]).nunique():,} drugs | "
      f"{data.cell_line_id.nunique()} cell lines\n")

print("Synergy score summary:")
print(data[metrics].describe().round(2).to_string(), "\n")

print("Combinations per tissue:")
print(data["tissue"].value_counts().to_string(), "\n")

# Combinations that look synergistic under all four metrics (score > 10 for each)
strong = data[(data[metrics] > 10).all(axis=1)]
print(f"{len(strong):,} combinations score > 10 on all four metrics. Top 10 by Bliss:")
cols = ["drug_1", "drug_2", "cell_line"] + metrics
print(strong.sort_values("synergy_bliss", ascending=False)[cols].head(10).to_string(index=False))
