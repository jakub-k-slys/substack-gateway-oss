Feature: Post like endpoints
  As a Pro API consumer
  I want to like and unlike Substack posts via the gateway
  So that I can manage post reactions programmatically

  Scenario: Successfully like a post
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack like-post endpoint returns status 200 for post 191598243
    When I send PUT /api/v1/posts/191598243/like
    Then the response status code is 204

  Scenario: Like post Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack like-post endpoint returns status 503 for post 191598243
    When I send PUT /api/v1/posts/191598243/like
    Then the response status code is 502

  Scenario: Like post authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack like-post endpoint returns status 401 for post 191598243
    When I send PUT /api/v1/posts/191598243/like
    Then the response status code is 401

  Scenario: Missing x-gateway-token header returns 422 on post like
    When I send PUT /api/v1/posts/191598243/like
    Then the response status code is 422

  Scenario: Successfully unlike a post
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack unlike-post endpoint returns status 204 for post 191598243
    When I send DELETE /api/v1/posts/191598243/like
    Then the response status code is 204

  Scenario: Unlike post Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack unlike-post endpoint returns status 503 for post 191598243
    When I send DELETE /api/v1/posts/191598243/like
    Then the response status code is 502

  Scenario: Unlike post authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack unlike-post endpoint returns status 401 for post 191598243
    When I send DELETE /api/v1/posts/191598243/like
    Then the response status code is 401
