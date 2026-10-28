from __future__ import annotations

from gateway_core.models.substack import SubstackPublicProfile
from gateway_profiles.schemas import ProfileAudience, ProfileResponse

_BASE = {"id": 7, "name": "Example", "handle": "example"}


def test_audience_maps_substack_counts():
    profile = SubstackPublicProfile.model_validate(
        {
            **_BASE,
            "followerCount": 3838,
            "subscriberCountNumber": 791,
            "subscriberCountString": "791 subscribers",
            "rough_num_free_subscribers_int": 100,
            "rough_num_free_subscribers": "Hundreds",
            "primaryPublicationRecommendationCount": 37,
        }
    )

    assert ProfileResponse.from_substack(profile).audience == ProfileAudience(
        followers=3838,
        subscribers=791,
        subscribers_label="791 subscribers",
        free_subscribers_rough=100,
        free_subscribers_rough_label="Hundreds",
        recommendations=37,
    )


def test_audience_is_all_null_when_substack_omits_counts():
    profile = SubstackPublicProfile.model_validate(_BASE)

    assert ProfileResponse.from_substack(profile).audience == ProfileAudience()


def test_unexpected_count_values_become_null_instead_of_failing():
    profile = SubstackPublicProfile.model_validate(
        {
            **_BASE,
            "followerCount": "lots",
            "subscriberCountNumber": {"value": 1},
            "subscriberCountString": 791,
            "primaryPublicationRecommendationCount": 5,
        }
    )

    audience = ProfileResponse.from_substack(profile).audience
    assert audience.followers is None
    assert audience.subscribers is None
    assert audience.subscribers_label is None
    assert audience.recommendations == 5
