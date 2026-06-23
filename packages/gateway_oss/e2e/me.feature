Feature: Me endpoints

  Background:
    Given valid credentials

  Scenario: Get own profile
    When I GET /api/v1/me
    Then the response status is 200
    And the response has field "id"
    And the response has field "name"

  Scenario: Get own notes
    Given a valid publication URL
    When I GET /api/v1/me/notes
    Then the response status is 200
    And the response field "items" is a list

  Scenario: Get own posts
    Given a valid publication URL
    When I GET /api/v1/me/posts
    Then the response status is 200
    And the response field "items" is a list

  Scenario: Get following list
    Given a valid publication URL
    When I GET /api/v1/me/following
    Then the response status is 200
    And the response field "items" is a list
