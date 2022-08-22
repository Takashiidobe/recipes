#!/usr/bin/env python3

import re

from recipe_scrapers import scrape_me

def scrape_recipe(url):
    scraper = scrape_me(url, wild_mode=True)
    s = ""
    snake_cased_title = (
        scraper.title()
        .replace(" ", "-")
        .replace("(", "")
        .replace(")", "")
        .replace("&", "and")
        .lower()
    )
    snake_cased_title = re.sub("[^a-zA-Z-]", "", snake_cased_title)
    snake_cased_title = snake_cased_title + ".md"

    if scraper.image() and scraper.title():
        s += "---\n"
        s += f"title: {scraper.title()}\n"
        s += "---\n"
        s += "\n"
        s += f"![{scraper.title()}]({scraper.image()})\n\n"
    if scraper.title():
        s += f"# {scraper.title()}\n\n"
    if scraper.url:
        s += f"- From: [link]({scraper.url})\n\n"
    try:
        scraper.total_time()
        s += f"- Cooking Time: {scraper.total_time()} minutes\n\n"
    except Exception:
        pass
    if scraper.ingredients():
        s += "## Ingredients:\n\n"
        for i in scraper.ingredients():
            s += f"- {i}\n"
        s += "\n"
    if scraper.instructions():
        s += "## Instructions:\n\n"
        s += scraper.instructions().replace("\n", "\n\n") + "\n"

    with open(f"src/{snake_cased_title}", "w+") as f:
        f.write(s)

    return (
        snake_cased_title,
        scraper.title().replace("(", "").replace(")", "").replace("&", "and"),
    )

recipes = []

with open("recipes_to_scrape.txt", "r") as f:
    for line in f:
        print(line)
        if line:
            recipes.append(scrape_recipe(line.strip()))

with open("./src/index.md", "a") as f:
    for (file_name, title) in recipes:
        f.write(f"- [{title.title()}](./{file_name})\n")
