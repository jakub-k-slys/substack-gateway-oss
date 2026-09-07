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
    And the "gateway-oss" module features contain "api:notes:like"
    And the "gateway-oss" module features contain "api:notes:reply"
    And the "gateway-oss" module features contain "mcp:notes:like"
    And the "gateway-oss" module features contain "mcp:notes:replies:list"
    And the "gateway-oss" module features contain "api:comments:create"
    And the "gateway-oss" module features contain "api:comments:delete"
    And the "gateway-oss" module features contain "api:comments:like"
    And the "gateway-oss" module features contain "api:comments:unlike"
    And the "gateway-oss" module features contain "api:comments:reply"
    And the "gateway-oss" module features contain "api:comments:replies:list"
    And the "gateway-oss" module features contain "mcp:comments:create"
    And the "gateway-oss" module features contain "mcp:comments:delete"
    And the "gateway-oss" module features contain "mcp:comments:get"
    And the "gateway-oss" module features contain "mcp:comments:like"
    And the "gateway-oss" module features contain "mcp:comments:unlike"
    And the "gateway-oss" module features contain "mcp:comments:reply"
    And the "gateway-oss" module features contain "mcp:comments:replies:list"
    And the "gateway-oss" module features contain "api:drafts:create"
    And the "gateway-oss" module features contain "mcp:drafts:create"
    And the "gateway-oss" module features contain "api:images:create"
    And the "gateway-oss" module features contain "mcp:images:upload"
    And the "gateway-oss" module features contain "api:stats:subscribers"
    And the "gateway-oss" module features contain "mcp:stats:subscribers"
    And the "gateway-oss" module features contain "api:posts:stats:engagement"
    And the "gateway-oss" module features contain "mcp:posts:stats:engagement"
    And the "gateway-oss" module features contain "api:posts:like"
    And the "gateway-oss" module features contain "api:posts:unlike"
    And the "gateway-oss" module features contain "api:posts:restack"
    And the "gateway-oss" module features contain "mcp:posts:like"
    And the "gateway-oss" module features contain "mcp:posts:unlike"
    And the "gateway-oss" module features contain "mcp:posts:restack"
