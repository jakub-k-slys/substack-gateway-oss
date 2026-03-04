Feature: Posts endpoints

  Background:
    Given valid credentials
    And a test post ID

  Scenario: Get post by ID
    When I fetch the test post
    Then the response status is 200
    And the response has field "id"
    And the response has field "title"

  Scenario: Get post comments
    When I fetch the test post comments
    Then the response status is 200
    And the response is a list
