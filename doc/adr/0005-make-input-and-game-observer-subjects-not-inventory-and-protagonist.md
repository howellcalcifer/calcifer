# 5. Make input and game observer subjects, not inventory and protagonist

Date: 2023-06-25

## Status

Accepted

Amends [3. use observer pattern to respond to changes in game state](0003-use-observer-pattern-for-game-events.md)

## Context

Implementing moving between locations made me realise that having separate observers 
for inventory and protagonist events was messy - both were really just about showing 
messages on actions.  

## Decision

I've made the game object the subject, and given it a "latest action" observed attribute.  
The game->output observer then just uses that to display messages.

I've also made the input controller interface a subject, meaning it can publish 
parsed actions out for the input->game observer to update the game state accordingly.
The input->game observer is now responsible for updating the game state based on
received actions, and also for setting the "latest action" attribute.  

There's therefore now a flow using observers of input->game->output.


## Consequences

Publishing action messages is now just the responsibility of the game->output controller
which makes extending with new actions easier, and has simplified testing.

I'm considering moving validation of actions out of the input controller and into the 
input->game observer so that the controller doesn't need to know about game state.

This would mean that there would probably need to be a way of publishing invalid actions out 
for the game->output observer to handle failure messages (e.g. "latest failed action" observed 
attribute).