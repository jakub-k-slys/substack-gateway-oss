Feature: Note like endpoints
  As a Pro API consumer
  I want to like and unlike Substack notes via the gateway
  So that I can manage note reactions programmatically

  Scenario: Successfully like a note
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack like-note endpoint returns status 200 for note 234058408
    When I send PUT /api/v1/notes/234058408/like
    Then the response status code is 204

  Scenario: Like note Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack like-note endpoint returns status 503 for note 234058408
    When I send PUT /api/v1/notes/234058408/like
    Then the response status code is 502

  Scenario: Like note authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack like-note endpoint returns status 401 for note 234058408
    When I send PUT /api/v1/notes/234058408/like
    Then the response status code is 401

  Scenario: Missing x-gateway-token header returns 422 on like
    When I send PUT /api/v1/notes/234058408/like
    Then the response status code is 422

  Scenario: Successfully unlike a note
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack unlike-note endpoint returns status 204 for note 238483442
    When I send DELETE /api/v1/notes/238483442/like
    Then the response status code is 204

  Scenario: Unlike note Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack unlike-note endpoint returns status 503 for note 238483442
    When I send DELETE /api/v1/notes/238483442/like
    Then the response status code is 502

  Scenario: Unlike note authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack unlike-note endpoint returns status 401 for note 238483442
    When I send DELETE /api/v1/notes/238483442/like
    Then the response status code is 401
