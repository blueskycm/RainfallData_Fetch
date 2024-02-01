import logging

def setup_logging():
    logging.basicConfig(filename='rainfall_alerts.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
