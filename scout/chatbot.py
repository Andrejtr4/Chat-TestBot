#!/usr/bin/env python3
"""
Playwright Test Generator Chatbot
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAPI_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAPI_KEY not found")


class TestGeneratorChatbot:
    """AI chatbot that generates Playwright tests"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4",
            temperature=0.2,
        )
        
        self.system_prompt = """You are a Playwright test code generator.
Generate complete, executable Python test code based on user descriptions.
Target: https://www.enbw.com/strom/privatkunden/produkte
Output: Only the Python code, ready to use."""
    
    def generate(self, description):
        response = self.llm.invoke([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": description},
        ])
        return response.content
    
    def chat(self):
        print("\n" + "="*70)
        print("🎭 PLAYWRIGHT TEST GENERATOR")
        print("="*70)
        print("\nWebsite: https://www.enbw.com/strom/privatkunden/produkte")
        print("\nDescribe what to test → generates Playwright code")
        print("Type 'save' to save, 'quit' to exit\n")
        print("="*70 + "\n")
        
        last_code = None
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'save':
                    if not last_code:
                        print("⚠️  No code yet\n")
                        continue
                    filename = input("Filename (no .py): ").strip()
                    if filename:
                        os.makedirs("scout/tests", exist_ok=True)
                        path = f"scout/tests/test_{filename}.py"
                        with open(path, 'w') as f:
                            f.write(last_code)
                        print(f"✅ Saved: {path}\n")
                    continue
                
                print("\n🤖 Generating...\n")
                code = self.generate(user_input)
                last_code = code
                
                print("="*70)
                print("📋 Generated Code:")
                print("="*70)
                print(code)
                print("="*70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
