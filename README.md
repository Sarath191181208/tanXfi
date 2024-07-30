# TanXFi 
An microservice application to solve the problem mentioned in the [problem.md](problem.md).
Basically a price monitoring system which mails when a certain threshold is met.

## Overview 
The project uses the fowlling technologies: 
- Django / DjangoREST 
- Celery 
- redis
- Docker 
- Docker compose 
- JWT 
- Websockets

## Architecture 
- This diagram is created using [https://diagrams.mingrammer.com](https://diagrams.mingrammer.com)
![Architecture diagram](./assets/email_notfication_system.png)

### Features 
- Create, Read, Delete alerts for the pricing alerts.
- Realtime price monitoring using wss://stream.binance.com.
- Highly scalable email notification system using redis as a queue.
    
### End points 

- `POST /api/token` Creates and responds with a JWT and a refresh token.
- `POST /api/token/refresh/` Refresh the current JWT token.
- `POST /alerts/create/` Creates a new alert 
- `DELETE /alerts/delete` Deletes an alert 
- `GET /alerts` Gets the alert and supports query params

## Requirements 
- docker installed `sudo pacman -Sy docker`
- docker-compose installed `sudo pacman -Sy docker-compse`

## Setting up the project locally 

1. Clone the repository
    ```bash
    git clone https://github.com/Sarath191181208/tanXfi
    ```
2. Go into the cloned repository
    ```bash
    cd tanXfi
    ```
3. Run the docker compose
    ```bash
    docker-compose up 
    ```
4. Credentials for using the app
    ```python
        ## admin
        name: admin 
        password: --none--
    
        ## user
        name: user
        password: user@2001
    ```

## Setting up dev environment 
**(THIS IS JUST MY PREFERENCE)**

If you use neovim you can easily set up a dev environment using `.tmux` file it's just a sh script.
These are the steps you have to follow:

1. Make the `.tmux` file executable
    ```bash
    chmod +x ./.tmux
    ```
2. Run the `.tmux` file to setup the neovim and tmux env.

    ```bash
    ./.tmux
    ```
3. What it does is it creates 4 windows namely `1.nvim`, `2.cmd`, `3.docker`, `4.lazydocker` and puts you in this tmux session. This helps you by saving configuring tmux manually.

## Unsafe practices 
All the unsafe practices like putting visible `passwords`, `keys`, `apis`, etc... Are to make the review purpose easier.

## Todo 
The work that needs to be done is put in [Todo.md](Todo.md).
