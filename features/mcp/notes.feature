Feature: MCP notes tools
  As a Claude AI assistant
  I want to use MCP tools to read public Substack notes
  So that I can inspect note content without authentication

  Scenario: get_note returns note data
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack reader comment endpoint returns the sample response for id 131648795
    When I call the MCP tool get_note with note_id 131648795
    Then the MCP result field "id" is not null
    And the MCP result field "body" is not null
