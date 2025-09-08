# Project Sentinel: Phase 3 - LangGraph Multi-Agent Workflow

## 1. Objective
The goal of Phase 3 was to advance the project from a single agent to a stateful, multi-step workflow using **LangGraph**. This demonstrates a more sophisticated and realistic approach to building AI systems, moving beyond simple request-response interactions.  

We aimed to create a system that could mimic a real-world business process for handling transaction alerts, including **triaging, conditional routing, and escalation**.

---

## 2. Architecture and Core Components
The heart of this phase is a **Stateful Graph**, which represents the flow of a transaction through our risk assessment process.

- **LangGraph**: Core library used to construct the workflow. It allows us to define a series of steps ("nodes") and the logic for moving between them ("edges").  
- **Graph State (GraphState)**: A Python dictionary that holds information about the transaction as it passes through the graph. It tracks:
  - `transaction_details`
  - `triage_result`
  - `final_recommendation`
- **Nodes**: Python functions that perform specific actions and update the state. Key nodes include:
  - `triage_node`: Entry point; calls `fraud_detection_tool` for an initial assessment.
  - `legitimate_node`: Triggered for non-fraudulent transactions → sets `final_recommendation` to **"Approve"**.
  - `fraudulent_node`: Triggered for fraudulent transactions → sets `final_recommendation` to **"Escalate for Human Review"**.
- **Conditional Edges**: Routing logic that inspects the `triage_result` and decides the next node. Implemented via a function `decide_next_node`.

---

## 3. How It Works: Step-by-Step Flow
1. **Entry**: Transaction details are loaded into the initial state, starting at `triage_node`.  
2. **Triage**: `triage_node` executes `fraud_detection_tool` → result (`"FRAUD"` / `"NOT FRAUD"`) stored in state.  
3. **Decision**: Conditional edge inspects `triage_result`.  
4. **Routing**:
   - If `"NOT FRAUD"` → graph moves to `legitimate_node`.  
   - If `"FRAUD"` → graph moves to `fraudulent_node`.  
5. **Final Action**:
   - `legitimate_node` sets recommendation to **Approve**.  
   - `fraudulent_node` sets recommendation to **Escalate for Human Review**.  
6. **End**: Both nodes connect to the END → process terminates, returning the final state.

---

## 4. Key Achievements
- **Stateful AI Workflow**: Enables multi-step processing beyond a stateless agent.  
- **Conditional Logic & Routing**: Demonstrates intelligent workflow branching.  
- **Real-World Mimicry**: Directly parallels fraud triage/escalation in financial institutions.  
- **Modularity & Scalability**: Easy to extend with new nodes (e.g., notification, logging).  

---

## 5. How to Run This Phase
The process is **fully automated**.

1. Ensure your `GOOGLE_API_KEY` is set in the `.env` file.  
2. From the project root, run:

   ```bash
   ./run_phase3.sh
   ```
3. The script will install dependencies and execute the graph for both legitimate and fraudulent transactions.
4. Step-by-step logs will be printed in the terminal.
