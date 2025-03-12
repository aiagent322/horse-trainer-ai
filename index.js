// Import necessary libraries
const express = require('express');
const bodyParser = require('body-parser');
const app = express();

// Middleware to parse incoming JSON requests
app.use(bodyParser.json());

// Define the webhook endpoint
app.post('/webhook', (req, res) => {
  const query = req.body.queryResult.queryText;
  let responseText = "";

  // Handle different queries
  if (query.includes('dressage')) {
    responseText = 'Great video on dressage';
  } else if (query.includes('reining')) {
    responseText = 'Check out these reining trainers';
  } else {
    responseText = 'Not sure about that topic, but I can help with/ 
horse training!';
  }

  // Send the response back to Dialogflow
  const response = {
    fulfillmentText: responseText
  };
  res.json(response);
});

// Set up the server to listen on a specified port
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Webhook server running on port ${PORT}`);
});
nano index.js
// Import necessary libraries
const express = require('express');
const bodyParser = require('body-parser');

// Initialize the Express application
const app = express();

// Middleware to parse incoming JSON requests
app.use(bodyParser.json());

// Define the webhook endpoint
app.post('/webhook', (req, res) => {
  const query = req.body.queryResult.queryText;  // Extract query from the 
request body
  let responseText = "";  // Variable to hold the response message

  // Handle different queries
  if (query.includes('dressage')) {
    responseText = 'Here’s a great video on dressage: [Dressage Video 
URL]';
  } else if (query.includes('reining')) {
    responseText = 'Check out these reining trainers: [Trainer List URL]';
  } else {
    responseText = 'I’m not sure about that topic, but I can help with 
horse training!';
  }

  // Construct the response object to send back to Dialogflow
  const response = {
    fulfillmentText: responseText  // Send the fulfillment message
  };

  // Send the response as JSON
  res.json(response);
});

// Set up the server to listen on a specified port
const PORT = process.env.PORT || 5000;  // Default port is 5000
app.listen(PORT, () => {
  console.log(`Webhook server running on port ${PORT}`);  // Log when the 
server starts
});
node index.js
// Import required libraries
const express = require('express');
const bodyParser = require('body-parser');

// Initialize the Express application
const app = express();

// Middleware to parse incoming JSON requests
app.use(bodyParser.json());

// Define the webhook endpoint
app.post('/webhook', (req, res) => {
  const query = req.body.queryResult.queryText;  // Extract query from the 
request body
  let responseText = "";  // Variable to hold the response message

  // Handle different queries
  if (query.includes('dressage')) {
    responseText = 'Here’s a great video on dressage: [Dressage Video 
URL]';
  } else if (query.includes('reining')) {
    responseText = 'Check out these reining trainers: [Trainer List URL]';
  } else {
    responseText = 'I’m not sure about that topic, but I can help with 
horse training!';
  }

  // Construct the response object to send back to Dialogflow
  const response = {
    fulfillmentText: responseText  // Send the fulfillment message
  };

  // Send the response back as JSON
  res.json(response);
});

// Set up the server to listen on a specified port
const PORT = process.env.PORT || 5000;  // Default port is 5000
app.listen(PORT, () => {
  console.log(`Webhook server running on port ${PORT}`);  // Log when the 
server starts
});

