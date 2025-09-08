# Project Sentinel: Phase 2 - AI Risk Assessment Agent

## 1. Objective

The goal of Phase 2 was to elevate the simple machine learning model created in Phase 1 into a sophisticated AI agent. Instead of just getting a binary output (0 or 1), we aimed to build a system that could reason about a transaction, use the model as a tool, and produce a structured, human-readable **risk assessment report**.

This phase demonstrates the integration of traditional machine learning with modern Large Language Model (LLM) frameworks.

---

## 2. Architecture and Core Components

The agent is built using a combination of our custom model and the LangChain framework.

- **LangChain Framework** — The orchestrator. We use LangChain to construct the agent, define its tools, and manage interactions between components.
- **Google Gemini (LLM)** — Acts as the "brain" of the agent. Gemini understands the task, decides which tool(s) to call, and formulates the final natural-language response using tool outputs.
- **`fraud_detection_tool` (Custom Tool)** — Bridge between Phase 1 and the LangChain agent. The XGBoost model (`xgb_fraud_detector.joblib`) was wrapped in a Python function and exposed to the LLM via LangChain's `@tool` decorator, enabling the LLM to call the model with structured inputs.

---

## 3. How It Works: The ReAct Logic

The agent follows the **ReAct** (Reasoning and Acting) pattern. It runs in a loop of internal reasoning and tool use until it can produce a final answer.

1. **Thought:** The agent receives transaction details and reasons about the task. _Example_: "I need to use the fraud detection tool to analyze this transaction."
2. **Action:** The agent decides to call `fraud_detection_tool`.
3. **Action Input:** Transaction features are formatted into the comma-separated string the tool expects.
4. **Observation:** The tool runs the XGBoost model and returns a raw prediction, e.g. `Tool raw prediction: 1, result: FRAUD`.
5. **Thought:** The agent inspects the observation and determines whether it needs more information or can proceed.
6. **Final Answer:** The agent synthesizes the tool output into a structured, professional risk assessment report as instructed by its prompt.

> The full ReAct trace (thoughts, actions, observations) is printed to the terminal at runtime for transparency and debugging.

---

## 4. Key Achievements

- **Successful ML + LLM integration:** The classic XGBoost model is exposed as a callable tool for the LLM-powered agent.
- **Autonomous tool usage & reasoning:** The agent reasons about tasks and autonomously decides when and how to use available tools.
- **Structured, business-ready output:** Raw model predictions are converted into high-quality, human-readable risk assessment reports.
- **Engineering resilience:** Addressed real-world issues (library/version mismatches, data-format inconsistencies, API changes) during development.

---

## 5. How to Run This Phase

1. Ensure the model artifacts from Phase 1 are available (for example: `xgb_fraud_detector.joblib`, `scaler.joblib`). Place them in the expected `models/` or `artifacts/` directory.
2. Ensure your `GOOGLE_API_KEY` (and any other required API keys) are set in a `.env` file in the project root.

```bash
# From project root
./run_phase2.sh
```

The script will install any new dependencies (if needed), execute the agent, and print the full reasoning trace and final assessments to the terminal.

---

## Notes & Tips

- The agent was developed using LangChain and tested with Google Gemini as the LLM. If you swap the LLM provider, you may need to update the prompt templates and any provider-specific adapter code.
- Keep an eye on input formatting: the tool expects features in a specific (comma-separated) order — mismatches will lead to incorrect model inputs.
- For production use, consider adding rate-limiting, caching of model/tool results, and a human-review workflow for high-risk cases.

---

*End of Phase 2 report.*

