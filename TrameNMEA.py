import folium

def system(data):
# Retourne le type de système de géolocalisation

    type_trame = data[1 : 3]
    if type_trame == "BD" or type_trame == "GB" : type_signal = "BEIDOU"
    elif type_trame == "GA" : type_signal = "GALILEO"
    elif type_trame == "GP" : type_signal = "GPS"
    elif type_trame == "GL" : type_signal = "GLONASS"
    elif type_trame == "GN" : type_signal = "GPS et GLONASS"

    return type_signal

# Entrez les 6 premiers champs de la trame
trame="$GPGGA,123519,4852.1224,N,00218.5990,E,1,08,0.9,545.4,M,46.9,M, , *42"

type_signal = system(trame)
print('Le système de géolocalisation est de type', type_signal)

Champs=trame.split(",")

# Affiche l'horaire et les coordonnées
print('Horaire : ', Champs[1])
print('Latitude : ', Champs[2], Champs[3])
print('Longitude : ', Champs[4],Champs[5])

# Affiche la carte dans un navigateur

def convertir(dms,direction="N"):
    """Conversion de coordonnées au format degrés minutes secondes au format degré décimal"""
    dms = dms.split(".")
    deg_dec = int(dms[0][:-2]) + int(dms[0][-2:])/60 + float(dms[1][:2]+"."+dms[1][2:])/3600
    if direction in ["N", "E"]:
        return deg_dec
    else:
        return -1*deg_dec

latitude = convertir(Champs[2],Champs[3])
longitude = convertir(Champs[4],Champs[5])

carte = folium.Map(location=[latitude,longitude],zoom_start=20)
carte.save("carte.html")
        
