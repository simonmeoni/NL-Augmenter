import itertools
import random

import torch

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformers import AutoModel, AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class TestTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.QUESTION_ANSWERING,
        TaskType.SENTIMENT_ANALYSIS,
        TaskType.TEXT_TAGGING
    ]
    languages = ["en"]

    def __init__(self, ner_model='dslim/bert-base-NER',
                 ner_tokenizer='dslim/bert-base-NER', masking_model='distilroberta-base'):
        self.masking_model = AutoModel.from_pretrained(masking_model).eval()
        self.masking_tokenizer = AutoTokenizer.from_pretrained(masking_model, use_fast=True)
        self.ner = pipeline("ner", model= AutoModelForTokenClassification.from_pretrained(ner_model),
                                  tokenizer=AutoTokenizer.from_pretrained(ner_tokenizer, use_fast=True))

    # [{'word': 'John', 'score': 0.9990864396095276, 'entity': 'B-PER', 'index': 1, 'start': 0, 'end': 4}, {'word': '##ath', 'score': 0.9761947393417358, 'entity': 'I-PER', 'index': 2, 'start': 4, 'end': 7}, {'word': '##an', 'score': 0.8689031004905701, 'entity': 'B-PER', 'index': 3, 'start': 7, 'end': 9}, {'word': 'Jean', 'score': 0.9995222091674805, 'entity': 'B-PER', 'index': 7, 'start': 25, 'end': 29}, {'word': '-', 'score': 0.7230081558227539, 'entity': 'I-PER', 'index': 8, 'start': 29, 'end': 30}, {'word': 'Pascal', 'score': 0.9278112649917603, 'entity': 'I-PER', 'index': 9, 'start': 30, 'end': 36}, {'word': 'Paris', 'score': 0.9995789527893066, 'entity': 'B-LOC', 'index': 14, 'start': 53, 'end': 58}]
    # ######## eats pizza and John eats pickles in Paris
    def generate(self, sentence: str):
        with torch.no_grad():
            ner_entities = [entity for entity in self.ner(sentence) if entity == 'B-PER'
                            and entity == 'I-PER']

            for entity in ner_entities:
                if entity['entity'] == 'B-PER':
                    start = entity['start']
                    end = entity['end']
                    entity_mem = entity['entity']

                elif entity['entity'] == 'I-PER':
                    end = entity['end']
                    entity_mem = entity['entity']
        return [sentence.upper()]
