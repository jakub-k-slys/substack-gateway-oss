Feature: MCP agent flow
  As an MCP agent (e.g. Claude)
  I want to connect to the gateway, authenticate via OAuth, and use MCP tools
  So that I can interact with Substack programmatically

  # These tests simulate the full MCP agent lifecycle using raw HTTP calls
  # against the MCP streamable-http transport. They require:
  #   - SUBSTACK_GATEWAY_BASE_URL (e.g. http://localhost:5001)
  #   - SUBSTACK_TOKEN (base64-encoded Substack credentials)
  #   - SUBSTACK_PUBLICATION_URL (e.g. https://example.substack.com)
  #   - SUBSTACK_GATEWAY_ADMIN_TOKEN (admin token for user management API)
  # OAuth must be enabled on the target server.
  # A temporary test user is created via the admin API and deleted after each scenario.

  Background:
    Given OAuth is enabled on the gateway
    And a temporary test user exists

  # ------------------------------------------------------------------
  # Flow 1: Connect → Authorize → Use token → Call tool
  # ------------------------------------------------------------------

  Scenario: Full MCP agent flow — OAuth, initialize, list tools, call tool
    # 1) Discover OAuth metadata
    When I discover the OAuth metadata
    Then the metadata contains token and authorization endpoints
    # 2) Register as an OAuth client
    When I register as an OAuth client via the registration endpoint
    Then I have a registered client_id
    # 3) Start authorization flow
    When I start the OAuth authorization flow
    Then I am redirected to the login page
    # 4) Complete login (email/password + Substack token)
    When I complete the login and token submission
    Then I have an authorization code
    # 5) Exchange auth code for tokens
    When I exchange the authorization code for tokens
    Then I have an access token and a refresh token
    # 6) MCP initialize
    When I send an MCP initialize request with the access token
    Then the MCP server responds with capabilities
    # 7) List tools
    When I send an MCP tools/list request
    Then the tool list includes "get_me"
    And the tool list includes "get_note"
    And the tool list includes "create_draft"
    # 8) Call get_me tool
    When I call the MCP tool "get_me" with no arguments
    Then the MCP tool call succeeds

  # ------------------------------------------------------------------
  # Flow 2: Refresh token → Call tool with new token
  # ------------------------------------------------------------------

  Scenario: Token refresh flow — refresh and use new token
    # Setup: full OAuth handshake
    When I discover the OAuth metadata
    And I register as an OAuth client via the registration endpoint
    And I start the OAuth authorization flow
    And I complete the login and token submission
    And I exchange the authorization code for tokens
    And I save the current tokens
    # 1) Refresh the token
    When I exchange the refresh token for new tokens
    Then the new access token differs from the original
    # 2) MCP initialize with refreshed token
    When I send an MCP initialize request with the refreshed access token
    Then the MCP server responds with capabilities
    # 3) Call tool with refreshed token
    When I call the MCP tool "get_me" with no arguments
    Then the MCP tool call succeeds
    # 4) Verify old token is revoked
    When I send an MCP initialize request with the original access token
    Then the MCP server rejects the request
