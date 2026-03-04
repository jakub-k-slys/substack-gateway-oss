Feature: Me endpoints

  Background:
    Given valid credentials

  Scenario: Get own profile
    When I GET /api/v1/me
    Then the response status is 200
    And the response has field "id"
    And the response has field "name"

  Scenario: Get own notes
    When I GET /api/v1/me/notes
    Then the response status is 200
    And the response field "notes" is a list

  Scenario: Get own posts
    When I GET /api/v1/me/posts
    Then the response status is 200
    And the response is a list

  Scenario: Get following list
    When I GET /api/v1/me/following
    Then the response status is 200
    And the response is a list
