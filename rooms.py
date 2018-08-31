rooms = {
    "Tavern": {
        "description": "You're in a cozy tavern warmed by an open fire.",
        "exits": {"outside": "Outside"},
        "items": ["Blaster","StimPack"],
        "tools": ["Sink","Towel"],
    },
    "Outside": {
        "description": "You're standing outside a tavern. It's raining.",
        "exits": {"inside": "Tavern"},
        "items":[],
        "tools":[],
    }
}
