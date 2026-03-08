Feature: Notes end-to-end lifecycle
  As an API consumer
  I want to create, list, fetch, and delete notes
  So that I can manage notes through their full lifecycle

  Scenario: Plain text note lifecycle — create, list, fetch, delete
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack notes endpoint cycles through initial, after-create, and after-delete responses
    And the Substack create-note endpoint returns the sample response
    And the Substack reader comment endpoint returns the sample response for id 131719084
    And the Substack delete-note endpoint returns status 204 for note 131719084
    # 1) List notes — check we have the initial 20
    When I send GET /api/v1/me/notes
    Then the response status code is 200
    And the response list "items" has 20 items
    # 2) Create a new plain text note
    When I send POST /api/v1/notes with JSON body {"content": "Hello world!"}
    Then the response status code is 201
    And the response field "id" is not null
    # 3) List notes again — the new note should appear (21 items)
    When I send GET /api/v1/me/notes
    Then the response status code is 200
    And the response list "items" has 21 items
    # 4) Fetch the created note by ID
    When I send GET /api/v1/notes/131719084
    Then the response status code is 200
    And the response field "id" is not null
    And the response field "body" is not null
    # 5) Delete the note
    When I send DELETE /api/v1/notes/131719084
    Then the response status code is 204
    # 6) List notes — should be back to 20
    When I send GET /api/v1/me/notes
    Then the response status code is 200
    And the response list "items" has 20 items

  Scenario: Note with attachment lifecycle — create, list, fetch, delete
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack notes endpoint cycles through initial, after-create, and after-delete responses
    And the Substack create-attachment endpoint returns the sample response
    And the Substack create-note endpoint returns the sample response
    And the Substack reader comment endpoint returns the sample response for id 131719084
    And the Substack delete-note endpoint returns status 204 for note 131719084
    # 1) List notes — initial 20
    When I send GET /api/v1/me/notes
    Then the response status code is 200
    And the response list "items" has 20 items
    # 2) Create a note with a link attachment
    When I send POST /api/v1/notes with JSON body {"content": "Hello world!", "attachment": "https://iam.slys.dev"}
    Then the response status code is 201
    And the response field "id" is not null
    # 3) List notes — should now have 21
    When I send GET /api/v1/me/notes
    Then the response status code is 200
    And the response list "items" has 21 items
    # 4) Fetch the created note by ID
    When I send GET /api/v1/notes/131719084
    Then the response status code is 200
    And the response field "id" is not null
    And the response field "body" is not null
    # 5) Delete the note
    When I send DELETE /api/v1/notes/131719084
    Then the response status code is 204
    # 6) List notes — back to 20
    When I send GET /api/v1/me/notes
    Then the response status code is 200
    And the response list "items" has 20 items
