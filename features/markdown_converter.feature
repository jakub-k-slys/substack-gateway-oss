Feature: Markdown to Substack note payload converter
  As an API implementor
  I want to convert markdown text to the Substack note JSON payload
  So that I can create notes via the API

  # ------------------------------------------------------------------
  # Basic text formatting
  # ------------------------------------------------------------------

  Scenario: Plain text paragraph
    When I convert the markdown "This is a simple paragraph."
    Then the note payload has 1 paragraph
    And paragraph 1 has 1 text node with text "This is a simple paragraph."

  Scenario: Bold text
    When I convert the markdown "This is **bold text**."
    Then the note payload has 1 paragraph
    And paragraph 1 text node 1 is plain "This is "
    And paragraph 1 text node 2 is bold "bold text"
    And paragraph 1 text node 3 is plain "."

  Scenario: Italic text
    When I convert the markdown "This is *italic text*."
    Then the note payload has 1 paragraph
    And paragraph 1 text node 1 is plain "This is "
    And paragraph 1 text node 2 is italic "italic text"
    And paragraph 1 text node 3 is plain "."

  Scenario: Inline code
    When I convert the markdown "This is `inline code` in text."
    Then the note payload has 1 paragraph
    And paragraph 1 text node 1 is plain "This is "
    And paragraph 1 text node 2 is code "inline code"
    And paragraph 1 text node 3 is plain " in text."

  Scenario: Mixed inline formatting
    When I convert the markdown "This is **bold**, *italic*, and `code` text."
    Then the note payload has 1 paragraph
    And paragraph 1 text node 1 is plain "This is "
    And paragraph 1 text node 2 is bold "bold"
    And paragraph 1 text node 3 is plain ", "
    And paragraph 1 text node 4 is italic "italic"
    And paragraph 1 text node 5 is plain ", and "
    And paragraph 1 text node 6 is code "code"
    And paragraph 1 text node 7 is plain " text."

  # ------------------------------------------------------------------
  # Headings
  # ------------------------------------------------------------------

  Scenario: Heading rendered as bold paragraph
    When I convert the markdown "## Main Heading"
    Then the note payload has 1 paragraph
    And paragraph 1 has 1 text node with bold text "Main Heading"

  Scenario: Multiple heading levels all become bold paragraphs
    When I convert the markdown:
      """
      # H1 Heading
      ## H2 Heading
      ### H3 Heading
      #### H4 Heading
      """
    Then the note payload has 4 paragraphs
    And paragraph 1 has 1 text node with bold text "H1 Heading"
    And paragraph 2 has 1 text node with bold text "H2 Heading"
    And paragraph 3 has 1 text node with bold text "H3 Heading"
    And paragraph 4 has 1 text node with bold text "H4 Heading"

  # ------------------------------------------------------------------
  # Multiple paragraphs
  # ------------------------------------------------------------------

  Scenario: Multiple paragraphs separated by blank lines
    When I convert the markdown:
      """
      ## Heading

      First paragraph with **bold** text.

      Second paragraph with *italic* text.
      """
    Then the note payload has 3 paragraphs
    And paragraph 1 has 1 text node with bold text "Heading"
    And paragraph 2 text node 1 is plain "First paragraph with "
    And paragraph 2 text node 2 is bold "bold"
    And paragraph 2 text node 3 is plain " text."
    And paragraph 3 text node 1 is plain "Second paragraph with "
    And paragraph 3 text node 2 is italic "italic"
    And paragraph 3 text node 3 is plain " text."

  # ------------------------------------------------------------------
  # Links
  # ------------------------------------------------------------------

  Scenario: Link rendered as "text (url)" plain text
    When I convert the markdown "Check out [n8n](https://n8n.io) for automation."
    Then the note payload has 1 paragraph
    And paragraph 1 text node 1 is plain "Check out "
    And paragraph 1 text node 2 is plain "n8n (https://n8n.io)"
    And paragraph 1 text node 3 is plain " for automation."

  Scenario: Multiple links in one paragraph
    When I convert the markdown "Visit [n8n](https://n8n.io) and [Substack](https://substack.com) today."
    Then the note payload has 1 paragraph
    And paragraph 1 text node 1 is plain "Visit "
    And paragraph 1 text node 2 is plain "n8n (https://n8n.io)"
    And paragraph 1 text node 3 is plain " and "
    And paragraph 1 text node 4 is plain "Substack (https://substack.com)"
    And paragraph 1 text node 5 is plain " today."

  # ------------------------------------------------------------------
  # Lists
  # ------------------------------------------------------------------

  Scenario: Unordered list items become paragraphs with bullet prefix
    When I convert the markdown:
      """
      - First item
      - Second item
      - Third item
      """
    Then the note payload has 3 paragraphs
    And paragraph 1 text node 1 is plain "• "
    And paragraph 1 text node 2 is plain "First item"
    And paragraph 2 text node 1 is plain "• "
    And paragraph 2 text node 2 is plain "Second item"
    And paragraph 3 text node 1 is plain "• "
    And paragraph 3 text node 2 is plain "Third item"

  Scenario: Ordered list items become paragraphs with number prefix
    When I convert the markdown:
      """
      1. First item
      2. Second item
      3. Third item
      """
    Then the note payload has 3 paragraphs
    And paragraph 1 text node 1 is plain "1. "
    And paragraph 1 text node 2 is plain "First item"
    And paragraph 2 text node 1 is plain "2. "
    And paragraph 2 text node 2 is plain "Second item"
    And paragraph 3 text node 1 is plain "3. "
    And paragraph 3 text node 2 is plain "Third item"

  Scenario: List items with inline formatting
    When I convert the markdown:
      """
      - First **bold** item
      - Second *italic* item
      - Third `code` item
      """
    Then the note payload has 3 paragraphs
    And paragraph 1 text node 1 is plain "• "
    And paragraph 1 text node 2 is plain "First "
    And paragraph 1 text node 3 is bold "bold"
    And paragraph 1 text node 4 is plain " item"
    And paragraph 2 text node 1 is plain "• "
    And paragraph 2 text node 2 is plain "Second "
    And paragraph 2 text node 3 is italic "italic"
    And paragraph 2 text node 4 is plain " item"
    And paragraph 3 text node 1 is plain "• "
    And paragraph 3 text node 2 is plain "Third "
    And paragraph 3 text node 3 is code "code"
    And paragraph 3 text node 4 is plain " item"

  Scenario: Empty list items are skipped
    When I convert the markdown with an empty list item
    Then the note payload has 2 paragraphs
    And paragraph 1 text node 2 is plain "First item"
    And paragraph 2 text node 2 is plain "Third item"

  # ------------------------------------------------------------------
  # Preprocessing
  # ------------------------------------------------------------------

  Scenario: Literal backslash-n sequences are converted to newlines
    When I convert the markdown with literal backslash-n escapes
    Then the note payload has 2 paragraphs
    And paragraph 1 has 1 text node containing a newline
    And paragraph 2 has 1 text node with text "Third paragraph"

  # ------------------------------------------------------------------
  # Payload envelope
  # ------------------------------------------------------------------

  Scenario: Payload has correct envelope fields
    When I convert the markdown "Hello world."
    Then the note payload tabId is "for-you"
    And the note payload surface is "feed"
    And the note payload replyMinimumRole is "everyone"
    And the note payload bodyJson type is "doc"
    And the note payload bodyJson schemaVersion is "v1"

  # ------------------------------------------------------------------
  # Error cases
  # ------------------------------------------------------------------

  Scenario: Empty markdown raises an error
    When I convert the empty markdown
    Then a ValueError is raised with message "Note body cannot be empty - at least one paragraph with content is required"

  Scenario: Whitespace-only markdown raises an error
    When I convert the whitespace-only markdown
    Then a ValueError is raised with message "Note body cannot be empty - at least one paragraph with content is required"

  Scenario: Only empty headings raises an error
    When I convert the markdown "## \n### \n#### "
    Then a ValueError is raised with message "Note must contain at least one paragraph with actual content"

  Scenario: Only empty list items raises an error
    When I convert the markdown "- \n* \n1. "
    Then a ValueError is raised with message "Note must contain at least one paragraph with actual content"
