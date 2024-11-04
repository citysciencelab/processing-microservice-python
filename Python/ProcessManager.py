from PIL import Image
import io, logging
import base64

async def simulate_results(inputParameters):
    finalResults = {}

    try:
        # Mapping von Eingabeschlüsseln zu Ausgabeschlüsseln
        input_to_output_mapping = {
            "stringInput": "stringOutput",
            "measureInput": "measureOutput",
            "dateInput": "dateOutput",
            "doubleInput": "doubleOutput",
            "arrayInput": "arrayOutput",
            "complexObjectInput": "complexObjectOutput",
            "geometryInput": "geometryOutput",
            "boundingBoxInput": "boundingBoxOutput",
            "imagesInput": "imagesOutput",
            "featureCollectionInput": "featureCollectionOutput"
        }

        # Durchlaufen Sie die Eingaben und ändern Sie die Schlüssel
        for key, value in inputParameters.items():
            if key in input_to_output_mapping:
                new_key = input_to_output_mapping[key]
                finalResults[new_key] = value
            else:
                finalResults[key] = value  # Falls kein Mapping vorhanden ist, den ursprünglichen Schlüssel verwenden

        # Laden Sie das Bild und extrahieren Sie die binären Daten
        with Image.open('Python/geotiff_result.tif') as img:
            logging.info("Trying to load image")
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='TIFF')
            img_byte_arr = img_byte_arr.getvalue()
            img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
            finalResults['imagesOutput'] = img_base64

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    return finalResults
