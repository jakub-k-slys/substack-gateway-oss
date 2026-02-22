Feature: Profile posts endpoint
  As an API consumer
  I want to fetch posts for any Substack profile by slug
  So that I can list a user's published posts

  Scenario: Successfully fetch posts for a profile
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint returns the sample response for "jakubslys"
    And the Substack posts endpoint returns the sample response for user 254824415
    When I send GET /api/v1/profiles/jakubslys/posts
    Then the response status code is 200
    And the response list "items" has 1 item
    And the first item field "title" is "Sample Post Title"

  Scenario: Profile not found returns 404
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint for "unknown" returns status 404
    When I send GET /api/v1/profiles/unknown/posts
    Then the response status code is 404

  Scenario: Authentication failure returns 401
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint for "jakubslys" returns status 401
    When I send GET /api/v1/profiles/jakubslys/posts
    Then the response status code is 401

  Scenario: Missing authorization header returns 422
    When I send GET /api/v1/profiles/jakubslys/posts
    Then the response status code is 422

  Scenario: Malformed authorization header returns 401
    Given a malformed authorization header and publication URL "https://example.substack.com"
    When I send GET /api/v1/profiles/jakubslys/posts
    Then the response status code is 401

