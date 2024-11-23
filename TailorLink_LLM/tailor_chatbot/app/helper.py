from app.data import get_sample_car_data
from app.llm import analyze_user_input  # LLM 함수를 import

# 경제 상태 카테고리 정의
economic_categories = {
    "low": {"min_price": 0, "max_price": 2000},
    "mid": {"min_price": 2001, "max_price": 5000},
    "high": {"min_price": 5001, "max_price": 10000}
}

# 자동차 추천 함수
def recommend_cars(economic_status: str, car_type: str = None) -> list[dict]:
    cars = get_sample_car_data()
    category = economic_categories[economic_status]
    recommended = [
        car for car in cars
        if category["min_price"] <= car["price"] <= category["max_price"]
        and (car_type is None or car["type"] == car_type)
    ]
    return recommended

# 챗봇 응답 생성 함수
def generate_bot_response(user_input: str) -> str:
    analysis = analyze_user_input(user_input)
    economic_status = analysis["economic_status"]
    car_type = analysis.get("car_type")
    
    # economic_status가 유효한 값인지 확인
    if economic_status not in economic_categories:
        economic_status = "mid"  # 기본값 설정 또는 오류 처리
    
    recommended_cars = recommend_cars(economic_status, car_type)

    if recommended_cars:
        car_list = ', '.join([f"{car['make']} {car['model']} ({car['price']}만원)" for car in recommended_cars])
        bot_response = f"고객님께 추천드리는 차량은 {car_list} 입니다. 더 궁금하신 사항이 있으신가요?"
    else:
        bot_response = "죄송하지만 해당 조건에 맞는 차량을 찾을 수 없습니다. 다른 조건을 말씀해 주시겠어요?"

    return bot_response
