Feature: Health check endpoints
  As an API consumer
  I want to check if the gateway is alive and connected to Substack
  So that I can verify the service is operational

  # ------------------------------------------------------------------
  # Public liveness probe — no auth required
  # ------------------------------------------------------------------

  Scenario: Liveness probe returns 200 without any headers
    When I send GET /api/v1/health/live
    Then the response status code is 200
    And the response field "status" is "ok"

  # ------------------------------------------------------------------
  # Authenticated readiness probe — checks Substack connectivity
  # ------------------------------------------------------------------

  Scenario: Gateway is connected to Substack
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack API is reachable
    When I send GET /api/v1/health/ready
    Then the response status code is 200
    And the response field "connected" is true
    And the response field "tokens" is absent

  Scenario: Tokens are returned when show=true
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack API is reachable
    When I send GET /api/v1/health/ready?show=true
    Then the response status code is 200
    And the response field "connected" is true
    And the response field "tokens" is not null
    And the response nested field "tokens.substack_sid" is "test-token"
    And the response nested field "tokens.connect_sid" is "test-token"
    And the response nested field "tokens.gateway_key" is "test"

  Scenario: Gateway cannot reach Substack
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack API is unreachable
    When I send GET /api/v1/health/ready
    Then the response status code is 200
    And the response field "connected" is false

  Scenario: Substack API timeout is treated as unreachable
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack API times out
    When I send GET /api/v1/health/ready
    Then the response status code is 200
    And the response field "connected" is false

  Scenario: Expired token still reports connected (service is reachable)
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack feed/following endpoint returns status 401
    When I send GET /api/v1/health/ready
    Then the response status code is 200
    And the response field "connected" is true

  Scenario: Missing authorization header returns 422
    When I send GET /api/v1/health/ready
    Then the response status code is 422

  Scenario: Malformed authorization header returns 401
    Given a malformed authorization header and publication URL "https://example.substack.com"
    When I send GET /api/v1/health/ready
    Then the response status code is 401

  Scenario: Bearer token with extra surrounding whitespace is accepted
    Given a bearer token with extra whitespace and publication URL "https://example.substack.com"
    And the Substack API is reachable
    When I send GET /api/v1/health/ready
    Then the response status code is 200
    And the response field "connected" is true
