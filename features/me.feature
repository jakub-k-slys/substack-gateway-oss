Feature: User profile endpoint
  As an API consumer
  I want to fetch my own Substack profile
  So that I can view my profile information

  Scenario: Successfully fetch own profile
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack handles endpoint returns handle "testuser"
    And the Substack public profile endpoint returns a profile for "testuser"
    When I send GET /api/v1/me
    Then the response status code is 200
    And the response field "handle" is "testuser"
    And the response field "slug" is "testuser"

  Scenario: Authentication failure returns 401
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack handles endpoint returns status 401
    When I send GET /api/v1/me
    Then the response status code is 401

  Scenario: Substack API error returns 502
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack handles endpoint returns status 503
    When I send GET /api/v1/me
    Then the response status code is 502

  Scenario: Missing authorization header returns 422
    When I send GET /api/v1/me
    Then the response status code is 422

  Scenario: Malformed authorization header returns 401
    Given a malformed authorization header and publication URL "https://example.substack.com"
    When I send GET /api/v1/me
    Then the response status code is 401
