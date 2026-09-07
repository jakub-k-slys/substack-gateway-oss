Feature: MCP post-stats tools
  As a Claude AI assistant
  I want to use MCP tools to read a post's analytics
  So that I can report on how individual posts performed

  Scenario: get_post_engagement returns engagement
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack post engagement endpoint returns the sample response for post 42
    When I call the MCP tool get_post_engagement with post_id 42
    Then the MCP result field "likes_count" is not null

  Scenario: get_post_traffic returns traffic breakdown
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack post traffic endpoint returns the sample response for post 42
    When I call the MCP tool get_post_traffic with post_id 42
    Then the MCP result field "referrers" is not null

  Scenario: get_post_recipients returns recipient rows
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack post recipients endpoint returns the sample response for post 42
    When I call the MCP tool get_post_recipients with post_id 42
    Then the MCP result field "rows" is not null

  Scenario: get_post_growth returns growth data
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack post growth endpoint returns the sample response for post 42
    When I call the MCP tool get_post_growth with post_id 42
    Then the MCP result field "totalFreeSignups" is not null

  Scenario: get_post_discussion returns discussion items
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack post discussion endpoint returns the sample response for post 42
    When I call the MCP tool get_post_discussion with post_id 42
    Then the MCP result field "items" is not null
