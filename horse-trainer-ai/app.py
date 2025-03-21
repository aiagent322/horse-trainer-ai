from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class HorseTrainer:
    def get_greeting(self):
        return "Welcome to EquineCoach! How can I help with your horse 
training today?"
    
    def get_response(self, user_input):
        if "training" in user_input.lower():
            return "For training techniques, I recommend starting with 
groundwork to build trust."
        elif "nutrition" in user_input.lower():
            return "Horses should eat 1.5-2% of their body weight in 
forage daily. Fresh water should always be available."
        elif "health" in user_input.lower():
            return "Regular veterinary care, deworming, and dental checks 
are essential for horse health."
        elif "behavior" in user_input.lower():
            return "Understanding horse behavior starts with recognizing 
they are prey animals. Patience and consistency are key."
        else:
            return "I can provide advice on training, nutrition, health 
care, and behavior. What would you like to know about?"

trainer = HorseTrainer()

@app.route("/")
def home():
    return render_template('index.html', greeting=trainer.get_greeting())

@app.route('/get_response', methods=['POST'])
def get_response():
    message = request.json['message']
    return jsonify({'response': trainer.get_response(message)})

if __name__ == "__main__":
    app.run(debug=True)

