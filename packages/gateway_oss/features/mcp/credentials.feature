Feature: MCP credential resolution

  Scenario: A tool called without credentials reports how to supply them
    When I call the MCP tool get_note without credentials
    Then the MCP call fails asking for credentials
