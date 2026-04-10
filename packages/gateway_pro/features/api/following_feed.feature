Feature: Following feed endpoint
  As a Pro API consumer
  I want to fetch an Atom feed for the people I follow
  So that I can consume their recent posts and notes in one place

  Scenario: Successfully fetch the following feed
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack user-settings endpoint returns user id 254824415
    And the Substack subscriber-lists endpoint returns the sample response for user 254824415
    And the Substack followed profile notes endpoint returns a sample response for user 111111 with handle "anotheruser"
    And the Substack followed profile posts endpoint returns a sample response for user 111111 with title "Another User Post"
    And the Substack followed profile notes endpoint returns a sample response for user 222222 with handle "bob"
    And the Substack followed profile posts endpoint returns a sample response for user 222222 with title "Bob Post"
    When I send GET /api/v1/me/following/feed?limit=3&total=3
    Then the response status code is 200
    And the response content type starts with "application/atom+xml"
    And the response body contains "<feed"
    And the response body contains "Another User Post"
    And the response body contains "Bob Post"
    And the response body contains "note:"
    And the response body contains "limit=3"
    And the response body contains "total=3"
    And the response body contains exactly 3 "<entry>" markers

  Scenario: Missing x-gateway-token header returns 422
    When I send GET /api/v1/me/following/feed
    Then the response status code is 422

  Scenario: Returns partial feed when one followed profile fetch fails
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack user-settings endpoint returns user id 254824415
    And the Substack subscriber-lists endpoint returns the sample response for user 254824415
    And the Substack followed profile notes endpoint returns a sample response for user 111111 with handle "anotheruser"
    And the Substack followed profile posts endpoint returns a sample response for user 111111 with title "Another User Post"
    And the Substack followed profile notes endpoint returns status 404 for user 222222
    And the Substack followed profile posts endpoint returns a sample response for user 222222 with title "Bob Post"
    When I send GET /api/v1/me/following/feed?limit=3&total=3
    Then the response status code is 200
    And the response header "X-Partial-Data" is "true"
    And the response body contains "Another User Post"
    And the response body contains "Bob Post"
