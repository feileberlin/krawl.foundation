"""
Image Stream Extractor - Lade Bilder von Social Media und extrahiere Event-Infos

Workflow:
1. Lade letzte N Bilder von Instagram/Facebook
2. Extrahiere Alt-Text / mache OCR
3. Zeige Bild + Text im Terminal
4. Öffne interaktiven Editor für Event-JSON
5. Speichere oder verwerfe

Dependencies:
- pillow (Bilder anzeigen)
- pytesseract (OCR, optional)
- imgcat oder chafa (Terminal-Bild-Display)
"""

from typing import List, Dict, Any, Optional, Tuple
import requests
from pathlib import Path
import json
import subprocess
import tempfile
from datetime import datetime


class ImageStreamExtractor:
    """Extract event info from social media images with OCR/Alt-Text."""
    
    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path(".cache/images")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Check available tools
        self.has_ocr = self._check_ocr()
        self.image_viewer = self._detect_image_viewer()
    
    def _check_ocr(self) -> bool:
        """Check if OCR is available."""
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            return True
        except:
            return False
    
    def _detect_image_viewer(self) -> Optional[str]:
        """Detect available terminal image viewer."""
        viewers = ['imgcat', 'chafa', 'catimg']
        for viewer in viewers:
            try:
                subprocess.run([viewer, '--version'], 
                             capture_output=True, check=False)
                return viewer
            except FileNotFoundError:
                continue
        return None
    
    def fetch_instagram_images(self, profile: str, count: int = 5) -> List[Dict[str, Any]]:
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
                save_metadata=False
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
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                
                images.append({
                    'source': 'instagram',
                    'profile': profile,
                    'image_path': image_path,
                    'url': f"https://www.instagram.com/p/{post.shortcode}/",
                    'caption': post.caption or "",
                    'alt_text': post.accessibility_caption or "",
                    'date': post.date_local,
                    'shortcode': post.shortcode
                })
                
                print(f"  ✓ {i+1}/{count}: {post.shortcode}")
            
        except ImportError:
            print("⚠️  Instaloader nicht installiert: pip install instaloader")
        except Exception as e:
            print(f"Fehler beim Laden von Instagram: {e}")
        
        return images
    
    def fetch_facebook_images(self, page_id: str, count: int = 5, 
                             access_token: str = None) -> List[Dict[str, Any]]:
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
                'access_token': access_token,
                'fields': 'id,images,alt_text,name,created_time,link',
                'limit': count
            }
            
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            for photo in data.get('data', []):
                # Get highest resolution image
                image_url = photo.get('images', [{}])[0].get('source', '')
                
                if image_url:
                    # Download
                    image_path = self.cache_dir / f"fb_{photo['id']}.jpg"
                    
                    if not image_path.exists():
                        img_response = requests.get(image_url)
                        with open(image_path, 'wb') as f:
                            f.write(img_response.content)
                    
                    images.append({
                        'source': 'facebook',
                        'page_id': page_id,
                        'image_path': image_path,
                        'url': photo.get('link', ''),
                        'caption': photo.get('name', ''),
                        'alt_text': photo.get('alt_text', ''),
                        'date': photo.get('created_time', ''),
                        'photo_id': photo['id']
                    })
            
        except Exception as e:
            print(f"Fehler beim Laden von Facebook: {e}")
        
        return images
    
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
            text = pytesseract.image_to_string(img, lang='deu+eng')
            return text.strip()
            
        except Exception as e:
            return f"[OCR Fehler: {e}]"
    
    def display_image_in_terminal(self, image_path: Path) -> bool:
        """
        Display image in terminal if viewer available.
        
        Args:
            image_path: Path to image
            
        Returns:
            True if displayed, False otherwise
        """
        if not self.image_viewer:
            return False
        
        try:
            if self.image_viewer == 'imgcat':
                subprocess.run(['imgcat', str(image_path)])
            elif self.image_viewer == 'chafa':
                subprocess.run(['chafa', '--size=80x40', str(image_path)])
            elif self.image_viewer == 'catimg':
                subprocess.run(['catimg', str(image_path)])
            return True
        except Exception as e:
            print(f"Fehler beim Anzeigen: {e}")
            return False
    
    def interactive_event_editor(self, image_data: Dict[str, Any], 
                                 ocr_text: str = "") -> Optional[Dict[str, Any]]:
        """
        Interactive editor for creating event from image data.
        
        Args:
            image_data: Image metadata
            ocr_text: Extracted OCR text
            
        Returns:
            Event dict or None if skipped
        """
        print("\n" + "="*80)
        print("📝 INTERAKTIVER EVENT-EDITOR")
        print("="*80)
        
        # Show image
        print("\n📷 BILD:")
        if not self.display_image_in_terminal(image_data['image_path']):
            print(f"   Öffne manuell: {image_data['image_path']}")
            print(f"   URL: {image_data['url']}")
        
        # Show texts
        print("\n📄 EXTRAHIERTE TEXTE:")
        print("-" * 80)
        
        if image_data.get('caption'):
            print(f"Caption:\n{image_data['caption']}\n")
        
        if image_data.get('alt_text'):
            print(f"Alt-Text:\n{image_data['alt_text']}\n")
        
        if ocr_text:
            print(f"OCR:\n{ocr_text}\n")
        
        print("-" * 80)
        
        # Interactive prompts
        print("\n✏️  EVENT-DATEN EINGEBEN (Enter = skip):")
        
        # Generate template
        template = {
            'title': '',
            'date': '',
            'venue': image_data.get('profile', 'Unknown Venue'),
            'location': 'Berlin',
            'description': image_data.get('caption', '')[:200],
            'url': image_data['url'],
            'image_url': image_data['url'],
            'source': image_data['source'],
            'source_id': image_data.get('shortcode') or image_data.get('photo_id'),
            'scraped_at': datetime.now().isoformat(),
            'status': 'draft'
        }
        
        # Prompt for each field
        try:
            title = input("Titel: ").strip()
            if not title:
                print("⏭️  Übersprungen (kein Titel)")
                return None
            template['title'] = title
            
            date = input("Datum (YYYY-MM-DD): ").strip()
            if date:
                template['date'] = date
            
            venue = input(f"Venue [{template['venue']}]: ").strip()
            if venue:
                template['venue'] = venue
            
            location = input(f"Ort [{template['location']}]: ").strip()
            if location:
                template['location'] = location
            
            price = input("Preis (z.B. 15€): ").strip()
            if price:
                template['price'] = price
            
            genre = input("Genre: ").strip()
            if genre:
                template['genre'] = genre
            
            # Show preview
            print("\n📋 VORSCHAU:")
            print(json.dumps(template, indent=2, ensure_ascii=False))
            
            # Confirm
            confirm = input("\n💾 Speichern? [j/N]: ").strip().lower()
            if confirm in ['j', 'y', 'ja', 'yes']:
                return template
            else:
                print("❌ Verworfen")
                return None
                
        except KeyboardInterrupt:
            print("\n❌ Abgebrochen")
            return None
    
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
        date_str = event.get('date', datetime.now().strftime('%Y-%m-%d'))
        title_slug = event.get('title', 'event')[:30].lower()
        title_slug = ''.join(c if c.isalnum() else '-' for c in title_slug)
        
        filename = f"{date_str}-{title_slug}.json"
        filepath = output_dir / filename
        
        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(event, f, indent=2, ensure_ascii=False)
        
        return filepath


