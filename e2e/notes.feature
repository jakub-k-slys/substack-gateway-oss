Feature: Notes endpoints

  Scenario: Get note by ID
    Given valid credentials
    And a test note ID
    When I fetch the test note
    Then the response status is 200
    And the response has field "id"

  Scenario: Create, fetch, and delete a note
    Given valid credentials
    When I create a note with content "e2e test note - safe to delete"
    Then the response status is 201
    And the response has field "id"
    Given the created note ID is saved
    When I fetch the test note
    Then the response status is 200
    And the response has field "id"
    And the response has field "body"
    When I delete the test note
    Then the response status is 204
