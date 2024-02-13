# Importando librerías y mediapipe sirve para la gestión y detección de manos.
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
# Variable para almacenar los datos de las manos.
mp_drawing = mp.solutions.drawing_utils
# Parámetros para la detección de los dedos de la mano.
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
# Almacena los valores de las puntas de los dedos
tipIds = [4, 8, 12, 16, 20]

# Define una función para contar los dedos.

def countFingers(image, hand_landmarks, handNo=0):
    
    if hand_landmarks:
        # Obtén todos los puntos de referencia de la PRIMERA mano VISIBLE.
        landmarks = hand_landmarks[handNo].landmark
        # imprime (landmarks).

        # Cuenta los dedos.        
        fingers = []

        for lm_index in tipIds:
                # Obtén los valores y de la punta de los dedos y la parte inferior.
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y
                
                # Obtén los valores y de la punta del pulgar y la parte inferior.
                thumb_tip_x = landmarks[lm_index].x
                thumb_bottom_x = landmarks[lm_index - 2].x

                # Verifica si algún DEDO está ABIERTO o CERRADO.
                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        print("DEDO con id ",lm_index," está abierto")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        print("DEDO con id ",lm_index," está cerrado")
                else:
                    if thumb_tip_x > thumb_bottom_x:
                        fingers.append(1)
                        print("PULGAR está abierto")

                    if thumb_tip_x < thumb_bottom_x:
                        fingers.append(0)
                        print("PULGAR está cerrado")


        # imprime (fingers)
        totalFingers = fingers.count(1)

        # Muestra el texto.
        text = f'Fingers: {totalFingers}'

        cv2.putText(image, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

# Define una función para 
def drawHandLanmarks(image, hand_landmarks):

    # Dibuja conexiones entre los puntos de referencia.
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Pasa la información de lo detectado por el video.
    results = hands.process(image)

    # Obtén la posición de los puntos de referencia del resultado procesado.
    hand_landmarks = results.multi_hand_landmarks

    # Dibuja los puntos de referencia.
    drawHandLanmarks(image, hand_landmarks)

    # Obtén las posiciones de los dedos de la mano.       
    countFingers(image, hand_landmarks)

    cv2.imshow("Controlador de medios", image)

    # Cierra la ventana al presionar la barra espaciadora.
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
