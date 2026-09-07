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
