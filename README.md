# Multi-Agent Discussion Panel

A Streamlit-powered interactive discussion panel featuring AI agents with customizable personas. The system simulates a late-night radio show format where user-defined personas engage in meaningful dialogue about submitted topics.

## 🌟 Features

- Real-time AI-generated responses from multiple agents
- Late-night radio show format with a host and guest speakers
- Customizable personas:
  - Create and manage unique personas
  - Define personality traits and expertise
  - Save personas for future use
- Dynamic participant selection (1-3 participants)
- Clean, intuitive Streamlit interface
- Persistent persona storage

## 📁 Project Structure

```
multi-agent-panel/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── personas.json         # Saved persona configurations
├── .env                  # Environment variables
└── README.md            # Project documentation

Key Files:
- app.py: Streamlit application with UI and chat logic
- personas.json: Persistent storage for created personas
```

## 🛠 Technical Stack

- Streamlit
- Python 3.8+
- Anthropic Claude API
- JSON for persona storage

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Anthropic API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd multi-agent-panel
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```env
CLAUDE_API_KEY=your_anthropic_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## 💡 Usage

### Managing Personas

1. Create New Personas:
   - Click "Create New Persona" in the right sidebar
   - Enter name and description
   - Click "Add Persona" to save

2. View Personas:
   - Existing personas appear in the gallery view
   - Click to expand and view full descriptions
   - Delete unwanted personas

### Setting Up Discussions

1. Select Participants:
   - Choose up to 3 participants from dropdown menus
   - Each participant uses a saved persona
   - Host is always included by default

2. Start a Discussion:
   - Enter your topic or question
   - Click "Start Discussion"
   - View the AI-generated conversation

## 🏗 System Architecture

### Persona Management
- JSON-based storage for persistence
- Dynamic persona creation and deletion
- Automatic loading of saved personas

### Discussion System
- Host + 1-3 additional participants
- Flexible participant selection
- Contextual responses based on persona descriptions

## 🔒 Security

- Environment variables for API keys
- Local storage for persona data
- Input validation and sanitization

## 🐛 Troubleshooting

Common issues and solutions:

1. **Persona Not Saving**
   - Check write permissions for personas.json
   - Verify JSON format
   - Clear browser cache

2. **API Response Issues**
   - Verify API key in .env
   - Check internet connection
   - Monitor API rate limits

## 🚧 Future Improvements

- Add persona categories/tags
- Implement conversation history export
- Add persona templates
- Enable persona sharing
- Add conversation branching

## 📝 License

MIT License - feel free to use and modify for your own projects.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
