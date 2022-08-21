from discord import Embed
from bs4 import BeautifulSoup as bs
import requests
import re

from helpers import general_helper


async def get_themes_link(malID: int):
    links = {
        "name": {},
        "op": {},
        "ed": {}
    }

    html = requests.get(f"https://myanimelist.net/anime/{malID}/").text
    soup = bs(html, "html.parser")

    links["name"] = name = soup.find("div", id="myanimelist").find(
        "div", class_="wrapper").find("div", id="contentWrapper").find("strong").string

    ending_divs = soup.find(
        "div", attrs={"class": "theme-songs js-theme-songs ending"})
    opening_divs = soup.find(
        "div", attrs={"class": "theme-songs js-theme-songs opnening"})  # opnening lmfao

    opening_themes = opening_divs.find("table", recursive=False).find_all("tr")
    ending_themes = ending_divs.find("table", recursive=False).find_all("tr")

    for theme in opening_themes:

        name = theme.find("span", attrs={"class": "theme-song-title"}).contents
        url = theme.find("input", value=re.compile("spotify"))["value"]

        links["op"][name[0]] = url

    for theme in ending_themes:

        name = theme.find("span", attrs={"class": "theme-song-title"}).contents
        url = theme.find("input", value=re.compile("spotify"))["value"]

        links["ed"][name[0]] = url

    return links


async def get_themes_embed(malID: int) -> Embed:

    links = await get_themes_link(malID)

    embd = (await general_helper.get_information_embed(
        title="Op/Ed for {}".format(links["name"].capitalize())))

    op_themes = ""
    ed_themes = ""

    for name, url in links["op"].items():
        op_themes += "**{}** : [Spotify]({}) \n".format(name, url)

    for name, url in links["ed"].items():
        ed_themes += "**{}** : [Spotify]({}) \n".format(name, url)

    embd.add_field(
        name="Openings",
        value=op_themes,
        inline=False
    )

    embd.add_field(
        name="Endings",
        value=ed_themes,
        inline=False
    )

    return embd
