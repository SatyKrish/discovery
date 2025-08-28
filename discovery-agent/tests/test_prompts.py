import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "temporal"))

from prompts import (
    GENAI_PROMPT,
    TOOL_COMPLETION_PROMPT,
    render_genai_prompt,
    render_tool_completion_prompt,
)


def test_render_genai_prompt_substitution_and_escaping():
    history = [
        {"role": "user", "content": "Compute {1+1}"},
        {"role": "assistant", "content": "Result was {2}"},
    ]
    goal = "Answer {math question}"
    tools = ["calc", "search{engine}"]

    prompt = render_genai_prompt(history, goal, tools)

    # Check that placeholders were substituted
    assert "Answer {math question}" in prompt
    assert "user: Compute {1+1}" in prompt
    assert "assistant: Result was {2}" in prompt
    assert "- calc" in prompt and "- search{engine}" in prompt

    # Ensure no raw template fields remain
    assert "{goal}" not in prompt
    assert "{history}" not in prompt
    assert "{tools}" not in prompt

    # Ensure braces were preserved, not treated as format tokens
    assert "{{" not in prompt and "}}" not in prompt


def test_render_tool_completion_prompt_substitution_and_escaping():
    output = render_tool_completion_prompt(
        tool="calc{tool}",
        result="5 > 3 {True}",
        goal="Explain {comparison}",
    )

    assert "calc{tool}" in output
    assert "5 > 3 {True}" in output
    assert "Explain {comparison}" in output
    assert "{result}" not in output
    assert "{goal}" not in output
    assert "{{" not in output and "}}" not in output
