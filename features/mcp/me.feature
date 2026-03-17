Feature: MCP me and posts tools
  As a Claude AI assistant
  I want to use MCP tools to fetch my own profile, notes, posts, and individual posts
  So that I can read my own Substack content programmatically

  Scenario: get_me returns own profile
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack handles endpoint returns the sample response
    And the Substack public profile endpoint returns the sample response for "jakubslys"
    When I call the MCP tool get_me
    Then the MCP result field "handle" is "jakubslys"

  Scenario: get_my_notes returns notes page
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack notes endpoint returns the sample response
    When I call the MCP tool get_my_notes
    Then the MCP result field "items" is not null

  Scenario: get_my_posts returns posts page
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack handles endpoint returns the sample response
    And the Substack public profile endpoint returns the sample response for "jakubslys"
    And the Substack posts endpoint returns the sample response for user 254824415
    When I call the MCP tool get_my_posts
    Then the MCP result field "items" is not null

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

  Scenario: get_my_following returns following list
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack user-settings endpoint returns user id 254824415
    And the Substack subscriber-lists endpoint returns the sample response for user 254824415
    When I call the MCP tool get_my_following
    Then the MCP result field "items" is not null
