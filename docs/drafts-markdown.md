# Draft Markdown dialect

Draft bodies are exchanged as Markdown, over REST (`body` of
`POST /api/v1/drafts` and `PUT /api/v1/drafts/{draft_id}`, returned by
`GET /api/v1/drafts/{draft_id}`) and over MCP (`create_draft`, `update_draft`,
`get_draft`). The Markdown is a small dialect: plain Markdown plus a few
extensions for the things Substack drafts contain that Markdown cannot say
(buttons, image size and watermark, alignment, callouts, horizontal rules).

The dialect is **lossless**. `get_draft` returns every node and attribute of the
stored draft, including nodes the dialect has no syntax for, and feeding that
Markdown back to `update_draft` stores an identical body. An agent can therefore
read a draft the author edited in the web editor, change one paragraph, and write
it back without losing anything else.

- [Workflow](#workflow)
- [Quick reference](#quick-reference)
- [Text, headings, lists, quotes](#text-headings-lists-quotes)
- [Inline formatting](#inline-formatting)
- [Horizontal rule](#horizontal-rule)
- [Buttons](#buttons)
- [Images](#images)
- [Alignment](#alignment)
- [Callouts](#callouts)
- [Code, LaTeX and Datawrapper](#code-latex-and-datawrapper)
- [Verbatim nodes (`substack-node`)](#verbatim-nodes-substack-node)
- [Instructions and state](#instructions-and-state)
- [Escaping](#escaping)
- [Errors and conflicts](#errors-and-conflicts)
- [Input details](#input-details)

## Workflow

1. `get_draft` returns `body` (dialect Markdown) and `updated_at`.
2. Edit the Markdown. Keep every block you do not mean to change exactly as it
   was returned.
3. `update_draft` with the new `body` and `expected_updated_at` set to the
   `updated_at` from step 1. If the author (or anything else) changed the draft
   in the meantime, the update is refused instead of overwriting their edit:
   fetch the draft again and redo the edit on top of the new version. A
   successful update returns the new `updated_at`; use it for the next update.

`expected_updated_at` is optional but always worth passing. The check is a read
followed by a write, so it catches edits made since your last read; it is not an
atomic lock against an edit that lands between the two requests.

## Quick reference

| Element | Markdown |
|---|---|
| Horizontal rule | `---` on its own line |
| Button | `::button[Subscribe now]{href=subscribe}` (also `share`, `comment`, or a URL) |
| Image size | `![alt](src){size=normal}` (also `large`, `full`) |
| Image watermark | `![alt](src){watermark}` or `{watermark=8%}` |
| Default alignment | `::defaults{align=justify}` as the first block |
| Aligned section | `:::align{center}` ... `:::` |
| Callout | `:::callout` ... `:::` |
| Pullquote | `\|> text` |
| Blockquote | `> text` |
| LaTeX | `$$` ... `$$` |
| Code | ```` ```lang ```` ... ```` ``` ```` |
| Datawrapper chart | ```` ```datawrapper ```` + chart URL ... ```` ``` ```` |
| Anything else | ```` ```substack-node ```` + JSON ... ```` ``` ```` (move or delete only) |

## Text, headings, lists, quotes

- A blank line separates blocks. Consecutive non-blank lines of text belong to
  the same paragraph and are joined with a space; the dialect has no hard line
  break.
- `#` to `######` followed by a space is a heading.
- `-`, `*` or `+` followed by a space is a bullet list item; `1.` (any number,
  followed by a space) is an ordered list item, renumbered from 1. A list item is
  one paragraph. Nested lists are not part of the dialect: an indented line
  (`  - sub`) does not nest, it becomes paragraph text. A draft that contains a
  nested list comes back as a [`substack-node`](#verbatim-nodes-substack-node) block.
- `> text` is a blockquote and `|> text` is a pullquote. The body after the
  marker is parsed as Markdown again, so quotes can hold several paragraphs
  (separated by a bare `>` line) and lists.
- **Adjacent blocks of the same kind.** Two blockquotes, two pullquotes, two
  bullet lists or two ordered lists directly after one another would merge into
  one block when read back. `get_draft` therefore puts the second one in an
  `:::align{...}` container, which keeps them apart. Write them the same way when
  you add one next to another.

## Inline formatting

| Markdown | Result |
|---|---|
| `**text**` | bold |
| `*text*` | italic (`_text_` is not italic: underscores are plain text) |
| `~~text~~` | strikethrough |
| `` `text` `` | inline code (cannot be combined with other marks) |
| `[text](https://example.com)` | link |

Bold, italic and strikethrough combine freely (`***both***`, `**~~x~~**`) and can
sit inside a link text (`[**bold link**](url)`). A delimiter run that has
whitespace (or the start or end of the text) on both sides is literal, so
`2 * 3` stays `2 * 3`. A delimiter that never closes is literal too.

Marks the dialect has no syntax for (for example underline) make the whole block
come back as a `substack-node` block; links whose attributes differ from the
default (anything but `href`) do the same.

## Horizontal rule

`---` alone on a line is a horizontal rule. A `---` inside a sentence is text.

## Buttons

```markdown
::button[Subscribe now]{href=subscribe}
::button[Share this post]{href=share}
::button[Leave a comment]{href=comment}
::button[Read the docs]{href=https://example.com/docs}
```

`href=subscribe`, `share` and `comment` are Substack's own button targets (they
are stored as the placeholders `%%checkout_url%%`, `%%share_url%%` and
`%%half_magic_comments_url%%`, which Substack fills in when the post is sent).
Any other `href` is a URL used as written. The text goes between the brackets;
write `\]` and `\\` for a literal `]` and `\`. The text and `href` are both
required. Other button attributes (`action`, `class`) can be set the same way as
`href`, in the attribute block, but are normally left out.

## Images

An image is a line of its own:

```markdown
![Alt text](https://example.com/photo.jpg)
![Alt text](https://example.com/photo.jpg){size=large}
![Alt text](https://example.com/photo.jpg){size=full watermark=8%}
```

- **Source.** A URL on one of Substack's image hosts, `substack-post-media.s3.amazonaws.com`
  or `substackcdn.com` (for example one returned by `upload_image`), is kept as it
  is, with no request. The check is on the host: any other URL, including
  `cdn.substack.com` and path-style S3 URLs such as
  `s3.amazonaws.com/substack-post-media/...`, is treated as external, downloaded
  and uploaded to Substack when the draft is written.
- **`size=normal|large|full`.** Presets matching the web editor's image sizes
  (all three are centered and not fullscreen; `large` is 1200 px wide, `full` is
  full width). When an image's size attributes do not match a
  preset exactly, `get_draft` writes the raw attributes instead
  (`{imageSize=... resizeWidth=... align=... fullscreen=...}`, whichever differ
  from the defaults); keep them as they are.
- **Other attributes.** Any further `{key=value}` in the block is stored on the
  image as written (for example `href=...` to make it a link). Values are typed:
  whole numbers, `true`, `false` and `null` are not strings; quote anything else
  that contains spaces or `{ } = "` with double quotes (`title="a b"`, with `\"`
  and `\\` as escapes). A bare key means `true`.

### Watermark

`{watermark}` overlays the publication's logo, the way the web editor's
"watermark" button does. It is an *instruction*: it makes the gateway call
Substack's watermark endpoint while writing the draft.

| Attribute | Meaning |
|---|---|
| `watermark` | default watermark: 6 % of the image width, top-right, opacity 65 |
| `watermark=N%` | logo width as a percentage of the image width (above 0, up to 100) |
| `watermark-pos=top-right\|top-left\|bottom-right\|bottom-left` | corner (default `top-right`) |
| `watermark-opacity=0..100` | opacity (default 65) |

`watermark-pos` and `watermark-opacity` are errors without `watermark`.

The gateway needs the image's pixel size to place the logo. It has it for an
image it just uploaded, and for a Substack image whose file name ends in
`_<width>x<height>` before the extension (the usual form, for example
`photo_1536x1024.png`). For any other image the request is refused with an
error naming the image, and nothing is sent to Substack's watermark endpoint:
upload it with `upload_image` first, or leave the watermark off.

A watermarked image is stored with two URLs: the watermarked picture and the
original. `get_draft` shows both, as *state*:

```markdown
![Alt](https://.../watermarked_1536x1024.png){size=large original=https://.../original_1536x1024.png}
```

`original=` is the pristine image. Writing the line back unchanged only
re-stores those two URLs. To change the watermark, keep `original=` and add the
instruction; the logo is then regenerated from the original:

```markdown
![Alt](https://.../watermarked_1536x1024.png){size=large original=https://.../original_1536x1024.png watermark=10%}
```

To remove the watermark, delete `original=` and use the original URL as the image
source.

## Alignment

Paragraph and heading alignment is one of `left`, `center`, `right`, `justify`
or `default` (Substack's default, no explicit alignment).

### `::defaults{align=...}`

```markdown
::defaults{align=justify}

First paragraph...
```

Sets the alignment of every paragraph in the draft that is not inside an
`:::align` container: top level, list items, quotes and callouts. It does not
apply to headings. It must be the very first block, and there can be only one. A
draft with no `::defaults` line has the default alignment.

`get_draft` writes this line when it helps: it picks the alignment most
paragraphs have (on a tie, none).

### `:::align{...}`

```markdown
:::align{center}
A centered paragraph.

## A centered heading
:::
```

Sets the alignment of the paragraphs and headings inside, whatever
`::defaults` says (`:::align{default}` forces the default alignment). The
container ends at a line holding only `:::`.

- Allowed at top level, inside `:::callout` and inside `>` / `|>` quotes.
- Containers do not nest.
- A whole list can sit inside one container (all its items then share that
  alignment), but a container cannot open or close in the middle of a list. A
  list whose items have different alignments comes back as a `substack-node`
  block.

## Callouts

```markdown
:::callout
Anything that goes in a callout, as ordinary blocks.
:::
```

A callout is allowed at top level only: not inside a quote or an `:::align`
container, and callouts do not nest. `:::callout` takes no attributes. An
`:::align` container can sit inside it.

## Code, LaTeX and Datawrapper

**Code**

````markdown
```python
print("hello")
```
````

The text after the opening backticks is the language. The body is kept exactly as
written. A code block whose text contains a line starting with three backticks is
returned as a `substack-node` block. Substack's per-block id is shown as an
attribute and must be kept: ```` ```python {nodeId=abc123} ````.

**LaTeX**

```markdown
$$ x^2 + y^2 = z^2 $$

$$ {id=QWERTYUIOP}
\int_0^1 x\,dx
$$
```

A one-line `$$expr$$` or a block between `$$` lines. A block that already exists
in the draft shows its Substack id as `{id=...}` on the opening line; keep it.
A new block gets a generated id.

**Datawrapper**

````markdown
```datawrapper
https://www.datawrapper.de/_/aBcDe/
```
````

The body is the chart's URL (`datawrapper.de/_/<id>` or `dwcdn.net/<id>`). This
is an *instruction*: Substack's embed endpoint is asked for the chart's metadata
while the draft is written. A chart already in a draft comes back from
`get_draft` as a `substack-node` block, not as a `datawrapper` fence.

## Verbatim nodes (`substack-node`)

````markdown
```substack-node
{
  "type": "digestPostEmbed",
  "attrs": { "...": "..." }
}
```
````

When a block cannot be written as readable dialect syntax without losing
anything, `get_draft` writes it as a `substack-node` fence holding the node's JSON.
This happens for node types the dialect does not know (including ones Substack
adds later) such as `digestPostEmbed`, charts that are already in the draft,
unsupported marks, nested lists, empty paragraphs and an alignment the dialect
cannot place. It is the escape hatch that makes the round trip lossless.

The rule: **move or delete a `substack-node` block, never edit it.** It is not
meant to be edited; a block you change by hand may be rejected or stored
differently from what you intended. Writing it back unchanged stores the original
node.

The fence takes no attributes and must hold one JSON object with a `"type"`. A
node type starting with `_` (the gateway's own internal placeholders) is
rejected. The gateway can also write a block as a `substack-node` fence when it
finds that its readable form would not read back identically; that is expected
and harmless.

## Instructions and state

Some syntax is an *instruction*: it makes the gateway do something while the
draft is written. What `get_draft` returns is *state*: it reproduces the stored
nodes and triggers nothing.

| Syntax | Kind | What happens on write |
|---|---|---|
| `![..](external-url)` | instruction | the image is uploaded to Substack |
| `{watermark...}` | instruction | the watermark is generated (see [Watermark](#watermark)) |
| ```` ```datawrapper ```` + URL | instruction | the chart's metadata is fetched |
| `![..](substack-url)` | state | kept as is |
| `{original=URL}` | state | stored as the image's non-watermarked source |
| `substack-node` fence | state | stored as given |
| everything else | state | stored as given |

So a `get_draft` result written back unchanged does not upload, watermark or
fetch anything.

## Escaping

A backslash before any ASCII punctuation character makes it literal: `\*`, `\[`,
`\#`, `\\`. `get_draft` escapes `\ * ` [ ] ~ { }` inside text for you, and puts a
backslash in front of a line that would otherwise open a block (`#`, `>`, `|>`,
`-`, `+`, `1.`, `::`, `$$`, ```` ``` ````, `!`). Write the same escapes when your
text needs them.

To write a line that *looks* like dialect syntax as plain text, start it with a
backslash:

```markdown
\::button[this stays text]{href=subscribe}

\:::align{center}

\```not a fence
```

This matters because a line that starts with a directive name (`::button`,
`::defaults`, `:::align`, `:::callout`) or with three backticks, and is not valid
syntax, is an **error** rather than text. That keeps typos from silently becoming
body text. A `---` or `{size=large}` inside a sentence, and a line such as `:::note`
(not one of the names above), is ordinary text. A bare `:::` that closes no open
container is an error as well (write `\:::` for literal text).

## Errors and conflicts

| Situation | REST | MCP |
|---|---|---|
| Malformed dialect (unclosed `:::align` / `:::callout` or fence, `::defaults` not the first block, a malformed directive or attribute, an invalid `substack-node` fence, a watermark on an image of unknown size) | `400`, `detail` starts with `line N:` for syntax errors | tool error with the same message |
| `expected_updated_at` differs from the draft's current `updated_at` | `409`; nothing is written | tool error saying the draft changed since it was read and must be fetched again; nothing is written |

Syntax errors name the 1-based line of the input, so an agent can fix the exact
spot. After a conflict, call `get_draft` again, apply the edit to the new body and
retry with the new `updated_at`.

## Input details

- `\r\n` and `\r` line endings are accepted, trailing spaces and tabs after
  syntax lines (`---`, `:::`, fences) are ignored, and any number of blank lines
  may separate blocks.
- Input without a single real newline whose text contains a literal `\n` (a
  backslash and an `n`, as JSON-escaped clients sometimes send) has those
  sequences turned into newlines. Multi-line input is never rewritten this way,
  so `\neg` in LaTeX is safe. `get_draft` output always ends with a newline.
- Drafts created by older versions of the gateway (paragraphs and headings without
  explicit alignment) read back as plain Markdown and need no special handling.
