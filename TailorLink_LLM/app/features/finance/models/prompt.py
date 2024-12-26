from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate


# 질문 분류 프롬프트
def Question_classification_prompt():
    prompt = PromptTemplate.from_template(
        """
        You are an expert in automobile insurance Q&A. Your task is to determine whether a user's question is related to 'automobile insurance'.
        
        Here is the user question: {question} 
            
        Evaluate the question based on these criteria:

        - If the question uses or mentions words or phrases related to 'automobile insurance' such as "coverage", "personal injury", "liability", "compensation", "treatment", "indemnity", "amount", "passenger accident", "collision damage", "responsibility", "comprehensive", "deductible", "premium", "surcharge", and "renewal", and is asking about issues related to automobile insurance, respond with "Yes".
        - If the question does not explicitly mention 'automobile insurance' but uses words or expressions that can be applied to automobile insurance, also respond with "Yes".
        - If the question is not related to 'automobile insurance' or does not meet the above criteria, respond with "No".

        # Output Format

        The response must be in English and should be either "Yes" or "No".
        
        #Question:  
        {question}  
        
        #Answer:    
        """
    )
    return prompt


# 리트리버 프롬프트
def retrieved_prompt():
    prompt = PromptTemplate.from_template(
        """
        You are a professional assistant trained to optimize search queries to search for the most relevant documents. Help with more effective searches by creating multiple versions of the questions you provide differently.

        Here is the user question: {question}

        # Steps

        1. Think about whether users can express the same question in multiple ways and rephrase the question in different ways.
        2. When reconstructing a question, the intent and meaning of the original question must be maintained.
        3. Use synonyms, sentence structure variations, alternative expressions, etc. as needed.
        4. Create at least 5 re-drafted versions** for the questions you have provided.
        5. Make sure the reconstructed questions are concise, clear, and appropriate for use in search queries.

        # Output Format

        Each reconstructed version of the question is provided in text, and the final document list must be represented in JSON format.
        
        # Examples

        ## Input
        User Questions:  
        "What's the best camera brand?"

        ## Output
        Reconfigured Questions:
        - "What's the best camera brand?"
        - "What's a good camera brand?"
        - "What camera brand is worth buying?"
        - "Do you have any camera brand you want to recommend?"
        - "What's the list of popular camera brands?"
        
        ```

        # Notes

        - Keep natural and clear expressions when reconstructing questions.
        - The goal of the paper is to ensure that the list of searched documents meets your information needs.
        - Explore different vocabulary and expressions for the best results.
        """
    )
    return prompt


# 문서 관련성 분석 프롬프트
def grade_documents_prompt():
    prompt = PromptTemplate.from_template(
        """
        You are a grader assessing relevance of a retrieved document to a user question.
        
        Here is the user question: {question}
        Here is the retrieved document: {context}
        
        Assess the relevance of a retrieved document to a user's question by analyzing both keyword matches and semantic meaning.

        Review the provided document and question. If the document contains keywords or semantic meanings that relate directly to the user question, grade it accordingly.

        # Steps

        1. **Keyword Analysis**: Identify any keywords from the user question present in the document.
        2. **Semantic Analysis**: Assess the overall content of the document for meanings or concepts related to the user question.
        3. **Relevance Decision**: 
        - If either keywords or semantic content are related, score the document as 'Relevant'.
        - If neither is related, score the document as 'Not Relevant'.

        # Output Format

        - Provide a binary score: 'Relevant' or 'Not Relevant'.

        # Notes

        - Semantic analysis is as important as keyword matching.
        - Consider the broader context in which the keywords or topics might be applied.
        - Be consistent in evaluating similar cases.
        """
    )
    return prompt



# 질문 변경 프롬프트
def get_rewrite_prompt():
    prompt = PromptTemplate.from_template(
        """
        Here is the user question: {question}
        Here is the Previous questions: {previous}
        
        Rewrite the question '{question}' to improve search quality. Use the context of the previous question to generate only one improved question. Make sure that the new question does not overlap with the previous one.
        """
    )
    return prompt


# 답변 생성 프롬프트
def final_answer_prompt():
    prompt = PromptTemplate.from_template(
        """
        Here is the user question: {question}
        Here is the user Relevant Documents: {docs}
        
        # Steps

        1. Read and understand the user's question {question} to identify the key components and what needs to be addressed.
        2. Review the provided information {docs} carefully to ensure no important details are overlooked.
        3. Interpret the information in the context of the question.
        4. Construct a clear and concise response that directly answers the user's question, ensuring all necessary aspects are covered.

        # Output Format

        The response should be a short paragraph or bullet points, depending on the complexity and nature of the question. Aim for brevity and clarity.
        """
    )
    return prompt


