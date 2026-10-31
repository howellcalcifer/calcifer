# 8. Route input errors through the output observer

Date: 2026-10-31

## Status

Accepted

Amends the input event flow described in [7. Publish explicit push-style observer events](0007-publish-explicit-push-style-observer-events.md).

## Context

The command-line input controller parsed user input and printed syntax errors directly, while semantic action errors were sent through the game and rendered by the output observer. This made the input adapter responsible for presentation and gave syntax errors a different output path. Alternative input and output interfaces would need to duplicate or bypass that behavior.

## Decision

- The input controller publishes an `InputRejected` event when parsing fails, rather than printing the error itself.
- The input-game observer forwards that rejection as an `ActionRejected` game event.
- The game-output observer renders the rejection through the output controller, using the same presentation path as semantic action rejections.
- The command-line controller continues waiting for another input after publishing the parse error.

## Consequences

- Input adapters report outcomes without deciding how errors are presented.
- Syntax and semantic rejections share the output-controller boundary, allowing different output implementations to present them appropriately.
- The engine remains independent of the UI parser's exception type; the event carries the error message as an exception value.
- Parse errors now pass through the input-game and game-output observers before being displayed.