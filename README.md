# FOSSistant AI API Server

A Foundational AI API Server for FOSSistant

## Overview

FOSSistant AI API Server is designed to serve AI models for FOSSistant in a containerized environment, making it easy to deploy and scale AI services.

## Prerequisites

- Docker and Docker Compose installed on your system
- AI model files compatible with the server
- Sufficient disk space for model storage

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/FOSSistant_AI_API.git
   cd FOSSistant_AI_API
   ```

2. Place the required AI model files in the `models/` directory
   - Ensure models are in the correct format
   - Verify model compatibility with the server

## Usage

1. Start the server using Docker Compose:

   ```bash
   docker compose up -d
   ```

2. The API server will be available at `http://localhost/` (default port: HTTP/80)

3. To stop the server:
   ```bash
   docker compose down
   ```

## API Documentation

The API documentation is available at `http://localhost/docs` when the server is running.

## License

This project is licensed under the Apache License 2.0.
