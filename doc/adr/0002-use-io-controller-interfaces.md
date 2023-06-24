# 2. use IO controller interfaces

Date: 2023-06-24

## Status

Accepted

## Context

I'm making a text adventure, using "plain english" keyboard syntax using command line input and output.  
But down the line I might want to have alternative ways of providing game input/output (e.g. point and click
graphical, audio out) to run the same game.

## Decision

Provide a generic input controller and output controller interface.  The input controller should return user
actions in a normalised form that is independent of whether generated from a text or e.g. graphical UI.  The output 
controller should receive generic "Scene" objects that could be rendered either as text or graphical/audio changes
(animations, background image change, audio, etc).

These interfaces will initially be implemented with text / command line concrete classes.

## Consequences

Should make implenting alternative game IO later while keeping the same engine for game logic.

