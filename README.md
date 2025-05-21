
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

  ### InstantClient

  Mais abaixo haverá um Link para baixar o mesmo e aqui mostrarei como configurar ele:

   - Após baixar o arquivo ele virá como formato .zip para seus downloads, crie uma pasta no seu disco C e extraia tudo do zip para a mesma:
     ![Captura de tela 2025-05-21 143755](https://github.com/user-attachments/assets/f17ba147-b9bb-46b3-b11e-9205697607f2)

     ![Captura de tela 2025-05-21 143958](https://github.com/user-attachments/assets/fbce81db-4ff8-4694-9e59-a84763141585)

     ![Captura de tela 2025-05-21 144146](https://github.com/user-attachments/assets/6904b789-174f-4252-a82a-c0c57e6bbace)


  - Após isso copie o caminho do diretório e abra as variáveis de ambiente do sistema:
  
  ![Captura de tela 2025-05-21 144340](https://github.com/user-attachments/assets/96cb6d8e-6ab9-4281-80f9-3ced7843d98f)

  ![image](https://github.com/user-attachments/assets/01654f8e-1edd-4cfc-a3a9-29d7c5a6b61b)
  
  ![Captura de tela 2025-05-21 144454](https://github.com/user-attachments/assets/e850c426-77c3-43d0-9d72-edc319a9c1f6)

  - Dentro das variáveis procure nas variáveis de sistema uma variável chamada Path, clique nela e depois em editar, lá dentro clique em novo e cole o caminho do seu instant_client
 
  ![Captura de tela 2025-05-21 144454](https://github.com/user-attachments/assets/b3a255b0-ee66-4afb-86c1-b205f56905c6)

  ![Captura de tela 2025-05-21 144653](https://github.com/user-attachments/assets/a98e7659-a66d-467c-9223-32ef909d9a31)

  ![Captura de tela 2025-05-21 144740](https://github.com/user-attachments/assets/aa426345-bc93-4358-b8bd-9ab3cb15da3f)

  - Após isso basta clicar em ok, aplicar e estará tudo certo
 
  OBS: CASO NÃO FUNCIONE EXISTE UMA PATH TAMBÉM NAS VARIÁVEIS DE USUÁRIO, VOCÊ PODE ADICIONAR NELAS TAMBÉM POR VIA DAS DÚVIDAS!!!

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
- Utilize seu usuário e senha do Oracle.

---

## Utilização

 - Basta pegar uma imagem ou vídeo qualquer que contenha uma moto e apontar para sua câmera que a mágica já será feita.
 - Garanta de ter a tabela no banco de dados criada utilizando o script que está dentro do projeto.

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

## Resultados

 - Detecção de motos:

   ![Captura de tela 2025-05-21 142307](https://github.com/user-attachments/assets/43eff66a-d8a7-4775-873c-3b232245e513)


- Resultados no banco de dados:

  ![Captura de tela 2025-05-21 142323](https://github.com/user-attachments/assets/c8bc6737-afa8-49b2-a2a3-8c6ead432763)

---
## Links

 - Vídeo do youtube mostrando a aplicação: https://youtu.be/1uLmbTtyB0w
 - Link para baixar o InstaClient(Necessário para fazer o banco de dados rodar): https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html

   

