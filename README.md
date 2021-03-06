# Jisho Bot 

[![CodeFactor](https://www.codefactor.io/repository/github/lauchmelder23/jishobot/badge)](https://www.codefactor.io/repository/github/lauchmelder23/jishobot)

A simple discord bot implementing the [Jisho](https://jisho.org/) API. This bot aims to provide all the information typically available on the website in a neat discord embed interface.

## What can it do?
As of right now, the Bot displays all the information from Jisho's search page as an interactive discord embed.
It includes information about
* Spelling and Reading
* Meanings and Definitions
* JLPT grades and Wanikani levels

![An example embed](https://i.imgur.com/apxYK10.png)

It now also delivers information about Kanji, including
* Kun/On Readings
* Stroke count
* Radicals

![An example embed](https://i.imgur.com/16REFh2.png)

The embed is interactive and can be controlled via Reactions. This will then show the next/previous entry. Right now, only the latest embed will be interactive, so if you use the bot again the previous responses will become inactive.

## How do I get it?
Either [invite](https://discord.com/api/oauth2/authorize?client_id=742658127060795393&permissions=59456&scope=bot) a bot I am hosting or [set it up](#setup) yourself. Note that if you invite the bot you won't be able to change its prefix!

## Usage
To perform a normal dictionary search, use

    -[search|s] <query>

To perform a kanji search, use

    -[kanji|k] <kanji(s)>

The prefix can be changed in the config file.

## <a name="setup"></a>Setup
Clone this repo, create a `config.json` in the root directory with the following layout

    {
        "key": Your discord bot token,
        "prefix": Your prefix,
    }


If there a re questions or requests you can find me on discord: `Lauchmelder#1234`