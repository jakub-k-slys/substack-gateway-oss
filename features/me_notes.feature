Feature: Own notes endpoint
  As an API consumer
  I want to fetch my own Substack notes
  So that I can list notes I have published

  Scenario: Successfully fetch own notes
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack notes endpoint returns the sample response
    When I send GET /api/v1/me/notes
    Then the response status code is 200
    And the response list "items" has 1 item
    And the first item field "body" is "This is a sample note from the gateway test."

  Scenario: Authentication failure returns 401
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack notes endpoint returns status 401
    When I send GET /api/v1/me/notes
    Then the response status code is 401

  Scenario: Substack API error returns 502
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack notes endpoint returns status 503
    When I send GET /api/v1/me/notes
    Then the response status code is 502

  Scenario: Missing authorization header returns 422
    When I send GET /api/v1/me/notes
    Then the response status code is 422
