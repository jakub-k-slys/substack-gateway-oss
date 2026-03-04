Feature: Notes endpoints

  Background:
    Given valid credentials
    And a test note ID

  Scenario: Get note by ID
    When I GET the test note
    Then the response status is 200
    And the response has field "id"
