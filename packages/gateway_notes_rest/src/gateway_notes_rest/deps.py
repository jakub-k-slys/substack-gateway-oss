from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_notes.service import NotesService
from gateway_rest_common.deps import get_publication_client, get_substack_client


def get_notes_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> NotesService:
    return NotesService(pub, sub)
