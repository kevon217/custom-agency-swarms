## gpt-powered fashion advice bot

Currently leading the development of an AI-driven backend chat application for a fashion website, utilizing a team of custom-configured OpenAI GPT assistants to offer personalized fashion advice and product
recommendations, with integration of FastAPI for efficient API management and WebSocket for real-time user interactions.

## studysearch-app

studysearch_app is a search interface for the Federal Interagency for Traumatic Brain Injury Research (FITBIR) Data Repository, which is an instance of the National Institutes of Health's (NIH) Biomedical Research Informatics and Computing System (BRICS) platform. It is designed to facilitate natural language querying of metadata associated with traumatic brain injury (TBI) studies stored in the FITBIR Data Repository. Leveraging the capabilities of Retrieval-Augmented Generation (RAG) supported by the LlamaIndex data framework, studysearch_app provides efficient semantic search and LLM-based generative capabilities, enabling researchers to quickly find relevant studies in the FITBIR Data Repository.

## data-dictionary-cui-mapping

This package assists with mapping a user's data dictionary fields to UMLS concepts. It is designed to be modular and flexible to allow for different configurations and use cases.

Roughly, the high-level steps are as follows:

Configure yaml files
Load in data dictionary
Preprocess desired columns
Query for UMLS concepts using any or all of the following pipeline modules:
umls (UMLS API)
metamap (MetaMap API)
semantic_search (relies on access to a custom Pinecone vector database)
hydra_search (combines any combination of the above three modules)
Manually curate/select concepts in excel
Create data dictionary file with new UMLS concept fields

## study-closeout-analysis

Data submitted to the FITBIR data repository must undergo a study closeout analysis before they are shared with the FITBIR community. The closeout analysis script checks for the following:

Demographic data have been submitted for all participants.
Duplicate entries.
Partial data (i.e., a subset of participants are missing values for a given data point).
Extra-validation scoring algorithms errors.
Correspondence between GUIDs and reported subject IDs (if submitted) throughout all submissions.
Overall, these checks ensure that data for each participant are consistent, properly reported, and as complete as possible. These detailed findings are reported to the study team and will be corrected by the study team if necessary before sharing the data.

## fhir-to-brics

fhir_to_json is a preliminary Python package designed for extracting and transforming HL7 FHIR resource element schemas into Biomedical Resource Informatics Computing System (BRICS) data elements.

## brics-crossmap

The brics_crossmap tool is a Python-based utility for semantically mapping individual metadata fields of a user's variables to corresponding metadata fields in BRICS data elements. It uses language model embeddings to encode the semantics of each individually specified metadata field and facilitates the one-to-one field mapping process through a vector database search and reranking pipeline. The tool includes features for setting up an initial index with the embedded data elements and provides functionality to update this index as new data becomes available or existing data is modified.
