Feature: Root endpoint
  As an API consumer
  I want the service root to expose application metadata
  So that I can quickly identify the running build

  Scenario: Root returns the OSS application metadata
    When I send GET /
    Then the response status code is 200
    And the response field "application" is "substack-gateway"
    And the response contains a module named "gateway-oss"
    And the "gateway-oss" module version matches the OSS package version
    And the "gateway-oss" module features contain "api:notes:create"
    And the "gateway-oss" module features contain "api:profiles:posts:list"
    And the "gateway-oss" module features contain "mcp:notes:create"
    And the "gateway-oss" module features contain "mcp:posts:get"
