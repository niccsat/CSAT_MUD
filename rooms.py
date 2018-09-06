rooms = {
    "Lab 1": {
        "description": "You're in a white room filled with chemistry equipment.",
        "exits": {"hallway": "Hallway 1"},
        "items": ["Blaster","StimPack"],
        "tools": ["Boiler","Towel","Workbench"],
    },
    "Hallway 1": {
        "description": "You're standing in a white hallway.",
        "exits": {"lab": "Lab 1", "staircase": "Staircase 1"},
        "items":[],
        "tools":[],
    },
    "Staircase 1": {
        "description": "You're standing in a white hallway.",
        "exits": {"hallway": "Hallway 1"},
        "items":[],
        "tools":[],
    },
}
