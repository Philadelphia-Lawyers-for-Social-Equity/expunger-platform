# API

## Authentication

The API handles authentication via JSON Web Tokens, as provided by [django rest
framework simple
jwt](https://github.com/davesque/django-rest-framework-simplejwt).  Endpoints
are:

- **api/v0.1.0/auth/token/**
    - accepts: `{"username": "xxx", "password": "yyy"}`
    - returns: `{"access": "...", "refresh": "..."}`
    - The access token must be provided in the `Authorization: Bearer ...`
      header for requests to private endpoints.
    - The refresh token can be used to retrieve a fresh access token when the
      access token expires.
- **api/v0.1.0/refresh/token**
    - accepts: `{"refresh": "..."}`
    - returns: `{"access": "..."}`
