Feature: MCP notes tools
  As a Claude AI assistant
  I want to use MCP tools to interact with Substack notes
  So that I can read, create, and delete notes programmatically

  Scenario: get_note returns note data
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack reader comment endpoint returns the sample response for id 131648795
    When I call the MCP tool get_note with note_id 131648795
    Then the MCP result field "id" is not null
    And the MCP result field "body" is not null

  Scenario: create_note returns created note data
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack create-note endpoint returns the sample response
    When I call the MCP tool create_note with content "Hello **world**."
    Then the MCP result field "id" is not null

  Scenario: delete_note returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack delete-note endpoint returns status 204 for note 131648795
    When I call the MCP tool delete_note with note_id 131648795
    Then the MCP result is "Note 131648795 deleted successfully."

  Scenario: invalid token raises ValueError
    Given an invalid MCP token and publication URL "https://example.substack.com"
    When I call the MCP tool get_note with note_id 131648795
    Then the MCP tool raises a ValueError
