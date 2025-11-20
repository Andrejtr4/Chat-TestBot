#!/usr/bin/env python3
"""
Entry point for Playwright Test Generator Chatbot

Usage:
    uv run python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from scout.chatbot import TestGeneratorChatbot


def main():
    """Run the chatbot"""
    try:
        chatbot = TestGeneratorChatbot()
        chatbot.chat()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
