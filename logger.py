import logging

def setup_logging():
    logging.basicConfig(filename='rainfall_alerts.log', 
                        filemode='a', 
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S',  # Specify date and time format up to seconds
                        level=logging.INFO)
