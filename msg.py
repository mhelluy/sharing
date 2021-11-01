import socket
import threading
import sys

IP = "10.0.1.1"
PORT = 2548

if sys.argv[1] == "server":
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cs.bind((IP, PORT))
    cs.listen(5)
    cc, info = cs.accept()  # on attend une connection client
elif sys.argv[1] == "client":
    cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cc.connect((IP, PORT))
else:
    print("Invalid argument : {}".format(sys.argv[1]))
    exit()

active = True


# les deux fonctions sendThread et recvThread sont lancées en parallèle grâce au module threading
# ainsi, le programme peut gérer simultanément l'envoi et la réception de messages
def recvThread():
    global active #le mot clef 'global' permet la modification de la variable dans la fonction
    while active:
        resp = cc.recv(1024).decode() # le message reçu est de type "bytes" que l'on convertit en "string" avec .decode()
        if resp == "STOP":
            print("\n Signal d'arrêt reçu.")
            active = False
        else:
            print("\n Vous avez reçu : {}\nMessage : ".format(resp), end='')


def sendThread():
    global active
    while active:
        msg = input("Message : ")
        cc.send(msg.encode())
        if msg == "STOP":
            active = False


th1 = threading.Thread(target=recvThread)
th1.daemon = True
th1.start()  # on lance le thread qui gère la réception

th2 = threading.Thread(target=sendThread)
th2.daemon = True
th2.start()  # on lance parallèlement le thread qui gère l'envoi

while active:
    # tant que la communication est active, le programme ne s'arrête pas (pendant ce temps, les deux threads tournent)
    pass
cc.close()  # on ferme la connexion
if sys.argv[1] == "server":
    cs.close()  # on ferme le serveur si le programme en a ouvert un
sys.exit()  # fermeture de tous les threads
