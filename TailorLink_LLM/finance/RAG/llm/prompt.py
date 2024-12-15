from langchain_core.prompts import PromptTemplate

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


def get_rewrite_prompt():
    prompt = PromptTemplate.from_template(
        """
        Here is the user question: {question}
        Here is the Previous questions: {previous}
        
        Rewrite the question '{question}' to improve search quality. Use the context of the previous question to generate only one improved question. Make sure that the new question does not overlap with the previous one.
        """
    )
    return prompt

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