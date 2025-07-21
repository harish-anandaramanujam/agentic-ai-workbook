# Import the gRPC runtime host for worker agents from the autogen extension
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
# Import custom Agent and Creator classes
from agent import Agent
from creator import Creator
# Import the gRPC worker agent runtime
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
# Import AgentId for identifying agents
from autogen_core import AgentId
# Import custom messages module
import messages
import asyncio

# Load environment variables from a .env file, overriding existing ones if necessary
from dotenv import load_dotenv
load_dotenv(override=True)

# Number of agents to create and orchestrate
HOW_MANY_AGENTS = 20

# Asynchronous function to create an agent, send a message, and write the response to a file
async def create_and_message(worker, creator_id, i: int):
    try:
        # Send a message to the worker agent, requesting it to process 'agent{i}.py'
        result = await worker.send_message(messages.Message(content=f"agent{i}.py"), creator_id)
        # Write the agent's response content to a markdown file
        with open(f"idea{i}.md", "w") as f:
            f.write(result.content)
    except Exception as e:
        # Print any exceptions that occur during the process
        print(f"Failed to run worker {i} due to exception: {e}")

# Main asynchronous function to orchestrate agent creation and messaging
async def main():
    # Start the gRPC host for worker agents
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start() 
    # Create a worker agent runtime connected to the host
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker.start()
    # Register the Creator agent with the worker
    result = await Creator.register(worker, "Creator", lambda: Creator("Creator"))
    # Create an AgentId for the Creator
    creator_id = AgentId("Creator", "default")
    # Prepare coroutines for creating and messaging multiple agents in parallel
    coroutines = [create_and_message(worker, creator_id, i) for i in range(1, HOW_MANY_AGENTS+1)]
    # Run all coroutines concurrently
    await asyncio.gather(*coroutines)
    try:
        # Stop the worker and host after all tasks are complete
        await worker.stop()
        await host.stop()
    except Exception as e:
        # Print any exceptions that occur during shutdown
        print(e)

# Entry point: run the main function if this script is executed directly
if __name__ == "__main__":
    asyncio.run(main())


