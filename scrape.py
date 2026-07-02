import feedparser
import re

def parse(username, page, amount_per_page):
    start = (page - 1) * amount_per_page
    end = start + amount_per_page

    feed = feedparser.parse(f"https://letterboxd.com/{username}/rss/")

    entry = feed.entries[start:end]

    clean_entry = []
    for e in entry:
        summary = re.sub(r"<.*?>", "", e.summary).strip() # type: ignore
        clean_entry.append({
            "link": e.link,
            "watched_date": e.letterboxd_watcheddate,
            "film_title": e.letterboxd_filmtitle,
            "film_year": e.letterboxd_filmyear,
            "member_rating": e.letterboxd_memberrating,
            "member_like": True if e.letterboxd_watcheddate == "Yes" else False,
            "member_rewatch": True if e.letterboxd_rewatch == "Yes" else False,
            "tmbd_movieid": e.tmdb_movieid,
            "review": summary
        })

    return clean_entry
