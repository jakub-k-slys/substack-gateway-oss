Feature: Publication stats endpoints
  As an API consumer
  I want to read my publication's analytics via the gateway
  So that I can track subscribers and traffic programmatically

  # ------------------------------------------------------------------
  # GET /stats/subscribers
  # ------------------------------------------------------------------

  Scenario: Successfully fetch the subscriber timeseries
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack subscriber-timeseries endpoint returns the sample response
    When I send GET /api/v1/stats/subscribers
    Then the response status code is 200
    And the response list "items" has 3 items
    And the first item field "date" is "2025/07/10"
    And the first item field "total" is 120

  Scenario: Subscriber timeseries Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack subscriber-timeseries endpoint returns status 503
    When I send GET /api/v1/stats/subscribers
    Then the response status code is 502

  Scenario: Subscriber timeseries authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack subscriber-timeseries endpoint returns status 401
    When I send GET /api/v1/stats/subscribers
    Then the response status code is 401

  # ------------------------------------------------------------------
  # GET /stats/30d-views
  # ------------------------------------------------------------------

  Scenario: Successfully fetch trailing 30-day views
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack 30d-views endpoint returns the sample response
    When I send GET /api/v1/stats/30d-views
    Then the response status code is 200
    And the response field "views_30d" is 4200
    And the response field "views_delta_30d" is 315

  Scenario: 30-day views Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack 30d-views endpoint returns status 503
    When I send GET /api/v1/stats/30d-views
    Then the response status code is 502
