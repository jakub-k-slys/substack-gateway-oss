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

  # ------------------------------------------------------------------
  # GET /stats/arr
  # ------------------------------------------------------------------

  Scenario: Successfully fetch the ARR timeseries
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "ARR-timeseries" endpoint returns the sample response
    When I send GET /api/v1/stats/arr
    Then the response status code is 200
    And the response list "items" has 2 items
    And the response path "items.0.arr" equals JSON 258.19
    And the response path "items.1.arr" equals JSON 1262.4
    And the response path "items.0.arr_display" equals JSON "$258.19"

  Scenario: ARR timeseries Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "ARR-timeseries" endpoint returns status 503
    When I send GET /api/v1/stats/arr
    Then the response status code is 502

  Scenario: ARR timeseries rejects a malformed from parameter
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    When I send GET /api/v1/stats/arr?from=garbage
    Then the response status code is 422

  # ------------------------------------------------------------------
  # GET /stats/emails
  # ------------------------------------------------------------------

  Scenario: Successfully fetch the email timeseries
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "email-timeseries" endpoint returns the sample response
    When I send GET /api/v1/stats/emails
    Then the response status code is 200
    And the response list "items" has 2 items
    And the response path "items.0.emails" equals JSON 411

  Scenario: Email timeseries Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "email-timeseries" endpoint returns status 503
    When I send GET /api/v1/stats/emails
    Then the response status code is 502

  # ------------------------------------------------------------------
  # GET /stats/dashboard
  # ------------------------------------------------------------------

  Scenario: Successfully fetch the dashboard summary
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "dashboard-summary" endpoint returns the sample response
    When I send GET /api/v1/stats/dashboard
    Then the response status code is 200
    And the response path "arr" equals JSON 1262.4
    And the response path "app_subscribers_last_30_days" equals JSON 3
    And the response path "is_bestseller" equals JSON false

  Scenario: Dashboard summary Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "dashboard-summary" endpoint returns status 503
    When I send GET /api/v1/stats/dashboard
    Then the response status code is 502

  Scenario: Dashboard summary authentication failure returns 401
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "dashboard-summary" endpoint returns status 401
    When I send GET /api/v1/stats/dashboard
    Then the response status code is 401

  # ------------------------------------------------------------------
  # GET /stats/dashboard/period
  # ------------------------------------------------------------------

  Scenario: Successfully fetch the dashboard period summary
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "dashboard-period" endpoint returns the sample response
    When I send GET /api/v1/stats/dashboard/period?range_days=90
    Then the response status code is 200
    And the response path "range_days" equals JSON 90
    And the response path "total_subscribers" equals JSON {"start": 300, "end": 420}

  Scenario: Dashboard period Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "dashboard-period" endpoint returns status 503
    When I send GET /api/v1/stats/dashboard/period
    Then the response status code is 502

  Scenario: Dashboard period rejects a non-positive range_days
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    When I send GET /api/v1/stats/dashboard/period?range_days=0
    Then the response status code is 422

  # ------------------------------------------------------------------
  # GET /stats/recommendations/{direction}
  # ------------------------------------------------------------------

  Scenario: Successfully fetch outgoing recommendation stats
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "recommendations-from" endpoint returns the sample response
    When I send GET /api/v1/stats/recommendations/outgoing?limit=2
    Then the response status code is 200
    And the response list "items" has 2 items
    And the response path "items.0.publication.name" equals JSON "Example Weekly"
    And the response path "items.0.signups" equals JSON 17
    And the response path "next_offset" equals JSON 2
    And the response path "items.0.publication" equals JSON {"id": 1001, "name": "Example Weekly", "subdomain": "exampleweekly", "custom_domain": null, "logo_url": "https://example.com/logo.png"}

  Scenario: Successfully fetch incoming recommendation stats
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "recommendations-to" endpoint returns the sample response
    When I send GET /api/v1/stats/recommendations/incoming
    Then the response status code is 200
    And the response path "items.0.publication.name" equals JSON "Fictional Notes"
    And the response path "next_offset" equals JSON null

  Scenario: Recommendation stats reject an unknown direction
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    When I send GET /api/v1/stats/recommendations/sideways
    Then the response status code is 422

  Scenario: Recommendation stats Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "recommendations-from" endpoint returns status 503
    When I send GET /api/v1/stats/recommendations/outgoing
    Then the response status code is 502

  # ------------------------------------------------------------------
  # GET /stats/posts/counts
  # ------------------------------------------------------------------

  Scenario: Successfully fetch post counts
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "post-counts" endpoint returns the sample response
    When I send GET /api/v1/stats/posts/counts
    Then the response status code is 200
    And the response path "published" equals JSON 120
    And the response path "drafts_is_capped" equals JSON false

  Scenario: Post counts Substack API error returns 502
    Given a valid gateway token "test-token" and publication URL "https://example.substack.com"
    And the Substack stats "post-counts" endpoint returns status 503
    When I send GET /api/v1/stats/posts/counts
    Then the response status code is 502
