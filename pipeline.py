from agents import search_agent , reader_agent , writer_chain , critic_chain
# Base function
def research_pipeline(topic : str) -> dict:
    state = {}

    s_agent = search_agent()
    s_result = s_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["s_results"] = s_result["messages"][-1].content    # Key and value
    print("\nSearch result",state["s_results"])

    r_agent = reader_agent()
    r_result = reader_agent.invoke({
        "messages" : [("user",
            f"Based on the following search results about'{topic}'"
            f"Pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results: \n{state['s_result'][:800]}")]
    })
    state["scraped_results"] = r_result["messages"][-1].content   # Key and value
    print("\nScraped result",state["scraped_results"])

    research_combined = (
        f"SEARCH RESULTS : \n {state["s_results"]}\n\n",
        f"DETAILED SCRAPED CONTENT : \n {state["scraped_result"]}"
    )

    state['report'] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })
    print("\n Final Report \n ", state["report"])

    state["feedback"] = critic_chain.invoke({
        "report":state["report"]
    })
    print("\n Critic Report \n", state["feedback"])

    return state

if __name__ == "__main__":                # to call pipeline
    topic = input("\n Enter a research topic :")
    research_pipeline(topic)
    