import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# Mistral AI Configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

app = Flask(__name__)

def get_mistral_suggestions(symptoms, age):
    logger.info("\n🤖 Using Mistral AI API for this request...")
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        f"You are an AI health assistant. A patient reports the following symptoms: {symptoms}. "
        f"The patient's age is {age}. Format your response in two sections as shown below:\n\n"
        "IMPORTANT FORMATTING RULES:\n"
        "1. Use ONLY HTML tags for formatting - never use markdown\n"
        "2. Never use asterisks (**) for any formatting\n"
        "3. Use <strong>medication name</strong> for bold text\n"
        "4. Use <span style='color: #ff0000'>text</span> for side effects and warnings\n"
        "5. Use <br> for line breaks\n\n"
        "Start with a summary sentence:\n"
        "<p class='summary'>Providing suggestions for <strong>{symptoms}</strong> in a {age} year old patient.</p><br>\n\n"
        "SECTION 1 - MEDICATIONS:\n"
        "For each medication entry, provide:\n"
        "1. Name in <strong> tags\n"
        "2. Standard usage and dosage SPECIFICALLY for age {age}\n"
        "3. Side effects in red span tags\n"
        "<span style='color: #ff0000'>Note: These suggestions are specifically tailored for {age} years of age. Different dosages may apply for other age groups.</span><br><br>\n\n"
        "SECTION 2 - HOME REMEDIES:\n"
        "<h3>Home Remedies</h3>\n"
        "For each home remedy, provide:\n"
        "1. Name in <strong> tags\n"
        "2. Preparation time: X minutes\n"
        "3. Required ingredients with quantities\n"
        "4. Brief preparation method\n"
        "5. Usage instructions SPECIFICALLY for age {age}\n"
        "6. Any warnings in red span tags\n"
        "7. Source link for detailed information\n\n"
        "Example format for home remedy:\n"
        "<strong>Remedy Name</strong><br>\n"
        "Preparation Time: X minutes<br>\n"
        "Ingredients: List with quantities<br>\n"
        "Method: Brief preparation steps<br>\n"
        "Usage: Instructions for {age} years old<br>\n"
        "<span style='color: #ff0000'>Warnings: Any precautions specific to this age</span><br>\n"
        "To get detailed recipe: <a href='short_url' target='_blank'>: Brief source name</a><br><br>\n\n"
        "Remember:\n"
        "• Never use markdown asterisks (**)\n"
        "• Only HTML formatting is allowed\n"
        "• Only side effects and warnings should be in red text\n"
        "• All suggestions must be appropriate for {age} years of age\n"
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        logger.info("✅ Mistral AI request successful")
        return result['choices'][0]['message']['content'].replace("\n", "<br>").replace("**", "")
    except Exception as e:
        logger.error(f"❌ Mistral AI error: {str(e)}")
        raise Exception(f"Mistral API error: {str(e)}")

