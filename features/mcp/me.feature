Feature: MCP public post tools
  As a Claude AI assistant
  I want to use MCP tools to fetch public Substack post data
  So that I can read posts programmatically without authentication

  Scenario: get_post returns post data
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack full post endpoint returns the sample response for post 987654
    When I call the MCP tool get_post with post_id 987654
    Then the MCP result field "title" is "Sample Post Title"
    And the MCP result field "slug" is "sample-post-title"

  Scenario: get_post_comments returns comments
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack comments endpoint returns the sample response for post 987654
    When I call the MCP tool get_post_comments with post_id 987654
    Then the MCP result field "items" is not null
    And the MCP result list "items" has 2 items
    And the first MCP item in "items" has "id" equal to 111222333

  Scenario: get_post_comments propagates Substack auth failures
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack comments endpoint for post 987654 returns status 401
    When I call the MCP tool get_post_comments with post_id 987654
    Then the MCP tool raises a SubstackAuthError
