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
import time
from ultralytics import YOLO
import cx_Oracle
import sys

# === CONFIGURAÇÃO DO BANCO ORACLE COM TRATAMENTO DE ERRO ===
try:
    dsn = cx_Oracle.makedsn("oracle.fiap.com.br", 1521, service_name="orcl")
    conn = cx_Oracle.connect(
        user="rm558043",
        password="fiap24",
        dsn=dsn
    )
    print("Conectado ao banco com sucesso!")
    cursor = conn.cursor()
except cx_Oracle.DatabaseError as e:
    print("Erro ao conectar ao banco de dados Oracle:", e)
    sys.exit(1)

# === FUNÇÃO PARA INSERIR OU ATUALIZAR NO BANCO ===
def salvar_ou_atualizar_no_banco(dado):
    try:
        sql = """
        MERGE INTO MOTOS_LOCALIZADAS dest
        USING (
            SELECT :object_id AS object_id FROM dual
        ) src
        ON (dest.OBJECT_ID = src.object_id)
        WHEN MATCHED THEN
            UPDATE SET 
                TIMESTAMP_REG = TO_DATE(:timestamp, 'YYYY-MM-DD HH24:MI:SS'),
                CLASSE = :classe,
                POS_X = :pos_x,
                POS_Y = :pos_y,
                X1 = :x1,
                Y1 = :y1,
                X2 = :x2,
                Y2 = :y2
        WHEN NOT MATCHED THEN
            INSERT (OBJECT_ID, TIMESTAMP_REG, CLASSE, POS_X, POS_Y, X1, Y1, X2, Y2)
            VALUES (
                :object_id,
                TO_DATE(:timestamp, 'YYYY-MM-DD HH24:MI:SS'),
                :classe, :pos_x, :pos_y, :x1, :y1, :x2, :y2
            )
        """
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dado["timestamp"]))
        cursor.execute(sql, {
            "object_id": dado["object_id"],
            "timestamp": ts,
            "classe": dado["class"],
            "pos_x": dado["position"]["x"],
            "pos_y": dado["position"]["y"],
            "x1": dado["bbox"]["x1"],
            "y1": dado["bbox"]["y1"],
            "x2": dado["bbox"]["x2"],
            "y2": dado["bbox"]["y2"]
        })
        conn.commit()
    except cx_Oracle.DatabaseError as e:
        print("Erro ao salvar dados no banco:", e)

# === CARREGAMENTO DO MODELO ===
model = YOLO("yolov8s.pt")

# === TENTATIVA DE ABRIR A CÂMERA ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao acessar a câmera.")
    sys.exit(1)

print("Pressione 'q' para encerrar")

intervalo_segundos = 5
distancia_minima_movimento = 30
ultimo_registro = time.time()
historico_objetos = {}

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame da câmera.")
            break

        # Inferência + rastreamento
        results = model.track(frame, persist=True, conf=0.5)
        frame_with_boxes = results[0].plot()
        boxes = results[0].boxes

        tempo_atual = time.time()
        if tempo_atual - ultimo_registro >= intervalo_segundos:
            for box in boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]

                if class_name == "motorcycle":
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    obj_id = int(box.id[0]) if box.id is not None else None
                    pos_atual = (center_x, center_y)

                    registrar = False

                    if obj_id is not None:
                        if obj_id not in historico_objetos:
                            registrar = True
                        else:
                            dx = abs(pos_atual[0] - historico_objetos[obj_id][0])
                            dy = abs(pos_atual[1] - historico_objetos[obj_id][1])
                            if dx >= distancia_minima_movimento or dy >= distancia_minima_movimento:
                                registrar = True

                    if registrar:
                        data = {
                            "timestamp": tempo_atual,
                            "object_id": obj_id,
                            "class": class_name,
                            "position": {"x": center_x, "y": center_y},
                            "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
                        }

                        salvar_ou_atualizar_no_banco(data)
                        historico_objetos[obj_id] = pos_atual

            ultimo_registro = tempo_atual

        # Exibe o vídeo com as detecções
        cv2.imshow("Rastreamento de Motos", frame_with_boxes)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Encerrando...")
            break
except Exception as e:
    print("Erro durante execução principal:", e)
finally:
    # Libera todos os recursos mesmo em caso de erro
    cap.release()
    cv2.destroyAllWindows()
    try:
        cursor.close()
        conn.close()
        print("Recursos liberados e conexão encerrada.")
    except Exception as e:
        print("Erro ao encerrar conexão com o banco:", e)
