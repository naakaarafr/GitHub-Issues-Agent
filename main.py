from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings  # Alternative to Google embeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from github import fetch_github_issues
from note import note_tool

load_dotenv()

def connect_to_vstore():
    # Use OpenAI embeddings as alternative (more stable)
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")
    
    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None
        
    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="github",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    return vstore

print("Connecting to vector store...")
vstore = connect_to_vstore()
print("Connected successfully!")

add_to_vectorstore = input("Do you want to update the issues? (y/N): ").lower() in [
    "yes",
    "y",
]

if add_to_vectorstore:
    # Using a repository with actual issues for testing
    # Change these back to your repo once you have issues
    owner = "microsoft"
    repo = "vscode"
    
    print(f"Fetching issues from {owner}/{repo}...")
    issues = fetch_github_issues(owner, repo)

    if not issues:
        print("No issues found. This could be because:")
        print("- The repository has no issues")
        print("- Your GitHub token doesn't have permission to read issues")
        print("- The repository is private and your token lacks access")
    else:
        print(f"Found {len(issues)} issues to add to vector store.")

        try:
            print("Deleting existing collection...")
            vstore.delete_collection()
            print("Collection deleted successfully.")
        except Exception as e:
            print(f"Could not delete collection (this is normal if collection doesn't exist): {e}")

        print("Reconnecting to vector store...")
        vstore = connect_to_vstore()
        
        print("Adding issues to vector store...")
        vstore.add_documents(issues)
        print("Issues added successfully!")

print("\nSearching for 'flash messages'...")
results = vstore.similarity_search("flash messages", k=3)

if results:
    print(f"Found {len(results)} results:")
    for i, res in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Content: {res.page_content[:200]}...")  # First 200 chars
        print(f"Metadata: {res.metadata}")
else:
    print("No results found for 'flash messages'")
    print("This is normal if:")
    print("- No issues were added to the vector store")
    print("- None of the issues contain content related to 'flash messages'")

print("\nProgram completed successfully!")

retriever = vstore.as_retriever(search_kwargs={"k": 3})
retriever_tool = create_retriever_tool(
    retriever,
    "github_search",
    "Search for information about github issues. For any questions about github issues, you must use this tool!",
)

# You can use either OpenAI or Google Gemini for the chat model
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Create a prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant with access to tools. Use the tools available to answer user questions about GitHub repositories, issues, and code analysis.

Available tools:
{tools}

When you need to use a tool, follow this format:
1. Think about what information you need
2. Use the appropriate tool with the correct parameters
3. Analyze the results
4. Provide a comprehensive answer

Always be thorough in your analysis and provide actionable insights."""),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Use OpenAI ChatGPT
llm = ChatOpenAI(
    model="gpt-3.5-turbo", 
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

tools = [retriever_tool, note_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while (question := input("Ask a question about github issues (q to quit): ")) != "q":
    result = agent_executor.invoke({"input": question})
    print(result["output"])