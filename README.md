
# 📍 GeoMottu - Detecção e Rastreamento de Motos com YOLOv8 e Oracle

O projeto **GeoMottu** tem como objetivo detectar e rastrear motos em tempo real utilizando visão computacional com o modelo YOLOv8. As informações de localização e bounding boxes são armazenadas em um banco de dados Oracle para análise e persistência histórica.

---

## 🚀 Funcionalidades

- Detecção em tempo real de motos usando webcam ou vídeos.
- Rastreamento com IDs únicos para cada moto.
- Armazenamento automático das informações de localização no banco Oracle.
- Verificação de movimentação mínima para evitar registros duplicados.
- Tratamento de exceções para robustez em produção.

---

## 📦 Bibliotecas Utilizadas

- **[Ultralytics](https://github.com/ultralytics/ultralytics)** (`ultralytics`): Framework moderno para usar modelos YOLO (You Only Look Once), usado aqui para detecção e rastreamento.
- **OpenCV** (`opencv-python`): Usado para capturar vídeo, desenhar bounding boxes e exibir frames processados.
- **cx_Oracle**: Biblioteca de conexão com o banco de dados Oracle.
- **Pandas**: Dependência comum para manipulação de dados (pode ser usada para futuras análises, embora não esteja ativa neste script).

---

## ⚙️ Pré-requisitos

- Python 3.8 ou superior
- Oracle Client instalado (para uso do `cx_Oracle`)
- Webcam
- Acesso ao banco Oracle FIAP (com usuário/senha válidos)

---

## 🛠️ Instruções de Execução

### 1. Criar o ambiente virtual

```bash
python -m venv venv
```

### 2. Ativar o ambiente virtual

- **Windows:**
```bash
venv\Scripts\activate
```

- **Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install ultralytics opencv-python cx_Oracle pandas
```

### 4. Executar o script

```bash
python GeoMottu.py
```

Ou use o botão de **play** no PyCharm.

---

## 📋 Observações

- Certifique-se de estar no diretório correto antes de rodar os comandos.
- O script salva no banco de dados a cada 5 segundos **apenas se** a moto tiver se movido uma distância mínima (30 pixels).
- A detecção é feita apenas para a classe `motorcycle`.
- Os dados salvos incluem: ID do objeto, timestamp, classe, posição central, e coordenadas do bounding box.

---

## 💾 Exemplo de Registro no Banco

A tabela `MOTOS_LOCALIZADAS` recebe os seguintes dados:

| Campo           | Descrição                        |
|----------------|----------------------------------|
| OBJECT_ID      | ID único da moto rastreada       |
| TIMESTAMP_REG  | Data/hora da detecção            |
| CLASSE         | Nome da classe detectada         |
| POS_X / POS_Y  | Coordenadas centrais da moto     |
| X1, Y1, X2, Y2  | Bounding box completo da moto    |

---
