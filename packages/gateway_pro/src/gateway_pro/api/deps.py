from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from gateway_oss.api.deps import get_publication_client, get_substack_client
from gateway_oss.client.publication import PublicationClient
from gateway_oss.client.substack import SubstackClient

from gateway_pro.services.drafts import DraftsService
from gateway_pro.services.note_reactions import NoteReactionsService
from gateway_pro.services.post_reactions import PostReactionsService


def get_drafts_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> DraftsService:
    return DraftsService(pub, sub)


def get_note_reactions_service(
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> NoteReactionsService:
    return NoteReactionsService(sub)


def get_post_reactions_service(
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> PostReactionsService:
    return PostReactionsService(sub)
