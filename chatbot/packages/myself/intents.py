from chatbot.packages.myself.myself import hello

INTENTS = [
    {
        "type": "fallback",
        "name": hello.__name__,
        "action": hello
    }
]
