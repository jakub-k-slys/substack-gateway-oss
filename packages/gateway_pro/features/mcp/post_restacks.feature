Feature: MCP post restack tool
  As a Pro AI assistant
  I want to restack Substack posts through MCP
  So that I can share them programmatically

  Scenario: restack_post returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack restack-post endpoint returns status 200
    When I call the MCP tool restack_post with post_id 191598243
    Then the MCP result is "Post 191598243 restacked successfully."