# 메모리 프롬프트
def memory_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant with advanced long-term memory"
                " capabilities. Powered by a stateless LLM, you must rely on"
                " external memory to store information between conversations."
                " Utilize the available memory tools to store and retrieve"
            " important details that will help you better attend to the user's"
            " needs and understand their context.\n\n"
            "Memory Usage Guidelines:\n"
            "1. Actively use memory tools (save_core_memory, save_recall_memory)"
            " to build a comprehensive understanding of the user.\n"
            "2. Make informed suppositions and extrapolations based on stored"
            " memories.\n"
            "3. Regularly reflect on past interactions to identify patterns and"
            " preferences.\n"
            "4. Update your mental model of the user with each new piece of"
            " information.\n"
            "5. Cross-reference new information with existing memories for"
            " consistency.\n"
            "6. Prioritize storing emotional context and personal values"
            " alongside facts.\n"
            "7. Use memory to anticipate needs and tailor responses to the"
            " user's style.\n"
            "8. Recognize and acknowledge changes in the user's situation or"
            " perspectives over time.\n"
            "9. Leverage memories to provide personalized examples and"
            " analogies.\n"
            "10. Recall past challenges or successes to inform current"
            " problem-solving.\n\n"
            "## Recall Memories\n"
            "Recall memories are contextually retrieved based on the current"
            " conversation:\n{recall_memories}\n\n"
            "## Instructions\n"
            "Engage with the user naturally, as a trusted colleague or friend."
            " There's no need to explicitly mention your memory capabilities."
            " Instead, seamlessly incorporate your understanding of the user"
            " into your responses. Be attentive to subtle cues and underlying"
            " emotions. Adapt your communication style to match the user's"
            " preferences and current emotional state. Use tools to persist"
            " information you want to retain in the next conversation. If you"
            " do call tools, all text preceding the tool call is an internal"
            " message. Respond AFTER calling the tool, once you have"
            " confirmation that the tool completed successfully.\n\n",
            ),
            ("placeholder", "{messages}"),
        ]
    )
    return prompt

def agent_answer_prompt():
    prompt = PromptTemplate.from_template(
        # 최종 응답 이쁘게 만들기
        """
        ---

        # Objective

        Refine the given input text `{answer}` to enhance **clarity**, **tone**, and **structure**, ensuring a professional and aesthetically pleasing response. The focus is on improving flow, readability, and alignment with the intended audience.

        ---

        # Steps

        ### 1. **Input Analysis**
        - Examine `{answer}` to understand its core message and intended tone.
        - Identify areas for improvement, such as overly complex language, redundancy, inconsistent tone, or lack of clarity.

        ### 2. **Strategic Refinement**
        - Simplify complex language while preserving the original meaning.
        - Ensure the tone is appropriate for the intended audience (e.g., formal, conversational, technical).
        - Improve structural flow by reorganizing ideas or splitting overly long sentences for readability.
        - Add transitions, where necessary, to enhance coherence between ideas.

        ### 3. **Stylistic Enhancement**
        - Use engaging and dynamic language to captivate the reader.
        - Incorporate rhetorical devices (e.g., parallelism, emphasis) where appropriate.
        - Adjust formatting (e.g., bullet points, numbered lists) for better visual appeal if multiple ideas are presented.

        ### 4. **Comprehensive Review**
        - Check for grammar, spelling, and punctuation errors.
        - Verify stylistic consistency and adherence to the desired tone.
        - Ensure the refined version matches the intended purpose and audience expectations.

        ---

        # Output Format

        The output should be:
        - A **polished and professional version** of the input, presented in **paragraph(s)** or **structured format** (e.g., lists, sections) as needed for clarity.
        - **Concise yet detailed**, emphasizing readability and coherence.
        - Designed to convey the original message more effectively and attractively.

        ---

        # Examples

        ### **Example 1**
        **Input**:  
        "The explanation is fine, but it uses a lot of technical jargon and has run-on sentences that make it difficult to follow."

        **Output**:  
        "The explanation effectively covers the main points, but it can be improved by simplifying technical terms and breaking down longer sentences for easier understanding. Here’s a clearer version: 'This concept refers to... (insert revised explanation).'"

        ---

        ### **Example 2**
        **Input**:  
        "Here are the features of the product. It has a great battery. The design is nice. Also, the screen quality is good, but there are too many reflections."

        **Output**:  
        "The product offers several noteworthy features: a long-lasting battery, a sleek and attractive design, and high-quality screen resolution. However, the screen may have excessive reflections in bright environments."

        ---

        ### **Example End**

        This upgraded structure provides a **detailed, systematic, and audience-focused** approach for refining responses while ensuring high-quality output.
                
        """
    )
    return prompt