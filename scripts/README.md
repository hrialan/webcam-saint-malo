# Scripts

Utility scripts for the webcam project.

## check_webcams.py

Health check script for YouTube webcams. Verifies that all configured webcams are:
- Accessible and reachable
- Properly configured with valid video IDs
- Optionally checks if they are live streams

### Usage

```bash
python3 scripts/check_webcams.py
```

### Output

- ✓ = Accessible
- ✗ = Error (HTTP error, invalid ID, etc.)
- ⚠️ = Warning (not a live stream)

### Configuration

Edit the `WEBCAM_IDS` dictionary in the script to add or update video IDs.
