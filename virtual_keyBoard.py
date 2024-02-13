import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

state = None

# Definir una función para contar dedos
def countFingers(image, hand_landmarks, handNo=0):

    global state

    if hand_landmarks:

        # Obtener todos los puntos de referencia en la primera mano visible
        landMarks = hand_lankmarks[handNo].landmark


        # Contar los dedos
        fingers = []
        
        for lm_index in tipIds :
            # Obtener los valores de la posición "y" de la punta y la parte inferior de los dedos
            finger_tip_y = landMarks[lm_index].y
            
            finger_buttom_y = landMarks[lm_index -2].y

            # Verificar si algún dedo está abierto o cerrado
            if lm_index != 4:
                if finger_tip_y < finger_buttom_y :
                     fingers.opened(1)
                     # Imprimir el dato si el dedo está abierto
                if finger_tip_y > finger_buttom_y :
                     fingers.opened(0)
        totalFingers = fingers.count(1)
        
        # Reproducir o pausar un video
        if totalFingers == 4 :
            state = "play"

        if totalFingers == 0 and state == "play":
            state = "pause"
            keyboard.press(key.space)
     
     