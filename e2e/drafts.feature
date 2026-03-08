Feature: Drafts endpoints (e2e)

  Scenario: List drafts
    Given valid credentials
    When I GET /api/v1/drafts
    Then the response status is 200
    And the response field "items" is a list

  Scenario: Draft lifecycle — create, fetch, update, delete
    Given valid credentials
    # 1) Create a new draft
    When I create a draft with title "e2e test draft" and body "Hello from e2e tests"
    Then the response status is 201
    And the response has field "id"
    And the response has field "uuid"
    # 2) Save the ID and fetch the draft
    Given the created draft ID is saved
    When I fetch the test draft
    Then the response status is 200
    And the response has field "title"
    And the response has field "body"
    # 3) Update the draft title
    When I update the test draft with title "updated e2e title"
    Then the response status is 200
    # 4) Delete the draft
    When I delete the test draft
    Then the response status is 204
