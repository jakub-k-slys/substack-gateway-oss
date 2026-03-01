Feature: Markdown to Substack draft body converter
  As an API implementor
  I want to convert markdown text to the Substack draft body JSON string
  So that I can create and update drafts via the API

  # ------------------------------------------------------------------
  # Output format
  # ------------------------------------------------------------------

  Scenario: Output is a JSON string containing a doc node
    When I convert draft markdown "Hello world."
    Then the draft body is a JSON string
    And the draft doc type is "doc"
    And the draft doc has no schema version attribute

  # ------------------------------------------------------------------
  # Basic text formatting
  # ------------------------------------------------------------------

  Scenario: Plain text paragraph
    When I convert draft markdown "This is a simple paragraph."
    Then the draft doc has 1 node
    And draft node 1 is a paragraph with 1 text node "This is a simple paragraph."

  Scenario: Bold text uses strong mark
    When I convert draft markdown "This is **bold text**."
    Then the draft doc has 1 node
    And draft paragraph 1 text node 1 is plain "This is "
    And draft paragraph 1 text node 2 has mark "strong" and text "bold text"
    And draft paragraph 1 text node 3 is plain "."

  Scenario: Italic text uses em mark
    When I convert draft markdown "This is *italic text*."
    Then the draft doc has 1 node
    And draft paragraph 1 text node 1 is plain "This is "
    And draft paragraph 1 text node 2 has mark "em" and text "italic text"
    And draft paragraph 1 text node 3 is plain "."

  Scenario: Bold and italic combined produce two marks on one node
    When I convert draft markdown "This is ***bold italic***."
    Then the draft doc has 1 node
    And draft paragraph 1 text node 1 is plain "This is "
    And draft paragraph 1 text node 2 has marks "strong,em" and text "bold italic"
    And draft paragraph 1 text node 3 is plain "."

  Scenario: Inline code
    When I convert draft markdown "Use `code` here."
    Then the draft doc has 1 node
    And draft paragraph 1 text node 1 is plain "Use "
    And draft paragraph 1 text node 2 has mark "code" and text "code"
    And draft paragraph 1 text node 3 is plain " here."

  # ------------------------------------------------------------------
  # Headings
  # ------------------------------------------------------------------

  Scenario: Heading level 1 produces a heading node not a paragraph
    When I convert draft markdown "# Heading One"
    Then the draft doc has 1 node
    And draft node 1 is a heading with level 1 and text "Heading One"

  Scenario: Heading level 2
    When I convert draft markdown "## Heading Two"
    Then the draft doc has 1 node
    And draft node 1 is a heading with level 2 and text "Heading Two"

  Scenario: Heading level 3
    When I convert draft markdown "### Heading Three"
    Then the draft doc has 1 node
    And draft node 1 is a heading with level 3 and text "Heading Three"

  # ------------------------------------------------------------------
  # Lists
  # ------------------------------------------------------------------

  Scenario: Bullet list produces a single bullet_list node with list_item children
    When I convert draft markdown:
      """
      - item one
      - item two
      - item three
      """
    Then the draft doc has 1 node
    And draft node 1 is a bullet_list with 3 items
    And draft list item 1 text is "item one"
    And draft list item 2 text is "item two"
    And draft list item 3 text is "item three"

  Scenario: Ordered list produces an ordered_list node with correct attrs
    When I convert draft markdown:
      """
      1. item 1
      2. item 2
      3. item 3
      """
    Then the draft doc has 1 node
    And draft node 1 is an ordered_list with 3 items
    And draft ordered_list start attr is 1
    And draft list item 1 text is "item 1"
    And draft list item 2 text is "item 2"
    And draft list item 3 text is "item 3"

  Scenario: Blank lines between list items do not split the list
    When I convert draft markdown:
      """
      - first

      - second

      - third
      """
    Then the draft doc has 1 node
    And draft node 1 is a bullet_list with 3 items

  Scenario: Paragraph between two bullet lists creates two separate list nodes
    When I convert draft markdown:
      """
      - list one item

      paragraph in between

      - list two item
      """
    Then the draft doc has 3 nodes
    And draft node 1 is a bullet_list with 1 items
    And draft node 2 is a paragraph with 1 text node "paragraph in between"
    And draft node 3 is a bullet_list with 1 items

  # ------------------------------------------------------------------
  # Mixed content (the full example from the user)
  # ------------------------------------------------------------------

  Scenario: Full document matches Substack's expected structure
    When I convert draft markdown:
      """
      Hello! How are you? **This is BOLD.** *This is italic.* ***This is BOLD and italic.***

      # This is heading1

      this is normal text

      # this is another heading1

      this is normal text

      ## this is heading2

      here will be bullet list:

      - item
      - item
      - item

      ### this is heading 3

      some text

      this is numbered list

      1. item 1
      2. item 2
      3. item 3
      """
    Then the draft doc has 12 nodes
    And draft node 1 is a paragraph
    And draft node 2 is a heading with level 1 and text "This is heading1"
    And draft node 3 is a paragraph with 1 text node "this is normal text"
    And draft node 4 is a heading with level 1 and text "this is another heading1"
    And draft node 5 is a paragraph with 1 text node "this is normal text"
    And draft node 6 is a heading with level 2 and text "this is heading2"
    And draft node 7 is a paragraph with 1 text node "here will be bullet list:"
    And draft node 8 is a bullet_list with 3 items
    And draft node 9 is a heading with level 3 and text "this is heading 3"
    And draft node 10 is a paragraph with 1 text node "some text"
    And draft node 11 is a paragraph with 1 text node "this is numbered list"
    And draft node 12 is an ordered_list with 3 items
    And draft paragraph 1 text node 1 is plain "Hello! How are you? "
    And draft paragraph 1 text node 2 has mark "strong" and text "This is BOLD."
    And draft paragraph 1 text node 6 has marks "strong,em" and text "This is BOLD and italic."
