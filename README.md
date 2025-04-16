# Intdouction (Optional, feel free to skip)
Welcome to my first public project. I decided to make this repo because most of the work I do is confidenital for my clients only and I can't relase those. Most of my personal projects were bulit for my leanring and personal use, so rather than converting them, into public projects, I figured we can just start a new one! 
 
 I've decided to build something to showcase my skills and serve as an example for anybody out there who might be trying to learn or improve their own projects. 
I will be taking a microservices approach, so you can expect modular and scalable components. This also means that you will need to check the other repos to really get the most out of what I will be doing here. For example, after I get oders working and so forth, we'll focus on setting up some analytics, most likley with a seperate repo that focuses soley on analyzing that data. 

You might be worndering, if I'm mainly a data analyst, why wouldn't the first thing I start with not focus on analyics. As much as I love starting up a notebook, building dasboards, building machine learning models, and so forth, none of this really means much if it doens't acutally solve a problem. Instead, we will start with a problem, and we'll use anlaytics as  a solution  Our problem is, while we can make trades on diffrent assets, we don't know what to trade, when to trade it, how much of what to trade etc. So we will firstly build out a platform to make this stuff happen and then we will build data orinted solutions. If it isn't clear, we will need to do some kind of anlaysis to detemrine what to buy/sell, how much of it to buy/sell, when to do this etc. We will then take that anlaysis a step furhter and attempt to auamote as much of this as possible. 

You should expect more repos and funcainlity from me, but please keep in mind, this is very much a work in progress. You should expect a lack of documention, and sometimes best pratices will be skipped for sake of getting things working faster, at first. However, I fully plan to come back fix this later, as the end goal is to have a fully production ready project. There's going to be a lot of learning as we go for this, but eventually it will be fully production ready. 



If you have any questions, concerns, tips, feedback, feel free to reach out to me.

# Prolbme Statement 
- Making orders across muliple exchanges, asset classes and switching between live and paper accounts can be cumberson. 

# Solution
- Build an unified order management system that can track and manage orders across all exchanges, asset classes and can switch between live and paper accounts as needed. 

# Scope
- Though we will build this to be interapobable with other programs later, the main focus of this program is only order management.
- We are not conncred with porfilo mangement, startegeies, etc., only being able to place and manage our orders. 


# Purpose
- This program manages orders across multiple exchanges and platforms. This can be used to place orders across muliple exchanges. You be able to place order on paper or live accounts.
- I want to aslo showcase my skills and resroucefullness. Generally, while I will be building this entirley myself, if thers' an easier ready made soultion, I will just take that,  and focus on how I can add value. Ins ome cases, such as the order manager, intimantley undertsaning the ach




# Current Features
- Place orders (buy or sell, market orders only for now).
- Track active orders, including which ones are open, partiraly filled, or filled.
- Demo moduel that let's you simulate orders and even ranomzied order fills. 
- Control how long and how much an order is filled.

# Features Roadmap
- Manage orders from multiple exchanges ()
- Manage account types (Live, Paper).




# Conventional Commit Types

## 🔧 Core Conventional Commit Types

| Type       | Description                                                                 |
|------------|-----------------------------------------------------------------------------|
| **feat**   | A new feature                                                               |
| **fix**    | A bug fix                                                                   |
| **docs**   | Documentation only changes                                                  |
| **style**  | Changes that do not affect the meaning of the code (white-space, formatting, etc) |
| **refactor** | A code change that neither fixes a bug nor adds a feature                |
| **perf**   | A code change that improves performance                                     |
| **test**   | Adding or correcting tests                                                  |
| **build**  | Changes that affect the build system or external dependencies (e.g., npm)   |
| **ci**     | Changes to CI configuration files and scripts (e.g., GitHub Actions, Travis) |
| **chore**  | Other changes that don’t modify src or test files (e.g., release notes, configs) |
| **revert** | Reverts a previous commit                                                   |

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



# Closing Thoughts
For anybody out there looking at this program to learn and thinking you'll be able to vibe code your way through something like this, think again. While I strongly reomend using some form of Gen AI in your workflow, YOU need to be able to design the systems and such or you will have a very bad time. This means, Gen AI should be used to EHANCE yoru workflow, not do the work for you. Helping ou with syntax or lower level problems is fine. You need to be able to handle the higher level problems and so forth. You need to acutally read and undesratnd EVERY SINGEL LINE of code that you plan to acutally implmeent. 

Orginally, I wasn't too concered with this part of the project and I did want to just vibe code my way through the entire progam, but I quickly found that 

In my opinoin, if you're doing it right, using Gen AI in the workflow is acutally a more demanding  than doing it the tradiontal way. When you do it all by yourself, googling and using stack overlfow, you tend to spend a lot more time on already solved problems, and you see less code all together. This means if you run into a small low level issue, you have to stop thinking at a high level where the REAL value is driven and focus on these smaller tasks. You get increidly good at a small amount of code and lower level thinking, but you dont' get nearly as much expeirnce at a high level, nor are you able to think in terms of solving the problems an driving value. It allows you to tackle porjects on your own you never would've dreamed of doing alone. Lastly, it makes you a better communicator. This might sound strange but you have to be able to artiucluate the problem , often times over and over again, and you have to make it make sense to someone else. 

