# Snipp
An application that leverages ChatGPT to help you stay informed about your favorite news!

<img width="497" alt="Screenshot 2023-02-06 at 8 28 36 PM" src="https://user-images.githubusercontent.com/110851085/217148742-2ec7ff89-5bdd-4c79-a155-22bb048fa2e6.png">

## Overview

A lot of people don’t have time to read or watch the news. Yet, we'd still like to stay in touch with what’s going on in the world. Maybe there’s a new topic you want to learn more about. Maybe you want to get updates on professional tennis matches. No matter what it is, this product will help you do just that - with one text per day.

Snipp will text you a concise, easy-to-read summary (aka a Snippet) of the trending news related to your topic of choice. 

## Project Description

In short, this program takes in your desired topic and makes a search to the Google News API. It then collects the top few articles and analyzes the headlines to see which article has the most interesting/general/broader scope content. We then generate a concise, easy-to-read summary using GPT-3 and then format this information nicely into a text.

## How to Run this Project

You will need to create:
1. An OpenAI account (to access API)
2. Google Cloud account
3. Twilio Account
4. Slack workspace (optional)

### Authentication

Here are the keys and tokens you will need throughout the project:
- OpenAI API key
- Twilio account SID
- Twilio authorization token
- Slack bot token (optional)

### Messaging Options

I've incorporated a variety of options for sending and recieving daily Snipps, each of which have their own pros and cons. The preferred method is to directly access the Twilio API.

- SMS
  - Twilio (preferred)
  - Textbelt API
- Email via Python
- Slack

### Deployment/hosting via Google Cloud

In order to automate the process to text me a Snipp once a day, I utilized Google Cloud VM's and crontabs. Here's an amazing tutorial on how to host your personalized script on the Cloud: https://www.youtube.com/watch?v=5OL7fu2R4M8. It will walk you through all the setup an shell-scripting needed to launch the bot.

NOTE: When you create an instance, you can choose a small machine. I personally went with e2-micro and it works perfectly fine!

### Alternatives to GPT-3

In case you don't want to pay for OpenAI tokens, I've included an alternative free summarization method using the HuggingFace BART model. While testing it out, I realized GPT-3 does a better job of putting content into a concise, readable format, but BART also works great!

### Challenges

1. Paywalls

Some article are inaccessible while scraping because they are blocked by a paywall. In order to work around this, I implemented a parsing check in my code to detect paywalls and other inaccessible articles. If a paywall is found, we simply continue scraping the next article.

2. Determining relevant news/headlines

Some articles I came across had headlines that were too specific. For example, when my input topic was "Doordash", I got articles with headlines such as "DoorDash Driver Confronts Customer At Ring Camera Because Of Their $8 Tip". This isn't what I'm interested in, however. I want to know updates about DoorDash in terms of business - something more broad and general in scope. The solution here was to ask GPT-3 to do exactly this. Other models didn't end up performing as well on this task.

### A Sample Snipp

I am personally interested in the rapid grocery delivery industry, so here is the Snipp my program generated.

![Screenshot 2023-02-06 at 10 25 36 PM](https://user-images.githubusercontent.com/110851085/217165306-56e5aef8-f166-4cc3-98f9-3dd38e27afff.jpeg)