def get_medication_suggestions(symptoms, age):
    try:
        # Try Gemini first
        logger.info("\n🤖 Attempting to use Gemini API...")
        prompt = (
            f"You are an AI health assistant. A patient reports the following symptoms: {symptoms}. "
            f"The patient's age is {age}. Format your response in two sections as shown below:\n\n"
            "IMPORTANT FORMATTING RULES:\n"
            "1. Use ONLY HTML tags for formatting - never use markdown\n"
            "2. Never use asterisks (**) for any formatting\n"
            "3. Use <strong>medication name</strong> for bold text\n"
            "4. Use <span style='color: #ff0000'>text</span> for side effects and warnings\n"
            "5. Use <br> for line breaks\n\n"
            "Start with a summary sentence:\n"
            "<p class='summary'>Providing suggestions for <strong>{symptoms}</strong> in a {age} year old patient.</p><br>\n\n"
            "<div class='disclaimer-box'>\n"
            "<p><strong>Important Notice:</strong></p>\n"
            "<ul>\n"
            "<li>These suggestions are for informational purposes only</li>\n"
            "<li>Always consult a healthcare professional before taking any medication</li>\n"
            "<li>If symptoms persist or worsen, seek immediate medical attention</li>\n"
            "</ul>\n"
            "</div><br>\n\n"
            "SECTION 1 - MEDICATIONS:\n"
            "For each medication entry, provide:\n"
            "1. Name in <strong> tags\n"
            "2. Standard usage and dosage SPECIFICALLY for age {age}\n"
            "3. Side effects in red span tags\n"
            "<span style='color: #ff0000'>Note: These suggestions are specifically tailored for {age} years of age. Different dosages may apply for other age groups.</span><br><br>\n\n"
            "SECTION 2 - HOME REMEDIES:\n"
            "<h3>Home Remedies</h3>\n"
            "For each home remedy, provide:\n"
            "1. Name in <strong> tags\n"
            "2. Preparation time: X minutes\n"
            "3. Required ingredients with quantities\n"
            "4. Brief preparation method\n"
            "5. Usage instructions SPECIFICALLY for age {age}\n"
            "6. Any warnings in red span tags\n"
            "7. Source link for detailed information\n\n"
            "Example format for home remedy:\n"
            "<strong>Remedy Name</strong><br>\n"
            "Preparation Time: X minutes<br>\n"
            "Ingredients: List with quantities<br>\n"
            "Method: Brief preparation steps<br>\n"
            "Usage: Instructions for {age} years old<br>\n"
            "<span style='color: #ff0000'>Warnings: Any precautions specific to this age</span><br>\n"
            "To get detailed recipe: <a href='short_url' target='_blank'>: Brief source name</a><br><br>\n\n"
            "Remember:\n"
            "• Never use markdown asterisks (**)\n"
            "• Only HTML formatting is allowed\n"
            "• Only side effects and warnings should be in red text\n"
            "• All suggestions must be appropriate for {age} years of age\n"
        )
        
        response = model.generate_content(prompt)
        logger.info("✅ Gemini API request successful")
        return response.text.replace("\n", "<br>").replace("**", "")
    
    except Exception as gemini_error:
        logger.error(f"❌ Gemini API error: {str(gemini_error)}")
        logger.info("🔄 Falling back to Mistral AI...")
        try:
            # If Gemini fails, try Mistral
            return get_mistral_suggestions(symptoms, age)
        except Exception as mistral_error:
            # If both fail, raise the original Gemini error
            logger.error("❌ Both APIs failed!")
            raise Exception(f"Both APIs failed. Gemini error: {str(gemini_error)}. Mistral error: {str(mistral_error)}")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/medications", methods=["GET"])
def medications():
    return render_template("medications.html")

@app.route("/get_suggestions", methods=["POST"])
def get_suggestions():
    if request.is_json:
        try:
            data = request.get_json()
            symptoms = data.get("symptoms", "")
            age = data.get("age", "")
            
            if not symptoms:
                logger.error("❌ No symptoms provided")
                return jsonify({"error": "No symptoms provided"}), 400
            
            if not age:
                logger.error("❌ No age provided")
                return jsonify({"error": "No age provided"}), 400
            
            suggestions = get_medication_suggestions(symptoms, age)
            return jsonify({"suggestions": suggestions})
        
        except Exception as e:
            logger.error(f"❌ Error processing request: {str(e)}")
            return jsonify({"error": f"Error processing the request: {str(e)}"}), 500
    return jsonify({"error": "Request must be JSON"}), 400

@app.route("/health-monitoring")
def health_monitoring():
    return render_template("health_monitoring.html")

@app.route("/health-records")
def health_records():
    return render_template("health_records.html")

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    if request.is_json:
        try:
            data = request.get_json()
            feedback_type = data.get("type", "")  # helpful/not_helpful
            suggestion_id = data.get("suggestion_id", "")
            comment = data.get("comment", "")
            
            logger.info(f"✨ Feedback received - Type: {feedback_type}")
            # Here you can add code to store feedback in a database
            
            return jsonify({"message": "Thank you for your feedback!"}), 200
        except Exception as e:
            logger.error(f"❌ Error processing feedback: {str(e)}")
            return jsonify({"error": "Error processing feedback"}), 500
    return jsonify({"error": "Request must be JSON"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

