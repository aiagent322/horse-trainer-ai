"""
Configuration module for Horse Trainer AI
"""
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config(config_path):
    """
    Load configuration from a JSON file and override with environment variables.
    
    Args:
        config_path (str): Path to the configuration JSON file.
        
    Returns:
        dict: Configuration dictionary.
    """
    # Default configuration
    default_config = {
        'model': {
            'type': 'random_forest',
            'params': {
                'n_estimators': 100,
                'max_depth': 10,
                'random_state': 42
            }
        },
        'training': {
            'test_size': 0.2,
            'validation_method': 'cross_val',
            'n_splits': 5
        },
        'features': {
            'include_weather': True,
            'include_diet': True,
            'include_medical': True,
            'include_lineage': True
        },
        'recommendations': {
            'max_per_horse': 5,
            'min_confidence': 0.7
        },
        'api': {
            'host': '0.0.0.0',
            'port': 8000,
            'debug': False
        }
    }
    
    # Load configuration from file
    try:
        with open(config_path, 'r') as f:
            file_config = json.load(f)
            default_config.update(file_config)
    except FileNotFoundError:
        print(f"Config file {config_path} not found, using default configuration")
    except json.JSONDecodeError:
        print(f"Error parsing config file {config_path}, using default configuration")
    
    # Override with environment variables
    # Example: HORSE_TRAINER_MODEL_TYPE overrides config['model']['type']
    for key1 in default_config.keys():
        if isinstance(default_config[key1], dict):
            for key2 in default_config[key1].keys():
                env_var = f"HORSE_TRAINER_{key1.upper()}_{key2.upper()}"
                if env_var in os.environ:
                    # Convert environment variable to appropriate type
                    original_value = default_config[key1][key2]
                    if isinstance(original_value, bool):
                        default_config[key1][key2] = os.environ[env_var].lower() in ('true', 'yes', '1')
                    elif isinstance(original_value, int):
                        default_config[key1][key2] = int(os.environ[env_var])
                    elif isinstance(original_value, float):
                        default_config[key1][key2] = float(os.environ[env_var])
                    else:
                        default_config[key1][key2] = os.environ[env_var]
    
    return default_config

