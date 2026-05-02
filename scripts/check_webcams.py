#!/usr/bin/env python3
"""Check if YouTube webcams are accessible and live."""

import json
import re
import urllib.request
import urllib.error
import sys
from typing import Dict
from html.parser import HTMLParser


# Default IDs (used locally, can be overridden by CLI args)
DEFAULT_WEBCAM_IDS = {
    'top-left': 'VNOV8KgGR0c',
    'top-right': 'p6nAlz4_bdI',
    'bottom-left': 'OzYp4NRZlwQ',
    'bottom-right': '80s06q41pMo'
}


class VideoInfoParser(HTMLParser):
    """Parse video info from YouTube page meta tags."""

    def __init__(self):
        super().__init__()
        self.is_live = False
        self.title = None
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Check meta tags for video info
        if tag == 'meta':
            name = attrs_dict.get('name', '')
            property_name = attrs_dict.get('property', '')
            content = attrs_dict.get('content', '')

            if name == 'title' or property_name == 'og:title':
                self.title = content

            # Check for live indicators in meta content
            if 'content' in attrs_dict:
                content_lower = content.lower()
                if 'live' in content_lower and ('broadcast' in content_lower or 'stream' in content_lower):
                    self.is_live = True

        # Check for ytInitialData script
        if tag == 'script' and attrs_dict.get('type') == 'application/ld+json':
            pass

    def handle_data(self, data):
        pass


def check_webcam(position: str, video_id: str, debug: bool = False) -> Dict:
    """Check if a YouTube video is accessible and live."""
    # First check if video exists with oEmbed
    oembed_url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json'

    try:
        # Get oEmbed data
        with urllib.request.urlopen(oembed_url) as response:
            if response.status != 200:
                return {
                    'position': position,
                    'video_id': video_id,
                    'status': 'error',
                    'error': f'HTTP {response.status}',
                    'status_code': response.status
                }

            oembed_data = response.read().decode('utf-8')
            oembed = json.loads(oembed_data)
            title = oembed.get('title', '')

        # Now fetch the actual page to check for live status
        page_url = f'https://www.youtube.com/watch?v={video_id}'
        req = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')

        # Check for live indicators in the HTML
        is_live = False

        # First check if it's currently live (isLiveNow:true)
        # This is the most reliable indicator for currently broadcasting streams
        if re.search(r'"isLiveNow"\s*:\s*true', html):
            is_live = True
        # Also check isLive:true (alternative pattern)
        elif re.search(r'"isLive"\s*:\s*true', html):
            is_live = True
        # Also check isLiveContent:true but NOT if isLiveNow is false
        # (to avoid false positives for VOD recordings of past livestreams)
        elif re.search(r'"isLiveContent"\s*:\s*true', html) and not re.search(r'"isLiveNow"\s*:\s*false', html):
            is_live = True

        # Look for live badge indicators
        if re.search(r'"simpleText"\s*:\s*"(?:LIVE|EN DIRECT)"', html):
            is_live = True

        # Look for livestream indicators
        if re.search(r'"isLivelyContent"\s*:\s*true', html):
            is_live = True

        if debug:
            has_islive_now = bool(re.search(r'"isLiveNow"\s*:\s*true', html))
            has_islive_now_false = bool(re.search(r'"isLiveNow"\s*:\s*false', html))
            has_islive = bool(re.search(r'"isLive"\s*:\s*true', html))
            has_live_content = bool(re.search(r'"isLiveContent"\s*:\s*true', html))
            has_lively_content = bool(re.search(r'"isLivelyContent"\s*:\s*true', html))
            has_live_badge = bool(re.search(r'"simpleText"\s*:\s*"(?:LIVE|EN DIRECT)"', html))
            print(f"\n[DEBUG] {position}:")
            print(f"  Video ID: {video_id}")
            print(f"  Title: {title}")
            print(f"  Found 'isLiveNow': true: {has_islive_now}")
            print(f"  Found 'isLiveNow': false: {has_islive_now_false}")
            print(f"  Found 'isLive': true: {has_islive}")
            print(f"  Found 'isLiveContent': true: {has_live_content}")
            print(f"  Found 'isLivelyContent': true: {has_lively_content}")
            print(f"  Found LIVE badge: {has_live_badge}")
            print(f"  Is Live: {is_live}")

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


def main(debug: bool = False, webcam_ids: Dict = None):
    """Main function."""
    if webcam_ids is None:
        webcam_ids = DEFAULT_WEBCAM_IDS

    print('Webcam Status Report:')
    print('=' * 20)

    results = []
    for position, video_id in webcam_ids.items():
        result = check_webcam(position, video_id, debug=debug)
        results.append(result)

        status_symbol = '✓' if result['status'] == 'accessible' else '✗'
        print(f"{status_symbol} {result['position']}: {result['video_id']}")

        if result.get('title'):
            print(f"  Title: {result['title']}")
            if result.get('is_live'):
                print(f"  Status: 🔴 LIVE")
            else:
                print(f"  Status: Not currently broadcasting")

        if result.get('error'):
            print(f"  Error: {result['error']}")

        if result.get('status_code'):
            print(f"  HTTP: {result['status_code']}")

    # Check for failures and non-live streams
    failures = [r for r in results if r['status'] != 'accessible']
    non_live = [r for r in results if r['status'] == 'accessible' and not r.get('is_live', False)]

    has_errors = False

    if failures:
        print(f"\n❌ Error: {len(failures)} webcam(s) are not accessible!")
        for result in failures:
            print(f"  - {result['position']}: {result.get('error', 'Unknown error')}")
        has_errors = True

    if non_live:
        print(f"\n❌ Error: {len(non_live)} webcam(s) are NOT currently broadcasting:")
        for result in non_live:
            print(f"  - {result['position']}: {result.get('title', 'Unknown')}")
        has_errors = True

    if has_errors:
        sys.exit(1)

    print('\n✅ All webcams are live and accessible!')
    sys.exit(0)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Check YouTube webcams status')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--top-left', help='YouTube video ID for top-left webcam')
    parser.add_argument('--top-right', help='YouTube video ID for top-right webcam')
    parser.add_argument('--bottom-left', help='YouTube video ID for bottom-left webcam')
    parser.add_argument('--bottom-right', help='YouTube video ID for bottom-right webcam')
    args = parser.parse_args()

    # Build webcam IDs from args or use defaults
    webcam_ids = DEFAULT_WEBCAM_IDS.copy()
    if args.top_left:
        webcam_ids['top-left'] = args.top_left
    if args.top_right:
        webcam_ids['top-right'] = args.top_right
    if args.bottom_left:
        webcam_ids['bottom-left'] = args.bottom_left
    if args.bottom_right:
        webcam_ids['bottom-right'] = args.bottom_right

    main(debug=args.debug, webcam_ids=webcam_ids)
