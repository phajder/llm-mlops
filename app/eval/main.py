import os
import logging
import time

def main():
    log_path = os.environ.get("LOG_PATH", "/var/log")
    checkpoints_path = os.environ.get("CHECKPOINTS_PATH", "./checkpoints")
    models_path = os.environ.get("MODELS_PATH", "./models")

    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler(os.path.join(log_path, "eval.log")),
            logging.StreamHandler()
        ]
    )

    logging.info("Importing new checkpoints...")
    with open(os.path.join(checkpoints_path, "weights.txt"), 'r') as f:
        logging.info(f.read())
    logging.info("Weights loaded!")
    logging.info("Starting evaluation process...")
    accuracy = 0.8
    for i in range(10):
        logging.info(f"Record {i} processed. Current accuracy: {round(accuracy, 2)}")
        accuracy = accuracy + 0.01
        time.sleep(1)
    logging.info("Evaluation completed. Exporting new model...")
    model_timestamp = time.time()
    model_filename = f"model-{int(model_timestamp)}.txt"
    with open(os.path.join(models_path, model_filename), "w") as f:
        f.write(f"New model exported, timestamp: {model_timestamp}")

    # Argo output
    with open(os.path.join("/tmp", "output.txt"), "w") as f:
        f.write(model_filename)


if __name__ == "__main__":
    main()
