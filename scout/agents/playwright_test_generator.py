#!/usr/bin/env python3
"""
LangGraph Agent: Playwright Test Generator

An interactive agent that accepts user instructions in chat and generates
Playwright test code for https://www.enbw.com/strom/privatkunden/produkte

Architecture:
- LangGraph: Manages agent state and conversation flow
- OpenAI: Generates Python code (Playwright tests) based on user instructions
- MCP: Can be exposed as a tool for ChatGPT

Usage:
    uv run python scout/agents/playwright_test_generator.py
"""

import json
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAPI_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAPI_KEY not found in .env")


# Define the agent state
class AgentState(TypedDict):
    """State structure for the test generator agent"""
    messages: Annotated[list[BaseMessage], add_messages]
    generated_test: str
    test_description: str


class PlaywrightTestGenerator:
    """
    LangGraph agent that generates Playwright tests based on user instructions.
    """
    
    def __init__(self):
        """Initialize the agent with OpenAI LLM"""
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4",
            temperature=0.2,  # Low temperature for consistent code generation
        )
        
        # System prompt for test generation
        self.system_prompt = """You are an expert Playwright test generator for the EnBW website.

Your task is to generate high-quality, executable Playwright test code based on user instructions.

Target Website: https://www.enbw.com/strom/privatkunden/produkte

Requirements:
1. Generate complete, runnable Python code using Playwright async API
2. Use descriptive variable names and comments
3. Include proper error handling and waits
4. Add assertions to verify expected behavior
5. Generate tests that can run with: uv run pytest <test_file>

Output Format:
- Wrap the complete test code in triple backticks with ```python language tag
- Include proper imports (asyncio, pytest, playwright)
- Use async/await pattern
- Make tests independent and reusable

Example structure:
```python
import asyncio
import pytest
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_your_feature():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Your test steps here
        
        await browser.close()
```

Always:
- Use explicit waits (wait_for_timeout, wait_for_selector)
- Add clear print statements for debugging
- Handle exceptions gracefully
- Make tests maintainable and easy to modify"""
    
    def process_user_instruction(self, state: AgentState) -> AgentState:
        """
        Process user instruction and generate Playwright test code.
        """
        # Get the latest user message
        messages = state["messages"]
        
        # Build messages for the LLM
        system_msg = self.system_prompt
        user_instruction = messages[-1].content if messages else ""
        
        print(f"\n📝 User Instruction: {user_instruction}")
        print("🤖 Generating Playwright test code...\n")
        
        # Call the LLM to generate test code
        response = self.llm.invoke([
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_instruction},
        ])
        
        generated_code = response.content
        
        # Update state
        state["messages"].append(AIMessage(content=generated_code))
        state["generated_test"] = generated_code
        state["test_description"] = user_instruction
        
        return state
    
    def extract_test_code(self, state: AgentState) -> AgentState:
        """Extract Python code from markdown code blocks if needed"""
        code = state["generated_test"]
        
        # Check if code is wrapped in markdown backticks
        if "```python" in code:
            # Extract code from backticks
            start = code.find("```python") + len("```python")
            end = code.find("```", start)
            if end > start:
                code = code[start:end].strip()
                state["generated_test"] = code
        elif "```" in code:
            # Generic markdown code block
            start = code.find("```") + 3
            end = code.find("```", start)
            if end > start:
                code = code[start:end].strip()
                state["generated_test"] = code
        
        return state
    
    def format_output(self, state: AgentState) -> str:
        """Format the final output for display"""
        description = state["test_description"]
        code = state["generated_test"]
        
        output = f"""
{'='*70}
✨ PLAYWRIGHT TEST GENERATED
{'='*70}

📋 User Request:
{description}

{'='*70}
🔧 Generated Test Code:
{'='*70}

{code}

{'='*70}
✅ Ready to use! Save this code to a .py file and run with:
   uv run pytest <filename> -v
   or
   uv run python <filename>
{'='*70}
"""
        return output
    
    def build_workflow(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("process_instruction", self.process_user_instruction)
        workflow.add_node("extract_code", self.extract_test_code)
        
        # Add edges
        workflow.add_edge(START, "process_instruction")
        workflow.add_edge("process_instruction", "extract_code")
        workflow.add_edge("extract_code", END)
        
        return workflow.compile()
    
    def chat(self, user_message: str) -> str:
        """
        Interactive chat interface for the agent.
        Accept user instructions and return generated test code.
        """
        # Build the workflow
        app = self.build_workflow()
        
        # Initialize state
        initial_state: AgentState = {
            "messages": [HumanMessage(content=user_message)],
            "generated_test": "",
            "test_description": "",
        }
        
        # Run the workflow
        final_state = app.invoke(initial_state)
        
        # Format and return output
        return self.format_output(final_state)


def main():
    """Main interactive loop for chatting with the agent"""
    
    print("\n" + "="*70)
    print("🎭 Playwright Test Generator Agent")
    print("="*70)
    print("Generate automated Playwright tests for:")
    print("https://www.enbw.com/strom/privatkunden/produkte")
    print("\nType 'quit' or 'exit' to stop.")
    print("="*70 + "\n")
    
    generator = PlaywrightTestGenerator()
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 Your instruction (describe what to test): ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                print("⚠️ Please provide an instruction.")
                continue
            
            # Generate test
            output = generator.chat(user_input)
            print(output)
            
            # Option to save
            save = input("\n💾 Save this test? (y/n): ").strip().lower()
            if save == 'y':
                filename = input("   Filename (without .py): ").strip()
                if filename:
                    filepath = f"scout/tests/test_{filename}.py"
                    with open(filepath, 'w') as f:
                        # Extract just the code part
                        code = output.split("Generated Test Code:")[1].split("Ready to use!")[0].strip()
                        f.write(code)
                    print(f"✅ Saved to: {filepath}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
