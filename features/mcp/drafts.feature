Feature: MCP draft tools
  As a Claude AI assistant
  I want to use MCP tools to manage Substack post drafts
  So that I can read, create, and delete drafts programmatically

  Scenario: get_draft returns draft data
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack get-draft endpoint returns the sample response for draft 189535264
    When I call the MCP tool get_draft with draft_id 189535264
    Then the MCP result field "title" is not null

  Scenario: create_draft returns created draft data
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns the sample response
    When I call the MCP tool create_draft with title "Test Draft"
    Then the MCP result field "id" is not null
    And the MCP result field "uuid" is not null

  Scenario: delete_draft returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack delete-draft endpoint returns status 204 for draft 189535264
    When I call the MCP tool delete_draft with draft_id 189535264
    Then the MCP result is "Draft 189535264 deleted successfully."
