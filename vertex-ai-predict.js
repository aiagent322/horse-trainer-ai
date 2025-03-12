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
const endpointId = 
'projects/horsetraineronemedia_1734212354249/locations/us-central1/endpoints/horsetraineronemedia_1734212354249';  
// Replace with your Endpoint ID

