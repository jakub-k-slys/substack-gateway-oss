Feature: Health endpoints

  Scenario: Liveness probe returns 200
    When I GET /api/v1/health/live
    Then the response status is 200

  Scenario: Readiness probe with valid credentials returns 200
    Given valid credentials
    When I GET /api/v1/health/ready
    Then the response status is 200
    And the response has field "status"
