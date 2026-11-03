# site-feed

Public data feed for go9x.com. The website's mega navbar (Resources → Next 9x Live, Latest) and the 9x Pro hero (upcoming sessions stack) read **`nine-feed.json`** from GitHub Pages:

```
https://go9x.github.io/site-feed/nine-feed.json
```

Updating this file updates the website within about 10 minutes (GitHub Pages caches it up to 10 min). **No Framer publish is needed.**

**This is the only feed file.** The website reads nothing else. The Framer code files `NineFeed.tsx` (branch home-revamp) and `NineFeed_1.tsx` (branch improved-heros) are the reader, the same code under two names; they are never edited by the routine.
Visitors fetch it once per visit. If it can't be loaded, the site shows evergreen backups (no dates).

## Who updates it

A routine (agent) rebuilds the file and commits it to `main`:
- **daily**, and
- **right after each 9x Live**, so the next session shows up.

## Format (version 1)

```json
{
  "version": 1,
  "updated": "2026-11-02T08:00:00Z",
  "events": [
    {
      "title": "ChatGPT Work for Beginners",
      "kind": "live",
      "start": "2026-11-05T16:00:00.000Z",
      "end": "2026-11-05T17:00:00.000Z",
      "cover": "https://assets-v2.circle.so/…",
      "circle": "https://academy.go9x.com/c/9x-live-d45ed9/…",
      "luma": "https://luma.com/9x-w5ql"
    }
  ],
  "latest": [
    { "kind": "Video", "meta": "22:49", "title": "…", "href": "https://www.youtube.com/watch?v=…", "img": "https://i.ytimg.com/vi/…/mqdefault.jpg" },
    { "kind": "Article", "title": "…", "href": "/blog/…", "img": "https://framerusercontent.com/images/…" }
  ]
}
```

### `events`: public sessions from the 1st of this month onwards (past ones included)
| Field | Rule |
|---|---|
| `title` | Session name as on Circle. |
| `kind` | `"live"` = free 9x Live, `"pro"` = 9x Pro workshop. In Circle: topic "Free workshops" / "Pro workshops". |
| `start`, `end` | ISO 8601 in UTC. `end` is required: the site shows "Live now" between `start` and `end`. |
| `cover` | The Circle cover image URL (1024×366). Optional: the site draws an HTML cover if it's missing or broken. |
| `circle` | The Circle event page. |
| `luma` | Free sessions only: the Luma registration page (public calendar `luma.com/9x-live`). The navbar links here. |

**Only sessions from the public 9x Live space** (`academy.go9x.com/c/9x-live-d45ed9`). Never add client workshop spaces: this file is public, and client names must not appear in it.
Keep every session from the 1st of this month (Berlin time), past ones included: the 9x Pro hero shows the whole month, past sessions included (shown with their date only). The navbar only uses the upcoming ones. Sessions from earlier months drop out.

### `latest`: newest content, newest first
6 items, alternating videos and articles when possible.
| Field | Rule |
|---|---|
| `kind` | `"Video"` or `"Article"`. |
| `meta` | Videos: duration, e.g. `"22:49"`. Optional. |
| `title` | As published. |
| `href` | YouTube URL, or the blog path (`/blog/<slug>`). Published posts only. |
| `img` | YouTube `mqdefault.jpg` thumbnail, or the article's cover. |

## Checks before committing
- `version` is `1`, `events` has at least one session that hasn't ended, `latest` has at least 3 items.
- Every link opens.
- The file is valid JSON. The site ignores an invalid file and falls back to the last good copy, then to the backups.

`tools/build_feed.py` is a reference builder: it turns a Circle `list_events` response into `events` and matches Luma links by start time.
