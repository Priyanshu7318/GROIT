# GROIT - Advanced AI Assistant

GROIT is a comprehensive AI-powered assistant that combines multiple cutting-edge technologies to provide a seamless conversational experience. It features voice interaction, real-time web search, image generation, automation capabilities, and both desktop and web interfaces.

## Features

### Core Capabilities
- **Conversational AI**: Powered by Groq and Cohere APIs for intelligent responses
- **Voice Interaction**: Speech-to-text and text-to-speech functionality
- **Real-time Search**: Live web search and YouTube search integration
- **Image Generation**: AI-powered image creation from text prompts
- **Automation**: System control, app management, and task automation
- **Content Creation**: Text generation, drafting, and creative writing
- **Reminders**: Time-based reminder system
- **Multi-modal Interfaces**: Both desktop GUI and web application

### Technical Features
- **Decision-Making Model**: Intelligent query classification and routing
- **Modular Architecture**: Separated backend modules for different functionalities
- **RESTful API**: Flask-based API bridge for web integration
- **Cross-platform**: Works on macOS, Windows, and Linux
- **Persistent Chat Logs**: Maintains conversation history
- **Environment Configuration**: Secure API key management

## Project Structure

```
GROIT/
├── Main.py                 # Main application entry point
├── api_bridge.py          # Flask API server for web integration
├── requirements.txt       # Python dependencies
├── Backend/               # Core backend modules
│   ├── __init__.py
│   ├── Model.py           # Decision-making model (FirstLayerDMM)
│   ├── Chatbot.py         # AI conversation handler
│   ├── SpeechToText.py    # Voice input processing
│   ├── TextToSpeech.py    # Voice output generation
│   ├── RealtimeSearchEngine.py  # Web search functionality
│   ├── Automation.py      # System automation tasks
│   ├── Extraction.py      # Data extraction utilities
│   └── ImageGeneration.py # AI image generation
├── Frontend/              # Desktop interface
│   └── GUI.py            # PyQt6-based desktop application
├── web-frontend/          # Web interface
│   ├── src/
│   │   ├── App.jsx       # React web application
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
├── Data/                  # Application data storage
└── chromedriver-mac-arm64/  # WebDriver for automation
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+ (for web frontend)
- macOS/Windows/Linux

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd GROIT
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```env
Username=YourName
Assistantname=GROIT
GroqAPIkey=your_groq_api_key
CohereAPIkey=your_cohere_api_key
# Add other API keys as needed
```

### Web Frontend Setup

1. Navigate to web frontend:
```bash
cd web-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

## Usage

### Running the Application

1. Start the Flask API server:
```bash
python api_bridge.py
```

2. For desktop GUI (if implemented):
```bash
python -m Frontend.GUI
```

3. For web interface:
```bash
cd web-frontend
npm run dev
```

4. Main application:
```bash
python Main.py
```

### Voice Commands

GROIT supports various voice commands:

- **General Queries**: "Who was Albert Einstein?" → Provides AI-generated responses
- **Real-time Info**: "What's the current weather?" → Searches web for live data
- **App Control**: "Open Chrome", "Close Notepad"
- **Media**: "Play Bohemian Rhapsody"
- **Image Generation**: "Generate image of a sunset"
- **Automation**: "Set reminder for 3 PM meeting"
- **System Control**: "Mute system", "Volume up"
- **Content Creation**: "Write an email to my boss"

### API Endpoints

- `GET /api/status` - Get assistant status
- `GET /api/chat` - Retrieve chat history
- `POST /api/send` - Send message to assistant
- `GET /api/stats` - Get conversation statistics

## Configuration

### Environment Variables
- `Username`: Your name for personalization
- `Assistantname`: Name of the assistant (default: GROIT)
- `GroqAPIkey`: API key for Groq AI services
- `CohereAPIkey`: API key for Cohere AI services

### Data Storage
The application stores data in the `Data/` directory:
- `ChatLog.json`: Conversation history
- `Status.data`: Current assistant status
- `UserInput.data`: User input buffer
- `Responses.data`: AI responses

## Architecture

### Backend Modules

1. **Model.py**: Decision-Making Model
   - Classifies user queries into categories
   - Routes requests to appropriate handlers

2. **Chatbot.py**: AI Conversation
   - Handles general conversational queries
   - Integrates with Groq API

3. **SpeechToText.py**: Voice Input
   - Converts speech to text using SpeechRecognition
   - Supports multiple audio sources

4. **TextToSpeech.py**: Voice Output
   - Generates speech from text using edge-tts
   - Plays audio using pygame

5. **RealtimeSearchEngine.py**: Web Search
   - Performs Google and YouTube searches
   - Returns formatted search results

6. **Automation.py**: System Control
   - Manages application opening/closing
   - Handles system-level tasks

7. **ImageGeneration.py**: AI Images
   - Generates images from text prompts
   - Integrates with AI image generation APIs

8. **Extraction.py**: Data Processing
   - Extracts and processes web content
   - Handles data parsing tasks

### Frontend Interfaces

- **Desktop GUI**: PyQt6-based native application
- **Web App**: React-based responsive web interface
- **API Bridge**: Flask REST API for communication

## Dependencies

### Python Packages
- `groq`: AI language model API
- `cohere`: Alternative AI API
- `PyQt6`: Desktop GUI framework
- `SpeechRecognition`: Voice input processing
- `edge-tts`: Text-to-speech synthesis
- `selenium`: Web automation
- `beautifulsoup4`: HTML parsing
- `requests`: HTTP client
- `python-dotenv`: Environment management

### Web Dependencies
- `react`: UI framework
- `axios`: HTTP client for API calls
- `framer-motion`: Animation library
- `lucide-react`: Icon library
- `react-router-dom`: Client-side routing

## Development

### Adding New Features
1. Create new module in `Backend/`
2. Update `Model.py` for query classification
3. Integrate with main application in `Main.py`
4. Add API endpoints in `api_bridge.py` if needed
5. Update frontend interfaces

### Testing
```bash
# Run backend tests
python -m pytest

# Run frontend tests
cd web-frontend
npm test
```

### Building
```bash
# Build web frontend
cd web-frontend
npm run dev

# Create executable (using PyInstaller)
pyinstaller --onefile Main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


## Acknowledgments

- Built with Groq and Cohere AI APIs
- Uses various open-source libraries
- Inspired by modern AI assistant architectures</content>
