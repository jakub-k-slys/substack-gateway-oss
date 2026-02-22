Feature: Comment by ID endpoint
  As an API consumer
  I want to fetch a single Substack comment by its ID
  So that I can read the comment content

  Scenario: Successfully fetch a comment by ID
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack reader comment endpoint returns the sample response for id 131648795
    When I send GET /api/v1/comments/131648795
    Then the response status code is 200
    And the response field "id" is not null
    And the response field "body" is not null

  Scenario: Comment not found returns 502
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack reader comment endpoint for id 131648795 returns status 404
    When I send GET /api/v1/comments/131648795
    Then the response status code is 502

  Scenario: Authentication failure returns 401
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack reader comment endpoint for id 131648795 returns status 401
    When I send GET /api/v1/comments/131648795
    Then the response status code is 401

  Scenario: Missing authorization header returns 422
    When I send GET /api/v1/comments/131648795
    Then the response status code is 422
