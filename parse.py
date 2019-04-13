"""Parse Wilma's IG."""

import json
import os
from urllib.parse import urljoin

from bs4 import BeautifulSoup as Soup

from utils import get_driver


def process_html(
        driver,
        output_name,
):
    """Process IG post."""
    post_md = {}
    soup = Soup(driver.page_source, "lxml")

    # Get likes if image, get views if video
    likes_div = soup.find("div", class_="Nm9Fw")
    if likes_div:
        num_likes = likes_div.find("span").get_text()
        post_md["type"] = "image"
        post_md["num_likes"] = num_likes
    else:
        views_div = soup.find("div", class_="HbPOm")
        num_views = views_div.find("span", class_="").get_text()
        post_md["type"] = "video"
        post_md["num_views"] = num_views

    # Get post timestamp
    timestamp_div = soup.find("div", class_="k_Q0X")
    timestamp = timestamp_div.find("time")["datetime"]
    post_md["timestamp"] = timestamp

    # Keep clicking "Load more comments" button while exists on page
    comments_ul = soup.find("ul", class_="k59kT")
    post_md["comments"] = []
    if comments_ul:
        while comments_ul.find("button", class_="Z4IfV"):
            print("\tFound \"Load more comments\" button, clicking")
            driver.find_element_by_css_selector(".Z4IfV").click()
            soup = Soup(driver.page_source, "lxml")
            comments_ul = soup.find("ul", class_="k59kT")

        # Get post comments
        comments_li = comments_ul.find_all("li")
        post_md["num_comments"] = len(comments_li)

        for comment in comments_li:
            try:
                author = (
                    comment.find("h2") or
                    comment.find("h3")
                ).get_text()
            except AttributeError:
                print(comment)
            text = comment.find("span").get_text()
            post_md["comments"].append({
                "author": author,
                "text": text,
            })
    else:
        post_md["num_comments"] = 0

    with open(output_name, "w", encoding="utf-8") as output_json:
        output_json.write(
            json.dumps(post_md, indent=4, sort_keys=True, ensure_ascii=False),
        )


def main(
):
    """Process Wilma's IG posts."""
    driver = get_driver()
    with open("posts.txt") as posts:
        for post in posts:
            post = post.strip()
            print(post)
            driver.get(urljoin(
                "https://www.instagram.com/",
                post,
            ))
            os.makedirs("posts-data", exist_ok=True)
            process_html(
                driver,
                f"posts-data/{post.split('/')[2]}.json",
            )


if __name__ == "__main__":
    main()
