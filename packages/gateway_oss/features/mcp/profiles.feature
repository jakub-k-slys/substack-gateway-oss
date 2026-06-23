Feature: MCP profile tools
  As a Claude AI assistant
  I want to use MCP tools to look up Substack profiles and their content
  So that I can read any user's posts and notes programmatically

  Scenario: get_profile returns profile data
    Given the Substack public profile endpoint returns the sample response for "jakubslys"
    When I call the MCP tool get_profile with slug "jakubslys"
    Then the MCP result field "handle" is "jakubslys"

  Scenario: get_profile_posts returns posts page
    Given the Substack public profile endpoint returns the sample response for "jakubslys"
    And the Substack posts endpoint returns the sample response for user 254824415
    When I call the MCP tool get_profile_posts with slug "jakubslys"
    Then the MCP result field "items" is not null

  Scenario: get_profile_notes returns notes page
    Given the Substack public profile endpoint returns the sample response for "jakubslys"
    And the Substack profile notes endpoint returns the sample response for user 254824415
    When I call the MCP tool get_profile_notes with slug "jakubslys"
    Then the MCP result field "items" is not null
