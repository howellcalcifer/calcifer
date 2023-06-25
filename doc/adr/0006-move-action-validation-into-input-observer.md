# 6. Move action validation into input-game observer

Date: 2023-06-25

## Status

Accepted

## Context

Tests for action validation are awkward as they're tied to parsing from string input
currently.  It would be cleaner to separate them off into their own component.

## Decision

- Move action validation into its own component (ActionValidator)
- Publish unvalidated actions from input controller
- Move validation into the input-game observer and publish either the validation error or
the validated action from game context for the game-output observer to detect
- Game-output observer then outputs the appropriate scene/message

## Consequences

Testing validation is now easier as it's in its own component