import pandas
import requests
import argparse


VOCAB_QUERY = """PREFIX debias-o: <http://data.europa.eu/c4p/ontology#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX debias: <http://data.europa.eu/c4p/data/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>


SELECT DISTINCT ?uri ?term ?context ?suggestion ?disambiguation WHERE {{
    ?uri debias-o:hasContentiousIssue ?issue_uri .
    ?uri skosxl:literalForm ?term .
    ?issue_uri dct:description ?context .
    ?uri debias-o:isAmbiguous ?disambiguation .
    OPTIONAL {{
        ?uri debias-o:hasSuggestionNote ?suggestion_uri .
        ?suggestion_uri rdf:value ?suggestion .
        FILTER(langMatches(lang(?suggestion), "{LANG}")) .
    }}
    FILTER(langMatches(lang(?term), "{LANG}")) .
    FILTER NOT EXISTS {{ ?uri owl:deprecated "true"^^xsd:boolean }} .
    FILTER NOT EXISTS {{ ?uri debias-o:excludedFromDetection "true"^^xsd:boolean }} .
}}"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--savepath',
        type=str
    )
    parser.add_argument(
        '--language',
        type=str,
        choices=['en', 'de', 'fr', 'it', 'nl']
    )
    args = parser.parse_args()

    query = VOCAB_QUERY.format(LANG=args.language)

    base_url = 'https://publications.europa.eu/webapi/rdf/sparql'
    params = {
        'default-graph-uri': 'http://data.europa.eu/c4p/data',
        'run': 'Run Query',
        'debug': 'on',
        'format': 'application/json',
        'query': ' '.join(query.split('\n'))
    }
    payload = {}
    headers = {
        'User-Agent': 'PostmanRuntime/7.43.0'
    }

    response = requests.request('GET', base_url, params=params, headers=headers, data=payload)
    response = response.json()
    data = [{k: v['value'] for k, v in record.items()}
            for record in response['results']['bindings']]
    df = pandas.DataFrame.from_records(data)
    df.to_csv(args.savepath, index=False, quoting=1)


if __name__ == '__main__':
    main()
