## Install uv
Instructions to install uv from source can be found [here](https://docs.astral.sh/uv/).
or
```bash
pip install uv
```

## Installing Python with uv
```bash
uv python install 3.11
```

## Creating Virtual Environment
```bash
uv venv --python 3.11
```

## Pin a Python Version
```bash
uv python pin 3.11
```

## Activating Virtual Environment
```bash
source .venv/bin/activate
```

## Updating or Pulling Dependencies
```bash
uv sync
```

## Starting Server
```bash
uv start
```
## Add installing packages and information about running client.
how od I integrate the client startup when starting Python server?

## Architecture

The general application architecture is Domain Driven Design (DDD). The domain layer in the domain folder with services, repositories and models. 

I'm using ChromaDB as the vector store. For production applications, my choice is pgvector with Postgres.

For an LLM, I'm using OpenAI, because it's one of the most common LLMs.

## Rest API

https://flask-rest-api.readthedocs.io/en/stable/quickstart.html

## Agentic Agent Framework
smolagents

## Logging/Telemetry
- Nice to have, add a diagnostic view to see the raw output.

## Docker Instructions

## User Authentication

## Application Test assumptions
Using Cursor AI, Claude Code, Windsurf, etc. is not allowed, but using Codeium or Copilot is allowed.

## Deployment Strategy

## Security Scans

## Docker commands
docker build . -t duplocloud

## Assumptions
Hard coding the in the filesystem. A better apporach would be to pull the files daily and update the vector database. At first
we could do a total refresh of the vector database, but as our data grows, we'll need to do an incremental update.

Images in the files will be discarded. A possible solution would be to use a vision llm to generate a description of them to 
store in the vector database.

## Environment Variables

## Testing

## License

## Technology Stack
Used Flask because it was mentioned in the interview.

However, in we're staying in the Python ecosystem, FastAPI is a better choice because of its native support for async/await.

My recommendation is to use express or fastify with the Nodejs ecosystem for most operations. OpenAI and most LLM providers support both Python and Node api libraries. Nodejs is a better choice because of its native support for async/await and when used with TypeScript gives the benefit of static typing. Most UI libraries are also written in TypeScript so code sharing is possible. There are time when Python is the only choice, in the cases we can expose the a Python API to expose the functionality.

## Roadmap

## TODO
- Implement features
- Add Tests
- Add Documentation
