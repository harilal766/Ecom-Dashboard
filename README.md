# Ecom-Dashboard : A Django based web application made for E-commerce sellers to automate and simplify their daily tasks.
## Supported Ecommerce platforms.
1. Amazon Seller Central
2. Shopify

# Contents
- [Installation on local machine](#Installation)
- [Amazon Selling Parner API](#SPAPI)

## Installation
1. `python -m venv {{env_name}}`
2. `pip install -r requirements.txt`
3. Activate the environment.
4. Create a .env file on the root directory and store these credentials on this format.
    `ACCESS_TOKEN = {{your Access  token}}`<br>

    `REFRESH_TOKEN = {{Your Refresh token}}`<br>

    `CLIENT_ID = {{Your Client id}}`<br>

    `CLIENT_SECRET = {{Your Client secret}}`<br>

**NB : Make sure `.env` file is included in `.gitignore` to avoid pubslishing your API Credentials by accident.**

## SP API

## API Structure

## Important Model details and their API fields
### Orders Model
#### Unshipped Orders (Orders that are confirmed but not scheduled for pickup).
- Order id : AmazonOrderID
- Scheduled / Unscheduled : OrderStatuses -> Shipped / Unshipped.
- Ship by date  : LatestShipDate.

### Reports Model
- ReportType : 






Models : Orders, Reports, Easy ship



1. API call limit handling. 
2. Access token initialization from env file.
5. cache file.
6. auto data updation like js.
7. Sandbox switching in developer options.
8 . OTP login, email confirmation.