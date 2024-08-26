import os
import logging
from random import random
import time

def main():
    log_path = os.environ.get("LOG_PATH", "/var/log")
    models_path = os.environ.get("MODELS_PATH", "./models")
    model_filename = os.environ.get("MODEL_FILENAME")

    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler(os.path.join(log_path, "load.log")),
            logging.StreamHandler()
        ]
    )

    if model_filename is None:
        logging.error("Model filename not specified. Exiting with error...")
        exit(-1)

    logging.info(f"Loading new model named {model_filename}...")
    with open(os.path.join(models_path, model_filename), 'r') as f:
        logging.info(f.read())
    logging.info(f"Model {model_filename} loaded!")


if __name__ == "__main__":
    main()
