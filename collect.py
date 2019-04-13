"""Parse Wilma's IG."""

import sys
from time import sleep

from bs4 import BeautifulSoup as Soup

from utils import get_driver


def parse_html(
        html,
        post_set,
):
    """Parse soup for posts."""
    soup = Soup(html, "lxml")
    posts_article = soup.find("article", class_="FyNDV")
    for post in posts_article.find_all("div", class_="v1Nh3"):
        post_link = post.find("a")
        post_link = post_link["href"]
        if post_link not in post_set:
            with open("posts.txt", "a") as output:
                output.write(f"{post_link}\n")
        post_set.add(post_link)


def browse_page_for_posts(
        url,
):
    """Browser IG URl."""
    post_set = set()

    driver = get_driver()
    driver.get(url)

    progress = 0
    last_height = driver.execute_script(
        "return document.body.scrollHeight;"
    )
    while True:
        while progress < last_height:
            progress = min(progress + 250, last_height)
            driver.execute_script(
                f"window.scrollTo(0, {progress});"
            )
            parse_html(driver.page_source, post_set)

        sleep(1)

        new_height = driver.execute_script(
            "return document.body.scrollHeight;"
        )
        if new_height == last_height:
            break
        last_height = new_height

    return post_set


def main(
):
    """Process Wilma's IG posts."""
    browse_page_for_posts(
        f"https://www.instagram.com/{sys.argv[1]}/"
    )

if __name__ == "__main__":
    main()
