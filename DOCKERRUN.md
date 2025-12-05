# Running DevCluster with Docker

This guide explains how to build and run the DevCluster application using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- A GitHub Personal Access Token (see [Getting a GitHub Token](#getting-a-github-token))

---

## Getting a GitHub Token

1. Go to [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click **Generate new token** (classic)
3. Give it a name like `DevCluster Token`
4. Select scopes (minimum required: `public_repo` and `user:email`)
5. Click **Generate token** and copy it immediately (you won't see it again)
6. Store it securely — you'll use it to run the container

---

## Running with Docker Compose (Recommended)

### Option 1: Using a `.env` file (Easiest)

1. Create a `.env` file in the project root:
   ```bash
   echo GITHUB_API_TOKEN=your_token_here > .env
   ```
   Replace `your_token_here` with your actual GitHub token.

2. Build the image (first time only):
   ```bash
   docker-compose build
   ```

3. Run the container **interactively** (since `main.py` requires user input):
   ```bash
   docker-compose run devcluster python main.py
   ```

4. Stop the container:
   ```bash
   docker-compose down
   ```

**Note:** Use `docker-compose run` instead of `docker-compose up` to enable interactive input for the application.

### Option 2: Using environment variable (PowerShell)

1. Set the environment variable:
   ```powershell
   $env:GITHUB_API_TOKEN = "your_token_here"
   ```

2. Build the image (first time only):
   ```bash
   docker-compose build
   ```

3. Run the container **interactively**:
   ```bash
   docker-compose run devcluster python main.py
   ```

4. Stop the container:
   ```bash
   docker-compose down
   ```

---

## Running with Development Mode

For development with hot-reload (changes reflect immediately without rebuilding):

```bash
docker-compose -f docker-compose.dev.yml up
```

This mounts your entire project directory, so code changes are reflected in the container instantly. The application will prompt for input interactively in this mode.

---

## Running with Plain Docker (Advanced)

If you prefer to use Docker directly without Compose:

1. Build the image:
   ```bash
   docker build -t devcluster:latest .
   ```

2. Run the container interactively with your GitHub token:
   ```powershell
   docker run -it -e GITHUB_API_TOKEN="your_token_here" `
     -v $(pwd)/data:/app/data `
     -v $(pwd)/models:/app/models `
     -v $(pwd)/notebooks:/app/notebooks `
     --name devcluster-app `
     devcluster:latest python main.py
   ```

   The `-it` flags enable interactive terminal mode for user input.

3. Stop the container:
   ```bash
   docker stop devcluster-app
   docker rm devcluster-app
   ```

---

## Viewing Logs

To see the container's output/logs:

```bash
docker-compose logs -f
```

Or with plain Docker:
```bash
docker logs -f devcluster-app
```

The `-f` flag follows logs in real-time.

---

## Persisting Data

Both `docker-compose.yml` and `docker-compose.dev.yml` mount volumes for:
- **`./data`** — Raw and processed data files
- **`./models`** — Trained KMeans models (joblib files)
- **`./notebooks`** — Jupyter notebooks

Any data written to these directories persists on your host machine, even after the container stops.

---

## Common Issues

### Container exits immediately (EOFError: EOF when reading a line)
- This happens when using `docker-compose up` with an application that requires input
- **Solution:** Use `docker-compose run` instead: `docker-compose run devcluster python main.py`
- For development mode with interactive terminal, use `docker-compose -f docker-compose.dev.yml up`

### FileNotFoundError with Windows paths
- If you get `FileNotFoundError: [Errno 2] No such file or directory: 'C:\Users\...'`
- **Solution:** The application now uses cross-platform paths (`os.path.join()`) instead of hardcoded Windows paths
- Make sure you rebuild the Docker image: `docker-compose build`
- Then run: `docker-compose run devcluster python main.py`

### Token not being recognized
- Ensure your token is correctly set in `.env` or environment variable
- Verify the token hasn't expired (regenerate if needed)
- Check that there are no extra spaces around the token value

### Permission denied errors
- On Linux/Mac, you may need to run with `sudo` or add your user to the docker group
- On Windows, ensure Docker Desktop is running

### Version warning in docker-compose
- You may see: `the attribute 'version' is obsolete...`
- This is just a warning and doesn't affect functionality. You can remove `version: '3.8'` from `docker-compose.yml` to silence it.

---

## Environment Variables

The container respects these environment variables:

| Variable | Required | Example |
|----------|----------|---------|
| `GITHUB_API_TOKEN` | Yes | `ghp_xxxxxxxxxxxxxxxxxxxx` |
| `PYTHONUNBUFFERED` | No | `1` (already set in Dockerfile) |
| `PYTHONDONTWRITEBYTECODE` | No | `1` (already set in Dockerfile) |

---

## Next Steps

Once the container is running, you can:
- View extracted GitHub data in `./data/raw/`
- Check trained models in `./models/`
- Review analysis notebooks in `./notebooks/`
- Modify code and run again (especially in dev mode for instant feedback)

For more details on the DevCluster application itself, see [README.md](README.md).
