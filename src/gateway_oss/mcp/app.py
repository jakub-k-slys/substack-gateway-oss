from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from gateway_oss.auth import (
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway_oss.client.publication import PublicationClient
from gateway_oss.client.substack import SubstackClient
from gateway_oss.config import settings
from gateway_oss.extensions.runtime import get_runtime
from gateway_oss.models.schemas import (
    BearerCredentials,
    CommentsResponse,
    CreateNoteResponse,
    FollowingResponse,
    FullPostResponse,
    NoteResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)
from gateway_oss.services.following import FollowingService
from gateway_oss.services.notes import NotesService
from gateway_oss.services.posts import PostsService
from gateway_oss.services.profiles import ProfilesService

runtime = get_runtime()

_mcp = FastMCP("substack-gateway", auth=runtime.mcp_auth_provider)


def _anonymous_credentials() -> BearerCredentials:
    return BearerCredentials(
        publication_url=settings.substack_base_url,
        substack_sid="",
        connect_sid="",
    )


@contextlib.asynccontextmanager
async def _public_substack_client() -> AsyncIterator[SubstackClient]:
    async with make_substack_client(_anonymous_credentials()) as sub:
        yield sub


@contextlib.asynccontextmanager
async def _public_publication_client() -> AsyncIterator[PublicationClient]:
    credentials = _anonymous_credentials()
    assert credentials.publication_url is not None
    async with make_publication_client(
        credentials, credentials.publication_url
    ) as publication:
        yield publication


@contextlib.asynccontextmanager
async def _authenticated_clients(
    token: str,
) -> AsyncIterator[tuple[PublicationClient, SubstackClient]]:
    credentials = decode_bearer_credentials(token)
    assert credentials.publication_url is not None
    async with (
        make_publication_client(
            credentials, credentials.publication_url
        ) as publication,
        make_substack_client(credentials) as substack,
    ):
        yield publication, substack


async def get_note(
    note_id: int,
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        note = await NotesService(publication, substack).get_note_by_id(note_id)
    return NoteResponse.from_substack(note).model_dump(exclude_none=True)


async def create_note(
    content: str,
    token: str,
    attachment: str | None = None,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        note = await NotesService(publication, substack).create_note(
            content, attachment=attachment
        )
    return CreateNoteResponse.from_substack(note).model_dump()


async def delete_note(
    note_id: int,
    token: str,
) -> str:
    async with _authenticated_clients(token) as (publication, substack):
        await NotesService(publication, substack).delete_note(note_id)
    return f"Note {note_id} deleted successfully."


async def get_me(
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (_publication, substack):
        profile = await ProfilesService(substack).get_own_profile()
    return ProfileResponse.from_substack(profile).model_dump()


async def get_my_notes(
    token: str,
    cursor: str | None = None,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        page = await NotesService(publication, substack).get_own_notes(cursor=cursor)
    return NotesPageResponse.from_substack(page).model_dump()


async def get_my_posts(
    token: str,
    limit: int = 25,
    cursor: str | None = None,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        profiles = ProfilesService(substack)
        posts = PostsService(publication, substack)
        profile = await profiles.get_own_profile()
        page = await posts.get_posts_for_profile(profile.id, limit=limit, cursor=cursor)
    return PostsPageResponse.from_substack(page).model_dump()


async def get_post(
    post_id: int,
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        post = await PostsService(publication, substack).get_post_by_id(post_id)
    return FullPostResponse.from_substack(post).model_dump()


async def get_post_comments(
    post_id: int,
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        comments = await PostsService(publication, substack).get_comments_for_post(
            post_id
        )
    return CommentsResponse.from_substack(comments).model_dump()


async def get_my_following(
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        users = await FollowingService(publication, substack).get_own_following()
    return FollowingResponse.from_substack(users).model_dump()


@_mcp.tool(
    description="Retrieve a public Substack profile by its handle/slug.",
    tags={"profiles", "read"},
    annotations=ToolAnnotations(
        title="Get Profile",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={
        "category": "profiles",
        "substack_endpoint": "GET /user/{slug}/public_profile",
    },
)
async def get_profile(
    slug: str,
) -> dict[str, Any]:
    async with _public_substack_client() as substack:
        profile = await ProfilesService(substack).get_profile_by_slug(slug)
    return ProfileResponse.from_substack(profile).model_dump()


@_mcp.tool(
    description="Retrieve a paginated list of posts for a Substack profile identified by handle/slug.",
    tags={"profiles", "posts", "read"},
    annotations=ToolAnnotations(
        title="Get Profile Posts",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "profiles", "substack_endpoint": "GET /profile/posts"},
)
async def get_profile_posts(
    slug: str,
    limit: int = 25,
    cursor: str | None = None,
) -> dict[str, Any]:
    async with (
        _public_publication_client() as publication,
        _public_substack_client() as substack,
    ):
        profiles = ProfilesService(substack)
        posts = PostsService(publication, substack)
        profile_id = await profiles.get_profile_id_by_slug(slug)
        page = await posts.get_posts_for_profile(profile_id, limit=limit, cursor=cursor)
    return PostsPageResponse.from_substack(page).model_dump()


@_mcp.tool(
    description="Retrieve a paginated list of notes for a Substack profile identified by handle/slug.",
    tags={"profiles", "notes", "read"},
    annotations=ToolAnnotations(
        title="Get Profile Notes",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={
        "category": "profiles",
        "substack_endpoint": "GET /reader/feed/profile/{id}",
    },
)
async def get_profile_notes(
    slug: str,
    cursor: str | None = None,
) -> dict[str, Any]:
    async with (
        _public_publication_client() as publication,
        _public_substack_client() as substack,
    ):
        profiles = ProfilesService(substack)
        posts = PostsService(publication, substack)
        profile_id = await profiles.get_profile_id_by_slug(slug)
        page = await posts.get_notes_for_profile(profile_id, cursor=cursor)
    return NotesPageResponse.from_substack(page).model_dump()


def register_authenticated_tools(mcp: FastMCP) -> None:
    mcp.tool(
        description="Publish a new note to Substack from Markdown content, with an optional link attachment. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"notes", "write"},
        annotations=ToolAnnotations(
            title="Create Note",
            readOnlyHint=False,
            destructiveHint=False,
            idempotentHint=False,
            openWorldHint=True,
        ),
        meta={"category": "notes", "substack_endpoint": "POST /comment/feed/"},
    )(create_note)
    mcp.tool(
        description="Permanently delete a Substack note by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"notes", "write", "delete"},
        annotations=ToolAnnotations(
            title="Delete Note",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "notes", "substack_endpoint": "DELETE /comment/{note_id}"},
    )(delete_note)
    mcp.tool(
        description="Retrieve the authenticated user's own Substack public profile using an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"me", "profile", "read"},
        annotations=ToolAnnotations(
            title="Get My Profile",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /user/{slug}/public_profile"},
    )(get_me)
    mcp.tool(
        description="Retrieve the authenticated user's own notes, paginated via an optional cursor. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"me", "notes", "read"},
        annotations=ToolAnnotations(
            title="Get My Notes",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /notes"},
    )(get_my_notes)
    mcp.tool(
        description="Retrieve the authenticated user's own posts, paginated via limit and offset. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"me", "posts", "read"},
        annotations=ToolAnnotations(
            title="Get My Posts",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /profile/posts"},
    )(get_my_posts)
    mcp.tool(
        description="Retrieve the list of Substack profiles that the authenticated user follows using an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"me", "following", "read"},
        annotations=ToolAnnotations(
            title="Get My Following",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /user/{id}/subscriber-lists"},
    )(get_my_following)
    mcp.tool(
        description="Retrieve a single Substack note by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"notes", "read"},
        annotations=ToolAnnotations(
            title="Get Note",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "notes",
            "substack_endpoint": "GET /reader/comment/{note_id}",
        },
    )(get_note)
    mcp.tool(
        description="Retrieve the full content of a Substack post by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"posts", "read"},
        annotations=ToolAnnotations(
            title="Get Post",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "posts", "substack_endpoint": "GET /posts/by-id/{post_id}"},
    )(get_post)
    mcp.tool(
        description="Retrieve all comments for a Substack post by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"posts", "comments", "read"},
        annotations=ToolAnnotations(
            title="Get Post Comments",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "posts",
            "substack_endpoint": "GET /post/{post_id}/comments",
        },
    )(get_post_comments)


for extension in runtime.extensions:
    extension.register_mcp(_mcp, runtime.context)


mcp = _mcp.http_app(transport="streamable-http", path="/", stateless_http=True)
