import transformers
from transformers import pipeline
import torch

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary_bart(text):
  output = summarizer(text, max_length=100, min_length=75, do_sample=False)
  summary = output[0]['summary_text']
  return summary