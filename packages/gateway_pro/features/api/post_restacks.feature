Feature: Post restack endpoint
  As a Pro API consumer
  I want to restack Substack posts via the gateway
  So that I can share them programmatically

  Scenario: Successfully restack a post
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack restack-post endpoint returns status 200
    When I send POST /api/v1/posts/191598243/restack with JSON body {}
    Then the response status code is 204

  Scenario: Restack post Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack restack-post endpoint returns status 503
    When I send POST /api/v1/posts/191598243/restack with JSON body {}
    Then the response status code is 502

  Scenario: Restack post authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack restack-post endpoint returns status 401
    When I send POST /api/v1/posts/191598243/restack with JSON body {}
    Then the response status code is 401

  Scenario: Missing x-gateway-token header returns 422 on post restack
    When I send POST /api/v1/posts/191598243/restack with JSON body {}
    Then the response status code is 422
