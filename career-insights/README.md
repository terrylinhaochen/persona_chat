# Career Insights Generator

An AI-powered application that transforms workplace challenges into insightful podcast episode concepts, complete with book recommendations and pattern analysis.

## 🌟 Features

- Real-time AI-generated insights about workplace dynamics
- Podcast-style episode titles and descriptions
- Curated book recommendations for each topic
- Clean, minimalist user interface
- Error handling and validation
- Real-time response streaming
- Automatic posting to Mastodon with threaded responses

## 📁 Project Structure

```
career-insights/
├── src/
│   ├── App.jsx              # Main application component
│   └── main.jsx             # Application entry point
├── public/                  # Static assets
├── server.js               # Express backend server
├── package.json           # Project dependencies and scripts
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── index.html            # HTML template
├── vite.config.js        # Vite configuration
└── README.md             # Project documentation

Key Files:
- App.jsx: React component with UI and API integration
- server.js: Express server with Claude and Mastodon API integration
- .env: Configuration for API keys and endpoints
```

## 🛠 Technical Implementation

### Architecture

#### Frontend (React + Vite)
- Single page application built with React
- Uses native fetch API for backend communication
- Real-time state management with React hooks
- Clean, responsive UI with inline styles
- JSON response parsing and validation

#### Backend (Express + Node.js)
- Express server as API proxy
- Anthropic Claude API integration
- Mastodon API integration for social sharing
- CORS handling for local development
- Environment variable management
- Error handling and logging

### AI Integration
- Uses Claude 3 Sonnet model
- System prompt engineering for consistent outputs
- JSON response formatting
- Pattern recognition in workplace dynamics
- Book recommendation curation

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm (v6 or higher)
- Anthropic API key
- Mastodon account and API access token

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd career-insights
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory:
```env
CLAUDE_API_KEY=your_anthropic_api_key_here
MASTODON_ACCESS_TOKEN=your_mastodon_access_token_here
MASTODON_INSTANCE=https://your.mastodon.instance
```

### Running the Application

1. Start the backend server:
```bash
npm run server
```

2. In a new terminal, start the frontend development server:
```bash
npm run dev
```

3. Open your browser and navigate to:
```
http://localhost:5173
```

## 💡 Usage

1. Enter a workplace challenge or topic in the input field
2. Click "Generate Insight" or press Enter
3. Wait for the AI to generate:
   - A podcast episode title
   - A detailed description
   - Book recommendations
4. View the generated content on Mastodon:
   - Main post with the insight
   - Threaded reply with book recommendations

## 🔧 Implementation Details

### Frontend Structure
```
src/
  ├── App.jsx        # Main application component
  ├── main.jsx       # Application entry point
  └── index.html     # HTML template
```

### Key Components

#### App.jsx
- Manages application state
- Handles API communication
- Implements UI rendering
- Error handling and validation

#### Server.js
- Express server setup
- API proxy implementation
- Error handling middleware
- Environment variable management
- Mastodon integration

### API Integration

The application uses the Anthropic Claude API with the following structure:

```javascript
{
  model: "claude-3-sonnet-20240229",
  max_tokens: 1024,
  system: SYSTEM_PROMPT,
  messages: [
    {
      role: "user",
      content: "Generate a podcast episode about: " + topic
    }
  ]
}
```

### Response Format

The AI generates responses in the following JSON structure:
```json
{
  "episodeTitle": "title - with explanation",
  "description": "description that reveals patterns and connections",
  "books": {
    "primary": {
      "title": "core book exploring system dynamics",
      "author": "author name"
    },
    "supporting": [
      {
        "title": "first book offering pattern insights",
        "author": "author name"
      },
      {
        "title": "second book offering pattern insights",
        "author": "author name"
      }
    ]
  }
}
```

## 🔒 Security

- API keys stored in environment variables
- CORS configuration for security
- Input validation and sanitization
- Error message sanitization

## 🐛 Troubleshooting

Common issues and solutions:

1. **CORS Errors**
   - Ensure backend is running on port 3001
   - Check CORS configuration in server.js

2. **API Key Issues**
   - Verify .env file exists
   - Check API key is valid
   - Ensure no whitespace in API key

3. **Parsing Errors**
   - Check console for raw response
   - Verify JSON structure
   - Check for response validation

4. **Mastodon Issues**
   - Verify access token permissions
   - Check instance URL format
   - Ensure content length is within limits

## 📝 License

MIT License - feel free to use and modify for your own projects. 