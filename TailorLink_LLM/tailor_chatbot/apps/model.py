# # app/deepfm_model.py
# import torch
# import torch.nn as nn

# class FactorizationMachine(nn.Module):
#     def __init__(self, reduce_sum=True):
#         super().__init__()
#         self.reduce_sum = reduce_sum

#     def forward(self, x):
#         square_of_sum = torch.sum(x, dim=1) ** 2  
#         sum_of_square = torch.sum(x ** 2, dim=1)  
#         ix = square_of_sum - sum_of_square  
#         if self.reduce_sum:
#             ix = torch.sum(ix, dim=1, keepdim=True) 
#         return 0.5 * ix

# class DeepFM(nn.Module):
#     def __init__(self, field_dims, embed_dim=8, mlp_dims=[16, 16], dropout=0.2):
#         super().__init__()
#         self.num_fields = len(field_dims)
#         self.embedding = nn.Embedding(sum(field_dims), embed_dim)   
#         self.embed_output_dim = self.num_fields * embed_dim  

#         self.fm = FactorizationMachine(reduce_sum=True)

#         # MLP 초기화 (방법 2: 리스트 사용)
#         layers = []
#         input_dim = self.embed_output_dim
#         for dim in mlp_dims:
#             layers.append(nn.Linear(input_dim, dim))
#             layers.append(nn.ReLU())
#             layers.append(nn.Dropout(p=dropout))
#             input_dim = dim
#         layers.append(nn.Linear(input_dim, 1))
#         self.mlp = nn.Sequential(*layers)

#     def forward(self, x):
#         # 임베딩 계산
#         embed_x = self.embedding(x)
#         print("Embed_x shape:", embed_x.shape) 

#         # Factorization Machine 계산
#         x_fm = self.fm(embed_x)
#         print("FM output shape:", x_fm.shape)  

#         # MLP 계산: 임베딩 출력 크기 변환
#         batch_size = embed_x.size(0)
#         x_mlp_input = embed_x.view(batch_size, -1)
#         print("MLP input shape:", x_mlp_input.shape) 
#         x_mlp = self.mlp(x_mlp_input)

#         # 최종 출력 계산
#         x = x_fm + x_mlp
#         return torch.sigmoid(x.squeeze(1))


# def recommend_with_deepfm(user_features: dict, car_metadata: list, model: DeepFM) -> list:
#     feature_mapping = {
#         'age': lambda x: x // 10, 
#         'fuel_efficiency': {'low': 0, 'medium': 1, 'high': 2},
#         'type': {'소형차': 0, 'SUV': 1, '고급차': 2}
#     }   

#     # 사용자 특징 인코딩
#     user_feature_indices = []
#     user_age = feature_mapping['age'](user_features.get('age', 30))
#     user_feature_indices.append(user_age)

#     # 점수 계산을 위한 데이터 준비
#     scores = []
#     for car in car_metadata:
#         # 차량 특징 인코딩
#         car_type = feature_mapping['type'].get(car['type'], 0)
#         car_fuel = feature_mapping['fuel_efficiency'].get(car['fuel_efficiency'], 1)
#         car_feature_indices = [car_type, car_fuel]

#         # 입력 데이터 생성
#         feature_indices = torch.tensor(
#             [user_feature_indices + car_feature_indices], dtype=torch.long
#         )
#         print("Feature indices shape:", feature_indices.shape)  # 디버깅

#         # 모델 예측
#         with torch.no_grad():
#             try:
#                 score = model(feature_indices).item()
#             except Exception as e:
#                 print("Model prediction error:", e)
#                 raise ValueError(f"Feature indices shape: {feature_indices.shape}")
#         scores.append((car, score))

#     # 점수가 높은 순서로 정렬하여 상위 N개 반환
#     return sorted(scores, key=lambda x: x[1], reverse=True)[:3]
