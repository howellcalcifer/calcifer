# 3. use observer pattern to respond to changes in game state

Date: 2023-06-24

## Status

Accepted

## Context

Right now, I want to be able to respond to changes in inventory state and character actions like "look" 
with an appropriate message in the output.  Ultimately, similar changes in game state will need 
to trigger other behaviours (location change, plot elements unlocking, etc).

## Decision

Make the Character and Inventory classes subjects in the observer pattern.  Subscribe observers
to the protagonist and its inventory that respond to changes in their state by interacting with the output controller to 
show scene messages.

## Consequences

In future, other observers can easily be subscribed to these objects to respond to change in state to handle
different game behaviours, in a fairly loosely coupled way.  

I can also extend use of the pattern to observe other changes in game state.

I'll just use a pretty simple implementation of the classic observer pattern for now but this could be
re-implemented with a message broker and e.g. more complex pub-sub event topics if needed down the line.