from RAG.llm import prompt
from RAG.llm.prompt import *
from langchain.retrievers.multi_query import MultiQueryRetriever
from RAG.types import state
from RAG.llm.model import get_OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from RAG.database.database import faiss_db
from RAG.tools.memory_tools import *
from langgraph.prebuilt import ToolNode, tool_node, tools_condition

llm = get_OpenAI()
output_parser = StrOutputParser()

# memory tools
tools = [save_recall_memory, search_recall_memories, get_brand_list, get_model_list, get_year_list, get_detail_list, get_option_list]

tool_node = ToolNode(tools)

def load_memorizer(state: state) -> state:
    
    llm_with_tools = llm.bind_tools(tools)
    print("---메모리를 불러 왔습니다.---")
    prompt = memory_prompt()
    messages = state['messages']
    
    # 기존 메모리를 포맷팅
    recall_str = (
        "<recall_memory>\n" + "\n".join(state.get("recall_memories", [])) + "\n</recall_memory>"
    )
    chain = prompt | llm_with_tools
    
    # LLM에 현재 대화 및 기존 메모리 전달
    response = chain.invoke({
        "messages": messages,
        "recall_memories": recall_str
    })
    
    state['recall_memories'].append(response)
    
    # 대화 메시지에도 LLM 응답 추가
    state["messages"].append({"role": "assistant", "content": response})
    
    return state


# Routing
def Router(state: state) -> state:
    
    print("---질문을 분류 중입니다.---")
    prompt = Question_classification_prompt()
    
    chain = prompt | llm | output_parser
    response = chain.invoke({"question": state['messages']})
    
    # response 디버깅 출력
    print(f"Response: {response}")
    
    if response == "Yes":
        state['insurance_grading'] = "Yes"
    else:
        state['insurance_grading'] = "No"
        
    # 업데이트된 state 디버깅 출력
    print(f"Updated state: {state}")

    return state


# 조건부 연결 추가
# Router -> conditional_retriever
def conditional_retriever(state: state):
    """
    조건부 경로를 결정하는 함수.
    'insurance_grading' 결과에 따라 경로가 나뉨.
    """
    print("---질문 분류---")
    if state["insurance_grading"] == "Yes":
        return "retriever_tool"
    else:
        return "agent"


# 답변할 수 없는 질문
def agent(state: state):
    if state["insurance_grading"] == "No":
        print("---대답할 수 없는 질문입니다.---")
        
    
    return state


# retriever
def retriever_tool(state:state) -> state:
    
    multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=faiss_db().as_retriever(),
    llm=llm
    )
    
    print("---문서를 불러오는 중 입니다.---")
    
    query = state['messages']
    state['previous_question'].append(query)
    
    question = state["messages"][-1]["content"]
    prompt = retrieved_prompt()
    retrieved_docs = multi_query_retriever.get_relevant_documents(prompt)
    
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"question":question})
    
    state["retrieved_docs"] = retrieved_docs
    state["answer"] = response
    
    print(f"질문 분류: {state['retrieved_docs']}")
    return state


# 문서의 관련성 분석
def grade_documents(state: state) -> state:
    
    print("---문서 관련성을 분석 중입니다.---")
    messages = state["messages"]
    docs = state["retrieved_docs"]
    
        # Data model
    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'Relevant' or 'Not Relevant'")

    # LLM with tool and validation
    llm_with_tool = llm.with_structured_output(grade)
    
    prompt = grade_documents_prompt()

    print("---문서를 분류 중입니다.---")
    
    chain = prompt | llm_with_tool
    
    question = state["messages"]
    docs = state["retrieved_docs"]
    question = messages[0]["content"]
    
    scored_result = chain.invoke({"question": question, "context": docs})
    
    score = scored_result.binary_score

    state["document_grading"] = score
    
    # chain = prompt | llm_with_tool | llm | output_parser
    # response = chain.invoke({"question":question, "context":context})
    print(f"Document Grading: {state['document_grading']}")
    
    if score == "Relevant":
        state['document_grading'] = "Relevant"
    else:
        state['document_grading'] = "Not Relevant"

    return state


# 조건부 연결 추가
def conditional_decision(state: state):
    """
    조건부 경로를 결정하는 함수.
    'document_grading' 결과에 따라 경로가 나뉨.
    """
    if state["document_grading"] == "Relevant":
        return "generate"
    else:
        return "rewrite"
    
    
def rewrite(state: state) -> state:
    
    print('---질문 변경---')
    prompt = get_rewrite_prompt()
    previous = state['previous_question']
    question = state['messages'][0]["content"]

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({'previous': previous, 'question': question})

    # messages의 마지막 message 내용 업데이트
    state['message'] = response

    return state

def generate(state: state) -> state:
    
    print('---최종 답변 생성---')
    
    question = state['messages'][-1]["content"]
    docs = state["retrieved_docs"]
    prompt = final_answer_prompt()
    
    chain = prompt | llm | output_parser
    response = chain.invoke({"question":question, "docs":docs})
    state['message'] = response
    
    return {"messages": [response]}