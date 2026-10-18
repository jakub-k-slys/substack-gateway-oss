Feature: MCP stats tools
  As a Claude AI assistant
  I want to use MCP tools to read publication analytics
  So that I can report on subscribers and traffic

  Scenario: get_subscriber_timeseries returns points
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack subscriber-timeseries endpoint returns the sample response
    When I call the MCP tool get_subscriber_timeseries
    Then the MCP result field "items" is not null

  Scenario: get_30d_views returns view counts
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack 30d-views endpoint returns the sample response
    When I call the MCP tool get_30d_views
    Then the MCP result field "views_30d" is not null

  Scenario: get_arr_timeseries returns ARR rows
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack stats "ARR-timeseries" endpoint returns the sample response
    When I call the MCP tool get_arr_timeseries
    Then the MCP result path "items.0.arr" equals JSON 258.19

  Scenario: get_email_timeseries returns email subscriber rows
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack stats "email-timeseries" endpoint returns the sample response
    When I call the MCP tool get_email_timeseries
    Then the MCP result path "items.1.emails" equals JSON 415

  Scenario: get_dashboard_summary returns headline numbers
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack stats "dashboard-summary" endpoint returns the sample response
    When I call the MCP tool get_dashboard_summary
    Then the MCP result path "views" equals JSON 4200

  Scenario: get_dashboard_period returns the requested range
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack stats "dashboard-period" endpoint returns the sample response
    When I call the MCP tool get_dashboard_period with range_days 30
    Then the MCP result path "range_days" equals JSON 30
    And the MCP result path "paid_subscribers.end" equals JSON 6

  Scenario: get_recommendation_stats returns outgoing recommendations
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack stats "recommendations-from" endpoint returns the sample response
    When I call the MCP tool get_recommendation_stats with direction "outgoing"
    Then the MCP result path "items.1.publication.custom_domain" equals JSON "digest.example.com"

  Scenario: get_recommendation_stats returns incoming recommendations
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack stats "recommendations-to" endpoint returns the sample response
    When I call the MCP tool get_recommendation_stats with direction "incoming"
    Then the MCP result path "direction" equals JSON "incoming"

  Scenario: get_post_counts returns counts by state
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack stats "post-counts" endpoint returns the sample response
    When I call the MCP tool get_post_counts
    Then the MCP result path "scheduled" equals JSON 2

  Scenario: get_dashboard_summary surfaces an upstream auth failure
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack stats "dashboard-summary" endpoint returns status 401
    When I call the MCP tool get_dashboard_summary
    Then the MCP tool raises a SubstackAuthError
