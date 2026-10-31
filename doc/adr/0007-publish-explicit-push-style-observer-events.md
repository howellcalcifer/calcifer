# 7. Publish explicit push-style observer events

Date: 2026-10-31

## Status

Accepted

Amends the notification mechanism in [5. Make input and game observer subjects, not inventory and protagonist](0005-make-input-and-game-observer-subjects-not-inventory-and-protagonist.md) and [6. Move action validation into input-game observer](0006-move-action-validation-into-input-observer.md).

Parse-error presentation is further specified by [8. Route input errors through the output observer](0008-route-input-errors-through-output-observer.md).

## Context

The input-to-game-to-output flow used pull-style notifications. A subject notified observers by passing itself, and observers inspected a changed-attribute marker and read mutable fields such as the controller's action or the game's latest action and rejection. This split the notification from its meaning and payload, coupled observers to subject state, and made tests set multiple fields to represent one occurrence.

Actions and their outcomes are transient occurrences: output should respond to the specific action that was submitted, applied, or rejected, rather than infer what happened by reading the latest state. Game start and stop are also explicit lifecycle occurrences.

## Decision

- Keep the existing Observer pattern and the input-to-game-to-output subscription flow.
- Publish an event object to observers instead of passing the subject for observers to inspect.
- Represent flow notifications explicitly with `ActionSubmitted`, `ActionApplied`, `ActionRejected`, `GameStarted`, and `GameStopped` event types.
- Have the command-line input controller return its parsed action and publish it as `ActionSubmitted`. Have the game publish action outcomes and lifecycle events directly.
- Retain `ObservedAttribute` for other observed model attributes, but have it publish an `AttributeChanged` event instead of relying on a shared changed-attribute marker.

## Consequences

- Event meaning and its relevant payload travel together, removing the `latest_action`, `latest_rejected_action`, and `changed_observed_attribute` protocol from the game flow.
- Observers depend on the event types they handle rather than querying controller or game fields to infer what changed.
- Tests can exercise notifications by publishing the relevant event directly.
- Observers now depend on the event contract, so changes to event types or payloads need to be coordinated with their subscribers.
- Notifications remain synchronous and in-process; this decision does not introduce a message broker, queue, or durable event log.