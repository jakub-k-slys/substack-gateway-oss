from __future__ import annotations

from pydantic import BaseModel, Field

from gateway_core.models.substack import SubstackPublicProfile


class ProfileAudience(BaseModel):
    """Public audience counts from the profile; any value Substack omits is None."""

    followers: int | None = None
    """Substack users following this profile."""
    subscribers: int | None = None
    """Subscribers of the profile's primary publication (not of the user)."""
    subscribers_label: str | None = None
    """Substack's display string for ``subscribers``, e.g. ``"791 subscribers"``."""
    free_subscribers_rough: int | None = None
    """Lower bound of Substack's rough free-subscriber bucket, e.g. ``100``."""
    free_subscribers_rough_label: str | None = None
    """Substack's label for that bucket, e.g. ``"Hundreds"``."""
    recommendations: int | None = None
    """Publications recommending the profile's primary publication."""

    @classmethod
    def from_substack(cls, profile: SubstackPublicProfile) -> ProfileAudience:
        return cls(
            followers=profile.follower_count,
            subscribers=profile.subscriber_count_number,
            subscribers_label=profile.subscriber_count_string,
            free_subscribers_rough=profile.rough_num_free_subscribers_int,
            free_subscribers_rough_label=profile.rough_num_free_subscribers,
            recommendations=profile.primary_publication_recommendation_count,
        )


class ProfileResponse(BaseModel):
    id: int
    handle: str
    name: str
    url: str
    avatar_url: str
    bio: str | None = None
    audience: ProfileAudience = Field(default_factory=ProfileAudience)

    @classmethod
    def from_substack(cls, profile: SubstackPublicProfile) -> ProfileResponse:
        return cls(
            id=profile.id,
            handle=profile.handle,
            name=profile.name,
            url=f"https://substack.com/@{profile.handle}",
            avatar_url=profile.photo_url or "",
            bio=profile.bio,
            audience=ProfileAudience.from_substack(profile),
        )
