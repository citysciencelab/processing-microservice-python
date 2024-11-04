PYTHON_PROCESS_METADATA = {
    "id": "EchoProcess",
    "title": "Echo Process",
    "description": "This process accepts and number of input and simple echoes each input as an output.",
    "version": "1.0.0",
    "jobControlOptions": ["async-execute", "sync-execute"],
    "outputTransmission": ["value", "reference"],
    "inputs": {
        "stringInput": {
            "title": "String Literal Input Example",
            "description": "This is an example of a STRING literal input.",
            "schema": {"type": "string", "enum": ["Value1", "Value2", "Value3"]},
        },
        "measureInput": {
            "title": "Numerical Value with UOM Example",
            "description": "This is an example of a NUMERIC literal with an associated unit of measure.",
            "schema": {
                "type": "object",
                "required": ["value", "uom"],
                "properties": {
                    "measurement": {"type": "number"},
                    "uom": {"type": "string"},
                    "reference": {"type": "string", "format": "uri"},
                },
            },
        },
        "dateInput": {
            "title": "Date Literal Input Example",
            "description": "This is an example of a DATE literal input.",
            "schema": {"type": "string", "format": "dateTime"},
        },
        "doubleInput": {
            "title": "Bounded Double Literal Input Example",
            "description": "This is an example of a DOUBLE literal input that is bounded between a value greater than 0 and 10.  The default value is 5.",
            "schema": {
                "type": "number",
                "format": "double",
                "minimum": 0,
                "maximum": 10,
                "default": 5,
                "exclusiveMinimum": True,
            },
        },
        "arrayInput": {
            "title": "Array Input Example",
            "description": "This is an example of a single process input that is an array of values.  In this case, the input array would be interpreted as a single value and not as individual inputs.",
            "schema": {
                "type": "array",
                "minItems": 2,
                "maxItems": 10,
                "items": {"type": "integer"},
            },
        },
        "complexObjectInput": {
            "title": "Complex Object Input Example",
            "description": "This is an example of a complex object input.",
            "schema": {
                "type": "object",
                "required": ["property1", "property5"],
                "properties": {
                    "property1": {"type": "string"},
                    "property2": {"type": "string", "format": "uri"},
                    "property3": {"type": "number"},
                    "property4": {"type": "string", "format": "dateTime"},
                    "property5": {"type": "boolean"},
                },
            },
        },
        "geometryInput": {
            "title": "Geometry input",
            "description": "This is an example of a geometry input.  In this case the geometry can be expressed as a GML of GeoJSON geometry.",
            "minOccurs": 2,
            "maxOccurs": 5,
            "schema": {
                "oneOf": [
                    {
                        "type": "string",
                        "contentMediaType": "application/gml+xml; version=3.2",
                        "contentSchema": "http://schemas.opengis.net/gml/3.2.1/geometryBasic2d.xsd",
                    },
                    {
                        "allOf": [
                            {"format": "geojson-geometry"},
                            {
                                "$ref": "http://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/geometryGeoJSON.yaml"
                            },
                        ]
                    },
                ]
            },
        },
        "boundingBoxInput": {
            "title": "Bounding Box Input Example",
            "description": "This is an example of a BBOX literal input.",
            "schema": {
                "allOf": [
                    {"format": "ogc-bbox"},
                    {"$ref": "../../openapi/schemas/bbox.yaml"},
                ]
            },
        },
        "imagesInput": {
            "title": "Inline Images Value Input",
            "description": "This is an example of an image input.  In this case, the input is an array of up to 150 images that might, for example, be a set of tiles.  The oneOf[] conditional is used to indicate the acceptable image content types; GeoTIFF and JPEG 2000 in this case.  Each input image in the input array can be included inline in the execute request as a base64-encoded string or referenced using the link.yaml schema.  The use of a base64-encoded string is implied by the specification and does not need to be specified in the definition of the input.",
            "minOccurs": 1,
            "maxOccurs": 150,
            "schema": {
                "oneOf": [
                    {
                        "type": "string",
                        "contentEncoding": "binary",
                        "contentMediaType": "application/tiff; application=geotiff",
                    },
                    {
                        "type": "string",
                        "contentEncoding": "binary",
                        "contentMediaType": "application/jp2",
                    },
                ]
            },
        },
        "featureCollectionInput": {
            "title": "Feature Collection Input Example.",
            "description": "This is an example of an input that is a feature collection that can be encoded in one of three ways: as a GeoJSON feature collection, as a GML feature collection retrieved from a WFS or as a KML document.",
            "schema": {
                "oneOf": [
                    {
                        "type": "string",
                        "contentMediaType": "application/gml+xml; version=3.2",
                    },
                    {
                        "type": "string",
                        "contentSchema": "https://schemas.opengis.net/kml/2.3/ogckml23.xsd",
                        "contentMediaType": "application/vnd.google-earth.kml+xml",
                    },
                    {
                        "allOf": [
                            {"format": "geojson-feature-collection"},
                            {
                                "$ref": "https://geojson.org/schema/FeatureCollection.json"
                            },
                        ]
                    },
                ]
            },
        },
    },
    "outputs": {
        "stringOutput": {
            "title": "String Literal Output Example",
            "description": "This is an example of a STRING literal output.",
            "schema": {"type": "string", "enum": ["Value1", "Value2", "Value3"]},
        },
        "measureOutput": {
            "title": "Numerical Value with UOM Output Example",
            "description": "This is an example of a NUMERIC literal with an associated unit of measure output.",
            "schema": {
                "type": "object",
                "required": ["value", "uom"],
                "properties": {
                    "measurement": {"type": "number"},
                    "uom": {"type": "string"},
                    "reference": {"type": "string", "format": "uri"},
                },
            },
        },
        "dateOutput": {
            "title": "Date Literal Output Example",
            "description": "This is an example of a DATE literal output.",
            "schema": {"type": "string", "format": "dateTime"},
        },
        "doubleOutput": {
            "title": "Bounded Double Literal Output Example",
            "description": "This is an example of a DOUBLE literal output that is bounded between a value greater than 0 and 10.  The default value is 5.",
            "schema": {
                "type": "number",
                "format": "double",
                "minimum": 0,
                "maximum": 10,
                "default": 5,
                "exclusiveMinimum": True,
            },
        },
        "arrayOutput": {
            "title": "Array Output Example",
            "description": "This is an example of a single process output that is an array of values.  In this case, the output array would be interpreted as a single value and not as individual outputs.",
            "schema": {
                "type": "array",
                "minItems": 2,
                "maxItems": 10,
                "items": {"type": "integer"},
            },
        },
        "complexObjectOutput": {
            "title": "Complex Object Output Example",
            "description": "This is an example of a complex object output.",
            "schema": {
                "type": "object",
                "required": ["property1", "property5"],
                "properties": {
                    "property1": {"type": "string"},
                    "property2": {"type": "string", "format": "uri"},
                    "property3": {"type": "number"},
                    "property4": {"type": "string", "format": "dateTime"},
                    "property5": {"type": "boolean"},
                },
            },
        },
        "geometryOutput": {
            "title": "Geometry Output Example",
            "description": "This is an example of a geometry output.  In this case the geometry can be expressed as a GML of GeoJSON geometry.",
            "schema": {
                "oneOf": [
                    {
                        "type": "string",
                        "contentMediaType": "application/gml+xml",
                        "contentSchema": "http://schemas.opengis.net/gml/3.2.1/geometryBasic2d.xsd",
                    },
                    {
                        "allOf": [
                            {"format": "geojson-geometry"},
                            {
                                "$ref": "http://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/geometryGeoJSON.yaml"
                            },
                        ]
                    },
                ]
            },
        },
        "boundingBoxOutput": {
            "title": "Bounding Box Output Example",
            "description": "This is an example of a BBOX literal output.",
            "schema": {
                "allOf": [
                    {"format": "ogc-bbox"},
                    {"$ref": "../../openapi/schemas/bbox.yaml"},
                ]
            },
        },
        "imagesOutput": {
            "title": "Inline Images Value Output",
            "description": "This is an example of an image output. ",
            "schema": {
                "oneOf": [
                    {
                        "type": "string",
                        "contentEncoding": "binary",
                        "contentMediaType": "application/tiff; application=geotiff",
                    },
                    {
                        "type": "string",
                        "contentEncoding": "binary",
                        "contentMediaType": "application/jp2",
                    },
                ]
            },
        },
        "featureCollectionOutput": {
            "title": "Feature Collection Output Example.",
            "description": "This is an example of an output that is a feature collection that can be encoded in one of three ways: as a GeoJSON feature collection, as a GML feature collection retrieved from a WFS or as a KML document.",
            "schema": {
                "oneOf": [
                    {
                        "type": "string",
                        "contentMediaType": "application/gml+xml; version=3.2",
                    },
                    {
                        "type": "string",
                        "contentMediaType": "application/vnd.google-earth.kml+xml",
                        "contentSchema": "https://schemas.opengis.net/kml/2.3/ogckml23.xsd",
                    },
                    {
                        "allOf": [
                            {"format": "geojson-feature-collection"},
                            {
                                "$ref": "https://geojson.org/schema/FeatureCollection.json"
                            },
                        ]
                    },
                ]
            },
        },
    },
    "links": [
        {
            "href": "https://processing.example.org/oapi-p/processes/EchoProcess/execution",
            "rel": "http://www.opengis.net/def/rel/ogc/1.0/execute",
            "title": "Execute endpoint",
        }
    ],
    "example": {
        "inputs": {
            "stringInput": "Value1",
            "measureInput": {
                "measurement": 42.5,
                "uom": "meters",
                "reference": "http://example.org/measurement/42.5m",
            },
            "dateInput": "2023-08-24T14:30:00Z",
            "doubleInput": 7.5,
            "arrayInput": [5, 10, 15, 20],
            "complexObjectInput": {
                "property1": "Example string",
                "property2": "http://example.org/property",
                "property3": 100.5,
                "property4": "2023-08-24T14:30:00Z",
                "property5": true,
            },
            "geometryInput": [
                '{"type": "Point", "coordinates": [125.6, 10.1]}',
                '{"type": "LineString", "coordinates": [[125.6, 10.1], [125.7, 10.2]]}',
            ],
            "boundingBoxInput": {
                "type": "BoundingBox",
                "coordinates": [[102.0, 0.5], [105.0, 2.5]],
            },
            "imagesInput": [
                "iVBORw0KGgoAAAANSUhEUgAAA... (base64 TIFF)",
                "iVBORw0KGgoAAAANSUhEUgAAA... (base64 JP2)",
            ],
            "featureCollectionInput": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "coordinates": [
                                [
                                    [10.011650146831101, 53.556099741077134],
                                    [9.992305015802998, 53.556099741077134],
                                    [9.992305015802998, 53.542743797392035],
                                    [10.011650146831101, 53.542743797392035],
                                    [10.011650146831101, 53.556099741077134],
                                ]
                            ],
                            "type": "Polygon",
                        },
                    },
                    {
                        "type": "Feature",
                        "properties": {"wert": "wert"},
                        "geometry": {
                            "coordinates": [9.965428230070017, 53.56069349854644],
                            "type": "Point",
                        },
                        "id": 1,
                    },
                    {
                        "type": "Feature",
                        "properties": {"ewrt": "wert"},
                        "geometry": {
                            "coordinates": [9.9869732265619, 53.57479583674177],
                            "type": "Point",
                        },
                        "id": 2,
                    },
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "coordinates": [
                                [
                                    [10.013130968861645, 53.535180984134456],
                                    [9.99414712198552, 53.53562439587452],
                                    [9.982349821404284, 53.53802996562243],
                                    [9.97277604332578, 53.54351148862142],
                                    [9.953246543158428, 53.54394945580404],
                                    [9.94917669839407, 53.540112238518105],
                                    [9.954335707492191, 53.53474457257863],
                                    [9.954885189973055, 53.52838859284705],
                                    [9.958203887073836, 53.52499261284734],
                                    [9.965024643303707, 53.524007385008304],
                                    [9.996726260232037, 53.52159511658971],
                                    [10.011470696946589, 53.51973611960065],
                                    [10.018288891514231, 53.52828360895637],
                                    [10.019765190443167, 53.53518247418231],
                                    [10.013130968861645, 53.535180984134456],
                                ]
                            ],
                            "type": "Polygon",
                        },
                    },
                ],
            },
        }
    },
}
