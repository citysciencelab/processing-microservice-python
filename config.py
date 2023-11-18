
# Model server URL
URL = "http://localhost:5555"

# Process metadata
PROCESS_METADATA = {
    'version': '0.1.0',
            'id': 'tree-planting-robots',
            'title': {'en': 'CCmCC Tree planting robot Model'},
            'description': {'en': 'This is the Mesa-geo model for the CCmCC project tree planting robots'},
            'jobControlOptions': ['sync-execute', 'async-execute'],
    'links': [{
        'type': 'text/html',
        'rel': 'about',
        'title': 'information',
        'href': 'https://example.org/process',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'aquaponics': {
            'title': 'Local Urban Food Production - Aquaponics',
            'description': 'Food is produced locally in Hamburg in containers. Minimum: 0, Maximum: 4',
            'schema': {
                'type': 'number',
                'minimum': 0,
                'maximum': 4
            },
            'minOccurs': 1,
            'maxOccurs': 1,
              
        }
    },
    'outputs': {
        'simulation_results': {
            'title': 'Simulation results',
            'description': 'The simulated model with 50 year simulation span',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'aquaponics': 0
        }
    }
}
