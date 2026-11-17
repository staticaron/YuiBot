import re

import httpx
from bs4 import BeautifulSoup as bs

from helpers import general_helper
from views.scroller import Scroller


async def get_themes_link(malID: int):
    links = {"name": "", "op": {}, "ed": {}}

    async with httpx.AsyncClient() as client:
        html = (await client.get(f"https://myanimelist.net/anime/{malID}/")).text

    soup = bs(html, "html.parser")

    links["name"] = (
        soup.find("div", id="myanimelist")
        .find("div", class_="wrapper")
        .find("div", id="contentWrapper")
        .find("strong")
        .string
    )

    ending_divs = soup.find("div", attrs={"class": "theme-songs js-theme-songs ending"})
    opening_divs = soup.find(
        "div", attrs={"class": "theme-songs js-theme-songs opnening"}
    )  # opnening lmfao

    opening_themes = opening_divs.find("table", recursive=False).find_all("tr")
    ending_themes = ending_divs.find("table", recursive=False).find_all("tr")

    for theme in opening_themes:
        name_container = theme.find("span", attrs={"class": "theme-song-title"})

        if name_container is None:
            continue

        name = name_container.contents

        url_container = theme.find("input", value=re.compile("spotify"))

        url = url_container["value"] if url_container is not None else ""

        links["op"][name[0]] = url

    for theme in ending_themes:
        name_container = theme.find("span", attrs={"class": "theme-song-title"})

        if name_container is None:
            continue

        name = name_container.contents

        url_container = theme.find("input", value=re.compile("spotify"))

        url = url_container["value"] if url_container is not None else ""

        links["ed"][name[0]] = url

    return links


async def get_themes_embed(malID: int) -> Scroller:

    links = await get_themes_link(malID)

    op_themes = ""
    ed_themes = ""

    for name, url in links["op"].items():
        op_themes += f"**{name}**: [Spotify]({url}) \n"

    for name, url in links["ed"].items():
        ed_themes += f"**{name}**: [Spotify]({url}) \n"

    op_embd = await general_helper.get_information_embed(
        title="Openings for {}".format(links["name"].title())
    )

    op_embd.description = op_themes

    ed_embd = await general_helper.get_information_embed(
        title="Endings for {}".format(links["name"].title())
    )

    ed_embd.description = ed_themes

    return Scroller(embed_pages=[op_embd, ed_embd], show_all_btns=False)
