# Data dictionary

All files are UTF-8 CSV with a header row. IDs are DrugComb identifiers; join them to the lookup tables to get names.

## `AlgoraeOS_DrugComb_curated_synergy.csv`

359,556 rows, one per unique (drug 1, drug 2, cell line) combination. Each combination appears in one drug order only.

| Column | Type | Description |
|---|---|---|
| `block_id` | integer | DrugComb experiment (concentration-grid block) ID |
| `drug_row_id` | integer | DrugComb ID of drug 1 → `drugs.csv` |
| `drug_row_pubchem_cid_single` | integer | PubChem CID of drug 1 |
| `drug_col_id` | integer | DrugComb ID of drug 2 → `drugs.csv` |
| `drug_col_pubchem_cid_single` | integer | PubChem CID of drug 2 |
| `cell_line_id` | integer | DrugComb cell line ID → `cell_lines.csv` |
| `conc_r_unit`, `conc_c_unit` | text | Concentration units for drug 1 and drug 2 (`uM` = micromolar) |
| `synergy_zip` | float | ZIP (zero interaction potency) synergy score, within [−100, 100] |
| `synergy_loewe` | float | Loewe additivity synergy score, within [−100, 100] |
| `synergy_hsa` | float | HSA (highest single agent) synergy score, within [−100, 100] |
| `synergy_bliss` | float | Bliss independence synergy score, within [−100, 100] |
| `ic50_row`, `ic50_col` | float | IC50 of drug 1 and drug 2 alone |
| `ri_row`, `ri_col` | float | Relative inhibition of drug 1 and drug 2 alone |
| `css_row`, `css_col` | float | Combination sensitivity score from drug 1's and drug 2's perspective |
| `css_ri` | float | Combination sensitivity score (relative-inhibition based) |
| `S_sum`, `S_mean`, `S_max` | float | Synergy–antagonism (S) scores |
| `quality` | — | DrugComb quality flag; empty for every row, because flagged records were removed |

Synergy scores are SynergyFinder values as harmonised by DrugComb: positive means synergistic and negative means
antagonistic. A score above 10 is a common rule of thumb for likely synergy.

## `drugs.csv`

3,129 rows, one per drug that appears in the dataset.

| Column | Description |
|---|---|
| `drugcomb_drug_id` | DrugComb drug ID (matches `drug_row_id` / `drug_col_id`) |
| `pubchem_cid` | PubChem compound ID |
| `drug_name` | Drug name as listed by DrugComb (some compounds are named by a CAS number or vendor code) |
| `chembl_id`, `drugbank_id` | ChEMBL and DrugBank identifiers, where available |
| `inchikey`, `smiles` | Chemical structure identifiers |

## `cell_lines.csv`

170 rows, one per cancer cell line that appears in the dataset.

| Column | Description |
|---|---|
| `drugcomb_cell_line_id` | DrugComb cell line ID (matches `cell_line_id`) |
| `cell_line_name` | Cell line name |
| `tissue` | Tissue of origin (DrugComb / CCLE naming) |
| `cellosaurus_accession` | Cellosaurus accession (e.g. `CVCL_0023`) |
| `depmap_id` | DepMap model ID (e.g. `ACH-000681`) |
| `ccle_name` | CCLE name |

## Notes

- Source: [DrugComb](https://drugcomb.fimm.fi) v1.5. See the main [README](../README.md#how-the-dataset-was-built) for
  how the data were curated.
- 936 rows originally carried a garbled unit label (`ÂµM`, a text-encoding artefact for µM). These were normalised to
  `uM`; no values changed.
