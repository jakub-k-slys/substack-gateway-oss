Feature: Draft creation endpoint
  As an API consumer
  I want to create Substack post drafts via the gateway
  So that I can programmatically draft content

  Scenario: Successfully create a draft
    Given a bearer token authorized by gateway key "WW91IHNoYWxsIG5vdCBwYXNzCg==" and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns the sample response
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft", "subtitle": "A subtitle", "body": "<p>Hello</p>"}
    Then the response status code is 201
    And the response field "id" is not null
    And the response field "uuid" is not null

  Scenario: Create a draft with no fields
    Given a bearer token authorized by gateway key "WW91IHNoYWxsIG5vdCBwYXNzCg==" and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns the sample response
    When I send POST /api/v1/drafts with JSON body {}
    Then the response status code is 201
    And the response field "id" is not null

  Scenario: Wrong gateway key returns 403
    Given a bearer token authorized by gateway key "wrong-key" and publication URL "https://example.substack.com"
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft"}
    Then the response status code is 403

  Scenario: Missing gateway key returns 403
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft"}
    Then the response status code is 403

  Scenario: Substack API error returns 502
    Given a bearer token authorized by gateway key "WW91IHNoYWxsIG5vdCBwYXNzCg==" and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns status 503
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft"}
    Then the response status code is 502

  Scenario: Authentication failure returns 401
    Given a bearer token authorized by gateway key "WW91IHNoYWxsIG5vdCBwYXNzCg==" and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns status 401
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft"}
    Then the response status code is 401

  Scenario: Missing authorization header returns 422
    When I send POST /api/v1/drafts with JSON body {"title": "Test Draft"}
    Then the response status code is 422
