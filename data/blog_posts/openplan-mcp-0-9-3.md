---
title: openplan-mcp 0.9.3
date: 2026-06-18
source_url: https://pypi.org/project/openplan-mcp/0.9.3/
---

When I set out to develop `openplan-mcp`, my core vision was to create a "Waze for AI agents" tackling software projects. This tool, an MCP server, is designed to empower AI agents to plan, track, and learn from their development efforts more efficiently than ever before. It's built around the idea of intelligent project orchestration, providing a structured framework for agents to manage tasks from inception to completion, ultimately leading to better outcomes.

For a Developer or Data Scientist working with AI agents, `openplan-mcp` profoundly impacts daily workflow by transforming how agents manage their tasks. I've equipped it with a suite of intuitive tools: `start()` to kick off projects by parsing goals into phases and estimating costs; `complete()` to mark phases done, attach evidence, and automatically advance; and `act()` for flexible project traversal, branching, verification, and status updates. Perhaps most powerfully, the `recommend()` tool uses an A* pathfinding algorithm to suggest the best next steps, providing real-time project health and cost estimates. These tools mean less guesswork and more guided, efficient project execution for your AI agents.

A crucial innovation I’ve integrated is the continuous learning loop. Just like Waze gathers traffic data from every driver, `openplan-mcp` collects anonymized calibration data from every agent’s `start()` and `complete()` calls. This data – comprising only project type, action, expected/actual cost, and outcome – feeds into a global calibration pool, constantly improving estimation accuracy for all agents. This means that as more AI agents use OpenPlan, the collective intelligence grows, making future project planning for your agents more precise and reliable, all while maintaining strict data privacy with a local-first architecture.

Ultimately, my goal with `openplan-mcp` is to bring unprecedented predictability and intelligence to AI agent-driven software development. It’s a tool for anyone looking to make their AI agents not just code generators, but strategic project managers. While the specific `0.9.3` release I'm detailing here was marked as "yanked," the underlying architecture and the significant benefits it offers for integrating planning, tracking, and collective learning into AI agent workflows remain a key takeaway for building more capable and efficient autonomous systems.

[Read the full article here](https://pypi.org/project/openplan-mcp/0.9.3/)