from pathlib import Path
import logging

def setup_run_dirs(project_config, run_id):

    paths = project_config["paths"]

    logs_dir = Path(paths["logs_dir"]) / run_id
    interim_dir = Path(paths["interim_dir"]) / run_id
    processed_dir = Path(paths["processed_dir"]) / run_id
    results_dir = Path(paths["results_dir"])

    for path in [logs_dir, interim_dir, processed_dir, results_dir]:
        path.mkdir(parents=True, exist_ok=True)

    return {
        "logs_dir": logs_dir,
        "interim_dir": interim_dir,
        "processed_dir": processed_dir,
        "results_dir": results_dir
    }

def get_logger(name, log_path):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_path,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
