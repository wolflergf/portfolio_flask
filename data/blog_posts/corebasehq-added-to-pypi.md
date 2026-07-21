---
title: corebasehq added to PyPI
date: 2026-07-21
source_url: https://pypi.org/project/corebasehq/
---

I'm thrilled to announce that `corebasehq` is now available on PyPI, marking a significant step for developers and data scientists looking to integrate powerful AI capabilities with their proprietary data. This official Python SDK for the CoreBase Developer API is designed to streamline your daily work by providing an OpenAI-compatible interface for chatting over your connected data, managing data sources, triggering agent runs, and securing widget sessions. My goal with this release is to empower you to build sophisticated, data-aware applications with ease and familiarity.

One of the most immediate practical benefits for you is the OpenAI-compatible chat endpoint. This means that if you're already working with OpenAI's APIs, you can quickly integrate CoreBase by simply pointing your existing OpenAI clients to our API's base URL. This significantly reduces the learning curve and allows you to leverage your current tooling and expertise. Beyond chat, the SDK allows you to list and manage your data sources, execute governed agent runs for automation, and securely sign widget session tokens for embedding CoreBase functionality directly into your user interfaces.

I've ensured the SDK is easy to install, supporting `pip`, `uv`, and `poetry`, with a minimum Python version of 3.10. For developers, I've included both synchronous and asynchronous examples for chat completions, highlighting the flexibility in integrating the API into various application architectures. Crucially, the SDK comes equipped with robust features like configurable retry strategies for reliable API calls, comprehensive error handling with a dedicated `CorebaseError` class for easier debugging, and strong authentication using a bearer token. There's even specific IDE support for PyCharm users, offering enhanced integration with Pydantic.

Ultimately, my key takeaway for you is this: `corebasehq` is engineered to make integrating advanced conversational AI, data interaction, and intelligent automation into your applications straightforward and efficient. It provides the tools to build secure, scalable solutions that tap into your unique datasets, all while leveraging a developer experience that feels familiar. I encourage you to install the SDK and start exploring how you can transform your connected data into intelligent applications today.

[Read the full article here](https://pypi.org/project/corebasehq/)