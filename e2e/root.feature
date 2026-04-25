Feature: Root endpoint

  Scenario: Root metadata returns application info
    When I GET /
    Then the response status is 200
    And the response field "application" is "substack-gateway"
    And the response field "tier" is "oss"
    And the response field "features" is a list
