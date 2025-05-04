# ArogyaAI: Your Personal Health Companion

![ArogyaAI Logo](image.png)

## Overview

ArogyaAI is an AI-powered health assistant application that provides personalized medication suggestions and health guidance based on reported symptoms and age. The system uses advanced AI models from Google Gemini and Mistral to generate reliable health-related information.

## Live Demo

Access the live application: [ArogyaAI - Your Personal Health Companion](https://ai-health-assistant-azns.onrender.com/)

## Features

- **Medication Suggestions**: Get personalized medication recommendations based on symptoms and age
- **Home Remedies**: Discover effective home treatments with preparation instructions
- **Health Monitoring**: Track vital signs and health metrics (Coming Soon)
- **Health Records**: Securely store and manage medical records (Coming Soon)

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Models**: 
  - Google Gemini 1.5 Pro 
  - Mistral Large (fallback)
- **API Integration**: RESTful API for AI services
- **Deployment**: Render

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/adhi982/AI_Health_Assistant.git
   cd AI_Health_Assistant
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the project root with:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   MISTRAL_API_KEY=your_mistral_api_key
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Access the application at `http://localhost:5000` in your web browser.

## Usage

1. Navigate to the Medication Suggestions tab
2. Enter your symptoms and age
3. Review the personalized medication suggestions and home remedies
4. Use the feedback system to help improve recommendations

## Important Disclaimers

- This application is for informational purposes only.
- Always consult a healthcare professional before starting any medication.
- If symptoms persist or worsen, seek immediate medical attention.
- Not a substitute for professional medical advice, diagnosis, or treatment.

## Project Structure

```
AI_Health_Assistant/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not tracked by git)
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
│   ├── index.html         # Landing page
│   ├── medications.html   # Medication suggestions page
│   ├── health_records.html    # Health records page (coming soon)
│   └── health_monitoring.html # Health monitoring page (coming soon)
└── venv/                  # Virtual environment (not tracked by git)
```

## Security and Privacy

ArogyaAI is designed with user privacy in mind:
- No personal health data is stored permanently
- API communications are secured with encryption
- No user authentication is required to use the basic features

## Contributors

- **Adithya N T** - [LinkedIn](https://www.linkedin.com/in/adithya982) | [Email](mailto:adithyant982@gmail.com)
- **Poorvi Pal** - [LinkedIn](https://www.linkedin.com/in/poorvi-pal09/) | [Email](mailto:poorvipalimpu28@gmail.com)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Icons from [Flaticon](https://www.flaticon.com/)
- Font Awesome for UI icons
- Google Gemini and Mistral AI for powering the recommendation engine 