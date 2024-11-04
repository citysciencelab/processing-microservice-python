MESA_PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "geo_test_model",
    "title": {
        "en": "Model for testing various inputs and outputs"
    },
    "description": {
        "en": "This model is used to test various inputs and outputs"
    },
    "jobControlOptions": ["async-execute"],
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
