from click import prompt

from RAG.types import State
from langgraph.graph import START, END
from RAG.llm.prompt_templates import get_genesis_manual_classification_prompt, get_answer_with_context_prompt, get_score_answer_prompt, get_rewrite_query_prompt
from RAG.llm.model import get_OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from RAG.tools.tools import search_milvus
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# 제네시스 관련 질문 판단 노드 함수
def genesis_check(state: State):
    print('판단 시작')
    prompt = get_genesis_manual_classification_prompt()
    llm = get_OpenAI()

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"question":state['message']})

    if response == "yes":
        state['is_valid_question'] = True
    else:
        state['is_valid_question'] = False

    return state

def genesis_check_conditional(state: State):
    if state['is_valid_question']:
        return 'search'
    else:
        return END

# 벡터DB 조회 노드 함수
def vector_search(state: State) -> State:
    print('벡터 조회')
    query = state['message']
    state['previous_question'].append(query)

    context = search_milvus(query)
    prompt = get_answer_with_context_prompt()
    llm = get_OpenAI()

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"context": context, "question":state['message']})
    state['context'] = context
    state['answer'] = response

    return state

# 답변 점수 측정 노드 함수
def calculate_score(state: State):
    print('점수 측정')
    query = state['message']
    context = state['context']
    answer = state['answer']
    
    from langchain.output_parsers import ResponseSchema, StructuredOutputParser

    # 사용자의 질문에 대한 답변
    response_schemas = [
        ResponseSchema(
            name="score",
            description="질문에 대한 점수, 숫자여햐 한다.",
        ),
        ResponseSchema(name="reason", description="점수를 제외한 나머지 "),
    ]
    # 응답 스키마를 기반으로 한 구조화된 출력 파서 초기화
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)


    prompt = get_score_answer_prompt()
    llm = get_OpenAI()

    chain = prompt | llm | output_parser

    response = chain.invoke({"context": context, "question": query, "answer": answer})
    print(f'점수: {response['score']} ')
    if not state['best_answer'] or state['best_score'] < response['score']:
        state['best_answer'] = state['answer']
        state['best_score'] = response['score']

    if response['score']>=85 or response['change_count']==2:
        state['is_pass'] = True
    else:
        state['is_pass'] = False
        state['change_count'] += 1

    return state


def calculate_score_conditional(state: State):
    if state['is_pass']:
        return END
    else:
        return 'rewrite'

# 질문 쿼리 변경 노드 함수
def query_rewrite(state: State) -> State:
    print('쿼리변경')
    prompt = get_rewrite_query_prompt()
    llm = get_OpenAI()
    previous = state['previous_question']
    query = state['message']

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({'previous': previous, 'question': query})

    # messages의 마지막 message 내용 업데이트
    state['message'] = response

    return state


