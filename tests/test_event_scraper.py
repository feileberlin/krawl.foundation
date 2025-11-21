"""
Unit Tests für Event Scraper CLI
"""

import json
from pathlib import Path

import pytest

from cli.event_scraper import EventManager


@pytest.fixture
def event_manager(tmp_path):
    """Create EventManager with temporary directory."""
    return EventManager(events_dir=tmp_path)


@pytest.fixture
def sample_event():
    """Sample event data."""
    return {
        "title": "Test Concert",
        "date": "2025-12-01",
        "venue": "Test Venue",
        "location": "Berlin",
        "price": "15€",
    }


@pytest.fixture
def sample_event_updated():
    """Updated version of sample event."""
    return {
        "title": "Test Concert - Updated",
        "date": "2025-12-02",
        "venue": "Test Venue",
        "location": "Berlin",
        "price": "20€",
        "genre": "Rock",
    }


class TestEventManager:
    """Test EventManager class."""

    def test_save_and_load_json(self, event_manager, sample_event, tmp_path):
        """Test saving and loading JSON events."""
        filepath = tmp_path / "test-event.json"
        event_manager.save_event(sample_event, filepath)

        assert filepath.exists()

        loaded = event_manager.load_event(filepath)
        assert loaded == sample_event

    def test_list_events(self, event_manager, sample_event, tmp_path):
        """Test listing events."""
        # Create multiple events
        for i in range(3):
            filepath = tmp_path / f"event-{i}.json"
            event_manager.save_event(sample_event, filepath)

        events = event_manager.list_events()
        assert len(events) == 3

    def test_compare_identical_events(self, event_manager, sample_event):
        """Test comparing identical events."""
        diff = event_manager.compare_events(sample_event, sample_event)

        assert diff["identical"] is True
        assert len(diff["added_fields"]) == 0
        assert len(diff["removed_fields"]) == 0
        assert len(diff["modified_fields"]) == 0

    def test_compare_different_events(
        self, event_manager, sample_event, sample_event_updated
    ):
        """Test comparing different events."""
        diff = event_manager.compare_events(sample_event, sample_event_updated)

        assert diff["identical"] is False
        assert "genre" in diff["added_fields"]
        assert len(diff["modified_fields"]) > 0
        assert "title" in diff["modified_fields"]
        assert diff["modified_fields"]["title"]["old"] == "Test Concert"
        assert diff["modified_fields"]["title"]["new"] == "Test Concert - Updated"

    def test_merge_all_fields(self, event_manager, sample_event, sample_event_updated):
        """Test merging all fields."""
        merged = event_manager.merge_events(sample_event, sample_event_updated)

        assert merged["title"] == sample_event_updated["title"]
        assert merged["genre"] == sample_event_updated["genre"]
        assert "last_updated" in merged

    def test_merge_specific_fields(
        self, event_manager, sample_event, sample_event_updated
    ):
        """Test merging only specific fields."""
        merged = event_manager.merge_events(
            sample_event, sample_event_updated, fields=["date", "price"]
        )

        # These should be updated
        assert merged["date"] == sample_event_updated["date"]
        assert merged["price"] == sample_event_updated["price"]

        # These should NOT be updated
        assert merged["title"] == sample_event["title"]
        assert "genre" not in merged

    def test_generate_test_event_concert(self, event_manager):
        """Test generating concert test event."""
        event = event_manager.generate_test_event("concert")

        assert "title" in event
        assert "date" in event
        assert "venue" in event
        assert "genre" in event
        assert event["status"] == "draft"

    def test_generate_test_event_exhibition(self, event_manager):
        """Test generating exhibition test event."""
        event = event_manager.generate_test_event("exhibition")

        assert "title" in event
        assert "date" in event
        assert "end_date" in event
        assert "artists" in event
        assert isinstance(event["artists"], list)


class TestCLI:
    """Test CLI commands."""

    def test_cli_help(self, capsys):
        """Test CLI help output."""
        from cli.event_scraper import EventScraperCLI

        cli = EventScraperCLI()
        result = cli.run([])

        captured = capsys.readouterr()
        assert "Event Scraper CLI" in captured.out
        assert "list" in captured.out
        assert "diff" in captured.out
        assert "merge" in captured.out

    def test_cli_generate(self, tmp_path, capsys):
        """Test CLI generate command."""
        from cli.event_scraper import EventScraperCLI

        cli = EventScraperCLI()
        cli.manager.events_dir = tmp_path

        result = cli.run(
            [
                "generate",
                "--count",
                "3",
                "--type",
                "concert",
                "--output-dir",
                str(tmp_path),
            ]
        )

        assert result == 0

        # Check that files were created
        json_files = list(tmp_path.glob("*.json"))
        assert len(json_files) == 3

    def test_cli_diff_identical(self, tmp_path, sample_event, capsys):
        """Test CLI diff with identical events."""
        from cli.event_scraper import EventScraperCLI

        # Create two identical events
        file1 = tmp_path / "event1.json"
        file2 = tmp_path / "event2.json"

        with open(file1, "w") as f:
            json.dump(sample_event, f)
        with open(file2, "w") as f:
            json.dump(sample_event, f)

        cli = EventScraperCLI()
        result = cli.run(["diff", str(file1), str(file2)])

        assert result == 0
        captured = capsys.readouterr()
        assert "identisch" in captured.out

    def test_cli_merge(self, tmp_path, sample_event, sample_event_updated):
        """Test CLI merge command."""
        from cli.event_scraper import EventScraperCLI

        # Create event files
        base_file = tmp_path / "base.json"
        updates_file = tmp_path / "updates.json"
        output_file = tmp_path / "merged.json"

        with open(base_file, "w") as f:
            json.dump(sample_event, f)
        with open(updates_file, "w") as f:
            json.dump(sample_event_updated, f)

        cli = EventScraperCLI()
        result = cli.run(
            [
                "merge",
                str(base_file),
                str(updates_file),
                "--fields",
                "date,price",
                "--output",
                str(output_file),
            ]
        )

        assert result == 0
        assert output_file.exists()

        # Verify merged content
        with open(output_file) as f:
            merged = json.load(f)

        assert merged["date"] == sample_event_updated["date"]
        assert merged["price"] == sample_event_updated["price"]
        assert merged["title"] == sample_event["title"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
