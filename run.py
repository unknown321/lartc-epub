#!/usr/bin/env python3

from bs4 import BeautifulSoup
import logging
import os
import pathlib
from ebooklib import epub

logger = logging.getLogger(__name__)

def run(lang="en"):
    epub_name = "Linux Advanced Routing and Traffic Control HOWTO.epub"
    book = epub.EpubBook()
    book.set_language(lang)
    book.set_title("Linux Advanced Routing & Traffic Control HOWTO")
    book.add_author("Bert Hubert")
    book.add_author("Thomas Graf", file_as="section author")
    book.add_author("Greg Maxwell", file_as="section author")
    book.add_author("Remco van Mook", file_as="section author")
    book.add_author("Martijn van Oosterhout", file_as="section author")
    book.add_author("Paul B Schroeder", file_as="section author")
    book.add_author("Jasper Spaans", file_as="section author")
    book.add_author("Pedro Larroy", file_as="section author")
    book.add_author(author="unknown321", file_as="epub creator")

    css = "base.css"
    with open(css) as f:
        content = f.read()
    css_entry = epub.EpubItem(
        uid=css,
        file_name=css,
        media_type="text/css",
        content=content,
    )
    book.add_item(css_entry)

    index = open("howto/index.html",'r').read()
    soup = BeautifulSoup(index, 'lxml')
    dts = soup.find_all("dt")
    for d in dts:
        link = d.find("a")
        if link:
            if "#" in link["href"]:
                book.toc.append(epub.Link(link["href"].split("#")[0], d.text, d.text))
                continue
            rawpage = open("howto/" + link["href"]).read()
            page = BeautifulSoup(rawpage, 'lxml')
            header = page.find("div", {"class":"NAVHEADER"})
            if header:
                header.replace_with("")

            footer = page.find("div", {"class":"NAVFOOTER"})
            if footer:
                footer.replace_with("")

            c1 = epub.EpubHtml(title=d.text, file_name=link["href"])
            c1.content = str(page.prettify(formatter="minimal"))
            c1.add_item(css_entry)

            book.add_item(c1)
            book.spine.append(c1)
            book.toc.append(epub.Link(link["href"], d.text, d.text))

    book.add_item(epub.EpubNav())
    book.add_item(epub.EpubNcx())
    if pathlib.Path(epub_name).exists():
        os.remove(epub_name)
    epub.write_epub(epub_name, book)
    logger.info(f"Generated EPUB: {epub_name}")


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('Started')
    run()
    logger.info('Finished')


if __name__ == '__main__':
    main()

