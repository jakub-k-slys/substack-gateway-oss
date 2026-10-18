Feature: Draft endpoints
  As an API consumer
  I want to create and retrieve Substack post drafts via the gateway
  So that I can programmatically manage draft content

  # ------------------------------------------------------------------
  # GET /drafts
  # ------------------------------------------------------------------

  Scenario: Successfully list drafts
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack list-drafts endpoint returns the sample response
    When I send GET /api/v1/drafts
    Then the response status code is 200
    And the response field "items" is not null
    And the first item field "uuid" is "44fd4b78-d2e6-4fbb-8d14-fc2321b8cd9c"
    And the first item field "title" is "Retention strategies for keeping your best talent"
    And the first item field "updated" is "2024-08-28T11:09:36.995Z"

  Scenario: List drafts Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack list-drafts endpoint returns status 503
    When I send GET /api/v1/drafts
    Then the response status code is 502

  Scenario: List drafts authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack list-drafts endpoint returns status 401
    When I send GET /api/v1/drafts
    Then the response status code is 401

  Scenario: Successfully create a draft
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns the sample response
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft", "subtitle": "A subtitle", "body": "<p>Hello</p>"}
    Then the response status code is 201
    And the response field "id" is not null
    And the response field "uuid" is not null

  Scenario: Create a draft with no fields
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns the sample response
    When I send POST /api/v1/drafts with JSON body {}
    Then the response status code is 201
    And the response field "id" is not null

  Scenario: Create a draft with a broken substack-node fence returns 400
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack user-settings endpoint returns the sample response
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft", "body": "```substack-node\n{oops\n```"}
    Then the response status code is 400
    And the response field "detail" contains "line 1"
    And no Substack POST request was sent to the drafts endpoint

  Scenario: Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns status 503
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft"}
    Then the response status code is 502

  Scenario: Authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns status 401
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft"}
    Then the response status code is 401

  Scenario: Missing x-gateway-token header returns 422
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft"}
    Then the response status code is 422

  # ------------------------------------------------------------------
  # PUT /drafts/{draft_id}
  # ------------------------------------------------------------------

  Scenario: Successfully update all draft fields
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack update-draft endpoint returns the sample response for draft 189535264
    When I send PUT /api/v1/drafts/189535264 with JSON body {"title": "test1", "subtitle": "test2", "body": "test3"}
    Then the response status code is 200
    And the response field "title" is "test1"
    And the response field "subtitle" is "test2"

  Scenario: Update only title
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack update-draft endpoint returns the sample response for draft 189535264
    When I send PUT /api/v1/drafts/189535264 with JSON body {"title": "new title"}
    Then the response status code is 200

  Scenario: Update draft Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack update-draft endpoint returns status 503 for draft 189535264
    When I send PUT /api/v1/drafts/189535264 with JSON body {"title": "test1"}
    Then the response status code is 502

  Scenario: Stale expected_updated_at is rejected with 409 and nothing is written
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack get-draft endpoint returns the sample response for draft 189535264
    When I send PUT /api/v1/drafts/189535264 with JSON body {"title": "late edit", "expected_updated_at": "2026-01-01T00:00:00.000Z"}
    Then the response status code is 409
    And the response field "detail" contains "changed since it was read"
    And no Substack PUT request was sent

  Scenario: Matching expected_updated_at lets the update through
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack get-draft endpoint returns the sample response for draft 189535264
    And the Substack update-draft endpoint returns the sample response for draft 189535264
    When I send PUT /api/v1/drafts/189535264 with JSON body {"title": "test1", "expected_updated_at": "2026-03-01T09:53:35.569Z"}
    Then the response status code is 200
    And the response field "title" is "test1"
    And the response field "updated_at" is "2026-03-01T09:53:35.569Z"

  Scenario: Update with a broken substack-node fence returns 400 naming the line
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    When I send PUT /api/v1/drafts/189535264 with JSON body {"body": "```substack-node\n{oops\n```"}
    Then the response status code is 400
    And the response field "detail" contains "line 1"
    And no Substack PUT request was sent

  # ------------------------------------------------------------------
  # GET /drafts/{draft_id}
  # ------------------------------------------------------------------

  Scenario: Successfully fetch a draft
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack get-draft endpoint returns the sample response for draft 189535264
    When I send GET /api/v1/drafts/189535264
    Then the response status code is 200
    And the response field "title" is "test1"
    And the response field "subtitle" is "test2"
    # The sample body was written by an older gateway (its paragraph has no
    # attrs); it still reads back as plain Markdown, not a substack-node fence.
    And the response field "body" is "test3" followed by a newline

  Scenario: Get draft Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack get-draft endpoint returns status 503 for draft 189535264
    When I send GET /api/v1/drafts/189535264
    Then the response status code is 502

  Scenario: Get draft authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack get-draft endpoint returns status 401 for draft 189535264
    When I send GET /api/v1/drafts/189535264
    Then the response status code is 401

  # ------------------------------------------------------------------
  # DELETE /drafts/{draft_id}
  # ------------------------------------------------------------------

  Scenario: Successfully delete a draft
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack delete-draft endpoint returns status 204 for draft 189535264
    When I send DELETE /api/v1/drafts/189535264
    Then the response status code is 204

  Scenario: Delete draft Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack delete-draft endpoint returns status 503 for draft 189535264
    When I send DELETE /api/v1/drafts/189535264
    Then the response status code is 502

  Scenario: Delete draft authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack delete-draft endpoint returns status 401 for draft 189535264
    When I send DELETE /api/v1/drafts/189535264
    Then the response status code is 401
