Feature: MCP note like tools
  As a Pro AI assistant
  I want to like and unlike Substack notes through MCP
  So that I can manage note reactions programmatically

  Scenario: like_note returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack like-note endpoint returns status 200 for note 234058408
    When I call the MCP tool like_note with note_id 234058408
    Then the MCP result is "Note 234058408 liked successfully."

  Scenario: unlike_note returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack unlike-note endpoint returns status 204 for note 238483442
    When I call the MCP tool unlike_note with note_id 238483442
    Then the MCP result is "Note 238483442 unliked successfully."
