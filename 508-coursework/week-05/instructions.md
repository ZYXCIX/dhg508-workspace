# Week 5

Before our next class.

## Tasks

In class we looked at the documents an agent works from, how to keep them
short and organised, and how to keep every version with git. This week you
put that into practice, and you take the step from a skill inside opencode to
a small app of your own: a page anyone can open in a browser, backed by a
server on your computer that asks a real model and reads your database.

Do everything through opencode, and make it explain what it is doing.

## Challenges

### 1. Reorganise your skill

Restructure last week's skill into an index and three kinds of documents:

- `SKILL.md`: a short index that says which file to read for which job;
- what it does: how it answers questions from your database;
- how to maintain it: how to add new material, step by step;
- principles: the few rules that always hold.

Keep each file short, with one job per file. Point from one file to another
instead of repeating yourself.

### 2. Keep every version

Commit every change with a message that says what changed and why, and push
regularly. Your commit history is part of the work.

### 3. Register a DeepSeek API key

Create an account at https://platform.deepseek.com and an API key. Add a small
amount of credit if needed. Keep the key in an environment variable, never in a
file that goes into Git.

### 4. Build your own app

Look at `demo-building-app/` in this folder first. It is a web page, a small
Python server, a "model", and the Week 3 buildings database. Run it with
`python3 server.py` and drop a photo in. It looks clever, but its model is a
**fixture**: `ask_model()` in `server.py` returns the same saved answer for
every photo.

Then build your own app for your own data and your own question:

- a Python server and one web page (plain HTML and JavaScript is enough);
- your database behind it;
- a **real** DeepSeek call in place of the fixture. Give opencode the official
  DeepSeek API documentation and ask it to write the call with you.

Do not copy the demo. Decide what your users should do on the page and what
they should get back.

### 5. Optional: explore the Blender MCP

Blender is free 3D software. Its developers publish an official MCP server that
lets an agent work in Blender:
https://projects.blender.org/lab/blender_mcp

Install Blender, connect the MCP server to opencode with its help, and see what
the agent can do: build a simple model, change it, render it. Note what worked,
what did not, and one idea for your own research.

## Bring to class

A five-minute demo:

- **Your app**, running, answering one real request.
- **Where the fixture was**, and what replaced it.
- **Your skill**: the index and its files.
- **Your commit history.**

Keep API keys and large files out of Git. Unresolved questions go to
`questions.md`.
