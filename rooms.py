rooms = {
    "Hub 1 Center": {
        "description": "You are standing on on a dirt road intersection.  There is a large town around you.  To your left, a small cart sells melons.",
        "exits": {"west": "Road 1", "east": "Road 2"},
        "items": [],
        "tools": [],
        "npcs": ["melon shop 1"],
    },
    "Road 1": {
        "description": "You're standing on a dirt road.  There is a small hab on the left side of the road and a small arms shop on the other.",
        "exits": {"east": "Hub 1 Center", "arms shop": "Arms Shop 1", "hab": "Small Hab 1"},
        "items":[],
        "tools":[],
        "npcs": [],
    },
    "Arms Shop 1": {
        "description": "You're standing in a dusty arms shop.  There are a few weapons and armor plates for sale.",
        "exits": {"out": "Road 1"},
        "items":[],
        "tools":[],
        "npcs": ["arms shop 1"],
    },
    "Road 2": {
        "description": "You're standing on a dirt road.",
        "exits": {"west": "Hub 1 Center"},
        "items":[],
        "tools":[],
        "npcs": ["jordan harrison"],
    },
}
