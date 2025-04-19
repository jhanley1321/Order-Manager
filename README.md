# Overview
This project is an order management system built using a microservices architecture. It demonstrates placing and tracking orders, simulating order fills, and managing data storage and retrieval. 

 





# Introduction (Optional, feel free to skip)

Welcome to my first public project! I decided to make this repo because most of my work is confidential for clients, and I can't release those projects. Most of my personal projects were built for my own learning and use, so rather than converting them into public projects, I figured it would be better to just start a new one.

I've decided to build something to showcase my skills and serve as an example for anyone out there who might be trying to learn or improve their own projects. I will be taking a microservices approach, so you can expect modular and scalable components. This also means that you will need to check the other repos to really get the most out of what I’m doing here. For example, after I get orders working and so forth, I'll focus on setting up some analytics, most likely with a separate repo that focuses solely on analyzing that data.

If you have any questions, concerns, tips, or feedback, feel free to reach out to me.





# Running the app
Run this for the order management itself. You will need to provide your own values in the main file."
```
python main.py
```

If you want to use it with a front end, then simply run:
```
streamlit run front_end.py
```


# Problem Statement

Making orders across multiple exchanges and asset classes, and switching between live and paper accounts, can be cumbersome.

# Solution

Build a unified order management system that can track and manage orders across all exchanges and asset classes, and can switch between live and paper accounts as needed.

# Scope

Though we will build this to be interoperable with other programs later, the main focus of this program is only order management.  
We are not concerned with portfolio management, strategies, or anything else, only being able to place and manage our orders.

# Purpose

This program manages orders across multiple exchanges and platforms. It can be used to place orders across multiple exchanges, and you will be able to place orders on paper or live accounts.  
I also want to showcase my skills and resourcefulness. Generally, while I will be building this entirely myself, if there is an easier, ready made solution, I will use that and focus on how I can add value. In some cases, such as the order manager, intimately understanding the architecture is important.

# Current Features

* Place orders (buy or sell, market orders only for now).
* Track active orders, including which ones are open, partially filled, or filled.
* ~~Demo module that lets you simulate orders and even randomize order fills.~~
* Control how long and how much of an order is filled.
* Front end page for placing and using order in place of demo (this will likley be moved later).

# Features Roadmap

* Manage orders from multiple exchanges.
* Manage account types (Live, Paper).
* Add a Docker container for deployment and testing.
* Add MongoDB option for storing orders.
* Add Redis layer for cahing.
* Add specific support for Azure  (AWS, and GCP will come later).


# Conventional Commit Types

## 🔧 Core Conventional Commit Types

| Type       | Description                                                                       |
|------------|-----------------------------------------------------------------------------------|
| **feat**   | A new feature                                                                     |
| **fix**    | A bug fix                                                                         |
| **docs**   | Documentation only changes                                                        |
| **style**  | Changes that do not affect the meaning of the code (white-space, formatting, etc) |
| **refactor** | A code change that neither fixes a bug nor adds a feature                       |
| **perf**   | A code change that improves performance                                           |
| **test**   | Adding or correcting tests                                                        |
| **build**  | Changes that affect the build system or external dependencies (e.g., npm)         |
| **ci**     | Changes to CI configuration files and scripts (e.g., GitHub Actions, Travis)      |
| **chore**  | Other changes that don’t modify src or test files (e.g., release notes, configs)  |
| **revert** | Reverts a previous commit                                                         | 

## 🧪 Extended/Optional Types

| Type          | Description                                                         |
|---------------|---------------------------------------------------------------------|
| **wip**       | Work in progress; not ready for production                          |
| **merge**     | A merge commit                                                      |
| **hotfix**    | A quick fix for a critical issue                                    |
| **security**  | Security-related changes                                            |
| **deps**      | Updating or pinning dependencies                                    |
| **infra**     | Infrastructure-related changes (e.g., Terraform, Dockerfiles)       |
| **ux**        | Changes affecting user experience (not necessarily features)        |
| **i18n**      | Internationalization and localization changes                       |
| **release**   | Version bumps, changelog updates, tagging, etc.                     |
| **env**       | Environment-related changes (e.g., `.env` files, deployment configs)|

## 📚 Optional Scopes

You can add an optional scope in parentheses to clarify what part of the app is affected:





