# yt-topic-scraper
A command line tool for scraping Youtube titiles, urls, and transcripts on a specific topic/search.

## Youtube Data API Key
To run this script you must first get a Youtube Data API key (these are free):

1. Go to the [Google credentials page](https://console.cloud.google.com/apis/credentials).
2. Create a project if you haven't already.
3. Once that is created, go back to the credentials page and click "Create Credential" at the top.
4. Create an API Key.
5. Copy it and save it somewhere.

That's it!

## Installation
1. You must first [install `uv`](https://docs.astral.sh/uv/getting-started/installation/):
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Then just run the script with the appropriate cmdline args:
```sh
uv run ./main.py Macroeconomics 3 --api_key API_KEY
```

Output:
```
Video 1: Macroeconomics- Everything You Need to Know
Video ID: MKO1icFVtDc
Transcript:
hey how you doing econ students this is Jacob Clifford welcome to ACDC econ so in this quick video I'm going to cover everything you need for an introductory macroeconomics class or an AP macroeconomics class I'm going to go super fast but keep in mind this is not designed to retach you all the concepts it's designed to help you get ready

// ... cut for brevity

how to get exchange rates and don't get it tripped up when you're analyzing two different countries and whether the currency appreciates or depreciates hey thank you so much for watching this video I wish you all the best of luck on the AP test or on your big final exam hey you're going to do awesome okay thanks for watching till next time
--------------------------------------------------------------------------------

Video 2: Macroeconomics: Crash Course Economics #5
Video ID: d8uTB5XorBw
Transcript:
Adriene: Hi I'm Adriene Hill, welcome back
to Crash Course Economics. As you may remember from our first video, economics can be divided
into two parts: microeconomics and macroeconomics. Since macroeconomics is the one that's most
often in the news, that's where we're gonna start. We'll get to microeconomics, which

// ... cut for brevity

Economics. It was made with the help of all of these nice people. Now, if you want to
help keep Crash Course free for everyone forever, please consider subscribing over at Patreon.
It's a voluntary subscription platform that allows you to pay whatever you want per month
to make Crash Course exist, and it also increases GDP. Thanks for watching, DFTBA.
--------------------------------------------------------------------------------

Video 3: Lecture 1: Introduction to 14.02 Principles of Macroeconomics
Video ID: heBErnN3ZPk
Transcript:
[SQUEAKING] [RUSTLING] [CLICKING] RICARDO J. CABALLERO: OK. Let's start. So hello, everyone. Welcome to 1402, Introduction
to Macroeconomics. And I won't teach today. So that's a good news. I will start on Wednesday. So what I want to do today
is essentially tell you what macro is about,
macroeconomics is about, and also
the rules of the game. So what a difference
a single letter makes. Many of you must
have taken 1401.

// ... cut for brevity

Outlook, which will have lots of pictures like this. And you're going to be able to
write a little equation very simple on the side
to try to understand what is going on there, and to
catch the mistakes, as well. OK, WEO has less mistakes
than the Wall Street Journal, but you will catch
mistakes, you'll see, you'll be proud of those.
```
