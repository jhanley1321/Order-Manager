# Overview

This project is an order management system built using a microservices architecture. It demonstrates placing and tracking orders, simulating order fills, and managing data storage and retrieval.

# Introduction (Optional, feel free to skip)

Welcome to my first public project! I decided to make this repo because most of my work is confidential for clients, and I can't release those projects. Most of my personal projects were built for my own learning and use, so rather than converting them into public projects, I figured it would be better to just start a new one. I will move this section later as I release more projects.

If you have any questions, concerns, tips, or feedback, feel free to reach out to me.

# Running the App

Before running anything, I suggest first running the unit tests to verify that everything is working correctly:

```
python -m unittest discover
```

To run the order management system itself, you will need to provide your own values in the main file:

```
python main.py
```

If you want to use it with a front end, simply run:

```
streamlit run front_end.py
```

To run from the Docker image, run:

```
.\run-order-manager.bat
```

If you changed any values, you will need to run the following:

```
docker build -t my-python-app .
```

# How to Use

You will first need to create the OrderManager object:

```
manager = OrderManager(data_folder="Data")
```

`data_folder` tells the OrderManager class where to look for the data. You can set this to any folder you like.

To place a single order, use the following:

```
order = OrderDetails(ticker_id=1003, order_quantity=150, order_price=60.0, exchange_id=3)
manager.add_order(order)
```

`OrderDetails` is a class that handles the details of an order, including ticker ID, quantity, price, and exchange ID. These are all required for filling an order so it knows where to place the order as you add more tickers, exchanges, etc.

If you want to view the orders from the command line, simply run the following command:

```
manager.list_orders()
```


# How to use (Front End)

run the following command in the command line to start it

```
streamlit run main_frontend.py
```

# Purpose

This program manages orders across multiple exchanges and platforms. It can be used to place orders across multiple exchanges, and you will be able to place orders on paper or live accounts.  
I also want to showcase my skills and resourcefulness. Generally, while I will be building this entirely myself, if there is an easier, ready-made solution, I will use that and focus on how I can add value. In some cases, such as the order manager, intimately understanding the architecture is important.

# Current Features

* Place orders (buy or sell, market orders only for now).
* Track active orders, including which ones are open, partially filled, or filled.
* ~~Demo module that lets you simulate orders and even randomize order fills.~~
* Control how long and how much of an order is filled.
* Front end page for placing and using orders in place of demo (deprecated, but you can still technically use it).~~
* Add a Docker container for deployment and testing.

# Features Roadmap

* Manage orders from multiple exchanges.
* Manage account types (Live, Paper).
* Add PSQL/Timescale DB option for storing orders.
* Add Redis layer for caching.
* Add specific  cloud support for Azure (AWS and GCP will come later).
* Add Order-Maximizer
* Add support for Order Types
* Add support for custom order Types (write your own logic for how the order is placed, this is not a strategy function)
* Add cost basis optimizer 
* Add Capital gains tax optitmizer
* Add a cost basis/Cpaitla gains optimzier (Optimize the best combintion of the two.)


# Tech Stack
* Python
* Docker

# Conventional Commit Types

## 🔧 Core Conventional Commit Types

| Type         | Description                                                                       |
|--------------|-----------------------------------------------------------------------------------|
| **feat**     | A new feature                                                                     |
| **fix**      | A bug fix                                                                         |
| **docs**     | Documentation only changes                                                        |
| **style**    | Changes that do not affect the meaning of the code (white-space, formatting, etc) |
| **refactor** | A code change that neither fixes a bug nor adds a feature                         |
| **perf**     | A code change that improves performance                                           |
| **test**     | Adding or correcting tests                                                        |
| **build**    | Changes that affect the build system or external dependencies (e.g., npm)         |
| **ci**       | Changes to CI configuration files and scripts (e.g., GitHub Actions, Travis)      |
| **chore**    | Other changes that don't modify src or test files (e.g., release notes, configs)  |
| **revert**   | Reverts a previous commit                                                         |

## 🧪 Extended/Optional Types

| Type         | Description                                                         |
|--------------|---------------------------------------------------------------------|
| **wip**      | Work in progress; not ready for production                          |
| **merge**    | A merge commit                                                      |
| **hotfix**   | A quick fix for a critical issue                                    |
| **security** | Security-related changes                                            |
| **deps**     | Updating or pinning dependencies                                    |
| **infra**    | Infrastructure-related changes (e.g., Terraform, Dockerfiles)       |
| **ux**       | Changes affecting user experience (not necessarily features)        |
| **i18n**     | Internationalization and localization changes                       |
| **release**  | Version bumps, changelog updates, tagging, etc.                     |
| **env**      | Environment-related changes (e.g., `.env` files, deployment configs)|

## 📚 Optional Scopes

You can add an optional scope in parentheses to clarify what part of the app is affected.

# Contact Me

If you'd like to get in touch, feel free to reach out via email or connect with me on LinkedIn:

- **Email:** [carljames1321@gmail.com](mailto:carljames1321@gmail.com)
- **LinkedIn:** [https://www.linkedin.com/in/jchanley/](https://www.linkedin.com/in/jchanley/)