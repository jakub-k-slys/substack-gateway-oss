from __future__ import annotations

from xml.etree.ElementTree import Element, SubElement, tostring

from gateway_pro.services.profile_feed import AtomFeedEntry, AtomFeedPage

_ATOM_NS = "http://www.w3.org/2005/Atom"


def render_atom_feed(page: AtomFeedPage) -> str:
    feed = Element("feed", xmlns=_ATOM_NS)
    SubElement(feed, "id").text = page.feed_id
    SubElement(feed, "title").text = page.title
    SubElement(feed, "updated").text = page.updated_at

    author = SubElement(feed, "author")
    SubElement(author, "name").text = page.author.name
    SubElement(author, "uri").text = page.alternate_url

    if page.subtitle:
        SubElement(feed, "subtitle").text = page.subtitle
    if page.icon_url:
        SubElement(feed, "icon").text = page.icon_url

    _append_link(feed, href=page.self_url, rel="self")
    _append_link(feed, href=page.alternate_url, rel="alternate")
    if page.next_url:
        _append_link(feed, href=page.next_url, rel="next")

    for entry in page.entries:
        _append_entry(feed, entry)

    return tostring(feed, encoding="utf-8", xml_declaration=True).decode("utf-8")


def _append_entry(feed: Element, entry: AtomFeedEntry) -> None:
    node = SubElement(feed, "entry")
    SubElement(node, "id").text = entry.entry_id
    SubElement(node, "title").text = entry.title
    SubElement(node, "published").text = entry.published_at
    SubElement(node, "updated").text = entry.updated_at
    _append_link(node, href=entry.url, rel="alternate")

    author = SubElement(node, "author")
    SubElement(author, "name").text = entry.author.name
    SubElement(author, "uri").text = f"https://substack.com/@{entry.author.handle}"

    if entry.summary:
        SubElement(node, "summary").text = entry.summary
    if entry.content_html:
        content = SubElement(node, "content", type="html")
        content.text = entry.content_html


def _append_link(node: Element, *, href: str, rel: str) -> None:
    SubElement(node, "link", href=href, rel=rel)
