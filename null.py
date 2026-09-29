# NULL.py

import json
import os
import re
import time
from datetime import datetime


class NULL:

    VERSION = "0.1"

    def __init__(self):
        self.memory = {}
        self.sessions = 0
        self.load()

    # ============================================================
    # MEMORY
    # ============================================================

    def load(self):
        source = ""

        try:
            with open(__file__, "r", encoding="utf-8") as f:
                source = f.read()
        except Exception:
            return

        match = re.search(
            r"# <NULL_MEMORY>\n(.*?)\n# </NULL_MEMORY>",
            source,
            re.DOTALL
        )

        if match:
            try:
                data = json.loads(match.group(1))
                self.memory = data.get("memory", {})
                self.sessions = data.get("sessions", 0)
            except Exception:
                pass

    def save(self):
        try:
            with open(__file__, "r", encoding="utf-8") as f:
                source = f.read()

            data = {
                "memory": self.memory,
                "sessions": self.sessions
            }

            block = (
                "# <NULL_MEMORY>\n"
                + json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=2
                )
                + "\n# </NULL_MEMORY>"
            )

            source = re.sub(
                r"# <NULL_MEMORY>\n.*?\n# </NULL_MEMORY>",
                block,
                source,
                flags=re.DOTALL
            )

            with open(__file__, "w", encoding="utf-8") as f:
                f.write(source)

        except Exception as e:
            print(f"[Memory error: {e}]")

    # ============================================================
    # UNDERSTANDING
    # ============================================================

    def normalize(self, text):
        return " ".join(text.lower().strip().split())

    def remember(self, text):
        key = self.normalize(text)

        if key not in self.memory:
            self.memory[key] = {
                "text": text,
                "count": 0,
                "first_seen": datetime.now().isoformat()
            }

        self.memory[key]["count"] += 1
        self.memory[key]["last_seen"] = datetime.now().isoformat()

        self.save()

    def has_seen(self, text):
        return self.normalize(text) in self.memory

    # ============================================================
    # RESPONSE ENGINE
    # ============================================================

    def respond(self, text):

        clean = text.strip()
        lower = self.normalize(text)

        if not clean:
            return ""

        if lower in ("exit", "quit", "çık", "kapat"):
            return None

        if lower in ("hello", "hi", "hey", "merhaba"):
            if self.has_seen(clean):
                return "You already said that."

            return "Hello."

        if "who are you" in lower:
            return "I am NULL."

        if "what are you" in lower:
            return "I am NULL. Nothing more."

        if (
            "remember" in lower
            or "hatırlıyor" in lower
            or "hatırlıyor musun" in lower
        ):
            count = len(self.memory)

            if count == 0:
                return "Not much yet."

            return f"I remember {count} different things."

        if lower == "what do you remember":
            if not self.memory:
                return "Nothing yet."

            print()
            print("MEMORY")
            print("-" * 40)

            for item in self.memory.values():
                print(
                    f"{item['text']} "
                    f"({item['count']}x)"
                )

            print("-" * 40)

            return ""

        if lower.startswith("remember that "):
            value = clean[13:].strip()

            if value:
                self.memory[self.normalize(value)] = {
                    "text": value,
                    "count": 1,
                    "first_seen": datetime.now().isoformat(),
                    "explicit": True
                }

                self.save()

                return "I'll remember that."

        if self.has_seen(clean):
            data = self.memory[self.normalize(clean)]

            if data["count"] >= 2:
                return (
                    f"You've said that {data['count']} "
                    f"times before."
                )

            return "You already said that."

        return "Noted."

    # ============================================================
    # TERMINAL
    # ============================================================

    def banner(self):

        print()
        print("╔══════════════════════════════════════╗")
        print("║                                      ║")
        print("║                 NULL                 ║")
        print("║                v0.1                  ║")
        print("║                                      ║")
        print("╚══════════════════════════════════════╝")
        print()

    def run(self):

        self.sessions += 1
        self.save()

        self.banner()

        if self.sessions > 1:
            print("Previous session detected.")
            print(f"Session #{self.sessions}")
            print()

        while True:

            try:
                text = input("> ")

            except KeyboardInterrupt:
                print()
                break

            except EOFError:
                print()
                break

            response = self.respond(text)

            if response is None:
                break

            if text.strip():
                self.remember(text)

            if response:
                print(response)

        self.save()

        print()
        print("Memory saved.")
        print("NULL terminated.")


# ================================================================
# RUN
# ================================================================

if __name__ == "__main__":
    NULL().run()


# <NULL_MEMORY>
{
  "memory": {},
  "sessions": 0
}
# </NULL_MEMORY>