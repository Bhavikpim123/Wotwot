import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from typing import Optional

# Create FastAPI app
app = FastAPI(title="WhatsApp CRM Backend", description="A simplified version for testing")

# Pydantic models for request/response
class MessageGenerationRequest(BaseModel):
    prompt: str
    messageType: str = "promotional"
    tone: str = "friendly"

class MessageGenerationResponse(BaseModel):
    message: str
    success: bool

# CORS middleware configuration - Railway deployment friendly
allowed_origins = [
    "http://localhost:8080", 
    "http://localhost:8081", 
    "http://localhost:8084",
    "https://*.vercel.app",  # Vercel domains
    "https://*.netlify.app", # Netlify domains
    "*"  # Allow all for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint to test if the server is running"""
    return {
        "message": "WhatsApp CRM Backend is running!",
        "status": "success",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Backend server is operational"
    }

@app.get("/api/test")
async def test_endpoint():
    """Test API endpoint"""
    return {
        "data": "This is a test endpoint",
        "api_version": "v1"
    }

@app.post("/api/generate-message", response_model=MessageGenerationResponse)
async def generate_message(request: MessageGenerationRequest):
    """Generate a message based on the given prompt"""
    
    # Message templates based on type and tone
    templates = {
        "promotional": {
            "friendly": [
                "Hi {name}! 🎉 {prompt_context} Get ready for amazing deals and offers just for you! Shop now and save big! 💰",
                "Hello {name}! ✨ {prompt_context} Don't miss out on our exclusive offers designed specially for valued customers like you! 🛍️",
                "Hey {name}! 🌟 {prompt_context} Treat yourself to something special with our fantastic deals! Limited time only! ⏰"
            ],
            "professional": [
                "Dear {name}, {prompt_context} We are pleased to offer you exclusive deals on our premium products. Visit our store today.",
                "Hello {name}, {prompt_context} Take advantage of our professional services with special pricing for valued clients.",
                "Dear Valued Customer, {prompt_context} We invite you to explore our latest offerings with attractive discounts."
            ]
        },
        "greeting": {
            "friendly": [
                "Hello {name}! 🎊 {prompt_context} Wishing you joy, happiness, and prosperity! May this celebration bring you countless blessings! ✨",
                "Hi {name}! 🌟 {prompt_context} Sending you warm wishes and heartfelt greetings! Have a wonderful celebration! 🎉",
                "Hey {name}! 💫 {prompt_context} May this special occasion fill your life with happiness and success! Celebrate with joy! 🎈"
            ],
            "formal": [
                "Dear {name}, {prompt_context} We extend our warmest greetings and best wishes on this auspicious occasion.",
                "Respected {name}, {prompt_context} May this celebration bring you peace, prosperity, and happiness.",
                "Dear Valued Customer, {prompt_context} We wish you and your family a joyous celebration filled with blessings."
            ]
        },
        "informational": {
            "professional": [
                "Dear {name}, {prompt_context} Please find the important information regarding your account/service.",
                "Hello {name}, {prompt_context} We wanted to keep you informed about the latest updates.",
                "Dear Customer, {prompt_context} Here's the information you requested about our services."
            ],
            "friendly": [
                "Hi {name}! 📢 {prompt_context} Just wanted to keep you in the loop with some important updates!",
                "Hello {name}! ℹ️ {prompt_context} Here's some useful information we thought you'd like to know!",
                "Hey {name}! 💡 {prompt_context} Quick update for you - hope this helps!"
            ]
        },
        "reminder": {
            "friendly": [
                "Hi {name}! ⏰ {prompt_context} Just a friendly reminder about your upcoming appointment/service!",
                "Hello {name}! 🔔 {prompt_context} Don't forget - we're here to help when you need us!",
                "Hey {name}! 📅 {prompt_context} Quick reminder to help you stay on track!"
            ],
            "professional": [
                "Dear {name}, {prompt_context} This is a gentle reminder regarding your scheduled service.",
                "Hello {name}, {prompt_context} Please be reminded of your upcoming appointment with us.",
                "Dear Customer, {prompt_context} We wanted to remind you about your pending service request."
            ]
        },
        "support": {
            "friendly": [
                "Hi {name}! 🤝 {prompt_context} We're here to help! Feel free to reach out if you need any assistance!",
                "Hello {name}! 💪 {prompt_context} Our support team is ready to assist you with anything you need!",
                "Hey {name}! 🌟 {prompt_context} Don't hesitate to contact us - we're always happy to help!"
            ],
            "professional": [
                "Dear {name}, {prompt_context} Our customer support team is available to assist you with your queries.",
                "Hello {name}, {prompt_context} Please contact our support team for any assistance you may require.",
                "Dear Valued Customer, {prompt_context} We are committed to providing you with excellent support."
            ]
        }
    }
    
    # Special handling for festive greetings
    festive_keywords = {
        "diwali": "May this Diwali illuminate your life with joy, prosperity, and happiness! 🪔 Wishing you and your loved ones a very Happy Diwali!",
        "christmas": "Merry Christmas, {name}! 🎄 May this festive season bring you peace, joy, and wonderful memories with family and friends!",
        "new year": "Happy New Year, {name}! 🎊 May this new year bring you success, happiness, and endless opportunities!",
        "holi": "Happy Holi, {name}! 🌈 May your life be filled with colors of joy, love, and happiness!",
        "eid": "Eid Mubarak, {name}! 🌙 May this blessed occasion bring peace, happiness, and prosperity to you and your family!",
        "birthday": "Happy Birthday, {name}! 🎂 Wishing you a day filled with joy and a year filled with success!"
    }
    
    # Check for festive keywords in prompt
    prompt_lower = request.prompt.lower()
    festive_message = None
    for keyword, message in festive_keywords.items():
        if keyword in prompt_lower:
            festive_message = message
            break
    
    # If it's a festive greeting, use the predefined message
    if festive_message and request.messageType == "greeting":
        generated_message = festive_message
    else:
        # Get appropriate template
        message_templates = templates.get(request.messageType, templates["promotional"])
        tone_templates = message_templates.get(request.tone, list(message_templates.values())[0])
        
        # Select a random template
        selected_template = random.choice(tone_templates)
        
        # Generate context from prompt
        context = request.prompt.strip()
        if not context.endswith('.') and not context.endswith('!'):
            context += '.'
        
        # Fill the template
        generated_message = selected_template.format(
            name="{name}",  # Keep placeholder for personalization
            prompt_context=context
        )
    
    return MessageGenerationResponse(
        message=generated_message,
        success=True
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)