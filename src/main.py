#!/usr/bin/env python
"""
Horse Trainer AI - Main Application

This is the entry point for the Horse Trainer AI application.
"""
import argparse
import logging
import os
import sys

from src.config import load_config
from src.data.data_loader import DataLoader
from src.models.training_model import TrainingModel
from src.utils.logger import setup_logger

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Horse Trainer AI')
    parser.add_argument('--config', type=str, default='config/default.json',
                        help='Path to configuration file')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')
    parser.add_argument('--data-dir', type=str, default='data',
                        help='Directory containing training data')
    return parser.parse_args()

def main():
    """Main function to run the Horse Trainer AI."""
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logger(level=args.log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Horse Trainer AI")
    
    try:
        # Load configuration
        config = load_config(args.config)
        logger.info(f"Loaded configuration from {args.config}")
        
        # Load data
        data_loader = DataLoader(data_dir=args.data_dir)
        training_data = data_loader.load_training_data()
        horse_profiles = data_loader.load_horse_profiles()
        
        logger.info(f"Loaded {len(training_data)} training records")
        logger.info(f"Loaded {len(horse_profiles)} horse profiles")
        
        # Initialize model
        model = TrainingModel(config=config)
        
        # Train model if needed
        if config.get('train_model', True):
            logger.info("Training model...")
            model.train(training_data, horse_profiles)
            logger.info("Model training complete")
        
        # Run predictions or recommendations
        if config.get('generate_recommendations', True):
            recommendations = model.generate_recommendations(horse_profiles)
            logger.info(f"Generated {len(recommendations)} training recommendations")
            
            # Save recommendations
            output_dir = config.get('output_dir', 'output')
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, 'recommendations.json')
            model.save_recommendations(recommendations, output_file)
            logger.info(f"Saved recommendations to {output_file}")
        
        logger.info("Horse Trainer AI completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
