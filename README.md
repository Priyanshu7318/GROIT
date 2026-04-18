# GROIT Web Frontend

The web interface for GROIT AI Assistant, built with Python , React and Vite.

## Features

- **Modern UI**: Clean, responsive interface with smooth animations
- **Real-time Communication**: Live chat with the AI assistant
- **Status Visualization**: Animated assistant status indicator
- **Voice Integration**: Voice input/output controls
- **Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Prerequisites
- Node.js 16+
- Running GROIT backend API on `http://localhost:5001`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open [http://localhost:5173](http://localhost:5173) in your browser

### Build for Production

```bash
npm run build
```

## API Integration

The frontend communicates with the GROIT backend via REST API:

- `GET /api/status` - Assistant status
- `GET /api/chat` - Chat history
- `POST /api/send` - Send messages
- `GET /api/stats` - Conversation statistics

## Technologies Used

- **React 19**: Modern React with hooks and concurrent features
- **Vite**: Fast build tool and development server
- **Framer Motion**: Smooth animations and transitions
- **Lucide React**: Beautiful icons
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication

## Project Structure

```
src/
├── App.jsx          # Main application component
├── index.css        # Global styles
├── App.css          # Component styles
└── assets/          # Static assets
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Adding New Features

1. Create new components in `src/`
2. Update routing in `App.jsx` if needed
3. Add API calls using axios
4. Style with CSS or add animations with Framer Motion

## Contributing

Follow the main GROIT project contribution guidelines.
