import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Google Cloud imports - DISABLED (using open-source alternatives)
GOOGLE_CLOUD_AVAILABLE = False

# Alternative imports for speech recognition and TTS
try:
    import speech_recognition as sr
    import pyttsx3
    ALTERNATIVE_SPEECH_AVAILABLE = True
except ImportError:
    ALTERNATIVE_SPEECH_AVAILABLE = False

# Open-source STT/TTS (preferred fallbacks)
try:
    from faster_whisper import WhisperModel  # Fast, local Whisper
    WHISPER_AVAILABLE = True
except Exception as e:
    logging.warning(f"Whisper (faster-whisper) not available: {e}")
    WHISPER_AVAILABLE = False

try:
    from gtts import gTTS  # Free online TTS (supports Malayalam)
    GTTS_AVAILABLE = True
except Exception as e:
    logging.warning(f"gTTS not available: {e}")
    GTTS_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class GoogleAPIs:
    """Speech utilities using open-source components (Whisper STT, gTTS/pyttsx3 TTS)."""
    
    def __init__(self):
        self.recognizer = None
        self.tts_engine = None
        self.whisper_model = None  # Lazy-initialize
        
        # Initialize alternative speech APIs
        if ALTERNATIVE_SPEECH_AVAILABLE:
            self._init_alternative_speech_apis()
    
    # Google Cloud APIs removed - using open-source alternatives only
    
    def _init_alternative_speech_apis(self):
        """Initialize alternative speech recognition and TTS"""
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            logger.info("Alternative speech recognition initialized")
            
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.8)  # Volume level
            logger.info("Alternative TTS engine initialized")
            
        except Exception as e:
            logger.warning(f"Failed to initialize alternative speech APIs: {e}")
            self.recognizer = None
            self.tts_engine = None
    
    def speech_to_text(self, audio_file_path: str, language_code: str = "en-US") -> Dict[str, Any]:
        """
        Convert speech to text using Whisper (primary) or speech_recognition (fallback)
        
        Args:
            audio_file_path: Path to audio file
            language_code: Language code (e.g., 'en-US' for English, 'ml-IN' for Malayalam)
            
        Returns:
            Dict with transcription result and confidence
        """
        try:
            # Preferred order: Whisper → speech_recognition
            if WHISPER_AVAILABLE and os.path.exists(audio_file_path):
                return self._whisper_speech_to_text(audio_file_path, language_code)
            elif self.recognizer and os.path.exists(audio_file_path):
                # Use alternative speech recognition
                return self._alternative_speech_to_text(audio_file_path, language_code)
            else:
                return {
                    "success": False,
                    "error": "Speech-to-text not available or file not found",
                    "transcription": "",
                    "confidence": 0.0
                }
                
        except Exception as e:
            logger.error(f"Speech-to-text error: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcription": "",
                "confidence": 0.0
            }

    def _whisper_speech_to_text(self, audio_file_path: str, language_code: str) -> Dict[str, Any]:
        """Use faster-whisper (local Whisper) for STT"""
        try:
            # Map BCP-47 to Whisper codes
            lang_map = {
                "hi-IN": "hi",
                "en-US": "en",
                "en": "en",
                "ml-IN": "ml",
                "ml": "ml",
                "bn-IN": "bn",
                "ta-IN": "ta",
                "te-IN": "te",
                "mr-IN": "mr",
                "gu-IN": "gu",
                "kn-IN": "kn",
                "pa-IN": "pa",
            }
            whisper_lang = lang_map.get(language_code, "en")

            # Lazy load a small/fast model for server use
            if self.whisper_model is None:
                # "small" is a good balance for CPU; use "tiny" for lowest latency
                self.whisper_model = WhisperModel("small")
                logger.info("Whisper model (small) initialized")

            segments, info = self.whisper_model.transcribe(
                audio_file_path,
                language=whisper_lang,
                vad_filter=True,
                beam_size=1
            )
            text = "".join(seg.text for seg in segments).strip()

            return {
                "success": True,
                "transcription": text,
                "confidence": 0.0,  # faster-whisper doesn't provide a single confidence score
                "language_code": language_code,
                "method": "whisper"
            }
        except Exception as e:
            logger.warning(f"Whisper STT failed: {e}, falling back")
            # Fallback to speech_recognition
            if self.recognizer and os.path.exists(audio_file_path):
                return self._alternative_speech_to_text(audio_file_path, language_code)
            return {
                "success": False,
                "error": str(e),
                "transcription": "",
                "confidence": 0.0
            }
    
    # Google Cloud Speech-to-Text removed - using Whisper instead
    
    def _alternative_speech_to_text(self, audio_file_path: str, language_code: str) -> Dict[str, Any]:
        """Use alternative speech recognition"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            # Map language codes to recognizer languages
            lang_map = {
                "hi-IN": "hi-IN",  # Hindi
                "en-US": "en-US",  # English
                "bn-IN": "bn-BD",  # Bengali
                "ta-IN": "ta-IN",  # Tamil
                "te-IN": "te-IN",  # Telugu
                "mr-IN": "mr-IN",  # Marathi
                "gu-IN": "gu-IN",  # Gujarati
                "kn-IN": "kn-IN",  # Kannada
                "ml-IN": "ml-IN",  # Malayalam
                "pa-IN": "pa-IN",  # Punjabi
            }
            
            recognizer_lang = lang_map.get(language_code, "en-US")
            
            transcription = self.recognizer.recognize_google(audio, language=recognizer_lang)
            
            return {
                "success": True,
                "transcription": transcription,
                "confidence": 0.8,  # Alternative APIs don't provide confidence
                "language_code": language_code,
                "method": "alternative"
            }
            
        except sr.UnknownValueError:
            return {
                "success": False,
                "error": "Could not understand audio",
                "transcription": "",
                "confidence": 0.0
            }
        except Exception as e:
            logger.error(f"Alternative speech-to-text error: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcription": "",
                "confidence": 0.0
            }
    
    def translate_text(self, text: str, target_language: str = "en", source_language: str = None) -> Dict[str, Any]:
        """
        Simple translation placeholder (Google Translate removed)
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code
            
        Returns:
            Dict with translation result (returns original text for now)
        """
        # For now, return original text (can be enhanced with free translation APIs later)
        return {
            "success": True,
            "translated_text": text,
            "source_language": source_language or "unknown",
            "target_language": target_language,
            "original_text": text,
            "method": "no_translation"
        }
    
    def _google_translate(self, text: str, target_language: str, source_language: str = None) -> Dict[str, Any]:
        """Use Google Cloud Translation API"""
        try:
            if source_language:
                result = self.translate_client.translate(
                    text, 
                    target_language=target_language,
                    source_language=source_language
                )
            else:
                result = self.translate_client.translate(text, target_language=target_language)
            
            return {
                "success": True,
                "translated_text": result['translatedText'],
                "source_language": result.get('detectedSourceLanguage', source_language),
                "target_language": target_language,
                "original_text": text
            }
            
        except Exception as e:
            logger.error(f"Google Translation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "translated_text": text,
                "detected_language": source_language or "unknown"
            }
    
    def text_to_speech(self, text: str, output_file: str = None, language_code: str = "hi-IN", 
                      voice_name: str = None) -> Dict[str, Any]:
        """
        Convert text to speech using Google Text-to-Speech API
        
        Args:
            text: Text to convert to speech
            output_file: Output audio file path (optional)
            language_code: Language code (e.g., 'hi-IN' for Hindi)
            voice_name: Specific voice name (optional)
            
        Returns:
            Dict with audio file path and success status
        """
        try:
            # Preferred order: gTTS → Google Cloud → pyttsx3
            if GTTS_AVAILABLE:
                return self._gtts_text_to_speech(text, output_file, language_code)
            if self.tts_client:
                # Use Google Cloud Text-to-Speech
                return self._google_text_to_speech(text, output_file, language_code, voice_name)
            elif self.tts_engine:
                # Use alternative TTS
                return self._alternative_text_to_speech(text, output_file, language_code)
            else:
                return {
                    "success": False,
                    "error": "Text-to-speech not available",
                    "audio_file": None
                }
                
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_file": None
            }

    def _gtts_text_to_speech(self, text: str, output_file: str, language_code: str) -> Dict[str, Any]:
        """Use gTTS (online, free) for TTS. Supports Malayalam (ml)."""
        try:
            if not output_file:
                output_file = f"output_{language_code}.mp3"

            # Map to gTTS language tags
            lang_map = {
                "hi-IN": "hi",
                "en-US": "en",
                "en": "en",
                "ml-IN": "ml",
                "ml": "ml",
                "bn-IN": "bn",
                "ta-IN": "ta",
                "te-IN": "te",
                "mr-IN": "mr",
                "gu-IN": "gu",
                "kn-IN": "kn",
                "pa-IN": "pa",
            }
            gtts_lang = lang_map.get(language_code, "en")

            tts = gTTS(text=text, lang=gtts_lang)
            tts.save(output_file)

            return {
                "success": True,
                "audio_file": output_file,
                "language_code": language_code,
                "text_length": len(text),
                "method": "gtts"
            }
        except Exception as e:
            logger.warning(f"gTTS failed: {e}, falling back")
            if self.tts_client:
                return self._google_text_to_speech(text, output_file, language_code, None)
            if self.tts_engine:
                return self._alternative_text_to_speech(text, output_file, language_code)
            return {"success": False, "error": str(e), "audio_file": None}
    
    def _google_text_to_speech(self, text: str, output_file: str, language_code: str, voice_name: str) -> Dict[str, Any]:
        """Use Google Cloud Text-to-Speech API"""
        try:
            if not output_file:
                output_file = f"output_{language_code}.wav"
            
            # Configure voice
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name or self._get_default_voice(language_code),
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )
            
            # Configure audio
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
            )
            
            # Generate speech
            synthesis_input = texttospeech.SynthesisInput(text=text)
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Save audio file
            with open(output_file, "wb") as out:
                out.write(response.audio_content)
            
            return {
                "success": True,
                "audio_file": output_file,
                "language_code": language_code,
                "text_length": len(text)
            }
            
        except Exception as e:
            logger.error(f"Google Text-to-Speech error: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_file": None
            }
    
    def _alternative_text_to_speech(self, text: str, output_file: str, language_code: str) -> Dict[str, Any]:
        """Use alternative text-to-speech"""
        try:
            if not output_file:
                output_file = f"output_{language_code}.wav"
            
            # Configure voice based on language
            voices = self.tts_engine.getProperty('voices')
            
            # Try to find a voice for the language
            for voice in voices:
                if language_code.startswith(voice.id[:2]):
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            # Save to file
            self.tts_engine.save_to_file(text, output_file)
            self.tts_engine.runAndWait()
            
            return {
                "success": True,
                "audio_file": output_file,
                "language_code": language_code,
                "text_length": len(text),
                "method": "alternative"
            }
            
        except Exception as e:
            logger.error(f"Alternative Text-to-Speech error: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_file": None
            }
    
    def _get_default_voice(self, language_code: str) -> str:
        """Get default voice for language code"""
        voice_map = {
            "hi-IN": "hi-IN-Wavenet-A",  # Hindi
            "en-US": "en-US-Wavenet-D",  # English
            "bn-IN": "bn-IN-Wavenet-A",  # Bengali
            "ta-IN": "ta-IN-Wavenet-A",  # Tamil
            "te-IN": "te-IN-Wavenet-A",  # Telugu
            "mr-IN": "mr-IN-Wavenet-A",  # Marathi
            "gu-IN": "gu-IN-Wavenet-A",  # Gujarati
            "kn-IN": "kn-IN-Wavenet-A",  # Kannada
            "ml-IN": "ml-IN-Wavenet-A",  # Malayalam
            "pa-IN": "pa-IN-Wavenet-A",  # Punjabi
        }
        return voice_map.get(language_code, "en-US-Wavenet-D")
    
    def process_voice_query(self, audio_file_path: str, source_language: str = "hi-IN") -> Dict[str, Any]:
        """
        Complete voice processing pipeline: Speech-to-Text -> Translation -> English text
        
        Args:
            audio_file_path: Path to audio file
            source_language: Source language code
            
        Returns:
            Dict with processed results
        """
        try:
            # Step 1: Speech to Text
            stt_result = self.speech_to_text(audio_file_path, source_language)
            
            if not stt_result["success"]:
                return stt_result
            
            original_text = stt_result["transcription"]
            
            # Step 2: Translate to English (if not already English)
            if source_language.startswith("en"):
                translated_text = original_text
                translation_success = True
            else:
                translation_result = self.translate_text(original_text, "en", source_language)
                translated_text = translation_result["translated_text"]
                translation_success = translation_result["success"]
            
            return {
                "success": True,
                "original_text": original_text,
                "translated_text": translated_text,
                "source_language": source_language,
                "translation_success": translation_success,
                "confidence": stt_result.get("confidence", 0.0)
            }
            
        except Exception as e:
            logger.error(f"Voice processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_text": "",
                "translated_text": ""
            }
    
    def process_response_to_speech(self, text: str, target_language: str = "hi-IN") -> Dict[str, Any]:
        """
        Convert response text to speech in target language
        
        Args:
            text: Response text in English
            target_language: Target language code
            
        Returns:
            Dict with audio file and processing results
        """
        try:
            # Translate to target language if needed
            if not target_language.startswith("en"):
                translation_result = self.translate_text(text, target_language, "en")
                if translation_result["success"]:
                    text = translation_result["translated_text"]
                else:
                    logger.warning("Translation failed, using original text")
            
            # Convert to speech
            tts_result = self.text_to_speech(text, language_code=target_language)
            
            return {
                "success": tts_result["success"],
                "audio_file": tts_result.get("audio_file"),
                "translated_text": text,
                "target_language": target_language,
                "error": tts_result.get("error")
            }
            
        except Exception as e:
            logger.error(f"Response to speech processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_file": None
            }

def main():
    """Test the Google APIs integration"""
    print("=== Google APIs Test ===\n")
    
    try:
        google_apis = GoogleAPIs()
        
        print("Available services:")
        print(f"  Google Cloud Speech-to-Text: {google_apis.speech_client is not None}")
        print(f"  Google Cloud Translation: {google_apis.translate_client is not None}")
        print(f"  Google Cloud Text-to-Speech: {google_apis.tts_client is not None}")
        print(f"  Alternative Speech Recognition: {google_apis.recognizer is not None}")
        print(f"  Alternative Text-to-Speech: {google_apis.tts_engine is not None}")
        print()
        
        # Test translation
        test_text = "Hello, how are you?"
        print(f"Testing translation: '{test_text}'")
        
        translation_result = google_apis.translate_text(test_text, "hi", "en")
        if translation_result["success"]:
            print(f"Hindi translation: {translation_result['translated_text']}")
        else:
            print(f"Translation failed: {translation_result['error']}")
        
        print("\nGoogle APIs integration test completed")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
