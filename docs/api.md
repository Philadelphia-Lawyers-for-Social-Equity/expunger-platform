# API

## Authentication

The API handles authentication via JSON Web Tokens, as provided by [django rest
framework simple
jwt](https://github.com/davesque/django-rest-framework-simplejwt).  Endpoints
are:

- **api/v0.1.0/auth/token/**
    - POST accepts: `{"username": "xxx", "password": "yyy"}`
    - returns: `{"access": "...", "refresh": "..."}`
    - The access token is used in the `Authorization: Bearer ...`
      when making later requests to private endpoints
    - The refresh token can be used to retrieve a fresh access token when the
      access token expires.
- **api/v0.1.0/refresh/token**
    - POST accepts: `{"refresh": "..."}`
    - returns: `{"access": "..."}`

- **api/v0.1.0/expunger/attorney/<pk>**
    - Requires access token
    - GET returns attorney json, including:
        - url (api link for this attorney)
        - pk (integer id)
        - bar (attorney's bar identifier, string)
        - name (annorney's full name

- **api/v0.1.0/expunger/attorneys/**
    - Requires access token header
    - GET produces list of available attorneys, each formatted as above

- **api/v0.1.0/expunger/organization/<pk>**
    - Requires access token header
    - GET returns organization json, including:
        - url (api link for this organization)
        - pk (integer id)
        - name
        - phone
        - address
            - street1
            - street2 (may be null)
            - city
            - state
            - zipcode

- **api/v0.1.0/expunger/organizations**
    - Requires access token header
    - GET produces a list of available organizatiens, each formatted as above

- **api/v0.1.0/expunger/my-profile/**
    - Requires access token header
    - GET produces the authenticated users profile, or 404, including
        - attorney (see the attorney endpoint for all details)
        - organization (see the organization endpoint for all details)
        - user
            - first_name
            - last_name
            - email
            - username
    - POST allows the creation of a new profile, if the user has none
        - accepts `{"attorney": attorney pk, "organization": organization pk}`
        - attorney and organization are required
    - PUT allows updating an existing profile
        - accepts `{"attorney": attorney pk, "organization": organization pk}`
        - attorney and organization are optional
