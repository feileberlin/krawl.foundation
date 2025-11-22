#!/usr/bin/env python3
"""
Voice Transcriber using VOSK Speech Recognition
Converts Telegram voice messages (.ogg) to text transcription

Supports:
- German (deu)
- English (eng)
- Multi-language audio

Dependencies:
- vosk>=0.3.45
- pydub (for audio conversion)
- ffmpeg (system package)
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional

try:
    from vosk import Model, KaldiRecognizer, SetLogLevel
    from pydub import AudioSegment
except ImportError:
    print("❌ Fehlende Dependencies!")
    print("Installation:")
    print("  pip install vosk pydub")
    print("  sudo apt-get install ffmpeg")
    sys.exit(1)

# Suppress VOSK debug output
SetLogLevel(-1)

# Model URLs (small models for faster processing)
VOSK_MODELS = {
    'de': 'https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip',
    'en': 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip',
}

DEFAULT_MODEL = 'de'  # German default for krawl.foundation


class VoiceTranscriber:
    """VOSK-based voice transcription."""
    
    def __init__(self, model_path: Optional[Path] = None, language: str = DEFAULT_MODEL):
        """
        Initialize transcriber with VOSK model.
        
        Args:
            model_path: Path to VOSK model directory
            language: Language code ('de' or 'en')
        """
        self.language = language
        
        # Auto-detect or download model
        if model_path is None:
            model_path = self._get_or_download_model(language)
        
        self.model_path = Path(model_path)
        
        if not self.model_path.exists():
            raise FileNotFoundError(f"VOSK model not found: {self.model_path}")
        
        print(f"🔊 Loading VOSK model: {self.model_path}")
        self.model = Model(str(self.model_path))
        print("✅ Model loaded")
    
    def _get_or_download_model(self, language: str) -> Path:
        """
        Get model path or download if not exists.
        
        Args:
            language: Language code
            
        Returns:
            Path to model directory
        """
        # Check common model locations
        model_dirs = [
            Path.home() / '.cache' / 'vosk' / f'model-{language}',
            Path('/usr/share/vosk/models') / f'model-{language}',
            Path.cwd() / 'models' / f'vosk-model-{language}',
        ]
        
        for model_dir in model_dirs:
            if model_dir.exists() and (model_dir / 'am').exists():
                return model_dir
        
        # Download model
        print(f"📥 VOSK model not found locally. Download required.")
        print(f"Language: {language}")
        print(f"URL: {VOSK_MODELS.get(language, 'Unknown')}")
        print("")
        print("Manual download:")
        print(f"  wget {VOSK_MODELS.get(language, 'N/A')}")
        print(f"  unzip vosk-model-*.zip -d ~/.cache/vosk/model-{language}")
        print("")
        raise FileNotFoundError(
            f"VOSK model for '{language}' not found. "
            f"Download from: {VOSK_MODELS.get(language, 'N/A')}"
        )
    
    def convert_ogg_to_wav(self, ogg_path: Path) -> Path:
        """
        Convert Telegram .ogg to .wav for VOSK.
        
        Args:
            ogg_path: Path to .ogg file
            
        Returns:
            Path to converted .wav file
        """
        wav_path = ogg_path.with_suffix('.wav')
        
        if wav_path.exists():
            print(f"✓ WAV already exists: {wav_path}")
            return wav_path
        
        print(f"🔄 Converting {ogg_path.name} to WAV...")
        
        audio = AudioSegment.from_ogg(ogg_path)
        
        # VOSK requires 16kHz mono
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        audio.export(str(wav_path), format='wav')
        print(f"✓ Converted: {wav_path}")
        
        return wav_path
    
    def transcribe(self, audio_path: Path) -> dict:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file (.ogg or .wav)
            
        Returns:
            Transcription result dict with 'text', 'confidence', etc.
        """
        audio_path = Path(audio_path)
        
        # Convert OGG to WAV if needed
        if audio_path.suffix.lower() == '.ogg':
            audio_path = self.convert_ogg_to_wav(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"🎤 Transcribing: {audio_path.name}")
        
        # Initialize recognizer
        recognizer = KaldiRecognizer(self.model, 16000)
        recognizer.SetWords(True)  # Enable word-level timestamps
        
        # Process audio
        with open(audio_path, 'rb') as audio_file:
            while True:
                data = audio_file.read(4000)
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)
        
        # Get final result
        result = json.loads(recognizer.FinalResult())
        
        text = result.get('text', '').strip()
        
        if not text:
            print("⚠️ No speech detected or transcription failed")
            return {
                'text': '',
                'confidence': 0.0,
                'language': self.language,
                'result': result
            }
        
        print(f"✓ Transcribed: {text[:100]}...")
        
        return {
            'text': text,
            'confidence': self._calculate_confidence(result),
            'language': self.language,
            'result': result
        }
    
    def _calculate_confidence(self, result: dict) -> float:
        """
        Calculate average confidence from word-level results.
        
        Args:
            result: VOSK result dict
            
        Returns:
            Average confidence (0.0-1.0)
        """
        if 'result' in result and result['result']:
            confidences = [word.get('conf', 0.0) for word in result['result']]
            return sum(confidences) / len(confidences) if confidences else 0.0
        return 0.0


def main():
    """CLI for voice transcription."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Transcribe voice messages with VOSK"
    )
    parser.add_argument(
        'audio_file',
        help='Path to audio file (.ogg or .wav)'
    )
    parser.add_argument(
        '--language', '-l',
        default='de',
        choices=['de', 'en'],
        help='Language (default: de)'
    )
    parser.add_argument(
        '--model',
        help='Path to VOSK model directory'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output text file (default: stdout)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output JSON with metadata'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize transcriber
        transcriber = VoiceTranscriber(
            model_path=args.model,
            language=args.language
        )
        
        # Transcribe
        result = transcriber.transcribe(args.audio_file)
        
        # Output
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = result['text']
        
        if args.output:
            Path(args.output).write_text(output, encoding='utf-8')
            print(f"\n✅ Saved: {args.output}")
        else:
            print(f"\n📝 Transcription:\n{output}")
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
