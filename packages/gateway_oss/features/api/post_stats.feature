Feature: Per-post stats endpoints
  As an API consumer
  I want to read a published post's analytics tabs via the gateway
  So that I can measure how each post performed

  Scenario: Fetch post engagement
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack post engagement endpoint returns the sample response for post 42
    When I send GET /api/v1/posts/42/stats/engagement
    Then the response status code is 200
    And the response field "likes_count" is 33
    And the response field "comment_count" is 6
    And the response field "commenter_count" is 7
    And the response list "likes" has 1 item

  Scenario: Fetch post traffic
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack post traffic endpoint returns the sample response for post 42
    When I send GET /api/v1/posts/42/stats/traffic
    Then the response status code is 200
    And the response list "referrers" has 2 items
    And the response list "devices" has 2 items

  Scenario: Fetch post recipients
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack post recipients endpoint returns the sample response for post 42
    When I send GET /api/v1/posts/42/stats/recipients
    Then the response status code is 200
    And the response field "total" is 1
    And the response list "rows" has 1 item

  Scenario: Fetch post discussion
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack post discussion endpoint returns the sample response for post 42
    When I send GET /api/v1/posts/42/stats/discussion
    Then the response status code is 200
    And the response list "items" has 1 item

  Scenario: Fetch post growth
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack post growth endpoint returns the sample response for post 42
    When I send GET /api/v1/posts/42/stats/growth
    Then the response status code is 200
    And the response field "totalFreeSignups" is 12

  Scenario: Post engagement Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack post engagement endpoint returns status 503 for post 42
    When I send GET /api/v1/posts/42/stats/engagement
    Then the response status code is 502

  Scenario: Post engagement authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack post engagement endpoint returns status 401 for post 42
    When I send GET /api/v1/posts/42/stats/engagement
    Then the response status code is 401
