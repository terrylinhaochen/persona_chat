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

// Verify required environment variables
const CLAUDE_API_KEY = process.env.CLAUDE_API_KEY;
const MASTODON_ACCESS_TOKEN = process.env.MASTODON_ACCESS_TOKEN;
const MASTODON_INSTANCE = process.env.MASTODON_INSTANCE || 'https://mastodon.social';

if (!CLAUDE_API_KEY) {
  console.error('Error: CLAUDE_API_KEY is not set in environment variables');
  process.exit(1);
}

if (!MASTODON_ACCESS_TOKEN) {
  console.error('Error: MASTODON_ACCESS_TOKEN is not set in environment variables');
  process.exit(1);
}

async function postToMastodon(originalQuestion, insight) {
  try {
    // Format the main content
    const mainContent = `Q: ${originalQuestion}

📝 ${insight.episodeTitle}

${insight.description}`.trim();

    // Truncate main content if needed
    const truncatedMain = mainContent.length > 450 
      ? mainContent.slice(0, 447) + '...'
      : mainContent;

    // Post main content
    const mainPost = await axios.post(`${MASTODON_INSTANCE}/api/v1/statuses`, {
      status: truncatedMain,
      visibility: 'public'
    }, {
      headers: {
        'Authorization': `Bearer ${MASTODON_ACCESS_TOKEN}`,
        'Content-Type': 'application/json'
      }
    });

    // Format book recommendations
    const bookContent = `📚 Recommended Reading:

• ${insight.books.primary.title} by ${insight.books.primary.author}

Supporting reads:
• ${insight.books.supporting[0].title} by ${insight.books.supporting[0].author}
• ${insight.books.supporting[1].title} by ${insight.books.supporting[1].author}`.trim();

    // Post book recommendations as a reply
    const replyPost = await axios.post(`${MASTODON_INSTANCE}/api/v1/statuses`, {
      status: bookContent,
      in_reply_to_id: mainPost.data.id,
      visibility: 'public'
    }, {
      headers: {
        'Authorization': `Bearer ${MASTODON_ACCESS_TOKEN}`,
        'Content-Type': 'application/json'
      }
    });

    return {
      mainPost: mainPost.data,
      replyPost: replyPost.data
    };
  } catch (error) {
    console.error('Error posting to Mastodon:', error);
    throw new Error('Failed to post to Mastodon: ' + error.message);
  }
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

    // Parse the AI response
    const text = response.data.content[0].text.trim();
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No JSON object found in response');
    }
    const insight = JSON.parse(jsonMatch[0]);

    // Post to Mastodon
    const originalQuestion = req.body.messages[0].content.replace('Generate a podcast episode about: ', '');
    const mastodonResponse = await postToMastodon(originalQuestion, insight);

    // Return both the insight and Mastodon post URLs
    res.json({
      ...response.data,
      mastodon: {
        mainPost: {
          url: mastodonResponse.mainPost.url,
          id: mastodonResponse.mainPost.id
        },
        replyPost: {
          url: mastodonResponse.replyPost.url,
          id: mastodonResponse.replyPost.id
        }
      }
    });
  } catch (error) {
    console.error('Error details:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      requestBody: {
        model: req.body?.model,
        messageCount: req.body?.messages?.length
      }
    });

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