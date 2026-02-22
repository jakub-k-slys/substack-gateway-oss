Feature: Public profile endpoint
  As an API consumer
  I want to fetch any Substack user's public profile by slug
  So that I can view their profile information

  Scenario: Successfully fetch a public profile
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint returns the sample response for "jakubslys"
    When I send GET /api/v1/profiles/jakubslys
    Then the response status code is 200
    And the response field "handle" is "jakubslys"

  Scenario: Profile not found returns 404
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint for "unknown-user" returns status 404
    When I send GET /api/v1/profiles/unknown-user
    Then the response status code is 404

  Scenario: Authentication failure returns 401
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack public profile endpoint for "jakubslys" returns status 401
    When I send GET /api/v1/profiles/jakubslys
    Then the response status code is 401

  Scenario: Missing authorization header returns 422
    When I send GET /api/v1/profiles/jakubslys
    Then the response status code is 422

  Scenario: Malformed authorization header returns 401
    Given a malformed authorization header and publication URL "https://example.substack.com"
    When I send GET /api/v1/profiles/jakubslys
    Then the response status code is 401
