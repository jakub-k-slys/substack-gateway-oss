Feature: Health check endpoint
  As an API consumer
  I want to check if the gateway is connected to Substack
  So that I can verify the service is operational

  Scenario: Gateway is connected to Substack
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack API is reachable
    When I send GET /api/v1/health
    Then the response status code is 200
    And the response field "connected" is true

  Scenario: Gateway cannot reach Substack
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack API is unreachable
    When I send GET /api/v1/health
    Then the response status code is 200
    And the response field "connected" is false

  Scenario: Expired token still reports connected (service is reachable)
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack feed/following endpoint returns status 401
    When I send GET /api/v1/health
    Then the response status code is 200
    And the response field "connected" is true

  Scenario: Missing authorization header returns 422
    When I send GET /api/v1/health
    Then the response status code is 422

  Scenario: Malformed authorization header returns 401
    Given a malformed authorization header and publication URL "https://example.substack.com"
    When I send GET /api/v1/health
    Then the response status code is 401
