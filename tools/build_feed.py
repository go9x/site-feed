"""Builds nine-feed.json: the public data the go9x.com navbar and 9x Pro hero read.

events  = sessions in the public 9x Live Circle space only (never client workshop spaces),
          tier from the Circle topic, Luma registration link matched by start time.
latest  = newest videos and articles for the navbar's Latest carousel.

Usage: python3 build_feed.py --circle circle-events.json [--latest latest.json] [--out nine-feed.json]
circle-events.json = a Circle list_events response (records[]).
"""
import argparse, json, urllib.request
from datetime import datetime, timezone

LIVE_SPACE = "9x-live-d45ed9"              # the only Circle space allowed in the public feed
TOPIC_PRO, TOPIC_FREE = 556339, 556340     # "Pro workshops" / "Free workshops"
LUMA_CAL = "cal-VeJrmqwI5MyZGKH"           # luma.com/9x-live


def luma_links():
    url = f"https://api.lu.ma/calendar/get-items?calendar_api_id={LUMA_CAL}&period=future&pagination_limit=50"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    return {e["event"]["start_at"]: "https://luma.com/" + e["event"]["url"] for e in data.get("entries", [])}


def build_events(records, luma):
    now = datetime.now(timezone.utc)
    out = []
    for e in sorted(records, key=lambda x: x["starts_at"]):
        if (e.get("space") or {}).get("slug") != LIVE_SPACE:
            continue
        end = datetime.fromisoformat(e["ends_at"].replace("Z", "+00:00"))
        if end < now:
            continue
        kind = "pro" if TOPIC_PRO in (e.get("topics") or []) else "live"
        ev = {"title": e["name"].strip(), "kind": kind, "start": e["starts_at"], "end": e["ends_at"],
              "cover": e.get("cover_image_url") or "", "circle": e["url"]}
        if kind == "live" and e["starts_at"] in luma:
            ev["luma"] = luma[e["starts_at"]]
        out.append(ev)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--circle", required=True)
    ap.add_argument("--latest", default="latest.json")
    ap.add_argument("--out", default="nine-feed.json")
    a = ap.parse_args()
    records = json.load(open(a.circle))["records"]
    feed = {
        "version": 1,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "events": build_events(records, luma_links()),
        "latest": json.load(open(a.latest)),
    }
    assert feed["events"], "no upcoming events: refusing to publish an empty feed"
    assert len(feed["latest"]) >= 3, "latest needs at least 3 items"
    json.dump(feed, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"{a.out}: {len(feed['events'])} events, {len(feed['latest'])} latest")


if __name__ == "__main__":
    main()