def main():
    """CLI for image stream extraction."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Extract events from social media images'
    )
    parser.add_argument('source', choices=['instagram', 'facebook'],
                       help='Social media source')
    parser.add_argument('profile', help='Profile name or page ID')
    parser.add_argument('--count', '-n', type=int, default=5,
                       help='Number of images to check')
    parser.add_argument('--output', '-o', default='_events',
                       help='Output directory')
    parser.add_argument('--fb-token', help='Facebook API token')
    parser.add_argument('--ocr', action='store_true',
                       help='Run OCR on images (slow)')
    
    args = parser.parse_args()
    
    extractor = ImageStreamExtractor()
    
    # Fetch images
    if args.source == 'instagram':
        images = extractor.fetch_instagram_images(args.profile, args.count)
    else:
        images = extractor.fetch_facebook_images(args.profile, args.count, args.fb_token)
    
    if not images:
        print("❌ Keine Bilder gefunden")
        return
    
    print(f"\n✓ {len(images)} Bilder geladen\n")
    
    # Process each image
    events_created = 0
    output_dir = Path(args.output)
    
    for i, image_data in enumerate(images):
        print(f"\n{'='*80}")
        print(f"Bild {i+1}/{len(images)}")
        
        # OCR if requested
        ocr_text = ""
        if args.ocr:
            print("🔍 Führe OCR aus...")
            ocr_text = extractor.extract_text_from_image(image_data['image_path'])
        
        # Interactive editor
        event = extractor.interactive_event_editor(image_data, ocr_text)
        
        if event:
            filepath = extractor.save_event(event, output_dir)
            print(f"\n✅ Gespeichert: {filepath}")
            events_created += 1
    
    print(f"\n{'='*80}")
    print(f"🎉 Fertig! {events_created}/{len(images)} Events erstellt")


if __name__ == '__main__':
    main()
