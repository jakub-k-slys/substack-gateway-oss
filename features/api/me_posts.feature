Feature: Own posts endpoint
  As an API consumer
  I want to fetch my own Substack posts
  So that I can list posts I have published

  Scenario: Successfully fetch own posts
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack handles endpoint returns the sample response
    And the Substack public profile endpoint returns the sample response for "jakubslys"
    And the Substack posts endpoint returns the sample response for user 254824415
    When I send GET /api/v1/me/posts
    Then the response status code is 200
    And the response list "items" has 1 item
    And the first item field "title" is "Sample Post Title"

  Scenario: Authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack handles endpoint returns status 401
    When I send GET /api/v1/me/posts
    Then the response status code is 401

  Scenario: Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack handles endpoint returns status 503
    When I send GET /api/v1/me/posts
    Then the response status code is 502

  Scenario: Missing x-gateway-token header returns 422
    When I send GET /api/v1/me/posts
    Then the response status code is 422

  Scenario: Malformed x-gateway-token header returns 401
    Given a malformed x-gateway-token header and publication URL "https://example.substack.com"
    When I send GET /api/v1/me/posts
    Then the response status code is 401

  Scenario: limit=0 is rejected with 422
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    When I send GET /api/v1/me/posts?limit=0
    Then the response status code is 422

  Scenario: limit exceeding maximum is rejected with 422
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    When I send GET /api/v1/me/posts?limit=101
    Then the response status code is 422

