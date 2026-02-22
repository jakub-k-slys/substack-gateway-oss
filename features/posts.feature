Feature: Posts endpoints
  As an API consumer
  I want to fetch Substack posts and their comments
  So that I can read post content and discussions

  Scenario: Successfully fetch a post by ID
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack full post endpoint returns the sample response for post 987654
    When I send GET /api/v1/posts/987654
    Then the response status code is 200
    And the response field "title" is "Sample Post Title"
    And the response field "slug" is "sample-post-title"

  Scenario: Post not found returns 502
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack full post endpoint for post 987654 returns status 404
    When I send GET /api/v1/posts/987654
    Then the response status code is 502

  Scenario: Authentication failure on post fetch returns 401
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack full post endpoint for post 987654 returns status 401
    When I send GET /api/v1/posts/987654
    Then the response status code is 401

  Scenario: Missing authorization header on post fetch returns 422
    When I send GET /api/v1/posts/987654
    Then the response status code is 422

  Scenario: Successfully fetch comments for a post
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack comments endpoint returns the sample response for post 987654
    When I send GET /api/v1/posts/987654/comments
    Then the response status code is 200
    And the response list "items" has 2 items
    And the first item field "body" is "Great post!"

  Scenario: Authentication failure on comments fetch returns 401
    Given a valid bearer token "test-token" and publication URL "https://example.substack.com"
    And the Substack comments endpoint for post 987654 returns status 401
    When I send GET /api/v1/posts/987654/comments
    Then the response status code is 401

  Scenario: Missing authorization header on comments fetch returns 422
    When I send GET /api/v1/posts/987654/comments
    Then the response status code is 422
