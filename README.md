# REST API using Fast API

This API contains the following endpoints.

- `GET /users`
- `POST /users`
- `GET /users/:uuid`
- `PATCH /users/:uuid`
- `DELETE /users/:uuid`
- `PATCH /users/password/:uuid`
- `POST /auth/sign-in`
- `POST /auth/sign-up`
- `POST /auth/sign-out`

A sample request looks like this to the cloud deployment.
`GET https://fast-api-rest-api-76100969075.us-central1.run.app/api/v1/auth/sign-in`

You need to prefix `https://fast-api-rest-api-76100969075.us-central1.run.app/api/v1` for all the endpoints defined here.

To use the local development, follow the below instructions.

- Install conda and create a new environment
- Use poetry to add dependencies
- Change .env file's `DATABASE_HOST` to `db`
- Start the service with `docker-compose up --build` to start the PostgreSQL and the FastAPI

You can find the OpenAPI definition at, `https://fast-api-rest-api-76100969075.us-central1.run.app/docs`.
