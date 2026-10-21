# Week 8 · A Historical Simulation

Prepare before **Wednesday 28 October 2026**.

This class gave an overview of historical simulation. Now make a small one of your own.

**Mention your difficulties.**

## What we mean by a historical simulation

Not a game in the usual sense. A historical simulation rebuilds a real situation from the past: a place, the things in it, the people, and what happened or could happen there. Someone can enter it, look around, and try something.

Every part of it comes from sources, or is clearly marked as not coming from them. It need not be big; it must be historical. 2D or 3D, either is fine.

What matters most: **how does it help, as a medium, to teach a historical lesson?** Someone will ask you: why a simulation at all? If a film would teach the same thing just as well, the simulation has not yet earned its place. Find what someone learns only by being inside it and acting: choosing, trying, getting it wrong, seeing what follows.

## 1. Choose a situation

Choose **one** real situation from the past: a street, a room, a journey, a workplace, an event, a day in someone's life. Your Week 7 object can be part of it.

Say in two or three sentences what the simulation lets someone see or do, and what historical lesson they should come away with.

## 2. Ground it in sources

Collect the materials it rests on: photographs, maps, records, descriptions, data. Keep each with where it came from.

For every part of your simulation (the place, each object, each person, each rule of how things behave), mark one of:

- **evidenced**: taken from a source (say which);
- **inferred**: reasoned from sources (say how);
- **invented**: no source; made up so it works (say why).

## 3. Its people

The people in your simulation may be scripted in advance (a fixed dialogue tree, set routines): that is fine if you say why you chose it. Or they may be **agentic**: they decide for themselves.

- An agentic character has its own goals and a memory of who it is, written from your sources. It receives only what it could perceive in the scene (who is near, what was just said, what it can see), and it chooses its next action itself, including saying nothing.
- The world, not the language model, decides what actually happens. The character proposes "walk to the door" or "say X"; your page or game checks whether that is possible and reports the result back, so the model cannot simply claim it did something.
- Do not script it with rules ("always answer the player"). Describe the situation honestly and let it judge, but keep out of its mouth the history it could not have known.
- The smallest version: a web page with a text box and a short list of actions (say something, look at someone, walk to one of three named places). Each time something happens, send the character's background, what it perceives and the action list to a model API (DeepSeek or OpenRouter), ask for one action as JSON, carry it out in the page and show it.
- Log every call and its cost. One character for ten minutes costs a few cents if you send only what changed.

There is no worked example for this part. You already have every piece from earlier weeks; work out how to put them together:

1. **an agent**: your named agent and its skill (Weeks 3–5);
2. **tool calls**: the actions it can take, as in the agent we took apart in Week 4 (model, instructions, tools, loop);
3. **a knowledge base**: your database, with sources (Weeks 3–4);
4. **an API**: a real model call, as in your Week 5 app.

With these four you have everything you need. The rest is your own invention.

## 4. Build it

Any tools, any front end or back end. From simplest to fullest:

- **A web page** (plain HTML and JavaScript, or three.js): enough, if it is a real simulation.
- **Blender**: a modelled and rendered scene, built by an agent through the Blender MCP as shown last class, or by hand.
- **A game engine**: the easiest way to let someone walk or ride through a place.
  - Unity (https://unity.com) is the one shown in class.
  - If Unity does not work on your network or will not sign in, use Tuanjie (团结引擎, https://unity.cn), Unity's China edition.
  - Or use the open-source Godot (https://godotengine.org).

Best of all, bring together what we have done this term: image generation, 3D generation, 3D modelling by an agent through the Blender MCP, and your own database and skill (a person in the simulation can speak from them, with sources).

## Bring to class

- Your repository link, with an index.
- The simulation itself: a link, or a short screen recording if it cannot run on another computer.
- Your answer to "why not a film?": the historical lesson, and what only acting inside the simulation teaches.
- Your source list, and the table of parts marked evidenced / inferred / invented.
- What each tool did, what the AI did and what you checked yourself.
- At least one real difficulty, with its example.

Keep every prompt, input, output and cost. Keep large files out of Git: put files over a few MB in `artifacts/`, or store them elsewhere and link them. Keep API keys out of Git. Put unresolved questions in `questions.md`.
