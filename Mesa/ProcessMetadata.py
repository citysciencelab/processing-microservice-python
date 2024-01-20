MESA_PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "robot_model",
    "title": {
        "en": "Agent-based model of RE3",
        "de": "Agentenbasiertes Modell von RE3",
    },
    "description": {
        "en": "This is an tree planting robot model from the CCmCC project.",
        "de": "Dies ist ein agentenbasiertes Modell des Stadtteils Rothenburgsort in Hamburg, Deutschland. Es basiert auf einem Realexperiment im CUT-Projekt.",
    },
    "jobControlOptions": ["sync-execute", "async-execute"],
    "links": [
        {
            "type": "text/html",
            "rel": "about",
            "title": "information",
            "href": "https://example.org/process",
            "hreflang": "en-US",
        }
    ],
    "inputs": {
        "simulation-time": {
            "title": "Simulationszeit",
            "description": "Simulationszeit in time steps",
            "schema": {"type": "number", "minimum": 0, "maximum": 50},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "number-of-robots": {
            "title": "Anzahl der Roboter",
            "description": "Anzahl der Roboter zu Beginn der Simulation",
            "schema": {"type": "number", "minimum": 0, "maximum": 100},
            "minOccurs": 1,
            "maxOccurs": 1,
        }
    },
    "outputs": {
        "simulation_results": {
            "title": "Simulation results",
            "description": "The simulated model results",
            "schema": {"type": "object", "contentMediaType": "application/json"},
        }
    },
    "example": {
        "inputs": {
            "simulation-time": 10,
            "number-of-robots": 10
        }
    },
}
