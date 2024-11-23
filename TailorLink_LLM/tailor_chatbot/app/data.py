# app/data.py

def get_sample_car_data():
    cars = [
        {
            "id": 1,
            "make": "현대",
            "model": "아반떼",
            "price": 1500,
            "type": "소형차",
            "fuel_efficiency": "좋음",
            "description": "경제적인 소형차로 연비가 우수합니다."
        },
        {
            "id": 2,
            "make": "기아",
            "model": "셀토스",
            "price": 2000,
            "type": "SUV",
            "fuel_efficiency": "보통",
            "description": "컴팩트한 SUV로 실용성이 높습니다."
        },
        {
            "id": 3,
            "make": "현대",
            "model": "코나",
            "price": 1800,
            "type": "SUV",
            "fuel_efficiency": "좋음",
            "description": "스타일리시한 디자인의 소형 SUV입니다."
        },
        # 추가 데이터...
    ]
    return cars
