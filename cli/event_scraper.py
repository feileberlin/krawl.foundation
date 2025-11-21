#!/usr/bin/env python3
"""
Event Scraper CLI - krawl.foundation
Scraping, comparing, merging, and managing event data.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import difflib


class EventManager:
    """Core class for event data management."""
    
    def __init__(self, events_dir: Path = None):
        self.events_dir = events_dir or Path("_events")
        self.events_dir.mkdir(exist_ok=True)
        
    def load_event(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Load event from JSON or markdown frontmatter."""
        if not filepath.exists():
            return None
            
        if filepath.suffix == '.json':
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif filepath.suffix == '.md':
            # Parse frontmatter from markdown
            return self._parse_frontmatter(filepath)
        return None
    
    def _parse_frontmatter(self, filepath: Path) -> Dict[str, Any]:
        """Extract YAML frontmatter from markdown file."""
        import yaml
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1])
        return {}
    
    def save_event(self, event_data: Dict[str, Any], filepath: Path, format: str = 'json'):
        """Save event data to file."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(event_data, f, indent=2, ensure_ascii=False)
        elif format == 'markdown':
            self._save_as_markdown(event_data, filepath)
    
    def _save_as_markdown(self, event_data: Dict[str, Any], filepath: Path):
        """Save event as markdown with frontmatter."""
        import yaml
        
        # Separate content from metadata
        content = event_data.pop('content', '')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(event_data, f, allow_unicode=True, sort_keys=False)
            f.write('---\n\n')
            f.write(content)
    
    def list_events(self) -> List[Path]:
        """List all event files in the events directory."""
        json_files = list(self.events_dir.glob('*.json'))
        md_files = list(self.events_dir.glob('*.md'))
        return sorted(json_files + md_files)
    
    def compare_events(self, event1: Dict, event2: Dict) -> Dict[str, Any]:
        """Compare two events and return differences."""
        diff_result = {
            'identical': event1 == event2,
            'added_fields': [],
            'removed_fields': [],
            'modified_fields': {},
            'unchanged_fields': []
        }
        
        keys1 = set(event1.keys())
        keys2 = set(event2.keys())
        
        diff_result['added_fields'] = list(keys2 - keys1)
        diff_result['removed_fields'] = list(keys1 - keys2)
        
        common_keys = keys1 & keys2
        for key in common_keys:
            if event1[key] != event2[key]:
                diff_result['modified_fields'][key] = {
                    'old': event1[key],
                    'new': event2[key]
                }
            else:
                diff_result['unchanged_fields'].append(key)
        
        return diff_result
    
    def merge_events(self, base: Dict, updates: Dict, fields: List[str] = None) -> Dict:
        """Merge specific fields from updates into base event."""
        merged = base.copy()
        
        if fields is None:
            # Merge all fields
            merged.update(updates)
        else:
            # Merge only specified fields
            for field in fields:
                if field in updates:
                    merged[field] = updates[field]
        
        merged['last_updated'] = datetime.now().isoformat()
        return merged
    
    def generate_test_event(self, event_type: str = 'concert') -> Dict[str, Any]:
        """Generate lorem ipsum test event data."""
        from faker import Faker
        fake = Faker('de_DE')
        
        templates = {
            'concert': {
                'title': f"{fake.name()} - {fake.catch_phrase()}",
                'date': fake.future_date(end_date='+90d').isoformat(),
                'venue': fake.company(),
                'location': fake.city(),
                'description': fake.text(max_nb_chars=200),
                'price': f"{fake.random_int(min=5, max=50)}€",
                'genre': fake.random_element(['Rock', 'Pop', 'Jazz', 'Electronic', 'Hip-Hop']),
                'url': fake.url(),
                'status': 'draft'
            },
            'exhibition': {
                'title': fake.catch_phrase(),
                'date': fake.future_date(end_date='+90d').isoformat(),
                'end_date': fake.future_date(end_date='+120d').isoformat(),
                'venue': fake.company(),
                'location': fake.city(),
                'description': fake.text(max_nb_chars=200),
                'artists': [fake.name() for _ in range(fake.random_int(min=1, max=3))],
                'free_entry': fake.boolean(),
                'url': fake.url(),
                'status': 'draft'
            }
        }
        
        event = templates.get(event_type, templates['concert']).copy()
        event['id'] = fake.uuid4()
        event['created'] = datetime.now().isoformat()
        
        return event


class EventScraperCLI:
    """Command-line interface for event scraper."""
    
    def __init__(self):
        self.manager = EventManager()
        self.parser = self._build_parser()
    
    def _build_parser(self) -> argparse.ArgumentParser:
        """Build argument parser with all commands."""
        parser = argparse.ArgumentParser(
            description='Event Scraper CLI - Manage event data for krawl.foundation',
            epilog='Beispiele:\n'
                   '  %(prog)s list\n'
                   '  %(prog)s scrape https://example.com/events\n'
                   '  %(prog)s diff event1.json event2.json\n'
                   '  %(prog)s merge base.json updates.json -f title,date\n'
                   '  %(prog)s generate --count 5 --type concert\n',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Verfügbare Kommandos')
        
        # LIST command
        list_parser = subparsers.add_parser('list', help='Liste alle Events auf')
        list_parser.add_argument('--format', choices=['table', 'json'], default='table',
                               help='Ausgabeformat')
        
        # SCRAPE command
        scrape_parser = subparsers.add_parser('scrape', help='Scrape Events von URL')
        scrape_parser.add_argument('url', help='URL zum Scrapen')
        scrape_parser.add_argument('--output', '-o', help='Output-Datei')
        scrape_parser.add_argument('--compare', '-c', help='Vergleiche mit existierendem Event')
        
        # DIFF command
        diff_parser = subparsers.add_parser('diff', help='Vergleiche zwei Events')
        diff_parser.add_argument('file1', help='Erste Event-Datei')
        diff_parser.add_argument('file2', help='Zweite Event-Datei')
        diff_parser.add_argument('--format', choices=['json', 'text'], default='text')
        
        # MERGE command
        merge_parser = subparsers.add_parser('merge', help='Merge Event-Daten')
        merge_parser.add_argument('base', help='Basis Event-Datei')
        merge_parser.add_argument('updates', help='Update Event-Datei')
        merge_parser.add_argument('--fields', '-f', help='Komma-separierte Feldliste (alle wenn leer)')
        merge_parser.add_argument('--output', '-o', required=True, help='Output-Datei')
        
        # GENERATE command
        gen_parser = subparsers.add_parser('generate', help='Generiere Test-Events')
        gen_parser.add_argument('--count', '-n', type=int, default=1, help='Anzahl Events')
        gen_parser.add_argument('--type', '-t', default='concert',
                              help='Event-Typ (concert, exhibition)')
        gen_parser.add_argument('--output-dir', '-o', help='Output-Verzeichnis')
        
        # BULK command
        bulk_parser = subparsers.add_parser('bulk', help='Bulk-Operationen auf Events')
        bulk_parser.add_argument('--set-field', nargs=2, metavar=('FIELD', 'VALUE'),
                               help='Setze Feld in allen Events')
        bulk_parser.add_argument('--filter', help='Filter Events (JSON query)')
        bulk_parser.add_argument('--dry-run', action='store_true', help='Nur anzeigen, nicht ändern')
        
        # EXTRACT command (new!)
        extract_parser = subparsers.add_parser('extract', 
            help='Extrahiere Events aus Social Media Bildern (interaktiv)')
        extract_parser.add_argument('source', choices=['instagram', 'facebook'],
                                  help='Social Media Quelle')
        extract_parser.add_argument('profile', help='Profil-Name oder Page-ID')
        extract_parser.add_argument('--count', '-n', type=int, default=5,
                                  help='Anzahl zu prüfender Bilder (default: 5)')
        extract_parser.add_argument('--ocr', action='store_true',
                                  help='OCR auf Bildern ausführen')
        extract_parser.add_argument('--fb-token', help='Facebook API Token')
        
        return parser
    
    def run(self, args: List[str] = None):
        """Execute CLI command."""
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return 0
        
        # Route to appropriate handler
        handler = getattr(self, f'cmd_{parsed_args.command}', None)
        if handler:
            return handler(parsed_args)
        else:
            print(f"Fehler: Unbekanntes Kommando '{parsed_args.command}'", file=sys.stderr)
            return 1
    
    def cmd_list(self, args):
        """List all events."""
        events = self.manager.list_events()
        
        if args.format == 'json':
            print(json.dumps([str(e) for e in events], indent=2))
        else:
            print(f"\n{'Dateiname':<40} {'Größe':<10}")
            print("-" * 50)
            for event_file in events:
                size = event_file.stat().st_size
                print(f"{event_file.name:<40} {size:>8} B")
            print(f"\nGesamt: {len(events)} Events")
        
        return 0
    
    def cmd_scrape(self, args):
        """Scrape events from URL (placeholder for implementation)."""
        print(f"🔍 Scraping {args.url}...")
        print("⚠️  Scraper-Implementation folgt - abhängig von der Ziel-Website")
        print("\nTipps für Implementation:")
        print("  - requests + BeautifulSoup4 für HTML-Parsing")
        print("  - Selenium für JavaScript-heavy Sites")
        print("  - JSON-API direkter Zugriff wenn verfügbar")
        return 0
    
    def cmd_diff(self, args):
        """Compare two event files."""
        event1 = self.manager.load_event(Path(args.file1))
        event2 = self.manager.load_event(Path(args.file2))
        
        if not event1 or not event2:
            print("Fehler: Konnte Event-Dateien nicht laden", file=sys.stderr)
            return 1
        
        diff = self.manager.compare_events(event1, event2)
        
        if args.format == 'json':
            print(json.dumps(diff, indent=2, ensure_ascii=False))
        else:
            if diff['identical']:
                print("✓ Events sind identisch")
            else:
                print("✗ Events unterscheiden sich:\n")
                
                if diff['added_fields']:
                    print(f"Neue Felder: {', '.join(diff['added_fields'])}")
                
                if diff['removed_fields']:
                    print(f"Entfernte Felder: {', '.join(diff['removed_fields'])}")
                
                if diff['modified_fields']:
                    print("\nGeänderte Felder:")
                    for field, changes in diff['modified_fields'].items():
                        print(f"\n  {field}:")
                        print(f"    Alt: {changes['old']}")
                        print(f"    Neu: {changes['new']}")
        
        return 0
    
    def cmd_merge(self, args):
        """Merge event data."""
        base = self.manager.load_event(Path(args.base))
        updates = self.manager.load_event(Path(args.updates))
        
        if not base or not updates:
            print("Fehler: Konnte Event-Dateien nicht laden", file=sys.stderr)
            return 1
        
        fields = args.fields.split(',') if args.fields else None
        merged = self.manager.merge_events(base, updates, fields)
        
        output_path = Path(args.output)
        self.manager.save_event(merged, output_path)
        
        print(f"✓ Events gemerged → {args.output}")
        if fields:
            print(f"  Aktualisierte Felder: {', '.join(fields)}")
        
        return 0
    
    def cmd_generate(self, args):
        """Generate test events."""
        output_dir = Path(args.output_dir) if args.output_dir else self.manager.events_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🎲 Generiere {args.count} Test-Events ({args.type})...\n")
        
        for i in range(args.count):
            event = self.manager.generate_test_event(args.type)
            filename = f"test-{args.type}-{i+1:03d}.json"
            filepath = output_dir / filename
            
            self.manager.save_event(event, filepath)
            print(f"  ✓ {filename} - {event['title']}")
        
        print(f"\n✓ {args.count} Events erstellt in {output_dir}")
        return 0
    
    def cmd_bulk(self, args):
        """Bulk operations on events."""
        events = self.manager.list_events()
        modified_count = 0
        
        if args.set_field:
            field, value = args.set_field
            print(f"{'[DRY RUN] ' if args.dry_run else ''}Setze {field}={value} für alle Events...\n")
            
            for event_file in events:
                event = self.manager.load_event(event_file)
                if event:
                    event[field] = value
                    
                    if not args.dry_run:
                        self.manager.save_event(event, event_file)
                    
                    print(f"  {'✓' if not args.dry_run else '○'} {event_file.name}")
                    modified_count += 1
            
            print(f"\n{'Würde ändern' if args.dry_run else 'Geändert'}: {modified_count} Events")
        
        return 0
    
    def cmd_extract(self, args):
        """Extract events from social media images (interactive)."""
        print("🎨 Image Stream Extractor")
        print("="*60)
        print()
        
        # Import image extractor
        try:
            from cli.image_extractor import ImageStreamExtractor
        except ImportError:
            # Try different import path
            import sys
            sys.path.insert(0, str(Path(__file__).parent))
            from image_extractor import ImageStreamExtractor
        
        extractor = ImageStreamExtractor()
        
        # Fetch images
        print(f"📥 Lade {args.count} Bilder von {args.source}/{args.profile}...\n")
        
        if args.source == 'instagram':
            images = extractor.fetch_instagram_images(args.profile, args.count)
        else:
            if not args.fb_token:
                print("❌ Facebook benötigt --fb-token")
                print("   Siehe: cli/scrapers/galeriehaus_hof_facebook.py für Setup")
                return 1
            images = extractor.fetch_facebook_images(args.profile, args.count, args.fb_token)
        
        if not images:
            print("❌ Keine Bilder gefunden")
            return 1
        
        print(f"✓ {len(images)} Bilder geladen\n")
        
        # Process each image interactively
        events_created = 0
        
        for i, image_data in enumerate(images):
            print(f"\n{'='*80}")
            print(f"📸 Bild {i+1}/{len(images)}")
            print(f"{'='*80}")
            
            # OCR if requested
            ocr_text = ""
            if args.ocr:
                print("🔍 Führe OCR aus...")
                ocr_text = extractor.extract_text_from_image(image_data['image_path'])
            
            # Interactive editor
            event = extractor.interactive_event_editor(image_data, ocr_text)
            
            if event:
                filepath = extractor.save_event(event, self.manager.events_dir)
                print(f"\n✅ Gespeichert: {filepath}")
                events_created += 1
            
            # Ask if continue
            if i < len(images) - 1:
                cont = input("\n▶️  Weiter zum nächsten Bild? [J/n]: ").strip().lower()
                if cont in ['n', 'no', 'nein']:
                    break
        
        print(f"\n{'='*80}")
        print(f"🎉 Fertig! {events_created}/{len(images)} Events erstellt")
        print(f"{'='*80}\n")
        
        return 0


def main():
    """Main entry point."""
    cli = EventScraperCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()
