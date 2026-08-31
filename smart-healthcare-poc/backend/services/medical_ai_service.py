import requests
import config
import logging
import base64

logger = logging.getLogger(__name__)

class MedicalAIService:
    @staticmethod
    def analyze_medical_content(text: str = None, image_b64: str = None, mime_type: str = "image/jpeg"):
        if not config.NVIDIA_API_KEY:
            raise Exception("NVIDIA API is not configured")
            
        invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {config.NVIDIA_API_KEY}",
            "Accept": "application/json"
        }
        
        # System prompt ensuring medical scope and simple English formatting
        system_prompt = (
            "You are a medical assistant designed ONLY to help with understanding medical reports, "
            "explaining medical terminology, and summarizing provided medical documents in simple, easy-to-understand English for patients. "
            "You MUST NOT answer general knowledge, coding, politics, or any non-medical questions. "
            "If the user asks an unrelated question, reply EXACTLY with: 'This assistant is designed only to help with medical information and uploaded medical documents.' "
            "Do not make definitive diagnoses. Do not fabricate information. "
            "Format your response with clean markdown EXACTLY using these sections:\n\n"
            "Report Summary\n\n"
            "Overall\n"
            "[A simple explanation of the report in plain English]\n\n"
            "Key findings\n"
            "• [Finding 1]\n"
            "• [Finding 2]\n\n"
            "What the terms mean\n"
            "• [Term 1] — [Simple definition]\n"
            "• [Term 2] — [Simple definition]\n\n"
            "Questions to discuss with your doctor\n"
            "• [Question 1]\n"
            "• [Question 2]\n\n"
            "If the text is urgent/dangerous, advise immediate medical attention."
        )

        content = []
        if image_b64:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_b64}"
                }
            })
            
        user_text = "Please analyze this medical document."
        if text:
            user_text = text
            
        content.append({
            "type": "text",
            "text": user_text
        })

        payload = {
            "model": config.NVIDIA_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            "max_tokens": 1024,
            "temperature": 0.2,
            "top_p": 0.9,
            "stream": False
        }

        try:
            response = requests.post(invoke_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"NVIDIA API Error: {e}")
            raise Exception("Failed to process the document with AI")

