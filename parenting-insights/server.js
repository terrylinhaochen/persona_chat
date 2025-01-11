import express from 'express';
import cors from 'cors';
import axios from 'axios';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// Verify API key is present
const CLAUDE_API_KEY = process.env.CLAUDE_API_KEY;
if (!CLAUDE_API_KEY) {
  console.error('Error: CLAUDE_API_KEY is not set in environment variables');
  process.exit(1);
}

app.post('/api/generate', async (req, res) => {
  try {
    // Validate request body
    if (!req.body || !req.body.messages || !Array.isArray(req.body.messages)) {
      return res.status(400).json({ error: 'Invalid request body: messages array is required' });
    }

    // Log request for debugging
    console.log('Making request to Anthropic API:', {
      model: req.body.model,
      system: req.body.system,
      messageCount: req.body.messages.length
    });

    const response = await axios.post('https://api.anthropic.com/v1/messages', req.body, {
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
      }
    });

    if (!response.data) {
      throw new Error('No data received from Anthropic API');
    }

    // Log successful response
    console.log('Received response from Anthropic API:', {
      status: response.status,
      hasContent: !!response.data.content
    });

    res.json(response.data);
  } catch (error) {
    // Detailed error logging
    console.error('Error details:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      requestBody: {
        model: req.body?.model,
        messageCount: req.body?.messages?.length
      }
    });

    // Format error message based on error type
    let errorMessage = 'Failed to generate insight';
    if (error.response?.data?.error) {
      errorMessage = typeof error.response.data.error === 'string' 
        ? error.response.data.error 
        : error.response.data.error.message || 'Unknown API error';
    }

    res.status(500).json({
      error: errorMessage,
      details: error.message
    });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 