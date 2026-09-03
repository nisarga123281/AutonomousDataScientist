from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

# Create Gemini client
client = genai.Client()

# Send request
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Hello! Introduce yourself as the AI brain of AutoDS."
)

print("\n========== GEMINI RESPONSE ==========\n")
print(response.text)