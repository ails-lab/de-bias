# The DE-BIAS Tool
The DE-BIAS Tool detects outdated and potentially harmful language in descriptions of cultural heritage collections. It was developed by the DE-BIAS project.
## About the tool
The DE-BIAS tool was developed by the [DE-BIAS project](https://pro.europeana.eu/project/de-bias) which aimed to promote a more inclusive and respectful approach to describing digital collections. It builds on the [DE-BIAS vocabulary](https://pro.europeana.eu/page/the-de-bias-vocabulary) and utilises a series of Natural Language Processing (NLP) methods to detect and contextualise outdated or potentially harmful terms in object descriptions from cultural heritage institutions.

Through the tool, you can create statistics of biassed terms found in the collections you work with as a basis for next steps, annotate those terms with contextual information and, where appropriate, suggestions for alternative wording.
## Benefits of the tool
The DE-BIAS tool allows users to:
* Quickly check individual object descriptions where they suspect bias
* Collectively analyse smaller batches of object descriptions for contentious terms
* Repeatedly run large-scale bias detection on object descriptions in their own systems or in the context of preparing data for submission to Europeana.eu
* Get statistics and a general overview of detected bias to start discussing and deciding on next steps to address harmful language in their object descriptions
* Create annotations for detected bias terms linking to the DE-BIAS vocabulary for further contextualisation

It should be noted that, while some of these functions are available independent of the application context of the tool, some are only available either in the standalone version or in the API endpoint (see more below under ‘Technical information’). Furthermore, making the most of the tool in one’s own context will require some software development capacity and skills.
## Technical information
The tool is available as a [standalone application](https://debias-tool.ails.ece.ntua.gr/) accessible via a web interface and as an [API endpoint](https://debias-api.ails.ece.ntua.gr/) allowing users to connect to the tool in the context of their own workflows and systems. The API endpoint has also been integrated into the [Metis Sandbox](https://github.com/europeana/metis-sandbox) and can as such be used when preparing data for submission to [Europeana.eu](https://www.europeana.eu/en).

When using the standalone tool, data to be analysed can either be provided as a copy/paste into free text fields or in the form of .txt files, which will need to be uploaded in .zip format. When using the API endpoint integrated into the Metis Sandbox, data can be submitted in any of the formats that the Sandbox currently supports; the bias detection will become available once the data has been processed as usual and will then be applied to the EDM records in the Sandbox.

Building on the DE-BIAS vocabulary, which names and contextualises close to 700 outdated and harmful terms across five languages (Dutch, English, French, German and Italian), the tool applies a series of NLP methods to detect whether these terms can be found in the data to be analysed:
* **Tokenization**, splitting the plain input text into words, phrases or other meaningful elements for analysis, including the splitting of compound words in Dutch and in German;
* **Lemmatization**, identifying the lemma of a word to match a word from the vocabulary to a word in the analysed text, including different inflections;
* **Named Entity Recognition (NER)**, analysing a word’s context and positioning within the text to determine whether a term qualifies as a proper noun (e.g. a person's name or a place name), which may then be excluded from the tagging process;
* **Large Language Models (LLM)**, determining whether a term that can be contentious in one context, but appropriate in another is to be flagged.
## How to use it
An introduction to the development of the tool, its main functionalities, and the workflow of the standalone version and of the tool’s integration in the Metis Sandbox are included in these [slides](https://pro.europeana.eu/files/Europeana_Professional/Projects/DE-BIAS_tool_presentation_slides.pdf). Alternatively, rewatch the [recording from the Europeana Aggregators’ Forum’s Autumn Meeting 2024](https://www.youtube.com/watch?v=UNq8m2ORGfM), which includes a live demonstration.

More details can be found in the [full manual of the tool](https://pro.europeana.eu/files/Europeana_Professional/Projects/debias/DE-BIAS_tool_technical_documentation.pdf), which also covers information about the direct use of the API endpoint.

For comments and further information about the DE-BIAS tool, please contact project.debias@gmail.com.
