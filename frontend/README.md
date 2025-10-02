# NLP Word Analyzer - Frontend

A beautiful Vue.js application with Vuetify (Material Design) for analyzing words using natural language processing.

## Features

- 🎨 **Beautiful Material Design UI** - Built with Vuetify 3
- 🌙 **Dark/Light Theme Toggle** - Seamless theme switching
- 📱 **Responsive Design** - Works perfectly on all devices
- ⚡ **Real-time Analysis** - Instant word analysis results
- 🎯 **Quick Examples** - Pre-loaded example words to try
- 📊 **Rich Visualizations** - Color-coded parts of speech and organized results
- 🔄 **API Health Monitoring** - Real-time backend connection status

## Technology Stack

- **Vue.js 3** - Progressive JavaScript framework
- **Vuetify 3** - Material Design component library
- **Axios** - HTTP client for API communication
- **Material Design Icons** - Comprehensive icon set

## Setup Instructions

1. **Install Node.js** (v16 or higher)

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run serve
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

The application will be available at `http://localhost:8080`

## Project Structure

```
src/
├── components/
│   ├── WordInput.vue      # Word input form with validation
│   └── AnalysisResult.vue # Results display component
├── services/
│   └── nlpService.js      # API communication service
├── plugins/
│   └── vuetify.js         # Vuetify configuration
├── App.vue                # Main application component
└── main.js                # Application entry point
```

## API Integration

The frontend communicates with the Python Flask backend at `http://localhost:5000/api`

### Available Endpoints:
- `POST /api/analyze` - Analyze a word
- `GET /api/health` - Check API health

## Features Overview

### 🔤 Word Analysis
Enter any word to get comprehensive linguistic information including:
- Part of speech identification
- Detailed definitions
- Synonyms and antonyms
- Example sentences

### 🎨 User Interface
- Clean, modern Material Design
- Intuitive card-based layout
- Smooth animations and transitions
- Color-coded information categories
- Responsive mobile-first design

### 🛠 Technical Features
- Real-time API status monitoring
- Error handling with user-friendly messages
- Loading states and progress indicators
- Keyboard navigation support
- Share functionality for results