#!/usr/bin/env python3
"""Check if YouTube webcams are accessible and live."""

import json
import urllib.request
import urllib.error
import sys
from typing import Dict, List


WEBCAM_IDS = {
    'top-left': 'VNOV8KgGR0c',
    'top-right': 'p6nAlz4_bdI',
    'bottom-left': 'OzYp4NRZlwQ',
    'bottom-right': 'M6kN1wlNSk4'
}


def check_webcam(position: str, video_id: str) -> Dict:
    """Check if a YouTube video is accessible and live."""
    url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json'

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                return {
                    'position': position,
                    'video_id': video_id,
                    'status': 'error',
                    'error': f'HTTP {response.status}',
                    'status_code': response.status
                }

            data = response.read().decode('utf-8')
            oembed = json.loads(data)

            title = oembed.get('title', '')
            is_live = 'live' in title.lower() or 'en direct' in title.lower()

            return {
                'position': position,
                'video_id': video_id,
                'status': 'accessible',
                'title': title,
                'is_live': is_live,
                'status_code': 200
            }

    except urllib.error.HTTPError as e:
        return {
            'position': position,
            'video_id': video_id,
            'status': 'error',
            'error': f'HTTP {e.code}',
            'status_code': e.code
        }
    except Exception as e:
        return {
            'position': position,
            'video_id': video_id,
            'status': 'error',
            'error': str(e)
        }


def main():
    """Main function."""
    print('Webcam Status Report:')
    print('=' * 20)

    results = []
    for position, video_id in WEBCAM_IDS.items():
        result = check_webcam(position, video_id)
        results.append(result)

        status_symbol = '✓' if result['status'] == 'accessible' else '✗'
        print(f"{status_symbol} {result['position']}: {result['video_id']}")

        if result.get('title'):
            print(f"  Title: {result['title']}")
            if result.get('is_live'):
                print(f"  Status: LIVE")
            else:
                print(f"  Status: NOT LIVE (not a live stream)")

        if result.get('error'):
            print(f"  Error: {result['error']}")

        if result.get('status_code'):
            print(f"  HTTP: {result['status_code']}")

    # Check for failures
    failures = [r for r in results if r['status'] != 'accessible']
    non_live = [r for r in results if r['status'] == 'accessible' and not r.get('is_live', False)]

    if non_live:
        print(f"\n⚠️  Warning: {len(non_live)} webcam(s) are NOT live streams:")
        for result in non_live:
            print(f"  - {result['position']}: {result.get('title', 'Unknown')}")

    if failures:
        print(f"\n❌ Error: {len(failures)} webcam(s) failed!")
        sys.exit(1)

    print('\n✅ All webcams are accessible!')
    sys.exit(0)


if __name__ == '__main__':
    main()
