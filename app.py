#!/usr/bin/env python3
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Horse:
    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed

def recommend_training(horse):
    # Age-based recommendations
    if horse.age < 3:
        exercise = "walk"
        duration = 15
        intensity = "low"
        note = "Young horses need gentle exercise"
    elif horse.age < 10:
        exercise = "trot"
        duration = 30
        intensity = "medium"
        note = "Adult horses benefit from moderate exercise"
    else:
        exercise = "light canter"
        duration = 20
        intensity = "medium-low"
        note = "Senior horses need careful conditioning"
    
    # Breed adjustments
    if horse.breed == "Thoroughbred" and horse.age >= 3:
        exercise = "gallop"
        duration += 5
        note = "Thoroughbreds excel at speed work"
    elif horse.breed == "Draft" and horse.age >= 5:
        exercise = "pulling exercises"
        duration += 10
        note = "Draft horses benefit from strength training"
    
    return {
        "exercise": exercise,
        "duration": duration,
        "intensity": intensity,
        "note": note
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    data = request.json
    horse = Horse(data['name'], int(data['age']), data['breed'])
    recommendation = recommend_training(horse)
    return jsonify(recommendation)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
