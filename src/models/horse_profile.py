"""
Horse Profile Model

This module contains the HorseProfile class which represents 
a horse's characteristics and training history.
"""
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional

@dataclass
class MedicalRecord:
    """Medical record for a horse."""
    date: date
    condition: str
    treatment: str
    notes: Optional[str] = None

@dataclass
class TrainingSession:
    """Training session record."""
    date: date
    activity_type: str
    duration_minutes: int
    intensity: str  # 'low', 'medium', 'high'
    performance_rating: int  # 1-10
    notes: Optional[str] = None

@dataclass
class HorseProfile:
    """Horse profile containing all relevant information."""
    id: str
    name: str
    breed: str
    birth_date: date
    sex: str  # 'male', 'female', 'gelding'
    color: str
    height_hands: float
    weight_kg: float
    lineage: Dict[str, str] = field(default_factory=dict)
    dietary_restrictions: List[str] = field(default_factory=list)
    medical_history: List[MedicalRecord] = field(default_factory=list)
    training_history: List[TrainingSession] = field(default_factory=list)
    
    @property
    def age(self) -> float:
        """Calculate the horse's age in years."""
        today = date.today()
        born = self.birth_date
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return age
    
    @property
    def recent_training(self) -> List[TrainingSession]:
        """Get the last 30 days of training sessions."""
        today = date.today()
        thirty_days_ago = date.fromordinal(today.toordinal() - 30)
        return [session for session in self.training_history 
                if session.date >= thirty_days_ago]
    
    @property
    def has_medical_conditions(self) -> bool:
        """Check if the horse has any active medical conditions."""
        # This is a simplification - in reality, we'd need more complex logic
        # to determine if conditions are still active
        if not self.medical_history:
            return False
        recent_date = date.fromordinal(date.today().toordinal() - 90)  # Last 90 days
        return any(record.date >= recent_date for record in self.medical_history)
    
    def to_dict(self) -> Dict:
        """Convert the horse profile to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'breed': self.breed,
            'birth_date': self.birth_date.isoformat(),
            'age': self.age,
            'sex': self.sex,
            'color': self.color,
            'height_hands': self.height_hands,
            'weight_kg': self.weight_kg,
            'lineage': self.lineage,
            'dietary_restrictions': self.dietary_restrictions,
            'medical_history': [
                {
                    'date': record.date.isoformat(),
                    'condition': record.condition,
                    'treatment': record.treatment,
                    'notes': record.notes
                }
                for record in self.medical_history
            ],
            'training_history': [
                {
                    'date': session.date.isoformat(),
                    'activity_type': session.activity_type,
                    'duration_minutes': session.duration_minutes,
                    'intensity': session.intensity,
                    'performance_rating': session.performance_rating,
                    'notes': session.notes
                }
                for session in self.training_history
            ]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HorseProfile':
        """Create a HorseProfile from a dictionary."""
        # Convert date strings to date objects
        birth_date = date.fromisoformat(data['birth_date'])
        
        # Create a new HorseProfile
        profile = cls(
            id=data['id'],
            name=data['name'],
            breed=data['breed'],
            birth_date=birth_date,
            sex=data['sex'],
            color=data['color'],
            height_hands=data['height_hands'],
            weight_kg=data['weight_kg'],
            lineage=data.get('lineage', {}),
            dietary_restrictions=data.get('dietary_restrictions', [])
        )
        
        # Add medical history
        if 'medical_history' in data:
            for record in data['medical_history']:
                profile.medical_history.append(MedicalRecord(
                    date=date.fromisoformat(record['date']),
                    condition=record['condition'],
                    treatment=record['treatment'],
                    notes=record.get('notes')
                ))
        
        # Add training history
        if 'training_history' in data:
            for session in data['training_history']:
                profile.training_history.append(TrainingSession(
                    date=date.fromisoformat(session['date']),
                    activity_type=session['activity_type'],
                    duration_minutes=session['duration_minutes'],
                    intensity=session['intensity'],
                    performance_rating=session['performance_rating'],
                    notes=session.get('notes')
                ))
        
        return profile
