---
name: scholarly-search
description: Finds and records scholarly literature with OpenAlex and browser-assisted research. Use when a student asks an agent to search for literature relevant to a project or prepare a sourced bibliography.
---

# Scholarly search

## Start

Ask the student for the project question and a few useful terms. Propose search phrases in relevant languages, then search [OpenAlex](https://openalex.org/) using its [works API](https://help.openalex.org/api/searching/) or permitted browser tools. Record what you actually searched and found. Do not use OpenCode's simple web search for this assignment.

Example request to your agent:

> Use the `scholarly-search` skill. Help me find scholarship relevant to my project question: [question]. Search OpenAlex, record the queries and candidate works with source links, and explain which passages I should read. Help me search Google Scholar myself if useful.

## Set up browser automation in OpenCode

Use Vercel's [agent-browser](https://github.com/vercel-labs/agent-browser), a CLI made for coding agents. From the workspace root, a student can ask OpenCode:

> Use the `scholarly-search` skill. Please set up agent-browser using its official instructions, explain each step simply, and show me how you can search for my research question. Tell me if you need my help.

First check `agent-browser --version` and `node --version`. If missing, install Node.js from https://nodejs.org/ and follow the official installation: `npm install -g agent-browser`; then `agent-browser install` if no usable browser is detected. This may download a browser engine. It does not require the student to use Chrome developer tools or configure an MCP server. If a global install fails, diagnose permissions and use the project's documented local install; don't suggest unsafe permission changes. Restart OpenCode if a newly installed command is not visible.

For a permitted site, use `agent-browser open <URL>`, `agent-browser snapshot -i`, then `click` or `fill` a current snapshot reference, and take a fresh snapshot after navigation. For OpenAlex, open `https://openalex.org/works`, find its search box in the snapshot, fill it with the student’s terms, submit and inspect the results; alternatively URL-encode the terms in `https://openalex.org/works?search=YOUR_QUERY`. Open the original record and record its link. `agent-browser open <URL> --headed` opens a visible window; the student can watch and handle sign-in. Use a separate session; do not access the student's existing browser profile without asking. Close the agent browser after the task. If blocked, show the student the problem and switch to a human-operated search; don't bypass verification. Consult `agent-browser --help` or its own current skills for command details. Students give the agent instructions in ordinary language; they do not need to type these commands themselves.

## Browser search beyond academic indexes

Try [DuckDuckGo](https://duckduckgo.com/), [Bing](https://www.bing.com/) and Chinese-language [Baidu](https://www.baidu.com/) to find publisher pages, archives and further leads. Ask the agent to propose short queries in English and Chinese, including names, dates and alternative spellings. Search the same idea in more than one engine, open the original result, then record the query and direct source link. A web hit is not automatically scholarly literature.

Example request: “Use agent-browser to search DuckDuckGo for my question, inspect a few relevant results, and record the query and original links in my Markdown bibliography; tell me what you could actually access.” If a search is blank or blocked, report it and switch to OpenAlex or a human-operated search; do not claim results appeared. If browser tools are missing, explain how to set up a suitable tool or ask the student to search and share results. The student can search any of these in their own browser and share useful results with the agent. For browser automation, check the current site rules first: DuckDuckGo’s [robots file](https://duckduckgo.com/robots.txt) currently allows root search queries while disallowing `/html` and `/lite`; permitted automation still depends on applicable service terms and access. Bing’s [robots file](https://www.bing.com/robots.txt) disallows `/search` and Baidu’s [robots file](https://www.baidu.com/robots.txt) disallows automated access for the generic agent. Use those two manually. Do not bypass blocks, captchas or logins.

## Workflow

1. **Develop the query.** Derive two or three combinations from the student's design question, related concepts and historical context. Check the student's intended meaning; do not invent it.
2. **Search OpenAlex.** A small API query can be made without a key, for example `https://api.openalex.org/works?search=YOUR_QUERY&per-page=5` (URL-encode the query). If using browser automation instead, use the browser tools available to the student and follow the site's access rules. Explain the search and limits. If access or a key is needed, explain the actual requirement; do not assume a particular browser, extension or agent setup.
3. **Google Scholar, with the student at the controls.** Have the student enter the query and open results in their browser; the agent can suggest phrases and help assess links the student shares. Google Scholar asks automated software to respect its [robots rules](https://scholar.google.com/robots.txt), which disallow its search endpoint. Do not automate Scholar searches, scrape results, evade restrictions or bypass a CAPTCHA. The student handles any sign-in or verification.
4. **Open promising records.** Verify author, title, date, publication and DOI or stable link on the publisher or another authoritative record. An index result, abstract or Deep Research report is a lead, not proof that the full work was read. Identify accessible full text and tell the student what is unavailable. No invented citations or quotations.
5. **Keep a working bibliography and journal.** Use a plain Markdown bibliography in the project’s `research/` folder; no separate reference manager is required. For each candidate record the search route and query, citation, stable link, relevance, and access/reading status. When reading a work, distinguish the author's argument from the agent's suggestion and the student's thought. Give a page, section or precise locator for each claim or quotation; read the context before presenting it as evidence.
6. **Assign reading and return.** Ask agents to read available works for specific questions and return sourced passages. The student reads important passages personally, adds their thinking to the research journal and integrates resulting changes into the design document. Repeat the search if the evidence opens new questions.

Deep Research is optional if the student already has access; check its references and important claims against the actual works. Handle credentials privately and never save them in project files.
