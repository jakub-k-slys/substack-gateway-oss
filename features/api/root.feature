Feature: Root endpoint
  As an API consumer
  I want the service root to expose the gateway version
  So that I can quickly identify the running build

  Scenario: Root returns the gateway version
    When I send GET /
    Then the response status code is 200
    And the response field "gateway" matches the package version
