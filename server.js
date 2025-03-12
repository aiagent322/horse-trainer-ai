const express = require('express');
const axios = require('axios');
const app = express();

// Define the port
const port = process.env.PORT || 5000;

// Simple route to test
app.get('/', (req, res) => {
  res.send('Hello, Horse Trainer!');
});

// About page route
app.get('/about', (req, res) => {
  res.send('This is a page about Horse Trainer!');
});

// Example CrewAI API integration (Replace with actual CrewAI endpoint and 
key)
const crewAIApiKey = 'your-crewai-api-key';  // Replace with your actual 
CrewAI API key
const crewAIEndpoint = 'https://api.crewai.com/v1/your-endpoint';  // 
Replace with actual CrewAI API endpoint

// A route that communicates with CrewAI using Axios
app.get('/crewai', async (req, res) => {
  try {
    const response = await axios.post(crewAIEndpoint, {
      data: { /* Example data you want to send to CrewAI */ }
    }, {
      headers: {
        'Authorization': `Bearer ${crewAIApiKey}`,
        'Content-Type': 'application/json'
      }
    });

    // Return the response from CrewAI API
    res.json(response.data);
  } catch (error) {
    console.error('Error communicating with CrewAI:', error);
    res.status(500).send('Error communicating with CrewAI');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

const {PredictionServiceClient} = require('@google-cloud/aiplatform');
const client = new PredictionServiceClient();

async function predict() {
  const projectId = 'your-google-cloud-project-id';  // Replace with your 
project ID
  const endpointId = 'your-endpoint-id';             // Replace with your 
Vertex AI model endpoint ID
  const location = 'us-central1';                    // Your Vertex AI 
model location

  const endpoint = 
`projects/${projectId}/locations/${location}/endpoints/${endpointId}`;
  
  const instances = [
    {input: 'your input text'} // Replace with actual input
  ];

  try {
    const [response] = await client.predict({
      endpoint,
      instances,
    });
    
    console.log('Prediction result:', response.predictions);
  } catch (error) {
    console.error('Error making prediction:', error);
  }
}

predict();

