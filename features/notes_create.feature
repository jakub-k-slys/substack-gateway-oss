Feature: Create note endpoint
  As an API consumer
  I want to publish a Substack note from markdown content
  So that I can create notes programmatically

  Scenario: Successfully create a note from markdown
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-note endpoint returns the sample response
    When I send POST /api/v1/notes with JSON body {"content": "Hello **world**."}
    Then the response status code is 201
    And the response field "id" is not null

  Scenario: Create a note with multi-paragraph markdown
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-note endpoint returns the sample response
    When I send POST /api/v1/notes with JSON body {"content": "## Title\n\nFirst paragraph.\n\nSecond paragraph."}
    Then the response status code is 201

  Scenario: Empty content returns 400
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    When I send POST /api/v1/notes with JSON body {"content": ""}
    Then the response status code is 400

  Scenario: Whitespace-only content returns 400
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    When I send POST /api/v1/notes with JSON body {"content": "   "}
    Then the response status code is 400

  Scenario: Authentication failure on note creation returns 401
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-note endpoint returns status 401
    When I send POST /api/v1/notes with JSON body {"content": "Hello world."}
    Then the response status code is 401

  Scenario: Missing authorization header returns 422
    When I send POST /api/v1/notes with JSON body {"content": "Hello world."}
    Then the response status code is 422

  Scenario: Malformed authorization header returns 401
    Given a malformed authorization header and publication URL "https://example.substack.com"
    When I send POST /api/v1/notes with JSON body {"content": "Hello world."}
    Then the response status code is 401
