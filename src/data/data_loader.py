"""
Data Loader for Horse Trainer AI

This module handles loading and processing data for the Horse Trainer AI application.
"""
import json
import logging
import os
from datetime import date
from typing import Dict, List, Optional

import pandas as pd

from src.models.horse_profile import HorseProfile

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Data Loader class for loading and processing horse training data.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Directory containing the data files
        """
        self.data_dir = data_dir
        self._ensure_data_dir()
    
    def _ensure_data_dir(self) -> None:
        """Create the data directory if it doesn't exist."""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_horse_profiles(self, filename: str = "horse_profiles.json") -> List[HorseProfile]:
        """
        Load horse profiles from a JSON file.
        
        Args:
            filename: Name of the JSON file containing horse profiles
            
        Returns:
            List of HorseProfile objects
        """
        file_path = os.path.join(self.data_dir, filename)
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Convert dictionaries to HorseProfile objects
            profiles = [HorseProfile.from_dict(profile_data) for profile_data in data]
            logger.info(f"Loaded {len(profiles)} horse profiles from {file_path}")
            return profiles
            
        except FileNotFoundError:
            logger.warning(f"Horse profiles file not found: {file_path}")
            return []
        except json.JSONDecodeError:
            logger.error(f"Error parsing horse profiles file: {file_path}")
            return []
    
    def load_training_data(self, filename: str = "training_data.json") -> List[Dict]:
        """
        Load training data from a JSON file.
        
        Args:
            filename: Name of the JSON file containing training data
            
        Returns:
            List of training data records
        """
        file_path = os.path.join(self.data_dir, filename)
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            logger.info(f"Loaded {len(data)} training records from {file_path}")
            return data
            
        except FileNotFoundError:
            logger.warning(f"Training data file not found: {file_path}")
            return []
        except json.JSONDecodeError:
            logger.error(f"Error parsing training data file: {file_path}")
            return []
    
    def load_training_data_csv(self, filename: str = "training_data.csv") -> List[Dict]:
        """
        Load training data from a CSV file.
        
        Args:
            filename: Name of the CSV file containing training data
            
        Returns:
            List of training data records
        """
        file_path = os.path.join(self.data_dir, filename)
        
        try:
            df = pd.read_csv(file_path)
            
            # Convert DataFrame to list of dictionaries
            data = df.to_dict(orient='records')
            
            logger.info(f"Loaded {len(data)} training records from {file_path}")
            return data
            
        except FileNotFoundError:
            logger.warning(f"Training data CSV file not found: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading training data CSV file: {file_path} - {str(e)}")
            return []
    
    def save_horse_profiles(self, profiles: List[HorseProfile], filename: str = "horse_profiles.json") -> None:
        """
        Save horse profiles to a JSON file.
        
        Args:
            profiles: List of HorseProfile objects
            filename: Name of the JSON file to save
        """
        file_path = os.path.join(self.data_dir, filename)
        
        # Convert HorseProfile objects to dictionaries
        data = [profile.to_dict() for profile in profiles]
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved {len(profiles)} horse profiles to {file_path}")
    
    def create_sample_data(self) -> None:
        """
        Create sample data files for testing.
        This method generates sample horse profiles and training data.
        """
        # Create sample horse profiles
        from src.models.horse_profile import HorseProfile, TrainingSession, MedicalRecord
        
        horse_profiles = [
            HorseProfile(
                id="H001",
                name="Thunder",
                breed="Thoroughbred",
                birth_date=date(2015, 5, 12),
                sex="male",
                color="bay",
                height_hands=16.2,
                weight_kg=550,
                lineage={
                    "sire": "Storm Runner",
                    "dam": "Lightning Dash"
                },
                dietary_restrictions=[]
            ),
            HorseProfile(
                id="H002",
                name="Misty",
                breed="Arabian",
                birth_date=date(2016, 3, 23),
                sex="female",
                color="gray",
                height_hands=15.1,
                weight_kg=450,
                lineage={
                    "sire": "Desert Prince",
                    "dam": "Moonlight Dancer"
                },
                dietary_restrictions=["high sugar"]
            ),
            HorseProfile(
                id="H003",
                name="Duke",
                breed="Quarter Horse",
                birth_date=date(2014, 8, 15),
                sex="gelding",
                color="chestnut",
                height_hands=15.3,
                weight_kg=500,
                lineage={
                    "sire": "King's Ransom",
                    "dam": "Duchess of York"
                },
                dietary_restrictions=[]
            )
        ]
        
        # Add sample training history
        
        # Add training sessions for Thunder
        thunder_sessions = [
            TrainingSession(
                date=date(2023, 1, 15),
                activity_type="trot",
                duration_minutes=30,
                intensity="medium",
                performance_rating=7,
                notes="Good energy, responsive to commands"
            ),
            TrainingSession(
                date=date(2023, 1, 20),
                activity_type="canter",
                duration_minutes=25,
                intensity="medium",
                performance_rating=6,
                notes="Some resistance at transitions"
            ),
            TrainingSession(
                date=date(2023, 1, 25),
                activity_type="gallop",
                duration_minutes=15,
                intensity="high",
                performance_rating=8,
                notes="Excellent speed and control"
            )
        ]
        
        horse_profiles[0].training_history.extend(thunder_sessions)
        
        # Sample training data
        training_data = [
            {
                "horse_id": "H001",
                "activity_type": "trot",
                "date": "2023-01-15",
                "duration_minutes": 30,
                "intensity": "medium",
                "success_rating": 7,
                "improvement_score": 0.3,
                "notes": "Good energy, responsive to commands"
            },
            {
                "horse_id": "H001",
                "activity_type": "canter",
                "date": "2023-01-20",
                "duration_minutes": 25,
                "intensity": "medium",
                "success_rating": 6,
                "improvement_score": 0.2,
                "notes": "Some resistance at transitions"
            },
            {
                "horse_id": "H001",
                "activity_type": "gallop",
                "date": "2023-01-25",
                "duration_minutes": 15,
                "intensity": "high",
                "success_rating": 8,
                "improvement_score": 0.5,
                "notes": "Excellent speed and control"
            },
            {
                "horse_id": "H002",
                "activity_type": "trot",
                "date": "2023-01-16",
                "duration_minutes": 35,
                "intensity": "low",
                "success_rating": 6,
                "improvement_score": 0.2,
                "notes": "Somewhat distracted"
            },
            {
                "horse_id": "H002",
                "activity_type": "dressage",
                "date": "2023-01-22",
                "duration_minutes": 40,
                "intensity": "medium",
                "success_rating": 8,
                "improvement_score": 0.4,
                "notes": "Excellent precision in movements"
            },
            {
                "horse_id": "H003",
                "activity_type": "jump",
                "date": "2023-01-18",
                "duration_minutes": 25,
                "intensity": "high",
                "success_rating": 7,
                "improvement_score": 0.3,
                "notes": "Good height clearance, needs work on approach"
            }
        ]
        
        # Save the sample data
        self.save_horse_profiles(horse_profiles)
        
        # Save training data
        training_data_path = os.path.join(self.data_dir, "training_data.json")
        with open(training_data_path, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        logger.info(f"Created sample data in {self.data_dir}")
