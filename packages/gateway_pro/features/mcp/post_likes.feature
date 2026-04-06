Feature: MCP post like tools
  As a Pro AI assistant
  I want to like and unlike Substack posts through MCP
  So that I can manage post reactions programmatically

  Scenario: like_post returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack like-post endpoint returns status 200 for post 191598243
    When I call the MCP tool like_post with post_id 191598243
    Then the MCP result is "Post 191598243 liked successfully."

  Scenario: unlike_post returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack unlike-post endpoint returns status 204 for post 191598243
    When I call the MCP tool unlike_post with post_id 191598243
    Then the MCP result is "Post 191598243 unliked successfully."
