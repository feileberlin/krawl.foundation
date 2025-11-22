#!/usr/bin/env python3
"""
Image Stream Extractor - Batch OCR für Event-Flyer

Workflow (Option A - Batch Processing):
1. Lade Bilder von Instagram/Facebook oder lokalen Dateien
2. Führe OCR auf allen Bildern aus (Batch-Modus)
3. Extrahiere Daten und erstelle Event-Drafts automatisch
4. Keine User-Interaktion während Verarbeitung

Use Cases:
- Telegram Bot: Batch-Verarbeitung hochgeladener Flyer
- GitHub Actions: Automatische OCR-Pipeline
- CLI: Manueller Batch-Scan von Flyern

Dependencies:
- pillow (Bildverarbeitung)
- pytesseract (OCR)
"""

import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests


class ImageStreamExtractor:
    """Extract event info from social media images with OCR - Batch mode."""

    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path(".cache/images")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Check OCR availability
        self.has_ocr = self._check_ocr()

    def _check_ocr(self) -> bool:
        """Check if OCR is available."""
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            return True
        except:
            return False

    def fetch_instagram_images(
        self, profile: str, count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent images from Instagram profile.

        Args:
            profile: Instagram username
            count: Number of recent posts

        Returns:
            List of image data dicts
        """
        images = []

        try:
            import instaloader

            L = instaloader.Instaloader(
                download_pictures=True,
                download_videos=False,
                download_comments=False,
                save_metadata=False,
            )

            profile_obj = instaloader.Profile.from_username(L.context, profile)

            print(f"📸 Lade {count} neueste Bilder von @{profile}...")

            for i, post in enumerate(profile_obj.get_posts()):
                if i >= count:
                    break

                # Download image
                image_path = self.cache_dir / f"{profile}_{post.shortcode}.jpg"

                if not image_path.exists():
                    response = requests.get(post.url)
                    with open(image_path, "wb") as f:
                        f.write(response.content)

                images.append(
                    {
                        "source": "instagram",
                        "profile": profile,
                        "image_path": image_path,
                        "url": f"https://www.instagram.com/p/{post.shortcode}/",
                        "caption": post.caption or "",
                        "alt_text": post.accessibility_caption or "",
                        "date": post.date_local,
                        "shortcode": post.shortcode,
                    }
                )

                print(f"  ✓ {i+1}/{count}: {post.shortcode}")

        except ImportError:
            print("⚠️  Instaloader nicht installiert: pip install instaloader")
        except Exception as e:
            print(f"Fehler beim Laden von Instagram: {e}")

        return images

    def fetch_facebook_images(
        self, page_id: str, count: int = 5, access_token: str = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent images from Facebook page.

        Args:
            page_id: Facebook page ID or username
            count: Number of recent posts
            access_token: Facebook API token (optional)

        Returns:
            List of image data dicts
        """
        images = []

        if not access_token:
            print("⚠️  Facebook API Token fehlt - siehe README für Setup")
            return images

        try:
            api_url = f"https://graph.facebook.com/v18.0/{page_id}/photos/uploaded"

            params = {
                "access_token": access_token,
                "fields": "id,images,alt_text,name,created_time,link",
                "limit": count,
            }

            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            for photo in data.get("data", []):
                # Get highest resolution image
                image_url = photo.get("images", [{}])[0].get("source", "")

                if image_url:
                    # Download
                    image_path = self.cache_dir / f"fb_{photo['id']}.jpg"

                    if not image_path.exists():
                        img_response = requests.get(image_url)
                        with open(image_path, "wb") as f:
                            f.write(img_response.content)

                    images.append(
                        {
                            "source": "facebook",
                            "page_id": page_id,
                            "image_path": image_path,
                            "url": photo.get("link", ""),
                            "caption": photo.get("name", ""),
                            "alt_text": photo.get("alt_text", ""),
                            "date": photo.get("created_time", ""),
                            "photo_id": photo["id"],
                        }
                    )

        except Exception as e:
            print(f"Fehler beim Laden von Facebook: {e}")

        return images

    def load_local_images(
        self, path: str, recursive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Load images from local directory or file.

        Args:
            path: File path or directory path
            recursive: Search subdirectories recursively

        Returns:
            List of image data dicts
        """
        images = []
        local_path = Path(path).expanduser().resolve()

        # Supported image formats
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}

        if not local_path.exists():
            print(f"❌ Pfad existiert nicht: {local_path}")
            return images

        # Single file
        if local_path.is_file():
            if local_path.suffix.lower() in image_extensions:
                images.append(self._create_local_image_data(local_path))
            else:
                print(f"⚠️  Keine unterstützte Bilddatei: {local_path.suffix}")
            return images

        # Directory
        if local_path.is_dir():
            print(f"📂 Scanne Verzeichnis: {local_path}")
            
            if recursive:
                # Recursive search
                for ext in image_extensions:
                    images.extend([
                        self._create_local_image_data(p)
                        for p in local_path.rglob(f"*{ext}")
                    ])
                    images.extend([
                        self._create_local_image_data(p)
                        for p in local_path.rglob(f"*{ext.upper()}")
                    ])
            else:
                # Non-recursive
                for ext in image_extensions:
                    images.extend([
                        self._create_local_image_data(p)
                        for p in local_path.glob(f"*{ext}")
                    ])
                    images.extend([
                        self._create_local_image_data(p)
                        for p in local_path.glob(f"*{ext.upper()}")
                    ])

            # Sort by modification time (newest first)
            images.sort(key=lambda x: x['mtime'], reverse=True)

            print(f"✓ {len(images)} Bilder gefunden")

        return images

    def _create_local_image_data(self, image_path: Path) -> Dict[str, Any]:
        """
        Create image data dict for local file.

        Args:
            image_path: Path to local image

        Returns:
            Image data dict
        """
        stat = image_path.stat()
        
        return {
            "source": "local",
            "profile": str(image_path.parent),
            "image_path": image_path,
            "url": f"file://{image_path.absolute()}",
            "caption": "",
            "alt_text": "",
            "date": datetime.fromtimestamp(stat.st_mtime),
            "mtime": stat.st_mtime,
            "filename": image_path.name,
            "size": stat.st_size,
        }

    def extract_text_from_image(self, image_path: Path) -> str:
        """
        Extract text from image using OCR.

        Args:
            image_path: Path to image file

        Returns:
            Extracted text
        """
        if not self.has_ocr:
            return "[OCR nicht verfügbar - installiere: apt-get install tesseract-ocr && pip install pytesseract]"

        try:
            import pytesseract
            from PIL import Image

            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang="deu+eng")
            return text.strip()

        except Exception as e:
            return f"[OCR Fehler: {e}]"

    def batch_ocr(
        self, 
        images: List[Dict[str, Any]], 
        output_json: Optional[Path] = None
    ) -> List[Dict[str, Any]]:
        """
        Batch OCR processing for multiple images - non-interactive.
        
        Args:
            images: List of image data dicts
            output_json: Optional path to save results as JSON
            
        Returns:
            List of event drafts with OCR data
        """
        if not self.has_ocr:
            print("❌ OCR nicht verfügbar!")
            return []
        
        events = []
        total = len(images)
        
        print(f"\n🔍 Batch OCR: {total} Bilder werden verarbeitet...\n")
        
        for i, image_data in enumerate(images, 1):
            image_path = image_data["image_path"]
            print(f"[{i}/{total}] {image_path.name}... ", end="", flush=True)
            
            try:
                # Extract OCR text
                ocr_text = self.extract_text_from_image(image_path)
                
                # Create event draft with OCR data
                event = self._create_event_draft(image_data, ocr_text)
                events.append(event)
                
                print(f"✓ ({len(ocr_text)} chars)")
                
            except Exception as e:
                print(f"✗ Fehler: {e}")
                # Create minimal draft even on error
                event = self._create_event_draft(image_data, "")
                event['ocr_error'] = str(e)
                events.append(event)
        
        print(f"\n✅ {len(events)} Drafts erstellt")
        
        # Save to JSON if requested
        if output_json:
            output_json = Path(output_json)
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False, default=str)
            print(f"💾 Gespeichert: {output_json}")
        
        return events

    def _create_event_draft(
        self, 
        image_data: Dict[str, Any], 
        ocr_text: str
    ) -> Dict[str, Any]:
        """
        Create event draft from image data and OCR text.
        
        Args:
            image_data: Image metadata
            ocr_text: Extracted OCR text
            
        Returns:
            Event draft dict
        """
        # Basic template
        draft = {
            "status": "draft",
            "source": image_data["source"],
            "created_at": datetime.now().isoformat(),
            "image_file": str(image_data["image_path"]),
            "ocr_text": ocr_text,
            "needs_review": True,
        }
        
        # Add source-specific fields
        if image_data["source"] == "instagram":
            draft.update({
                "instagram_profile": image_data.get("profile"),
                "instagram_url": image_data.get("url"),
                "caption": image_data.get("caption", ""),
            })
        elif image_data["source"] == "facebook":
            draft.update({
                "facebook_page": image_data.get("page_id"),
                "facebook_url": image_data.get("url"),
                "caption": image_data.get("caption", ""),
            })
        elif image_data["source"] == "telegram":
            draft.update({
                "telegram_user_id": image_data.get("telegram_user_id"),
                "telegram_username": image_data.get("telegram_username"),
            })
        elif image_data["source"] == "local":
            draft.update({
                "filename": image_data.get("filename"),
                "filepath": str(image_data["image_path"]),
            })
        
        # Try to extract basic event data from OCR text
        draft.update(self._parse_event_data(ocr_text, image_data))
        
        return draft

    def _parse_event_data(
        self, 
        ocr_text: str, 
        image_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse event data from OCR text using simple heuristics.
        
        Args:
            ocr_text: OCR text
            image_data: Image metadata with caption/alt-text
            
        Returns:
            Parsed event fields
        """
        import re
        
        data = {
            "title": "Event Draft (OCR)",
            "venue": "TBD",
            "date": "TBD",
            "time": "TBD",
            "description": "",
        }
        
        if not ocr_text:
            return data
        
        lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
        
        # First non-empty line often contains title
        if lines:
            data["title"] = lines[0][:100]
        
        # Look for dates (YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY)
        date_patterns = [
            r'\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b',  # 2025-12-31
            r'\b(\d{1,2}[./]\d{1,2}[./]\d{4})\b',  # 31.12.2025
            r'\b(\d{1,2}[./]\d{1,2}[./]\d{2})\b',  # 31.12.25
        ]
        for pattern in date_patterns:
            match = re.search(pattern, ocr_text)
            if match:
                data["date"] = match.group(1)
                break
        
        # Look for time (HH:MM, HH.MM, HHhMM)
        time_pattern = r'\b(\d{1,2}[:h.]\d{2})\s*(Uhr|uhr)?\b'
        match = re.search(time_pattern, ocr_text)
        if match:
            data["time"] = match.group(1).replace('h', ':').replace('.', ':')
        
        # Look for venue/location keywords
        venue_keywords = ['@', 'im ', 'in ', 'bei ', 'Ort:', 'Location:', 'Venue:']
        for line in lines:
            for keyword in venue_keywords:
                if keyword.lower() in line.lower():
                    data["venue"] = line[:100]
                    break
        
        # Use caption as description fallback
        caption = image_data.get("caption", "")
        if caption:
            data["description"] = caption[:500]
        
        return data

    def save_event(self, event: Dict[str, Any], output_dir: Path) -> Path:
        """
        Save event to JSON file.

        Args:
            event: Event data
            output_dir: Output directory

        Returns:
            Path to saved file
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        date_str = event.get("date", datetime.now().strftime("%Y-%m-%d"))
        title_slug = event.get("title", "event")[:30].lower()
        title_slug = "".join(c if c.isalnum() else "-" for c in title_slug)

        filename = f"{date_str}-{title_slug}.json"
        filepath = output_dir / filename

        # Save
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(event, f, indent=2, ensure_ascii=False)

        return filepath


def main():
    """CLI for batch image OCR processing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Batch OCR extraction from social media or local images"
    )
    parser.add_argument(
        "source", 
        choices=["instagram", "facebook", "local"], 
        help="Source: instagram, facebook, or local files"
    )
    parser.add_argument(
        "profile", 
        help="Profile name, page ID, or local path (file/directory)"
    )
    parser.add_argument(
        "--recursive", "-r", action="store_true",
        help="Search local directory recursively"
    )
    parser.add_argument(
        "--count", "-n", type=int, default=5, 
        help="Number of images to process"
    )
    parser.add_argument(
        "--output-dir", "-o", default="_events", 
        help="Output directory for event JSONs"
    )
    parser.add_argument(
        "--output-json", help="Save all results to single JSON file"
    )
    parser.add_argument(
        "--fb-token", help="Facebook API token"
    )
    parser.add_argument(
        "--batch", action="store_true", 
        help="Batch mode: automatic OCR, no interaction (default)"
    )
    parser.add_argument(
        "--ocr", action="store_true", 
        help="Enable OCR (required for batch mode)"
    )

    args = parser.parse_args()

    extractor = ImageStreamExtractor()

    # Check OCR availability
    if not extractor.has_ocr:
        print("❌ OCR nicht verfügbar!")
        print("Installation:")
        print("  sudo apt-get install tesseract-ocr tesseract-ocr-deu")
        print("  pip install pytesseract pillow")
        return 1

    # Fetch images
    print(f"📥 Lade Bilder von {args.source}...")
    
    if args.source == "instagram":
        images = extractor.fetch_instagram_images(args.profile, args.count)
    elif args.source == "facebook":
        images = extractor.fetch_facebook_images(
            args.profile, args.count, args.fb_token
        )
    elif args.source == "local":
        images = extractor.load_local_images(args.profile, args.recursive)
        # Limit to count if specified
        if args.count and len(images) > args.count:
            images = images[:args.count]

    if not images:
        print("❌ Keine Bilder gefunden")
        return 1

    print(f"✓ {len(images)} Bilder geladen\n")

    # Batch OCR processing
    events = extractor.batch_ocr(
        images, 
        output_json=Path(args.output_json) if args.output_json else None
    )

    # Save individual event files
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 Speichere Event-Drafts nach {output_dir}/...")
    
    for event in events:
        filepath = extractor.save_event(event, output_dir)
        print(f"  ✓ {filepath.name}")

    print(f"\n{'='*80}")
    print(f"🎉 Fertig! {len(events)} Event-Drafts erstellt")
    print(f"📁 Ausgabe: {output_dir}/")
    if args.output_json:
        print(f"📄 JSON: {args.output_json}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main() or 0)
