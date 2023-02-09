import requests
from bs4 import BeautifulSoup
import os
from datetime import date
import nltk
from newspaper import Article

from twilio.rest import Client
import openai

import transformers
from transformers import pipeline
import torch

import pyshorteners

import smtplib
import ssl
from email.message import EmailMessage

import slack

nltk.download('punkt')

# URL shortener
def shorten_url(url):
  s = pyshorteners.Shortener()
  return s.tinyurl.short(url)

# Set up the OpenAI API client

openai.api_key = "YOUR_OPENAI_KEY" # os.environ(YOUR_KEY_NAME)

def call_gpt_api(prompt):

  model_engine = "text-davinci-003"

  # Generate a response
  completion = openai.Completion.create(
      engine=model_engine,
      prompt=prompt,
      max_tokens=110,
      n=1,
      stop=None,
      temperature=0.7,
  )

  response = completion.choices[0].text
  return response
  
def generate_snipp(topic):
    
    # construct the URL for the Google News search
    url = f"https://news.google.com/search?q={topic}&hl=en-US&gl=US&ceid=US:en"

    # send a request to the website and parse the HTML
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Get article links
    top_x_articles_threshold = 10
    article_links = [art['href'] for art in soup.find_all("a", class_="DY5T1d")[:top_x_articles_threshold]]
  
    # Find articles that are inaccessible (blocked by paywall)
    headlines = []
    contents = []
    summaries = []
    accessible_links = []

    num_inaccessible_articles = 0
    for link in article_links:
      url = f'https://news.google.com/{link[2:]}'
      article = Article(url)
      article.download()

      # detected inaccessible articles
      try:
        article.parse()
      except:
        num_inaccessible_articles += 1
        continue
      else:
        article.nlp()
        headlines.append(article.title)
        contents.append(article.text)
        summaries.append(article.summary)
        accessible_links.append(url)

    if num_inaccessible_articles > 7:
      print('Too many articles were detected as inaccessible. Increase the top_x_articles_threshold!')
      return
    
    # Call to GPT to determine broadest headline
    top_3_headlines = headlines[3:]
    gpt_prompt_selection = f"Given the following three headlines from news articles related to food delivery, select the headline that is more general or broader in scope. In your response, ONLY give me the headline itself. \n1. {top_3_headlines[0]} \n 2. {top_3_headlines[1]} \n 3. {top_3_headlines[2]}"
    best_headline = call_gpt_api(gpt_prompt_selection)

    # Retrieve the body text of the article corresponding to best_headline
    best_idx = headlines.index(best_headline) # instead, have it find the index of the headline semantically closest to best_headline
    best_article_text = summaries[0]

    # call to GPT to summarize in under 100 words
    gpt_prompt_summarization = f"Summarize the following text from an article in 100 words or less. Be mindful of what text is relevant: {best_article_text}"
    gpt_prompt_summarization_revised = f"Summarize the following text. {best_article_text}"
    snipp = call_gpt_api(gpt_prompt_summarization_revised)

    return snipp

def send_text_twilio(recieve_number, text_to_send):
   
    account_sid = "YOUR_ACC_SID" # os.environ(YOUR_KEY_NAME)
    auth_token = "YOUR_AUTH_TOKEN" # os.environ(YOUR_KEY_NAME)
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=text_to_send,
        from_='YOUR_TWILIO_NUMBER',
        to=recieve_number
    )

# Putting everything together
def send_snipp(topic, receiving_number, method):

  if method not in ['Twilio', 'Textbelt', 'Slack']:
    print('Invalid texting method. Please enter one of the following options: Twilio, Textbelt, Slack')
    return 

  snipp, link = generate_snipp(topic)
  shortened_url = shorten_url(link)

  # Compose message
  snipp_message = f'Here is your daily {topic} Snipp:\n\n{snipp}\n\nDive deeper here: {shortened_url} \n\nSnipp'

  # Send text
  if method == 'Twilio':
    send_text_twilio(receiving_number, snipp_message)
  elif method == 'Textbelt':
    send_text_textbelt(receiving_number, snipp_message)
  elif method == 'Slack':
    print('Sending via Slack')
    send_slack_message(snipp_message)
    return snipp_message

  print('\nSnipp successfully sent :)')
  print()
  print(snipp_message)
  return

# HERE IS YOUR MAIN CODE
topic = "YOUR_TOPIC_OF_CHOICE"
send_snipp(topic, "YOUR_NUMBER", 'Twilio')

