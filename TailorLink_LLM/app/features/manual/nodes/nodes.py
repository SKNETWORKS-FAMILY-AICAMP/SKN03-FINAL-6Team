from click import prompt

from app.features.manual.utils.types import State
from langgraph.graph import START, END
from app.features.manual.models.prompt_templates import *
from app.features.manual.models.model import create_openai_model, create_ollama_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from app.features.manual.models.schemas import QuestionList, GradeHallucinations, AnswerWithHistory
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from app.features.manual.tools.tools import search_milvus
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from app.features.manual.tools.tools import get_genesis_model

from app.core.logger import logger

def generate_history_base_answer(state: State):
    logger.info("Running generate history base answer")

    history_base_prompt = create_history_base_answer_prompt()
    llm = create_openai_model('gpt-4o-mini')
    structured_llm_grader = llm.with_structured_output(AnswerWithHistory)
    contextual_responder = history_base_prompt | structured_llm_grader

    response = contextual_responder.invoke({"chat_history": state['chat_history'], "question": state['message']})

    state['answer'] = response.answer

    if response.binary_score == 'yes':
        state['is_stop'] = True
    else:
        state['is_stop'] = False

    return state

def history_base_answer_check_conditional(state: State):
    if state['is_stop']:
        return END
    else:
        return "genesis_check"

# 제네시스 관련 질문 판단 노드 함수
def genesis_check_and_query_split(state: State) -> State:
    logger.info("Running genesis check")

    prompt = create_check_genesis_and_split_prompt()
    llm = create_openai_model('gpt-4o-mini')
    structured_llm_grader = llm.with_structured_output(QuestionList)

    chain = prompt | structured_llm_grader

    car_list = get_genesis_model()

    response = chain.invoke({"car_model": car_list, 'question': state['message']})

    state['questions'] = response.question_list
    state['answer'] = response.print
    state['is_stop'] = not response.vailid_question

    return state

def genesis_check_conditional(state: State):
    if state['is_stop']:
        return END
    else:
        return 'search'

# 벡터DB 조회 노드 함수
def generate_vector_search_base_answer(state: State) -> State:
    logger.info("Running vector search")

    query_list = state['questions']
    state['previous_question'].append(state['message'])

    if state['change_count'] > 0:
        query = state['message']
        context = search_milvus.invoke({"query_list":[query], "car_id":state['car_id']})
    else:
        context = search_milvus.invoke({"query_list":query_list, "car_id":state['car_id']})

    prompt = create_context_based_answer_prompt()
    llm = create_openai_model()

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"context": context, "question":state['message']})
    state['context'] = context
    state['answer'] = response

    return state

def grade_hallucination(state: State):
    logger.info('running grade_hallucination')

    hallucination_prompt = create_hallucination_prompt()
    llm = create_openai_model('gpt-4o-mini')
    structured_llm_grader = llm.with_structured_output(GradeHallucinations)

    hallucination_grader = hallucination_prompt | structured_llm_grader

    docs = state['context']
    generation = state['answer']

    response = hallucination_grader.invoke({"documents": docs, "generation": generation})

    if response.binary_score == 'yes':
        state['is_stop'] = False
    else:
        state['is_stop'] = True

def grade_hallucination_conditional(state: State):
    if state['is_stop']:
        return 'rewrite'
    else:
        return 'calculate'


# 답변 점수 측정 노드 함수
def calculate_score(state: State):
    logger.info("Running calculation score")

    query = state['message']
    context = state['context']
    answer = state['answer']
    
    from langchain.output_parsers import ResponseSchema, StructuredOutputParser

    # 사용자의 질문에 대한 답변
    response_schemas = [
        ResponseSchema(
            name="score",
            description="질문에 대한 점수, 숫자여야 한다.",
        ),
        ResponseSchema(name="reason", description="점수를 제외한 나머지 "),
    ]
    # 응답 스키마를 기반으로 한 구조화된 출력 파서 초기화
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    prompt = create_answer_evaluation_prompt()
    llm = create_openai_model()

    chain = prompt | llm | output_parser

    response = chain.invoke({"question": query, "response": answer})
    logger.info(f'점수: {response['score']}')

    if not state['best_score'] or state['best_score'] < response['score']:
        state['best_answer'] = state['answer']
        state['best_score'] = response['score']

    if response['score']>=85 or state ['change_count']==2:
        state['answer'] = state['best_answer']
        state['is_stop'] = True
    else:
        state['is_stop'] = False
        state['change_count'] += 1

    return state

def calculate_score_conditional(state: State):
    if state['is_stop']:
        return END
    else:
        return 'rewrite'

# 질문 쿼리 변경 노드 함수
def query_rewrite(state: State) -> State:
    logger.info("Running query rewrite")

    prompt = create_query_rewrite_prompt()
    llm = create_openai_model('gpt-4o-mini')
    previous = state['previous_question']
    query = state['message']

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({'previous': previous, 'question': query})

    # messages의 마지막 message 내용 업데이트
    state['message'] = response

    return state

