Feature: Root endpoint
  As an API consumer
  I want the service root to expose application metadata
  So that I can quickly identify the running build

  Scenario: Root returns the PRO application metadata
    When I send GET /
    Then the response status code is 200
    And the response field "application" is "substack-gateway"
    And the response field "tier" is "pro"
    And the response field "version" matches the PRO package version
    And the response list "features" contains "api:drafts:create"
    And the response list "features" contains "api:me:following:feed"
    And the response list "features" contains "mcp:drafts:create"
    And the response list "features" contains "mcp:posts:restack"
