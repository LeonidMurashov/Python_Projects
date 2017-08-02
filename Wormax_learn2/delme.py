from neural_network import build_model

LR = 1e-3
MODEL_NAME = 'models/wrm13-encoded-1e-04-15-ep-407k-data.model'
model = build_model(LR, 4)
model.load(MODEL_NAME)

model.s