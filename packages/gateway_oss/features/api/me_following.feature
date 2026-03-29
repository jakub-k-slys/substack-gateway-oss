Feature: Own following endpoint
  As an API consumer
  I want to fetch the list of users I follow on Substack
  So that I can see my following list

  Scenario: Successfully fetch own following
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack user-settings endpoint returns user id 254824415
    And the Substack subscriber-lists endpoint returns the sample response for user 254824415
    When I send GET /api/v1/me/following
    Then the response status code is 200
    And the response list "items" has 2 items
    And the first item field "handle" is "anotheruser"

  Scenario: Authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack user-settings endpoint returns status 401
    When I send GET /api/v1/me/following
    Then the response status code is 401

  Scenario: Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack user-settings endpoint returns status 503
    When I send GET /api/v1/me/following
    Then the response status code is 502

  Scenario: Missing x-gateway-token header returns 422
    When I send GET /api/v1/me/following
    Then the response status code is 422

  Scenario: Malformed x-gateway-token header returns 401
    Given a malformed x-gateway-token header and publication URL "https://example.substack.com"
    When I send GET /api/v1/me/following
    Then the response status code is 401
