import gradio as gr
from duckduckgo_search import DDGS


def search_duckduckgo(query, max_results=3):
    """
    Function to implement search on duck duck go
    """
    print(f"Searching for: {query}")  # Debug print
    try:
        results = DDGS().text(query, max_results=max_results)
        print(f"Raw search results: {results}")  # Debug print
        return results
    except Exception as e:
        print(f"Error in search: {str(e)}")  # Debug print
        return []

def generate_context(results):
    """
    Function to generate context from search results
    """
    context = ""
    for result in results:
        context += f"{result.get('title', '')} {result.get('body', '')} "
    return context.strip()

def chat(message, history):
    """
    Main chat function
    """
    print(f"Received message: {message}")  # Debug print
    if not history:
        # Initial query
        results = search_duckduckgo(message)
        print(f"Search function returned: {results}")  # Debug print
        if not results:
            print("No results found")  # Debug print
            return "I'm sorry, I couldn't find any relevant information. Could you please rephrase your question or try a different query?"
        
        response = "Here are the top 3 results I found:\n\n"
        for i, result in enumerate(results, 1):
            print(f"Processing result {i}: {result}")  # Debug print
            response += f"{i}. {result.get('title', 'No title')}\n{result.get('body', 'No body')}\nSource: {result.get('href', 'No source')}\n\n"
        response += "Do you have any follow-up questions about these results?"
    elif len(history)==1:
        previous_response = history[-1][1]
        if "Here are the top 3 results I found:" in previous_response:
            # This is the first follow-up question
            #follow_up_query = f"{message} context: {previous_response}"
            results = search_duckduckgo(message, max_results=1)
            
            if not results:
                return "I'm sorry, I couldn't find any additional information related to your follow-up question. Could you please rephrase or ask a different question?"
            
            response = "Based on your follow-up question, here's what I found:\n\n"
            for i, result in enumerate(results, 1):
                response += f"{result.get('title', 'No title')}\n{result.get('body', 'No body')}\nSource: {result.get('href', 'No source')}\n\n"
            response += "Is there anything else you'd like to know about this topic?"
    else:
        # Any further questions
        return "I'm sorry, I can only handle one follow-up question. Please ask a new initial question if you need more information."

        
    print(f"Sending response: {response}")  # Debug print
    return response

iface = gr.ChatInterface(
    chat,
    title="RCM Assistant",
    description="I can help answer your RCM-related questions. Ask me anything!",
)

if __name__ == "__main__":
    print("Starting the RCM Assistant...")  # Debug print
    iface.launch(debug=True)