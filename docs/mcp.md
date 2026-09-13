# MCP

The MCP server is mounted at `/mcp` and served over streamable HTTP
(stateless). It is assembled from each domain's `_mcp` capability (see
`CLAUDE.md` for the trio layout) and currently exposes 43 tools.

## Credentials and the `token` argument

Every authenticated tool takes an optional `token` argument: a
base64-encoded JSON object of `publication_url`, `substack_sid`, and
`connect_sid` — the same shape used for the REST `x-gateway-token` header
(see [Authentication](authentication.md)).

- If `token` is supplied, it is always used.
- If it is omitted, the gateway asks the installed credential resolver
  (`gateway_core.credentials`) to map the authenticated MCP caller to
  Substack credentials.
- This repository installs no resolver. An omitted `token` therefore raises
  `MissingCredentialsError`, whose message tells the caller to pass `token`.
  An extension may install its own resolver via
  `GatewayExtension.get_credential_resolver`.

**The three `profiles` tools need no credentials at all** —
`get_profile`, `get_profile_posts`, and `get_profile_notes` read Substack's
public global API directly and take no `token` parameter. Every other tool
in this reference is authenticated in the sense above, including read-only
ones like `get_note`, `get_post`, and `get_post_comments`.

## Notes (7)

- `get_note(note_id, token=None)` — return a single note by ID.
- `create_note(content, token=None, attachment=None)` — convert Markdown
  `content` to a Substack note and publish it; `attachment` is an optional
  URL.
- `delete_note(note_id, token=None)` — delete a note.
- `like_note(note_id, token=None)` — like a note.
- `unlike_note(note_id, token=None)` — remove a like from a note.
- `reply_to_note(note_id, body, token=None)` — reply to a note or to any
  comment in its thread.
- `list_note_replies(note_id, token=None)` — list direct replies to a note
  (or any node in its thread).

## Posts (4)

- `get_post(post_id, token=None)` — return a post with its full content
  (HTML converted to Markdown).
- `like_post(post_id, token=None)` — like a post.
- `unlike_post(post_id, token=None)` — remove a like from a post.
- `restack_post(post_id, token=None)` — restack a post.

## Profiles (3) — no credentials required

- `get_profile(slug)` — return a public profile by handle.
- `get_profile_posts(slug, limit=25, cursor=None)` — return a page of posts
  for the profile.
- `get_profile_notes(slug, cursor=None)` — return a page of notes for the
  profile.

## Following (1)

- `get_my_following(token=None)` — list the profiles the authenticated user
  follows.

## Me (3)

- `get_me(token=None)` — return the authenticated user's own profile.
- `get_my_notes(token=None, cursor=None)` — return a page of the
  authenticated user's own notes.
- `get_my_posts(token=None, limit=25, cursor=None)` — return a page of the
  authenticated user's own posts.

## Comments (8)

- `get_post_comments(post_id, token=None)` — return the comments for a post.
- `create_post_comment(post_id, body, token=None)` — create a top-level
  comment on a post.
- `reply_to_post_comment(comment_id, body, token=None)` — reply to an
  existing comment.
- `get_post_comment(comment_id, token=None)` — return a single comment by
  ID.
- `delete_post_comment(comment_id, token=None)` — delete a comment.
- `list_post_comment_replies(comment_id, token=None)` — list replies to a
  comment.
- `like_post_comment(comment_id, token=None)` — like a comment.
- `unlike_post_comment(comment_id, token=None)` — remove a like from a
  comment.

## Drafts (10)

- `list_drafts(token=None, next=None)` — list drafts newest first, in pages
  of 10; `next` is an opaque cursor from a previous call.
- `get_draft(draft_id, token=None)` — fetch a draft by ID.
- `create_draft(token=None, title=None, subtitle=None, body=None)` — create
  a new draft.
- `update_draft(draft_id, token=None, title=None, subtitle=None, body=None)`
  — update only the fields actually passed.
- `delete_draft(draft_id, token=None)` — delete a draft.
- `get_ai_detection(draft_id, token=None)` — run Substack's Pangram
  AI-writing detection on a draft.
- `check_draft(draft_id, token=None)` — run Substack's pre-publish
  validation on a draft.
- `schedule_draft(draft_id, scheduled_at, token=None, post_audience="only_paid", email_audience="only_paid")`
  — schedule a draft for timed release.
- `unschedule_draft(draft_id, token=None)` — cancel a draft's scheduled
  release.
- `upload_image(image_base64, token=None, content_type="image/png")` —
  upload a base64-encoded image to Substack and return its hosted URL and
  dimensions.

## Stats (2)

- `get_subscriber_timeseries(token=None, from_date=None)` — daily subscriber
  counts (paid / comps / free trials / total). If a cache extension is
  installed, only the tail beyond the last stored day is re-fetched from
  Substack on later calls; OSS ships no such cache.
- `get_30d_views(token=None)` — trailing-30-day publication views and their
  delta.

## Post Stats (5)

- `get_post_engagement(post_id, token=None)` — likes, comment summary, and
  commenters for a post.
- `get_post_traffic(post_id, token=None)` — referrers, devices, and category
  breakdown of a post's views.
- `get_post_recipients(post_id, token=None, limit=20, offset=0)` —
  per-recipient email delivery / open / click rows.
- `get_post_growth(post_id, token=None)` — subscriber growth attributed to a
  post.
- `get_post_discussion(post_id, token=None, cursor=None)` — comment /
  discussion thread for a post.

## Transport Notes

- Path: `/mcp`
- Transport: streamable HTTP
- HTTP mode: stateless (`stateless_http=True`)

## Extension Hooks

Extensions can register additional MCP tools, and their own auth provider or
credential resolver, through the `GatewayExtension` interface — see
[Development](development.md).
