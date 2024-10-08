NETLOGO_VARIABLES = {
    "simulation-time": "Simulationszeit",
    "initial-modernized-building-rate": "Anteil-Modernisierte-Wohnungen-zu-Beginn",
    "duration-planning-and-approval": "Dauer-Planung-und-Genehmigung-der-Modernisierung",
    "availability-of-construction-work": "Verfügbarkeit-Handwerks-und-Bauleistungen",
    "availability-of-funding": "Verfügbare-Fördermittel",
    "decision-to-move-after-modernization-notification": "Umzugsentscheidung-bei-Modernisierungsankündigung",
    "average-cost-of-modernization": "Durchschnittliche-Kosten-für-energetische-Modernisierung",
    "maximum-rent-increase": "Maximale-Modernisierungsmieterhöhung",
}

NETLOGO_REPORTERS = {
    "Modernisierungen nicht begonnen": 'count eigentumsverhältnisse with [modernisierungs-status = "nicht begonnen"]',
    "Modernisierungen in Finanzierung": 'count eigentumsverhältnisse with [modernisierungs-status = "in Finanzierung"]',
    "Modernisierungen in Planung": 'count eigentumsverhältnisse with [modernisierungs-status = "in Planung"]',
    "Modernisierungen in Bau": 'count eigentumsverhältnisse with [modernisierungs-status = "in Bau"]',
    "Modernisierungen erledigt": 'count eigentumsverhältnisse with [modernisierungs-status = "erledigt"]',
    "Durchschnittliche Mietkosten": "mean [mietkosten] of wohnverhältnisse",
    "Anzahl Anwohnende": "count (anwohnerschaft with [not weggezogen?])",
}

NETLOGO_PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "rothenburgsort_abm",
    "title": {
        "en": "Agent-based model of RE3",
        "de": "Agentenbasiertes Modell von RE3",
    },
    "description": {
        "en": "This is an agent-based model of the Rothenburgsort district in Hamburg, Germany. It is based on a real-world experiment in the CUT-project.",
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
            "description": "Simulationszeit in Jahren",
            "schema": {"type": "number", "minimum": 0, "maximum": 20},
            "minOccurs": 0,
            "maxOccurs": 1,
        },
        "initial-modernized-building-rate": {
            "title": "Anteil modernisierter Wohnungen zu Beginn",
            "description": "Anzahl der modernisierten Gebäude zu Beginn der Simulation",
            "schema": {"type": "number", "minimum": 0, "maximum": 100},
            "minOccurs": 0,
            "maxOccurs": 1,
        },
        "duration-planning-and-approval": {
            "title": "Dauer Planung und Genehmigung",
            "description": "Dauer der Planung und Genehmigung der Modernisierung in Monaten",
            "schema": {"type": "number", "minimum": 0, "maximum": 36},
            "minOccurs": 0,
            "maxOccurs": 1,
        },
        "availability-of-construction-work": {
            "title": "Verfügbarkeit von Handwerks- und Bauleistungen",
            "description": "Verfügbarkeit von Bauarbeiten in Gebäuden pro Monat",
            "schema": {"type": "number", "minimum": 0, "maximum": 25},
            "minOccurs": 0,
            "maxOccurs": 1,
        },
        "availability-of-funding": {
            "title": "Verfügbarkeit von Fördermitteln",
            "description": "Verfügbarkeit von Fördermitteln",
            "schema": {
                "type": "string",
            },
            "minOccurs": 0,
            "maxOccurs": 1,
        },
        "decision-to-move-after-modernization-notification": {
            "title": "Umzugsentscheidung bei Modernisierungsankündigung",
            "description": "Umzugsentscheidung bei Modernisierungsankündigung in Prozent",
            "schema": {"type": "number", "minimum": 0, "maximum": 100},
            "minOccurs": 0,
            "maxOccurs": 1,
        },
        "average-cost-of-modernization": {
            "title": "Durchschnittliche Kosten energetischen Modernisierung",
            "description": "Durchschnittliche Kosten der Modernisierung in Euro",
            "schema": {"type": "number", "minimum": 0, "maximum": 50000},
            "minOccurs": 0,
            "maxOccurs": 1,
        },
        "maximum-rent-increase": {
            "title": "Maximale Modernisierungsmieterhöhung",
            "description": "Maximale Modernisierungsmieterhöhung in Prozent",
            "schema": {"type": "number", "minimum": 0, "maximum": 100},
            "minOccurs": 0,
            "maxOccurs": 1,
        },
    },
    "outputs": {
        "title": "Result data of the simulation",
        "type": "object",
        "required": ["results"],
        "properties": {
            "results": {
                "type": "object",
                "required": ["simulation_results", "simulation_geometry"],
                "properties": {
                    "simulation_results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "Zeitschritt": {"type": "number"},
                                "Modernisierungen nicht begonnen": {"type": "number"},
                                "Modernisierungen in Finanzierung": {"type": "number"},
                                "Modernisierungen in Planung": {"type": "number"},
                                "Modernisierungen in Bau": {"type": "number"},
                                "Modernisierungen erledigt": {"type": "number"},
                                "Durchschnittliche Mietkosten": {"type": "number"},
                                "Anzahl Anwohnende": {"type": "number"},
                            },
                            "required": [
                                "Zeitschritt",
                                "Modernisierungen nicht begonnen",
                                "Modernisierungen in Finanzierung",
                                "Modernisierungen in Planung",
                                "Modernisierungen in Bau",
                                "Modernisierungen erledigt",
                                "Durchschnittliche Mietkosten",
                                "Anzahl Anwohnende",
                            ],
                        },
                    },
                    "simulation_geometry": {
                        "schema": {
                            "allOf": [
                                {"format": "geojson-feature-collection"},
                                {
                                    "$ref": "https://geojson.org/schema/FeatureCollection.json"
                                },
                            ]
                        },
                    },
                },
            },
        },
    },
    "example": {
        "inputs": {
            "simulation-time": 10,
            "initial-modernized-building-rate": 10,
            "duration-planning-and-approval": 6,
            "availability-of-construction-work": 10,
            "availability-of-funding": "mittel",
            "decision-to-move-after-modernization-notification": 10,
            "average-cost-of-modernization": 20000,
            "maximum-rent-increase": 8,
        }
    },
}
