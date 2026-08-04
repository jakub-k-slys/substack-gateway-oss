Feature: Note engagement endpoints
  As an API consumer
  I want to like, unlike, and reply to Substack notes via the gateway
  So that I can manage note engagement programmatically

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

  Scenario: Unlike note authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack unlike-note endpoint returns status 401 for note 238483442
    When I send DELETE /api/v1/notes/238483442/like
    Then the response status code is 401

  Scenario: Successfully reply to a note
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack note-reply endpoint returns id 555
    When I send POST /api/v1/notes/234058408/comments with JSON body {"body": "nice"}
    Then the response status code is 201
    And the response field "id" is 555

  Scenario: List replies to a note
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack note-replies endpoint returns two replies for note 234058408
    When I send GET /api/v1/notes/234058408/comments
    Then the response status code is 200
    And the response list "items" has 2 items
