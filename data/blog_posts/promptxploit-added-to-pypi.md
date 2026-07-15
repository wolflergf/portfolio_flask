---
title: promptxploit added to PyPI
date: 2026-07-15
source_url: https://pypi.org/project/promptxploit/
---

I'm excited to share details about `promptxploit`, my new open-source project now available on PyPI. As developers and data scientists increasingly integrate Large Language Models (LLMs) into applications, we face a critical challenge: securing them against prompt injection and jailbreak attacks. Manually uncovering these vulnerabilities is often a tedious, inconsistent, and incomplete process, leaving our LLM-powered systems exposed. `promptxploit` was built to address this directly, offering an automated, robust framework for LLM penetration testing.

For anyone working with LLMs, `promptxploit` is designed to seamlessly integrate into your daily workflow, transforming how you approach security. Instead of reactive firefighting, you can proactively discover weaknesses. Point it at any model or HTTP endpoint, and it will run a categorized set of adversarial prompts. What truly impacts your work is the local-first judging, ensuring sensitive model responses never leave your machine—a crucial privacy and security benefit. This means you can get structured, actionable reports of what attacks succeeded, all without disrupting your development environment or compromising data.

The practical benefits are significant. `promptxploit` streams attacks from curated datasets (like `tool_abuse`), providing comprehensive coverage that manual testing often misses. Its "rules-first" approach for verdict determination reduces false positives and minimizes costly model calls, making the process efficient and reliable. You'll receive clear JSON reports, complete with per-attack verdicts, risk scores, and rationales, enabling you to quickly pinpoint and prioritize fixes. Plus, with flexible rate limiting and framework-agnostic target support, `promptxploit` is adaptable to virtually any LLM setup you're working with.

Ultimately, my goal with `promptxploit` is to empower developers and data scientists to build more secure and trustworthy LLM applications. The key takeaway is that automated, systematic adversarial testing is no longer a luxury, but a necessity. By integrating `promptxploit` into your development and CI/CD pipelines, you gain a powerful ally in validating the robustness of your AI systems. And when combined with `PromptShield`, its defensive counterpart, you have a complete "test-then-defend-then-retest" workflow to harden your LLM applications against the evolving landscape of AI threats.

[Read the full article here](https://pypi.org/project/promptxploit/)