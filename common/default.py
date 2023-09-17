"""main path for output files"""
from pathlib import Path

# Default path
DEFAULT_PATH: Path = Path(__file__).resolve().parent


##############################################################################################
# TP1                                                                                        #
##############################################################################################
TP1_PATH: Path = DEFAULT_PATH / "../TP1/"
TP1_DATASET_PATH: Path = TP1_PATH / "datasets"

# dataset
TP1_PROBES_PATH: Path = TP1_DATASET_PATH / "probes.json"
TP1_ANCHORS_PATH: Path = TP1_DATASET_PATH / "anchors.json"

# results
TP1_RESULTS_PATH: Path = TP1_PATH / "results"
