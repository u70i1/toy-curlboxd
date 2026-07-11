from pyboxen import boxen
from fastapi import FastAPI, HTTPException
from scrape import parse
from fastapi.responses import PlainTextResponse

app = FastAPI()


def format_review(review: str):
    tagses = {"bold": ["b", "strong"], "italic": ["em", "i"]}
    review = review.replace("<p>", "\n")
    review = review.replace("</p>", "\n")

    for style, tags in tagses.items():
        for tag in tags:
            review = review.replace(f"<{tag}>", f"[{style}]")
            review = review.replace(f"</{tag}>", f"[/{style}]")

    return review


def star_maker(rating: float):
    rating = float(rating)
    star = "★"
    half = "½"

    if not rating.is_integer():
        rating -= 0.5
        result = star * int(rating)
        return f"[yellow bold]{result}{half}[/]"
    else:
        result = star * int(rating)
        return f"[yellow bold]{result}[/]"


@app.get("/{username}")
def fetch(username: str, page: int = 1, amount_per_page: int = 5):
    try:
        activities = parse(username, page, amount_per_page)
    except KeyError:
        raise HTTPException(status_code=500, detail="something bad might happen :(")

    all_reviews = []
    for activity in activities:
        (
            link,
            watched_date,
            film_title,
            film_year,
            member_rating,
            member_like,
            member_rewatch,
            tmdb_movieid,
            review,
        ) = activity.values()

        review_box = boxen(
            f"{format_review(review)}",
            title=f"{film_title} - {star_maker(member_rating)} {'[red bold]:heart:[/]' if member_like else ''}",
            color="#eeeeee",
            padding=(0, 1),  # type: ignore
        )
        all_reviews.append(review_box)

    return PlainTextResponse("\n\n".join(all_reviews))
