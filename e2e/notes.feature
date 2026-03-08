Feature: Notes endpoints

  Scenario: List own notes
    Given valid credentials
    When I GET /api/v1/me/notes
    Then the response status is 200
    And the response field "items" is a list

  Scenario: Get note by ID
    Given valid credentials
    And a test note ID
    When I fetch the test note
    Then the response status is 200
    And the response has field "id"

  Scenario: Create, fetch, and delete a note
    Given valid credentials
    # 1) Create a new note
    When I create a note with content "e2e test note — safe to delete"
    Then the response status is 201
    And the response has field "id"
    # 2) Capture the created note ID and fetch it
    Given the created note ID is saved
    When I fetch the test note
    Then the response status is 200
    And the response has field "id"
    And the response has field "body"
    # 3) Delete the note
    When I delete the test note
    Then the response status is 204
