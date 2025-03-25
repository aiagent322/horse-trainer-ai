# tests/test_agent.py
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 
'..')))

from src.main import main
from src.models.horse_profile import HorseProfile
from src.models.training_model import TrainingModel
from src.data.data_loader import DataLoader
from src.data.preprocessor import Preprocessor
from src.utils.logger import Logger


class TestHorseProfile(unittest.TestCase):
    """Test the HorseProfile class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.horse = HorseProfile(
            name="Thunder",
            age=5,
            breed="Thoroughbred",
            training_history=[{"date": "2023-01-01", "exercise": "gallop", 
"duration": 30}]
        )
    
    def test_profile_creation(self):
        """Test that a horse profile can be created correctly"""
        self.assertEqual(self.horse.name, "Thunder")
        self.assertEqual(self.horse.age, 5)
        self.assertEqual(self.horse.breed, "Thoroughbred")
        self.assertEqual(len(self.horse.training_history), 1)
    
    def test_add_training_session(self):
        """Test adding a new training session to the horse profile"""
        self.horse.add_training_session("2023-01-02", "trot", 45)
        self.assertEqual(len(self.horse.training_history), 2)
        self.assertEqual(self.horse.training_history[-1]["exercise"], 
"trot")


class TestTrainingModel(unittest.TestCase):
    """Test the TrainingModel class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.model = TrainingModel()
        self.horse = HorseProfile(
            name="Storm",
            age=4,
            breed="Arabian",
            training_history=[]
        )
    
    @patch('src.models.training_model.TrainingModel.predict')
    def test_recommend_training(self, mock_predict):
        """Test that the model can recommend training"""
        mock_predict.return_value = {"exercise": "canter", "duration": 25, 
"intensity": "medium"}
        
        recommendation = self.model.recommend_training(self.horse)
        
        self.assertIn("exercise", recommendation)
        self.assertIn("duration", recommendation)
        self.assertIn("intensity", recommendation)
        self.assertEqual(recommendation["exercise"], "canter")


class TestDataLoader(unittest.TestCase):
    """Test the DataLoader class"""
    
    @patch('src.data.data_loader.pd.read_csv')
    def test_load_horse_data(self, mock_read_csv):
        """Test loading horse data from CSV"""
        mock_df = MagicMock()
        mock_read_csv.return_value = mock_df
        
        loader = DataLoader()
        result = loader.load_horse_data("test_path.csv")
        
        mock_read_csv.assert_called_once_with("test_path.csv")
        self.assertEqual(result, mock_df)


class TestPreprocessor(unittest.TestCase):
    """Test the Preprocessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.preprocessor = Preprocessor()
    
    @patch('src.data.preprocessor.pd.DataFrame')
    def test_preprocess_training_data(self, mock_df):
        """Test preprocessing training data"""
        mock_df.fillna.return_value = mock_df
        mock_df.drop_duplicates.return_value = mock_df
        
        result = self.preprocessor.preprocess_training_data(mock_df)
        
        self.assertEqual(result, mock_df)
        mock_df.fillna.assert_called_once()
        mock_df.drop_duplicates.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integration tests for the Horse Trainer AI"""
    
    @patch('src.data.data_loader.DataLoader.load_horse_data')
    @patch('src.models.training_model.TrainingModel.recommend_training')
    def test_end_to_end_workflow(self, mock_recommend, mock_load_data):
        """Test the end-to-end workflow of the application"""
        # Mock the data loading
        mock_df = MagicMock()
        mock_load_data.return_value = mock_df
        
        # Mock the recommendation
        mock_recommend.return_value = {
            "exercise": "gallop", 
            "duration": 30, 
            "intensity": "high"
        }
        
        # Run the main function (you might need to adapt this to your 
actual implementation)
        with patch('sys.argv', ['main.py', '--test']):
            result = main()
        
        # Assert that the workflow completed successfully
        self.assertTrue(result)
        mock_load_data.assert_called_once()
        mock_recommend.assert_called()


# This allows the tests to be run from the command line
if __name__ == '__main__':
    unittest.main()
