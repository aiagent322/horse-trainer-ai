"""
API endpoints for Horse Trainer AI

This module defines the API endpoints for accessing the Horse Trainer AI functionality.
"""
import logging
from datetime import date
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.config import load_config
from src.data.data_loader import DataLoader
from src.models.horse_profile import HorseProfile, MedicalRecord, TrainingSession
from src.models.training_model import TrainingModel

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Horse Trainer AI API",
    description="API for accessing Horse Trainer AI functionality",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for getting the data loader
def get_data_loader():
    """Get the data loader instance."""
    return DataLoader()

# Dependency for getting the training model
def get_training_model():
    """Get the training model instance."""
    config = load_config("config/default.json")
    return TrainingModel(config)

# Pydantic models for request/response validation
class TrainingSessionModel(BaseModel):
    """Pydantic model for a training session."""
    date: str
    activity_type: str
    duration_minutes: int
    intensity: str
    performance_rating: int
    notes: Optional[str] = None

class MedicalRecordModel(BaseModel):
    """Pydantic model for a medical record."""
    date: str
    condition: str
    treatment: str
    notes: Optional[str] = None

class HorseProfileModel(BaseModel):
    """Pydantic model for a horse profile."""
    id: str
    name: str
    breed: str
    birth_date: str
    sex: str
    color: str
    height_hands: float
    weight_kg: float
    lineage: Dict[str, str] = Field(default_factory=dict)
    dietary_restrictions: List[str] = Field(default_factory=list)
    medical_history: List[MedicalRecordModel] = Field(default_factory=list)
    training_history: List[TrainingSessionModel] = Field(default_factory=list)

class TrainingRecommendationModel(BaseModel):
    """Pydantic model for a training recommendation."""
    horse_id: str
    horse_name: str
    activity_type: str
    confidence: float
    recommended_date: str
    recommended_duration: int
    recommended_intensity: str
    notes: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint returns basic API information."""
    return {
        "name": "Horse Trainer AI API",
        "version": "1.0.0",
        "description": "API for accessing Horse Trainer AI functionality"
    }

@app.get("/horses", response_model=List[HorseProfileModel])
async def get_horses(data_loader: DataLoader = Depends(get_data_loader)):
    """
    Get all horse profiles.
    
    Returns:
        List of horse profiles
    """
    try:
        profiles = data_loader.load_horse_profiles()
        return [profile.to_dict() for profile in profiles]
    except Exception as e:
        logger.error(f"Error getting horse profiles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/horses/{horse_id}", response_model=HorseProfileModel)
async def get_horse(
    horse_id: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """
    Get a specific horse profile by ID.
    
    Args:
        horse_id: ID of the horse
        
    Returns:
        Horse profile
    """
    try:
        profiles = data_loader.load_horse_profiles()
        for profile in profiles:
            if profile.id == horse_id:
                return profile.to_dict()
        
        raise HTTPException(status_code=404, detail=f"Horse with ID {horse_id} not found")
    except Exception as e:
        logger.error(f"Error getting horse profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/horses", response_model=HorseProfileModel)
async def create_horse(
    horse: HorseProfileModel,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """
    Create a new horse profile.
    
    Args:
        horse: Horse profile data
        
    Returns:
        Created horse profile
    """
    try:
        # Load existing profiles
        profiles = data_loader.load_horse_profiles()
        
        # Check if horse ID already exists
        for profile in profiles:
            if profile.id == horse.id:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Horse with ID {horse.id} already exists"
                )
        
        # Create new horse profile
        new_profile = HorseProfile.from_dict(horse.dict())
        profiles.append(new_profile)
        
        # Save profiles
        data_loader.save_horse_profiles(profiles)
        
        return new_profile.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating horse profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/horses/{horse_id}", response_model=HorseProfileModel)
async def update_horse(
    horse_id: str,
    horse: HorseProfileModel,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """
    Update a horse profile.
    
    Args:
        horse_id: ID of the horse to update
        horse: Updated horse profile data
        
    Returns:
        Updated horse profile
    """
    try:
        # Load existing profiles
        profiles = data_loader.load_horse_profiles()
        
        # Find horse profile to update
        for i, profile in enumerate(profiles):
            if profile.id == horse_id:
                # Update profile
                profiles[i] = HorseProfile.from_dict(horse.dict())
                
                # Save profiles
                data_loader.save_horse_profiles(profiles)
                
                return profiles[i].to_dict()
        
        raise HTTPException(status_code=404, detail=f"Horse with ID {horse_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating horse profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/horses/{horse_id}")
async def delete_horse(
    horse_id: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """
    Delete a horse profile.
    
    Args:
        horse_id: ID of the horse to delete
        
    Returns:
        Success message
    """
    try:
        # Load existing profiles
        profiles = data_loader.load_horse_profiles()
        
        # Find horse profile to delete
        for i, profile in enumerate(profiles):
            if profile.id == horse_id:
                # Remove profile
                profiles.pop(i)
                
                # Save profiles
                data_loader.save_horse_profiles(profiles)
                
                return {"message": f"Horse with ID {horse_id} deleted successfully"}
        
        raise HTTPException(status_code=404, detail=f"Horse with ID {horse_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting horse profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/training/{horse_id}", response_model=TrainingSessionModel)
async def add_training_session(
    horse_id: str,
    session: TrainingSessionModel,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """
    Add a training session to a horse's history.
    
    Args:
        horse_id: ID of the horse
        session: Training session data
        
    Returns:
        Added training session
    """
    try:
        # Load existing profiles
        profiles = data_loader.load_horse_profiles()
        
        # Find horse profile
        for profile in profiles:
            if profile.id == horse_id:
                # Add training session
                new_session = TrainingSession(
                    date=date.fromisoformat(session.date),
                    activity_type=session.activity_type,
                    duration_minutes=session.duration_minutes,
                    intensity=session.intensity,
                    performance_rating=session.performance_rating,
                    notes=session.notes
                )
                profile.training_history.append(new_session)
                
                # Save profiles
                data_loader.save_horse_profiles(profiles)
                
                return session
        
        raise HTTPException(status_code=404, detail=f"Horse with ID {horse_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding training session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendations", response_model=List[TrainingRecommendationModel])
async def get_recommendations(
    horse_id: Optional[str] = None,
    data_loader: DataLoader = Depends(get_data_loader),
    model: TrainingModel = Depends(get_training_model)
):
    """
    Get training recommendations for horses.
    
    Args:
        horse_id: Optional ID to filter recommendations for a specific horse
        
    Returns:
        List of training recommendations
    """
    try:
        # Load horse profiles
        profiles = data_loader.load_horse_profiles()
        
        # Filter profiles if horse_id is provided
        if horse_id:
            profiles = [profile for profile in profiles if profile.id == horse_id]
            if not profiles:
                raise HTTPException(status_code=404, detail=f"Horse with ID {horse_id} not found")
        
        # Load training data
        training_data = data_loader.load_training_data()
        
        # Train model if not already trained
        if not hasattr(model, 'model') or model.model is None:
            model.train(training_data, profiles)
        
        # Generate recommendations
        recommendations = model.generate_recommendations(profiles)
        
        return recommendations
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def start():
    """Start the API server using uvicorn."""
    import uvicorn
    
    config = load_config("config/default.json")
    api_config = config.get('api', {})
    
    host = api_config.get('host', '0.0.0.0')
    port = api_config.get('port', 8000)
    debug = api_config.get('debug', False)
    
    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run("src.api.endpoints:app", host=host, port=port, reload=debug)

if __name__ == "__main__":
    from src.utils.logger import setup_logger
    setup_logger()
    start()
