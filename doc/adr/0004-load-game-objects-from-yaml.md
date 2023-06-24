# 4. load game objects from yaml

Date: 2023-06-24

## Status

Accepted

## Context

I want to be able to define game world objects in a quick and readable way

## Decision

Provide definitions for:

- verbs available to the user
- characters (including the protagonist)
- locations
- items

in YAML format, which are loaded into string->object mappings at start up allowing them to be looked up
by a unique string key. 

## Consequences

- It's easy to add and modify world objects' definitions
- If we start to get lots of objects, may want to reimplement as a database rather than holding 
everything in memory
- Allows test contexts to be easily populated from alternative yaml definitions for integration/
functional testing
