import json
import os
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("log/application.log"),  # Log to a file
            logging.StreamHandler()  # Display logs in the console
        ]
    )

logger = logging.getLogger(__name__)

def load_user_agents(file_path="config/user_agents.json"):
    """
    Load a list of User Agents from a JSON file.
    """
    setup_logging()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            user_agents = json.load(f)
            if not user_agents:
                raise ValueError("The user_agents.json file is empty.")
            logger.info("User agents loaded successfully.")
            return user_agents
    except FileNotFoundError:
        logger.error(f"Error: The file '{file_path}' was not found.")
        raise
    except json.JSONDecodeError:
        logger.error("Error: Invalid JSON format in the user_agents.json file.")
        raise


