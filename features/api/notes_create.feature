Feature: Create note endpoint
  As an API consumer
  I want to publish a Substack note from markdown content
  So that I can create notes programmatically

  Scenario: Successfully create a note from markdown
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-note endpoint returns the sample response
    When I send POST /api/v1/notes with JSON body {"content": "Hello **world**."}
    Then the response status code is 201
    And the response field "id" is not null

  Scenario: Create a note with multi-paragraph markdown
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-note endpoint returns the sample response
    When I send POST /api/v1/notes with JSON body {"content": "## Title\n\nFirst paragraph.\n\nSecond paragraph."}
    Then the response status code is 201

  Scenario: Empty content returns 400
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    When I send POST /api/v1/notes with JSON body {"content": ""}
    Then the response status code is 400

  Scenario: Whitespace-only content returns 400
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    When I send POST /api/v1/notes with JSON body {"content": "   "}
    Then the response status code is 400

  Scenario: Authentication failure on note creation returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-note endpoint returns status 401
    When I send POST /api/v1/notes with JSON body {"content": "Hello world."}
    Then the response status code is 401

  Scenario: Missing x-gateway-token header returns 422
    When I send POST /api/v1/notes with JSON body {"content": "Hello world."}
    Then the response status code is 422

  Scenario: Malformed x-gateway-token header returns 401
    Given a malformed x-gateway-token header and publication URL "https://example.substack.com"
    When I send POST /api/v1/notes with JSON body {"content": "Hello world."}
    Then the response status code is 401

  Scenario: Create a note with a link attachment
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-attachment endpoint returns the sample response
    And the Substack create-note endpoint returns the sample response
    When I send POST /api/v1/notes with JSON body {"content": "Hello world.", "attachment": "https://substack.com"}
    Then the response status code is 201
    And the response field "id" is not null

  Scenario: Attachment endpoint failure returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-attachment endpoint returns status 500
    When I send POST /api/v1/notes with JSON body {"content": "Hello world.", "attachment": "https://substack.com"}
    Then the response status code is 502

  # ------------------------------------------------------------------
  # DELETE /notes/{note_id}
  # ------------------------------------------------------------------

  Scenario: Successfully delete a note
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack delete-note endpoint returns status 204 for note 131648795
    When I send DELETE /api/v1/notes/131648795
    Then the response status code is 204

  Scenario: Delete note Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack delete-note endpoint returns status 503 for note 131648795
    When I send DELETE /api/v1/notes/131648795
    Then the response status code is 502

  Scenario: Delete note authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack delete-note endpoint returns status 401 for note 131648795
    When I send DELETE /api/v1/notes/131648795
    Then the response status code is 401

  Scenario: Delete note missing x-gateway-token header returns 422
    When I send DELETE /api/v1/notes/131648795
    Then the response status code is 422
