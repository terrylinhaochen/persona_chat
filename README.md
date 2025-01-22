# Multi-Agent Discussion Panel

A real-time interactive discussion panel featuring AI agents with distinct personas, powered by FastAPI and React. The system simulates a late-night radio show format where historical figures engage in meaningful dialogue about user-submitted topics.

## 🌟 Features

- Real-time streaming responses from multiple AI agents
- Late-night radio show format with a host and guest speakers
- Historical personas with unique perspectives:
  - Host: A warm, professional radio show host
  - Handel: Baroque composer (circa 1741)
  - Sultan Mehmed II: Young Ottoman ruler
  - Scott: Antarctic explorer
- Document upload capability for each agent
- Responsive UI with Tailwind CSS
- Server-Sent Events (SSE) for real-time communication

## 📁 Project Structure

```
multi-agent-panel/
├── backend/
│   ├── config/
│   │   └── agent_configs.py     # Agent personality configurations
│   ├── agents/                  # Agent implementation modules
│   ├── routes/                  # API route handlers
│   ├── utils/                   # Utility functions
│   ├── main.py                  # FastAPI application entry
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   └── MultiAgentDialogue.jsx  # Main dialogue component
│   │   ├── App.jsx             # Root React component
│   │   └── main.jsx            # Application entry point
│   ├── public/                  # Static assets
│   ├── package.json            # Node.js dependencies
│   └── tailwind.config.js      # Tailwind CSS configuration
├── .env                        # Environment variables
└── README.md                   # Project documentation

Key Files:
- agent_configs.py: Defines agent personalities and behaviors
- MultiAgentDialogue.jsx: Manages agent interactions and UI
- main.py: FastAPI server with SSE implementation
```

## 🛠 Technical Stack

### Frontend
- React.js
- Tailwind CSS
- Server-Sent Events (SSE)
- Modern JavaScript (ES6+)

### Backend
- FastAPI
- Python 3.8+
- AutoGen framework for AI agents
- OpenAI GPT-4 API

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- OpenAI API key

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
FRONTEND_URL=http://localhost:3000
```

4. Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Install frontend dependencies:
```bash
cd frontend
npm install
```

2. Start the frontend development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## 🏗 System Architecture

### Agent System Design

The system implements a multi-agent dialogue system with four distinct personas:

1. **Host Agent**
   - Controls conversation flow
   - Introduces topics and manages transitions
   - Ensures balanced participation

2. **Guest Agents**
   - Each has a unique historical perspective
   - Maintains consistent character traits
   - Responds based on historical context

### Conversation Flow

1. User submits a topic/question
2. Host introduces the topic
3. Relevant guests respond based on their expertise
4. Host manages turn-taking and discussion depth
5. Conversation continues until natural conclusion

### Technical Implementation

#### Backend Architecture
- FastAPI handles HTTP requests and SSE
- AutoGen framework manages agent interactions
- Selector function determines speaking order
- Streaming responses ensure real-time interaction

#### Frontend Architecture
- React components for UI elements
- Real-time updates via SSE
- Tailwind CSS for styling
- File upload capability for each agent

## 📝 API Endpoints

### POST /chat
- Accepts user messages
- Returns SSE stream of agent responses
- Format: `{"content": "user_message"}`

### POST /upload-document
- Handles document uploads for agents
- Accepts multipart/form-data
- Returns upload confirmation

## 🔒 Security Considerations

- CORS configuration for frontend-backend communication
- Environment variables for sensitive data
- API key protection
- Rate limiting (to be implemented)

## 🐛 Troubleshooting

Common issues and solutions:

1. **SSE Connection Issues**
   - Check backend server is running
   - Verify CORS settings
   - Ensure proper event stream format

2. **Agent Response Delays**
   - Monitor API rate limits
   - Check system resources
   - Verify network connectivity

3. **File Upload Errors**
   - Check file size limits
   - Verify supported formats
   - Ensure proper form data

## 🚧 Future Improvements

- Add authentication system
- Implement conversation history
- Add more agent personas
- Enhance document processing capabilities
- Add conversation export functionality

## 📝 License

MIT License - feel free to use and modify for your own projects.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
