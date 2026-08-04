Feature: Comment engagement endpoints
  As an API consumer
  I want to create, reply to, delete, like, unlike, and list replies to comments
  So that I can participate in post discussions

  Scenario: Create a top-level comment on a post
    Given a valid gateway token "t" and publication URL "https://example.substack.com"
    And the Substack post comment endpoint for post 55 returns id 900
    When I send POST /api/v1/posts/55/comments with JSON body {"body": "hello"}
    Then the response status code is 201
    And the response field "id" is 900

  Scenario: Reply to a comment
    Given a valid gateway token "t" and publication URL "https://example.substack.com"
    And the Substack reader comment endpoint for id 42 resolves to post 77
    And the Substack comment reply endpoint for post 77 returns id 901
    When I send POST /api/v1/comments/42/comments with JSON body {"body": "re"}
    Then the response status code is 201
    And the response field "id" is 901

  Scenario: Reply to a comment with no resolvable post returns 404
    Given a valid gateway token "t" and publication URL "https://example.substack.com"
    And the Substack reader comment endpoint for id 42 returns status 404
    When I send POST /api/v1/comments/42/comments with JSON body {"body": "re"}
    Then the response status code is 404

  Scenario: Delete a comment
    Given a valid gateway token "t" and publication URL "https://example.substack.com"
    And the Substack delete comment endpoint for id 42 returns status 204
    When I send DELETE /api/v1/comments/42
    Then the response status code is 204

  Scenario: List a comment's replies
    Given a valid gateway token "t" and publication URL "https://example.substack.com"
    And the Substack comment replies endpoint for id 42 returns two replies
    When I send GET /api/v1/comments/42/comments
    Then the response status code is 200
    And the response field "items" is not null

  Scenario: Like a comment
    Given a valid gateway token "t" and publication URL "https://example.substack.com"
    And the Substack comment reaction endpoint for id 42 accepts a like
    When I send POST /api/v1/comments/42/reaction
    Then the response status code is 204

  Scenario: Unlike a comment
    Given a valid gateway token "t" and publication URL "https://example.substack.com"
    And the Substack comment reaction endpoint for id 42 accepts an unlike
    When I send DELETE /api/v1/comments/42/reaction
    Then the response status code is 204

  Scenario: Missing x-gateway-token header returns 422
    When I send POST /api/v1/posts/55/comments with JSON body {"body": "hello"}
    Then the response status code is 422
