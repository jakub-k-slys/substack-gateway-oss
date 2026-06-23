Feature: Profile endpoints

  Background:
    Given valid credentials
    And a test profile slug

  Scenario: Get profile by slug
    When I fetch the test profile
    Then the response status is 200
    And the response has field "id"
    And the response has field "name"

  Scenario: Get profile posts
    Given a valid publication URL
    When I fetch the test profile posts
    Then the response status is 200
    And the response field "items" is a list

  Scenario: Get profile notes
    Given a valid publication URL
    When I fetch the test profile notes
    Then the response status is 200
    And the response field "items" is a list
