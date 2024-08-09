# Crypto Trading Bot

## Overview
The Crypto Trading Bot is a Python-based tool designed to interact with Binance Futures using the Binance API. It allows users to place and cancel orders, retrieve account balances, and will be expanded with additional functionalities over time. Due to its ability to connect to a real Futures account, it is crucial to set up the bot correctly.

# Table of Contents
* [Prerequisites](#prerequisites)
* [Features](#Features)
* [Requirements](#Requirements)
* [Getting Started](#getting-started)

# Prerequisites
* Binance Futures Account

# Features
* Order Management: Place and cancel orders on Binance Futures.
* Account Balance: Retrieve and display account balance for selected assets.
* API Integration: Interacts directly with Binance Futures API.
* Extendable: Designed to be extended with additional trading functionalities.

# Requirements
* Python 3.x
* requests library

# Getting Started
1) Clone this repository to your local machine
2) fill the Credentials file with your api keys
3) execute the Credentials file.
Linux/mac command

```bash
source Credentials.sh or sh Credentials.sh
```
windows command(cmd)
```bash
call Credentials.bat
```

windows command(powershell)
```bash
.\Credentials.ps1
```
4) run the bot
```bash
python main.py 
```
