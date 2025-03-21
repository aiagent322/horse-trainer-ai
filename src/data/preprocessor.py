"""
Data Preprocessor for Horse Trainer AI

This module contains utilities for preprocessing and transforming data
for the Horse Trainer AI application.
"""
import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

from src.models.horse_profile import HorseProfile

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """
    Data preprocessing class for the Horse Trainer AI application.
    
    This class provides methods for cleaning, transforming, and preparing
    data for model training and prediction.
    """
    
    def __init__(self):
        """Initialize the data preprocessor."""
        self.numerical_scaler = StandardScaler()
        self.categorical_encoder = OneHotEncoder(handle_unknown='ignore')
        self.imputer = SimpleImputer(strategy='mean')
        self.fitted = False
    
    def preprocess_horse_data(self, 
                             horse_profiles: List[HorseProfile], 
                             fit: bool = False) -> pd.DataFrame:
        """
        Preprocess horse profile data for modeling.
        
        Args:
            horse_profiles: List of HorseProfile objects
            fit: Whether to fit the preprocessors on this data
            
        Returns:
            Preprocessed DataFrame
        """
        # Extract features
        features = []
        
        for horse in horse_profiles:
            # Basic features
            horse_features = {
                'horse_id': horse.id,
                'age': horse.age,
                'height_hands': horse.height_hands,
                'weight_kg': horse.weight_kg,
                'breed': horse.breed,
                'sex': horse.sex,
                'color': horse.color,
                'has_medical_conditions': int(horse.has_medical_conditions),
                'has_dietary_restrictions': int(len(horse.dietary_restrictions) > 0),
                'has_lineage_info': int(len(horse.lineage) > 0)
            }
            
            # Training statistics
            if horse.training_history:
                # Average performance by activity type
                perf_by_activity = {}
                for session in horse.training_history:
                    activity = session.activity_type
                    if activity not in perf_by_activity:
                        perf_by_activity[activity] = []
                    perf_by_activity[activity].append(session.performance_rating)
                
                # Add average performance for common activities
                for activity in ['trot', 'canter', 'gallop', 'jump', 'dressage', 'trail', 'groundwork']:
                    if activity in perf_by_activity:
                        horse_features[f'avg_perf_{activity}'] = np.mean(perf_by_activity[activity])
                    else:
                        horse_features[f'avg_perf_{activity}'] = np.nan
                
                # Intensity preferences
                intensity_counts = {'low': 0, 'medium': 0, 'high': 0}
                for session in horse.training_history:
                    intensity_counts[session.intensity] += 1
                total = sum(intensity_counts.values())
                if total > 0:
                    horse_features['pct_low_intensity'] = intensity_counts['low'] / total * 100
                    horse_features['pct_medium_intensity'] = intensity_counts['medium'] / total * 100
                    horse_features['pct_high_intensity'] = intensity_counts['high'] / total * 100
                else:
                    horse_features['pct_low_intensity'] = np.nan
                    horse_features['pct_medium_intensity'] = np.nan
                    horse_features['pct_high_intensity'] = np.nan
            else:
                # Set default values if no training history
                for activity in ['trot', 'canter', 'gallop', 'jump', 'dressage', 'trail', 'groundwork']:
                    horse_features[f'avg_perf_{activity}'] = np.nan
                
                horse_features['pct_low_intensity'] = np.nan
                horse_features['pct_medium_intensity'] = np.nan
                horse_features['pct_high_intensity'] = np.nan
            
            features.append(horse_features)
        
        # Convert to DataFrame
        df = pd.DataFrame(features)
        
        # Handle missing values and preprocessing
        return self._preprocess_dataframe(df, fit)
    
    def preprocess_training_data(self, 
                                training_data: List[Dict], 
                                fit: bool = False) -> pd.DataFrame:
        """
        Preprocess training data for modeling.
        
        Args:
            training_data: List of training record dictionaries
            fit: Whether to fit the preprocessors on this data
            
        Returns:
            Preprocessed DataFrame
        """
        # Convert to DataFrame
        df = pd.DataFrame(training_data)
        
        # Convert date strings to datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            
            # Extract date-related features
            df['month'] = df['date'].dt.month
            df['year'] = df['date'].dt.year
            df['day_of_week'] = df['date'].dt.dayofweek
            
            # Drop original date column
            df = df.drop('date', axis=1)
        
        # Handle missing values and preprocessing
        return self._preprocess_dataframe(df, fit)
    
    def _preprocess_dataframe(self, df: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """
        Preprocess a DataFrame with necessary transformations.
        
        Args:
            df: Input DataFrame
            fit: Whether to fit the preprocessors on this data
            
        Returns:
            Preprocessed DataFrame
        """
        # Make a copy to avoid modifying the original
        df_processed = df.copy()
        
        # Store ID column if present
        id_col = None
        if 'horse_id' in df_processed.columns:
            id_col = df_processed['horse_id'].copy()
            df_processed = df_processed.drop('horse_id', axis=1)
        
        # Split numerical and categorical columns
        numerical_cols = df_processed.select_dtypes(include=['number']).columns
        categorical_cols = df_processed.select_dtypes(include=['object']).columns
        
        # Handle missing values
        if len(numerical_cols) > 0:
            # Impute missing numerical values
            if fit or not self.fitted:
                self.imputer.fit(df_processed[numerical_cols])
                self.fitted = True
            
            df_processed[numerical_cols] = self.imputer.transform(df_processed[numerical_cols])
        
        # Scale numerical features if there are any
        if len(numerical_cols) > 0:
            if fit or not self.fitted:
                self.numerical_scaler.fit(df_processed[numerical_cols])
            
            # Transform and create a new DataFrame
            scaled_numerical = pd.DataFrame(
                self.numerical_scaler.transform(df_processed[numerical_cols]),
                columns=numerical_cols,
                index=df_processed.index
            )
            
            # Replace original numerical columns with scaled values
            for col in numerical_cols:
                df_processed[col] = scaled_numerical[col]
        
        # Encode categorical features if there are any
        if len(categorical_cols) > 0:
            if fit or not self.fitted:
                self.categorical_encoder.fit(df_processed[categorical_cols])
            
            # Get feature names
            feature_names = self.categorical_encoder.get_feature_names_out(categorical_cols)
            
            # Transform categorical columns
            cat_encoded = self.categorical_encoder.transform(df_processed[categorical_cols])
            
            # Convert to DataFrame
            cat_encoded_df = pd.DataFrame(
                cat_encoded.toarray(),
                columns=feature_names,
                index=df_processed.index
            )
            
            # Drop original categorical columns
            df_processed = df_processed.drop(categorical_cols, axis=1)
            
            # Concatenate with encoded columns
            df_processed = pd.concat([df_processed, cat_encoded_df], axis=1)
        
        # Add back ID column if it was present
        if id_col is not None:
            df_processed['horse_id'] = id_col
        
        return df_processed
    
    def preprocess_for_training(self, 
                               horse_profiles: List[HorseProfile], 
                               training_data: List[Dict]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Preprocess both horse profiles and training data for model training.
        
        Args:
            horse_profiles: List of HorseProfile objects
            training_data: List of training record dictionaries
            
        Returns:
            Tuple of (features DataFrame, target DataFrame)
        """
        # Preprocess horse profiles
        horse_df = self.preprocess_horse_data(horse_profiles, fit=True)
        
        # Preprocess training data
        training_df = self.preprocess_training_data(training_data, fit=True)
        
        # Merge data on horse_id
        merged_df = pd.merge(
            training_df, 
            horse_df, 
            on='horse_id', 
            how='inner',
            suffixes=('_training', '_horse')
        )
        
        # Extract target variables
        target_columns = ['activity_type', 'success_rating', 'improvement_score']
        target_df = merged_df[target_columns].copy()
        
        # Remove target variables from features
        feature_df = merged_df.drop(target_columns, axis=1)
        
        return feature_df, target_df
