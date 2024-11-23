# test_chatbot.py
from app.helper import generate_bot_response

user_input = "저는 예산이 2000만원 정도 있는데 저렴한 차를 찾고 있어요."
bot_response = generate_bot_response(user_input)
print("Bot Response:", bot_response)
