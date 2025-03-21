"""
Training Model for Horse Trainer AI

This module contains the TrainingModel class which analyzes horse data
and generates personalized training recommendations.
"""
import json
import logging
import pickle
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from src.models.horse_profile import HorseProfile

logger = logging.getLogger(__name__)

class TrainingModel:
    """
    Model for analyzing horse data and generating training recommendations.
    
    This class handles the entire machine learning pipeline, from feature
    extraction to model training and generation of recommendations.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize the training model with the given configuration.
        
        Args:
            config: Configuration dictionary containing model parameters
        """
        self.config = config
        self.model_config = config.get('model', {})
        self.training_config = config.get('training', {})
        self.features_config = config.get('features', {})
        self.recommendations_config = config.get('recommendations', {})
        
        self.model = None
        self.feature_pipeline = None
        self.performance_predictor = None
    
    def _extract_features(self, horse_profiles: List[HorseProfile]) -> pd.DataFrame:
        """
        Extract features from horse profiles for model training.
        
        Args:
            horse_profiles: List of HorseProfile objects
            
        Returns:
            DataFrame with extracted features
        """
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
            }
            
            # Add recent training statistics
            recent_training = horse.recent_training
            if recent_training:
                avg_duration = np.mean([s.duration_minutes for s in recent_training])
                avg_performance = np.mean([s.performance_rating for s in recent_training])
                training_types = set(s.activity_type for s in recent_training)
                intensity_counts = {
                    'low': sum(1 for s in recent_training if s.intensity == 'low'),
                    'medium': sum(1 for s in recent_training if s.intensity == 'medium'),
                    'high': sum(1 for s in recent_training if s.intensity == 'high')
                }
                
                horse_features.update({
                    'recent_training_count': len(recent_training),
                    'avg_training_duration': avg_duration,
                    'avg_performance_rating': avg_performance,
                    'training_variety': len(training_types),
                    'low_intensity_count': intensity_counts['low'],
                    'medium_intensity_count': intensity_counts['medium'],
                    'high_intensity_count': intensity_counts['high'],
                })
            else:
                # Default values if no recent training
                horse_features.update({
                    'recent_training_count': 0,
                    'avg_training_duration': 0,
                    'avg_performance_rating': 0,
                    'training_variety': 0,
                    'low_intensity_count': 0,
                    'medium_intensity_count': 0,
                    'high_intensity_count': 0,
                })
            
            # Add medical condition flag if enabled
            if self.features_config.get('include_medical', True):
                horse_features['has_medical_conditions'] = int(horse.has_medical_conditions)
            
            # Add dietary restrictions if enabled
            if self.features_config.get('include_diet', True):
                horse_features['has_dietary_restrictions'] = int(len(horse.dietary_restrictions) > 0)
            
            # Add lineage information if enabled
            if self.features_config.get('include_lineage', True) and horse.lineage:
                horse_features['has_lineage_info'] = int(len(horse.lineage) > 0)
            
            features.append(horse_features)
        
        # Convert to DataFrame
        df = pd.DataFrame(features)
        
        # Handle missing values
        df = df.fillna(0)
        
        return df
    
    def _create_feature_pipeline(self, X: pd.DataFrame) -> ColumnTransformer:
        """
        Create a preprocessing pipeline for features.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Scikit-learn ColumnTransformer pipeline
        """
        # Identify categorical and numerical columns
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        numerical_cols = X.select_dtypes(include=['number']).columns.tolist()
        
        # Remove 'horse_id' from numerical columns if present
        if 'horse_id' in numerical_cols:
            numerical_cols.remove('horse_id')
        
        # Create preprocessing pipelines
        numerical_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Combine preprocessing steps
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ],
            remainder='drop'  # Drop columns not specified
        )
        
        return preprocessor
    
    def _prepare_target_variables(self, training_data: List[Dict]) -> pd.DataFrame:
        """
        Prepare target variables from training data.
        
        Args:
            training_data: List of training records
            
        Returns:
            DataFrame with target variables
        """
        targets = []
        
        for record in training_data:
            target = {
                'horse_id': record['horse_id'],
                'activity_type': record['activity_type'],
                'success_rating': record['success_rating'],
                'improvement_score': record['improvement_score']
            }
            targets.append(target)
        
        return pd.DataFrame(targets)
    
    def train(self, 
              training_data: List[Dict], 
              horse_profiles: List[HorseProfile]) -> None:
        """
        Train the model using historical training data and horse profiles.
        
        Args:
            training_data: List of historical training records
            horse_profiles: List of HorseProfile objects
        """
        logger.info("Extracting features from horse profiles")
        X = self._extract_features(horse_profiles)
        
        logger.info("Preparing target variables")
        y = self._prepare_target_variables(training_data)
        
        # Merge X and y on horse_id
        merged_data = pd.merge(X, y, on='horse_id')
        
        # Remove horse_id column for modeling
        horse_ids = merged_data['horse_id']
        merged_data = merged_data.drop('horse_id', axis=1)
        
        # Split target variables
        y_activity = merged_data['activity_type']
        y_success = merged_data['success_rating']
        y_improvement = merged_data['improvement_score']
        
        # Remove target columns from features
        X = merged_data.drop(['activity_type', 'success_rating', 'improvement_score'], axis=1)
        
        # Create feature pipeline
        logger.info("Creating feature preprocessing pipeline")
        self.feature_pipeline = self._create_feature_pipeline(X)
        
        # Split data for training and testing
        test_size = self.training_config.get('test_size', 0.2)
        X_train, X_test, y_activity_train, y_activity_test = train_test_split(
            X, y_activity, test_size=test_size, random_state=42
        )
        
        # Transform features
        X_train_transformed = self.feature_pipeline.fit_transform(X_train)
        X_test_transformed = self.feature_pipeline.transform(X_test)
        
        # Create and train model for activity recommendation
        logger.info("Training activity recommendation model")
        model_type = self.model_config.get('type', 'random_forest')
        
        if model_type == 'random_forest':
            model_params = self.model_config.get('params', {})
            self.model = RandomForestClassifier(**model_params)
            
            # Train model
            self.model.fit(X_train_transformed, y_activity_train)
            
            # Evaluate model
            train_accuracy = self.model.score(X_train_transformed, y_activity_train)
            test_accuracy = self.model.score(X_test_transformed, y_activity_test)
            
            logger.info(f"Activity model training accuracy: {train_accuracy:.4f}")
            logger.info(f"Activity model testing accuracy: {test_accuracy:.4f}")
            
            # Train performance predictor
            logger.info("Training performance prediction model")
            self.performance_predictor = GradientBoostingRegressor(
                n_estimators=100, 
                learning_rate=0.1, 
                max_depth=5, 
                random_state=42
            )
            
            # Combine X with activity type for performance prediction
            X_with_activity = pd.concat([
                X_train.reset_index(drop=True),
                pd.get_dummies(y_activity_train, prefix='activity').reset_index(drop=True)
            ], axis=1)
            
            y_success_train = y_success.loc[X_train.index]
            self.performance_predictor.fit(X_with_activity, y_success_train)
            
            # Evaluate performance predictor
            performance_score = self.performance_predictor.score(X_with_activity, y_success_train)
            logger.info(f"Performance predictor R² score: {performance_score:.4f}")
            
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def generate_recommendations(self, 
                               horse_profiles: List[HorseProfile]) -> List[Dict]:
        """
        Generate training recommendations for each horse profile.
        
        Args:
            horse_profiles: List of HorseProfile objects
            
        Returns:
            List of recommendation dictionaries
        """
        if self.model is None or self.feature_pipeline is None:
            raise ValueError("Model has not been trained yet")
        
        recommendations = []
        
        # Extract features from profiles
        X = self._extract_features(horse_profiles)
        
        # Store horse_ids and remove from features
        horse_ids = X['horse_id'].copy()
        X = X.drop('horse_id', axis=1)
        
        # Transform features
        X_transformed = self.feature_pipeline.transform(X)
        
        # Get activity probabilities
        activity_probs = self.model.predict_proba(X_transformed)
        
        # Map horse profiles by ID for easy lookup
        profile_map = {horse.id: horse for horse in horse_profiles}
        
        # Get activity classes
        activity_classes = self.model.classes_
        
        # Generate recommendations for each horse
        for i, horse_id in enumerate(horse_ids):
            horse = profile_map[horse_id]
            
            # Sort activities by probability
            activity_scores = [(activity, prob) for activity, prob in 
                              zip(activity_classes, activity_probs[i])]
            activity_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Get top activities
            max_recommendations = self.recommendations_config.get('max_per_horse', 5)
            min_confidence = self.recommendations_config.get('min_confidence', 0.1)
            
            horse_recommendations = []
            
            for activity, confidence in activity_scores[:max_recommendations]:
                if confidence >= min_confidence:
                    # Create recommendation
                    recommendation = {
                        'horse_id': horse_id,
                        'horse_name': horse.name,
                        'activity_type': activity,
                        'confidence': round(float(confidence), 3),
                        'recommended_date': date.today().isoformat(),
                        'recommended_duration': self._recommend_duration(horse, activity),
                        'recommended_intensity': self._recommend_intensity(horse, activity),
                        'notes': self._generate_recommendation_notes(horse, activity)
                    }
                    
                    horse_recommendations.append(recommendation)
            
            recommendations.extend(horse_recommendations)
        
        return recommendations
    
    def _recommend_duration(self, horse: HorseProfile, activity: str) -> int:
        """Recommend training duration based on horse profile and activity."""
        # Base duration by activity type
        base_durations = {
            'trot': 30,
            'canter': 20,
            'gallop': 15,
            'jump': 25,
            'dressage': 40,
            'trail': 45,
            'groundwork': 35
        }
        
        # Get base duration, default to 30 minutes
        duration = base_durations.get(activity, 30)
        
        # Adjust for age - younger and older horses get shorter sessions
        if horse.age < 3:
            duration = max(15, duration - 15)  # Minimum 15 minutes
        elif horse.age > 15:
            duration = max(15, duration - 10)  # Minimum 15 minutes
        
        # Adjust for medical conditions
        if horse.has_medical_conditions:
            duration = max(15, duration - 10)  # Minimum 15 minutes
        
        # Round to nearest 5 minutes
        return round(duration / 5) * 5
    
    def _recommend_intensity(self, horse: HorseProfile, activity: str) -> str:
        """Recommend training intensity based on horse profile and activity."""
        # High-intensity activities
        high_intensity = ['gallop', 'jump']
        # Medium-intensity activities
        medium_intensity = ['canter', 'dressage', 'trail']
        # Low-intensity activities
        low_intensity = ['trot', 'groundwork']
        
        # Base intensity by activity type
        if activity in high_intensity:
            base_intensity = 'high'
        elif activity in medium_intensity:
            base_intensity = 'medium'
        else:
            base_intensity = 'low'
        
        # Adjust for age
        if horse.age < 3 or horse.age > 15:
            # Lower intensity for very young or older horses
            if base_intensity == 'high':
                return 'medium'
            elif base_intensity == 'medium':
                return 'low'
        
        # Adjust for medical conditions
        if horse.has_medical_conditions:
            # Lower intensity for horses with medical conditions
            if base_intensity == 'high':
                return 'medium'
            elif base_intensity == 'medium':
                return 'low'
        
        return base_intensity
    
    def _generate_recommendation_notes(self, horse: HorseProfile, activity: str) -> str:
        """Generate personalized notes for the recommendation."""
        notes = []
        
        # Add age-specific notes
        if horse.age < 3:
            notes.append("Young horse - keep sessions short and vary activities to maintain interest.")
        elif horse.age > 15:
            notes.append("Senior horse - monitor closely for signs of fatigue and allow extra warm-up time.")
        
        # Add medical condition notes
