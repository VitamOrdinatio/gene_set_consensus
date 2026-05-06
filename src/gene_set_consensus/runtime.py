from pathlib import Path
from datetime import datetime

def generate_run_id():
    return datetime.now().strftime("run_%Y_%m_%d_%H%M%S")

def initialize_run_directories(project_config, run_id):

    paths = project_config["paths"]

    logs_dir = Path(paths["logs_dir"]) / run_id
    interim_dir = Path(paths["interim_dir"]) / run_id
    processed_dir = Path(paths["processed_dir"]) / run_id

    for path in [logs_dir, interim_dir, processed_dir]:
        path.mkdir(parents=True, exist_ok=True)

    return {
        "logs_dir": logs_dir,
        "interim_dir": interim_dir,
        "processed_dir": processed_dir,
    }
