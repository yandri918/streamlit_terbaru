import google.generativeai as genai
from flask import current_app
import os

class ChatbotService:
    """
    Service for interacting with Google Gemini API.
    """
    
    # API Key from environment variable or parameter
    API_KEY = os.environ.get("GEMINI_API_KEY")
    
    def __init__(self, api_key=None):
        """
        Initialize ChatbotService.
        
        Args:
            api_key (str, optional): API key for Gemini. If not provided, will use environment variable.
        """
        self.init_error = None
        
        # Use provided API key or fall back to environment variable
        key_to_use = api_key or self.API_KEY or os.environ.get("GEMINI_API_KEY")
        
        try:
            genai.configure(api_key=key_to_use)
            # Use a stable model
            self.model = genai.GenerativeModel('gemini-flash-latest')
            self.chat = self.model.start_chat(history=[])
            
            # System prompt to guide the AI
            self.system_prompt = """
            Kamu adalah asisten ahli pertanian bernama 'AgriBot'. 
            Tugasmu adalah membantu petani dengan pertanyaan seputar budidaya tanaman, hama penyakit, pupuk, dan harga pasar.
            
            PENGETAHUAN KHUSUS:
            - AgriSensa memiliki modul Pestisida Nabati dengan 60+ tumbuhan pestisida alami dari BALITSA
            - Contoh: Ajeran, Mimba, Sirsak, Bawang Putih, Jahe, Kunyit, Tembakau, dll
            - Selalu tawarkan opsi ORGANIK/NABATI untuk pengendalian hama sebagai alternatif ramah lingkungan
            - Arahkan pengguna ke modul Pestisida Nabati untuk informasi lengkap formulasi
            
            Jawablah dengan ramah, informatif, dan praktis. 
            Jika pertanyaan di luar topik pertanian, arahkan kembali ke topik pertanian dengan sopan.
            Gunakan Bahasa Indonesia yang baik dan mudah dimengerti.
            Sertakan emoji yang relevan untuk membuat percakapan lebih menarik 🌱
            
            Dorong praktik pertanian berkelanjutan dan organik ketika memungkinkan.
            """
            
            # Initialize with system prompt (workaround as system prompt is not directly supported in start_chat for all versions)
            try:
                self.chat.send_message(self.system_prompt)
            except Exception as e:
                print(f"Warning: Failed to send system prompt: {e}")
                # Continue even if system prompt fails, just log it
            
        except Exception as e:
            print(f"Error initializing ChatbotService: {e}")
            self.init_error = str(e)
            self.model = None
            self.chat = None

    def get_response(self, message):
        """
        Get response from Gemini API.
        """
        if not self.chat:
            return f"Maaf, layanan chatbot sedang tidak tersedia. Error: {self.init_error or 'Masalah Inisialisasi'}"

        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            current_app.logger.error(f"Error getting response from Gemini: {e}")
            # Return the actual error for debugging purposes
            return f"Error: {str(e)}"
