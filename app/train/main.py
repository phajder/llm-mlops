import os
import logging
from random import random
import time

def main():
    log_path = os.environ.get("LOG_PATH", "/var/log")
    dataset_path = os.environ.get("DATASET_PATH", "./")
    checkpoints_path = os.environ.get("CHECKPOINTS_PATH", "./checkpoints")
    threshold = float(os.environ.get("TRAIN_THRESHOLD", 0.9))

    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler(os.path.join(log_path, "train.log")),
            logging.StreamHandler()
        ]
    )

    logging.info("Reading training dataset...")
    with open(os.path.join(dataset_path, "dataset.txt"), 'r') as f:
        logging.info(f.read())
    logging.info("End of the dataset!")
    
    logging.info("Starting training process...")
    for i in range(10):
        logging.info(f"Epoch {i} data.")
        time.sleep(1)
    if random() > threshold:
        logging.error("Oh no! training unsuccessful! Exiting with error...")
        exit(-1)
    logging.info("Training completed. Exporting last checkpoint...")
    with open(os.path.join(checkpoints_path, "weights.txt"), "w") as f:
        f.write(f"Checkpoint with new weights generated, timestamp: {time.time()}")


if __name__ == "__main__":
    main()
