Feature: Profile feed endpoint
  As a Pro API consumer
  I want to fetch a profile's Atom feed
  So that I can consume notes and posts as a single feed

  Scenario: Successfully fetch a profile feed
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint returns the sample response for "jakubslys"
    And the Substack profile feed-notes endpoint returns the sample response for user 254824415
    And the Substack profile feed-posts endpoint returns the sample response for user 254824415
    When I send GET /api/v1/profiles/jakubslys/feed
    Then the response status code is 200
    And the response content type starts with "application/atom+xml"
    And the response body contains "<feed"
    And the response body contains "<id>profile:254824415</id>"
    And the response body contains "Sample Post Title"
    And the response body contains "note:"
    And the response body contains "limit=50"

  Scenario: Fetch only post entries
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint returns the sample response for "jakubslys"
    And the Substack profile feed-posts endpoint returns the sample response for user 254824415
    When I send GET /api/v1/profiles/jakubslys/feed?type=post
    Then the response status code is 200
    And the response body contains "post:"
    And the response body does not contain "note:"

  Scenario: Fetch only note entries
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint returns the sample response for "jakubslys"
    And the Substack profile feed-notes endpoint returns the sample response for user 254824415
    When I send GET /api/v1/profiles/jakubslys/feed?type=note
    Then the response status code is 200
    And the response body contains "note:"
    And the response body does not contain "post:"

  Scenario: Limit caps returned entries
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint returns the sample response for "jakubslys"
    And the Substack profile feed-notes endpoint returns the sample response for user 254824415
    When I send GET /api/v1/profiles/jakubslys/feed?type=note&limit=3
    Then the response status code is 200
    And the response body contains "limit=3"
    And the response body contains exactly 3 "<entry>" markers

  Scenario: Profile not found returns 404
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint for "unknown" returns status 404
    When I send GET /api/v1/profiles/unknown/feed
    Then the response status code is 404

  Scenario: Missing x-gateway-token header returns 422
    When I send GET /api/v1/profiles/jakubslys/feed
    Then the response status code is 422
