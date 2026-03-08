Feature: Drafts end-to-end lifecycle
  As an API consumer
  I want to create, list, fetch, update, and delete drafts
  So that I can manage drafts through their full lifecycle

  Scenario: Draft lifecycle — create, list, fetch, update, delete
    Given a bearer token authorized by gateway key "WW91IHNoYWxsIG5vdCBwYXNzCg==" and publication URL "https://example.substack.com"
    And the Substack drafts list endpoint cycles through initial, after-create, and after-delete responses
    And the Substack create-draft endpoint returns the sample response
    And the Substack get-draft endpoint returns the created draft for draft 189531629
    And the Substack update-draft endpoint returns the updated draft for draft 189531629
    And the Substack delete-draft endpoint returns status 204 for draft 189531629
    # 1) List drafts — initial 2
    When I send GET /api/v1/drafts
    Then the response status code is 200
    And the response list "items" has 2 items
    # 2) Create a new draft
    When I send POST /api/v1/drafts with JSON body {"title": "Hello world!", "subtitle": "A test draft", "body": "Hello world!"}
    Then the response status code is 201
    And the response field "id" is not null
    And the response field "uuid" is not null
    # 3) List drafts — should now have 3
    When I send GET /api/v1/drafts
    Then the response status code is 200
    And the response list "items" has 3 items
    # 4) Fetch the created draft by ID
    When I send GET /api/v1/drafts/189531629
    Then the response status code is 200
    And the response field "title" is "Hello world!"
    And the response field "subtitle" is "A test draft"
    And the response field "body" is not null
    # 5) Update the draft title
    When I send PUT /api/v1/drafts/189531629 with JSON body {"title": "Updated title"}
    Then the response status code is 200
    And the response field "title" is "Updated title"
    # 6) Delete the draft
    When I send DELETE /api/v1/drafts/189531629
    Then the response status code is 204
    # 7) List drafts — back to 2
    When I send GET /api/v1/drafts
    Then the response status code is 200
    And the response list "items" has 2 items
