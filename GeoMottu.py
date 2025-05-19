'''
    Comandos para rodar:

    1- Criar o ambiente virtual caso não esteja no PyCharm: python -m venv venv

    2- Ativar o ambiente virtual: venv\Scripts\activate

    3- Baixar as dependências dentro do ambiente: pip install ultralytics opencv-python pandas
    
    Depois rode o script ou pelo botão de play ou pelo terminal usando o comando:
    python GeoMottu.py

    LEMBRETE: Garanta de estar dentro do diretório correto antes de rodar os comandos para que não haja problemas

'''

import cv2
import json
import time
from ultralytics import YOLO

# Carrega modelo YOLOv8 com rastreamento (pode usar yolov8s.pt para melhor desempenho)
model = YOLO("yolov8s.pt")

# Abre a webcam ou vídeo
cap = cv2.VideoCapture(0) 

# Dados salvos
detected_data = []

print("Pressione 'q' para encerrar")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Realiza a detecção
    results = model.track(frame, persist=True, conf=0.5)

    # Acesso aos resultados
    boxes = results[0].boxes
    frame_with_boxes = results[0].plot()

    # Extrai dados de motos
    for box in boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        if class_name == "motorcycle":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            obj_id = int(box.id[0]) if box.id is not None else None

            data = {
                "timestamp": time.time(),
                "object_id": obj_id,
                "class": class_name,
                "position": {"x": center_x, "y": center_y},
                "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            }

            detected_data.append(data)

    # Exibe a imagem com as caixas
    cv2.imshow("Rastreamento de Motos", frame_with_boxes)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()

# Salva os dados em JSON
with open("motos_detectadas.json", "w") as f:
    json.dump(detected_data, f, indent=4)

print("Detecção finalizada. Dados salvos em 'motos_detectadas.json'")
