Feature: MCP public post tools
  As a Claude AI assistant
  I want to use MCP tools to fetch public Substack post data
  So that I can read posts programmatically without authentication

  Scenario: get_post returns post data
    Given the Substack full post endpoint returns the sample response for post 987654
    When I call the MCP tool get_post with post_id 987654
    Then the MCP result field "title" is "Sample Post Title"
    And the MCP result field "slug" is "sample-post-title"

  Scenario: get_post_comments returns comments
    Given the Substack comments endpoint returns the sample response for post 987654
    When I call the MCP tool get_post_comments with post_id 987654
    Then the MCP result field "items" is not null
