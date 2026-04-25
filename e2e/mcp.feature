Feature: MCP public tools

  Background:
    Given a test profile slug
    And a test post ID
    And a test note ID

  Scenario: Initialize MCP and list public tools
    When I initialize the MCP session
    Then the MCP initialize request succeeds
    When I request the MCP tool list
    Then the MCP tool list includes "get_note"
    And the MCP tool list includes "get_post"
    And the MCP tool list includes "get_post_comments"
    And the MCP tool list includes "get_profile"
    And the MCP tool list includes "get_profile_posts"
    And the MCP tool list includes "get_profile_notes"

  Scenario: Call public MCP tools over HTTP
    When I initialize the MCP session
    Then the MCP initialize request succeeds
    When I call the MCP tool get_profile for the test slug
    Then the MCP tool call succeeds
    When I call the MCP tool get_post for the test post
    Then the MCP tool call succeeds
    When I call the MCP tool get_note for the test note
    Then the MCP tool call succeeds
