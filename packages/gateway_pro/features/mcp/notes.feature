Feature: MCP note management tools
  As a Claude AI assistant
  I want to use authenticated MCP tools to manage Substack notes
  So that I can create and delete notes programmatically

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
    When I call the MCP tool create_note with content "Hello **world**."
    Then the MCP tool raises a ValueError
