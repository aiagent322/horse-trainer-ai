"""
Visualization utilities for Horse Trainer AI

This module provides functions for visualizing horse training data.
"""
import logging
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.models.horse_profile import HorseProfile

logger = logging.getLogger(__name__)

def set_plotting_style():
    """Set the default plotting style."""
    sns.set(style="whitegrid")
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.rcParams["font.size"] = 12

def plot_training_history(horse_profile: HorseProfile, save_path: Optional[str] = None):
    """
    Plot the training history for a horse.
    
    Args:
        horse_profile: HorseProfile object
        save_path: Path to save the plot. If None, the plot will be displayed.
    """
    if not horse_profile.training_history:
        logger.warning(f"No training history for horse {horse_profile.name} (ID: {horse_profile.id})")
        return
    
    # Convert training history to DataFrame
    training_df = pd.DataFrame([
        {
            'date': session.date,
            'activity_type': session.activity_type,
            'duration_minutes': session.duration_minutes,
            'intensity': session.intensity,
            'performance_rating': session.performance_rating
        }
        for session in horse_profile.training_history
    ])
    
    # Sort by date
    training_df = training_df.sort_values('date')
    
    # Set up plotting style
    set_plotting_style()
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot performance over time
    sns.lineplot(
        data=training_df, 
        x='date', 
        y='performance_rating',
        hue='activity_type',
        markers=True,
        dashes=False,
        ax=ax1
    )
    ax1.set_title(f'Training Performance for {horse_profile.name}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Performance Rating (1-10)')
    ax1.grid(True)
    
    # Plot training duration by activity type
    sns.barplot(
        data=training_df,
        x='activity_type',
        y='duration_minutes',
        hue='intensity',
        ax=ax2
    )
    ax2.set_title('Training Duration by Activity Type')
    ax2.set_xlabel('Activity Type')
    ax2.set_ylabel('Duration (minutes)')
    ax2.grid(True)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save or display the plot
    if save_path:
        plt.savefig(save_path)
        logger.info(f"Training history plot saved to {save_path}")
    else:
        plt.show()

def plot_recommendation_confidence(recommendations: List[Dict], save_path: Optional[str] = None):
    """
    Plot the confidence levels for different activity recommendations.
    
    Args:
        recommendations: List of recommendation dictionaries
        save_path: Path to save the plot. If None, the plot will be displayed.
    """
    if not recommendations:
        logger.warning("No recommendations to plot")
        return
    
    # Convert recommendations to

