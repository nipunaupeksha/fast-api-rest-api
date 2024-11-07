# REST API using Fast API

This API contains the following endpoints.

- GET /users
- POST /users
- GET /users/:uuid
- PATCH /users/:uuid
- DELETE /users/:uuid
- PATCH /users/password/:uuid
- POST /auth/sign-in
- POST /auth/sign-up
- POST /auth/sign-out

To use the local development

- Install conda and create a new environment
- Use poetry to add dependencies
- Change .env file's `DATABASE_HOST` to `db`
- Start the service with `docker-compose up --build` to start the PostgreSQL and the FastAPI
