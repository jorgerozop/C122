import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

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

                # Verifica si algún DEDO está ABIERTO o CERRADO.
                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        print("FINGER with id ",lm_index," is Open")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        print("FINGER with id ",lm_index," is Closed")

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
    
    # Detecta los puntos de referencia de las manos. 
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
