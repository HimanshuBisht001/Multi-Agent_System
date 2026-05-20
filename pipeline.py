from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
from langchain_core.messages import ToolMessage


def run_research_pipleline(topic: str) -> dict:
    state = {}

    # Search agent working
    print("Step 1: Search Agent is woking -------------")
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {
            "messages": [
                ("user", f"Find the reliable and detailed information about: {topic}.")
            ]
        }
    )

    # Extract raw tool output
    raw_search_results = ""
    for msg in search_result["messages"]:

        if isinstance(msg, ToolMessage):
            raw_search_results = msg.content

    # Extract Final AI Summary
    state["search_summary"] = search_result["messages"][-1].content

    state["raw_search_results"] = raw_search_results

    print("\n Search Summary\n")
    print(state["search_summary"])

    print("\n Raw Search Reasult\n")
    print(state["raw_search_results"])

    # Step 2: Reader Agent
    print("\n Reader Agent is Scraping Top Resources...")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    #     f"""
                    #     Based on the following search results about: {topic}
                    #     Select the MOST relevant URL.
                    #     Then use the scraping tool to scrape detailed content from that URL.
                    #     Search Results:
                    #     {state['raw_search_results']}
                    # """,
                    f"""
                            Based on the following search results about: {topic}

                            Choose the MOST relevant NEWS ARTICLE URL.

                            Avoid:
                            - Twitter/X
                            - Facebook
                            - social media pages

                            Then scrape the webpage using the scraping tool.

                            Return the RAW scraped text only.
                            Do not summarize.

                            Search Results:
                            {state['raw_search_results']}
                            """,
                )
            ]
        }
    )

    state["scraped_content"] = reader_result["messages"][-1].content
    # print("\n Scraped_Content\n", state["scraped_content"])

    print("*" * 50)
    print("Writer is drafting the report ....")

    agent_research = (
        f"Search Summary:\n{state['search_summary']}\n\n"
        f"Scraped Content: {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({"topic": topic, "research": agent_research})

    print(f"\nFinal Report: {state['report']}")

    # Critic Report

    print("*" * 50)
    print("Critic is review the report!....")

    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    print("*" * 100)
    print("Feedback is ")
    print(state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic : ")
    run_research_pipleline(topic)
