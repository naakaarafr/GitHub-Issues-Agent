# GitHub Issues Agent

An intelligent system that fetches GitHub repository issues, stores them in a vector database, and provides AI-powered search and analysis capabilities using LangChain agents.

## Features

- **GitHub API Integration**: Fetch issues from any public GitHub repository
- **Vector Database Storage**: Store issues in AstraDB for efficient similarity search
- **AI-Powered Analysis**: Use OpenAI GPT models to analyze and answer questions about issues
- **Interactive Chat Interface**: Ask natural language questions about repository issues
- **Note-Taking Capability**: Save important insights to local notes
- **Flexible Embeddings**: Support for OpenAI embeddings for stable performance

## Architecture

The system consists of three main components:

1. **GitHub Data Fetcher** (`github.py`): Retrieves issues from GitHub repositories using the GitHub API
2. **Vector Store Manager** (`main.py`): Manages the AstraDB vector database and agent orchestration
3. **Note Tool** (`note.py`): Provides note-taking functionality for the AI agent

## Prerequisites

- Python 3.8+
- GitHub Personal Access Token
- OpenAI API Key
- AstraDB Database (DataStax)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/naakaarafr/GitHub-Issues-Agent/tree/main
   cd GitHub-Issues-Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root with the following variables:
   ```env
   # GitHub API
   GITHUB_TOKEN=your_github_personal_access_token
   
   # OpenAI API
   OPENAI_API_KEY=your_openai_api_key
   
   # AstraDB Configuration
   ASTRA_DB_API_ENDPOINT=your_astra_db_endpoint
   ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
   ASTRA_DB_KEYSPACE=your_keyspace_name
   ```

## Environment Setup Guide

### GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with the following permissions:
   - `repo` (for private repositories)
   - `public_repo` (for public repositories)
3. Copy the token to your `.env` file

### OpenAI API Key

1. Visit [OpenAI API Platform](https://platform.openai.com/)
2. Create an account and generate an API key
3. Add the key to your `.env` file

### AstraDB Setup

1. Create a free account at [DataStax Astra](https://astra.datastax.com/)
2. Create a new database
3. Generate an application token
4. Get your database endpoint
5. Add these credentials to your `.env` file

## Usage

### Basic Usage

1. **Run the main script**
   ```bash
   python main.py
   ```

2. **Update Issues** (when prompted)
   - Choose 'y' to fetch fresh issues from GitHub
   - Choose 'n' to use existing data in the vector store

3. **Interactive Chat**
   - Ask questions about the repository issues
   - Examples:
     - "What are the most common types of bugs reported?"
     - "Find issues related to performance problems"
     - "Summarize recent feature requests"

### Customizing the Repository

Edit the repository settings in `main.py`:

```python
# Change these to your target repository
owner = "your-username"
repo = "your-repository"
```

### Example Queries

- **Bug Analysis**: "What are the most critical bugs that need attention?"
- **Feature Requests**: "List all feature requests from the last month"
- **Performance Issues**: "Find issues related to memory or CPU usage"
- **User Feedback**: "What are users complaining about most?"

## Project Structure

```
├── main.py              # Main application and agent orchestration
├── github.py            # GitHub API integration
├── note.py              # Note-taking tool
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── notes.txt           # Generated notes (created automatically)
└── README.md           # This file
```

## Key Components

### GitHub Integration (`github.py`)

- Fetches issues using GitHub REST API v3
- Handles authentication with personal access tokens
- Converts issues to LangChain Document format
- Includes metadata: author, comments, labels, creation date

### Vector Database (`main.py`)

- Uses AstraDB as the vector store
- OpenAI embeddings for text vectorization
- Similarity search capabilities
- Collection management (create/delete)

### AI Agent System

- **Tools Available**:
  - `github_search`: Search through stored GitHub issues
  - `note_tool`: Save important insights to notes
- **LLM**: OpenAI GPT-3.5-turbo for analysis
- **Agent Type**: Tool-calling agent with function execution

## Configuration Options

### Changing the LLM Model

Replace the ChatOpenAI configuration in `main.py`:

```python
llm = ChatOpenAI(
    model="gpt-4",  # Upgrade to GPT-4 for better analysis
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1  # Adjust creativity level
)
```

### Adjusting Search Parameters

Modify the retriever configuration:

```python
retriever = vstore.as_retriever(
    search_kwargs={
        "k": 5,  # Number of results to retrieve
        "score_threshold": 0.7  # Minimum similarity score
    }
)
```

## Troubleshooting

### Common Issues

1. **GitHub API Rate Limiting**
   - Ensure you're using a valid GitHub token
   - Authenticated requests have higher rate limits (5000/hour vs 60/hour)

2. **No Issues Found**
   - Check if the repository has public issues
   - Verify your GitHub token has appropriate permissions
   - Try with a different repository (e.g., microsoft/vscode)

3. **Vector Store Connection Issues**
   - Verify AstraDB credentials in `.env`
   - Check that your database is active
   - Ensure the keyspace name is correct

4. **OpenAI API Errors**
   - Verify your API key is active
   - Check your OpenAI account balance
   - Monitor rate limits

### Debug Mode

Enable verbose logging by setting the agent executor:

```python
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,  # This enables detailed logging
    return_intermediate_steps=True
)
```

## Performance Optimization

### For Large Repositories

1. **Batch Processing**: Modify the GitHub fetcher to handle pagination
2. **Selective Filtering**: Filter issues by date, status, or labels
3. **Incremental Updates**: Only fetch new issues since last update

### Vector Store Optimization

1. **Embedding Caching**: Cache embeddings to avoid recomputation
2. **Index Configuration**: Optimize AstraDB index settings
3. **Chunk Size**: Adjust document chunking for better retrieval

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the GitHub Issues in this repository
3. Create a new issue with detailed information about your problem

## Roadmap

- [ ] Support for pull requests analysis
- [ ] GitHub webhooks for real-time updates
- [ ] Advanced analytics and visualization
- [ ] Multi-repository analysis
- [ ] Export capabilities (PDF, CSV)
- [ ] Custom prompt templates
- [ ] Integration with other version control systems

## Acknowledgments

- [LangChain](https://langchain.com/) for the agent framework
- [DataStax Astra](https://astra.datastax.com/) for vector database
- [OpenAI](https://openai.com/) for language models
- [GitHub API](https://docs.github.com/en/rest) for data access
