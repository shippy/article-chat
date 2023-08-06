# JournalArticle.chat

A thin wrapper around an vector-store-enriched conversation with an LLM chatbot.

## Setup

### Production

See [the infrastructure README](./infrastructure/README.md) for details.

### Development

- Populate `.env` with local environment variables.
- Run `npm install` in `frontend/` (use `make setup`), then `npm run dev` to start a development server.
- Run `docker-compose up` in root

### Testing

#### Frontend

We use Cypress.

1. Populate `frontend/.env` with Cognito credentials.
2. Start frontend and backend servers.
3. Run `npm run cypress:open` in `frontend/`.

#### Backend

1. Create a local virtualenv from `backend/requirements.txt` and `backend/requirements-dev.txt`.
2. Run `pytest` (or `ptw backend/` for continuous `pytest`s)