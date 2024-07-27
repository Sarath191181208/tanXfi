## Application Overview
Create a price alert application that triggers an email when the user’s target price is
Achieved.

Say, the current price of BTC is \$28,000, a user sets an alert for BTC at a price of 33,000\$.
The application should send an email to the user when the price of BTC reaches 33,000\$.
Similarly, say, the current price of BTC is 35,000\$, a user sets an alert for BTC at a price of
33,000\$. The application should send an email when the price of BTC reaches 33,000\$.

Things to do for the assignment
- Create a rest API endpoint for the user’s to create an alert `alerts/create/`
- Create a rest API endpoint for the user’s to delete an alert `alerts/delete/`
- Create a rest API endpoint to fetch all the alerts that the user has created.
- The response should also include the status of the alerts
(created/deleted/triggered/.. or any other status you feel needs to be included)
- Paginate the response.
- Include filter options based on the status of the alerts. Eg: if the user wanted
only the alerts that were triggered, then the endpoint should provide just that)
- Add user authentication to the endpoints. Use JWT tokens.
- There is no need to add tests.
- You can use Binance's WebSocket connection to get real-time price updates
- You can also use this endpoint to fetch the latest price of the cryptocurrency:
https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=ma
rket_cap_desc&per_page=100&page=1&sparkline=false but prefer using
Binance WebSocket
- When the price of the coin reaches the price specified by the users, send an email to the
user that set the alert at that price. (send mail using Gmail SMTP, SendGrid, etc). If this is
taking too much time, just print the output to the console.
- Add a caching layer for the “fetch all alerts” endpoints (use Redis/Memcache/etc)

## Requirements
- You can use Python/ Go/ Ruby
- If you are applying for the Ruby role, please use Ruby.
- Use Postgres to store data (or any DB you feel that gets the job done)
- Use Rabbit MQ / Redis as a message broker for the task to send emails.
- Bundle everything inside a docker-compose file.
- Document your solution in the README.md file. Consider adding the following details
- Steps to run the project (eg: docker-compose up)
- Document the endpoints
- Document the solution for sending alerts
