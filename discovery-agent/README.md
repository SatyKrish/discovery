# Discovery Agent

The `temporal.deep_agent` module provides a minimal autonomous agent used by the
Temporal workflow examples.  The new `create_deep_agent` factory makes it easy
to build a pre-configured agent with a base prompt, model, subagent registry,
extra tools, and step limit.

```python
from temporal.deep_agent import create_deep_agent
from langchain_community.tools import RequestsGetTool

agent = create_deep_agent(tools=[RequestsGetTool()])
result = await agent("2 + 2?")
```

The returned callable mirrors `run_agent` but applies the configuration above on
every invocation, letting callers focus on the question and optional
instructions.
