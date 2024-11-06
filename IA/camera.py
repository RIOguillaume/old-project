import time
import cv2
import numpy as np

cap = cv2.VideoCapture(1)


def image_to_white_line(image_to_line, threshold1=25, threshold2=150):
    return cv2.Canny(image_to_line, threshold1, threshold2, apertureSize=3)


def contour(image_to_outline):
    gray_image = image_to_gray(image_to_outline)
    ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    with_contours = cv2.drawContours(image_to_outline, contours, -1, (0, 255, 0), 3)
    return with_contours

#
#Cette fonction va déterminer 20 points importants sur l'image et les coordonnées des pounts et l'image
#avec les points affichées
#
def points_important(image_for_point):
    img = filtre_noir(image_for_point)
    gray_image = image_to_gray(img)
    orb = cv2.ORB_create(20)
    keypoint, des = orb.detectAndCompute(gray_image, None)
    pts = cv2.KeyPoint_convert(keypoint)
    img_final = cv2.drawKeypoints(image_for_point, keypoint, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return img_final, pts

def image_to_gray(image_to_change):
    return cv2.cvtColor(image_to_change, cv2.COLOR_BGR2GRAY)


def resize(img, scale_percent):
    # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def initialisation_camera(cap):
    print("Initialisation de la caméra :")
    if not (cap.isOpened()):
        print("Could not open video device")
    print("Initialisation terminé :")
    result, image_read = cap.read()
    time.sleep(1)
    result, image_read = cap.read()

    if result:
        print("image detected")
        time.sleep(0.5)
        return image_read
    else:
        print("No image detected. Please! try again")
        exit(0)


def save_image(image):
    cv2.imwrite("myCurrentPicture.jpg", image)
    time.sleep(0.5)
    print("image saved")
    return True


def reduire_bruit(img_blur):
    return cv2.GaussianBlur(img_blur, (3, 3), 0)


def isoler_groupe_line_vertical(image, threshold1=100, threshold2=25, threshold3=150, rho=1, pi=np.pi / 180):
    gray_image = image_to_gray(image)
    image_blur = reduire_bruit(gray_image)
    edges = image_to_white_line(image_blur, threshold2, threshold3)

    max_line_distance = 10
    max_line_angle = 0.100
    line_groups = []

    # Détecter les droites dans l'image en utilisant la transformée de Hough
    lines = cv2.HoughLines(edges, rho=rho, theta=pi, threshold=threshold1)
    # Erreur pas de line détecté on retourne donc -1
    if lines is None:
        return -1
    # Parcourir toutes les droites détectées et filtrer les droites ayant un angle proche de 0 ou 180 degrés
    for line in lines:
        rho, theta = line[0]
        angle = theta * 180 / np.pi
        if (angle < 10) or (angle > 170):
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            # Chercher si la ligne appartient à un groupe existant
            found_group = False
            for group in line_groups:
                # Vérifier si la ligne est suffisamment proche et a une orientation similaire à celles du groupe
                if abs(angle - group["angle"]) <= max_line_angle and \
                        min(abs(x1 - group["x1"]), abs(x1 - group["x2"]), abs(x2 - group["x1"]),
                            abs(x2 - group["x2"])) <= max_line_distance and \
                        min(abs(y1 - group["y1"]), abs(y1 - group["y2"]), abs(y2 - group["y1"]),
                            abs(y2 - group["y2"])) <= max_line_distance:
                    # Ajouter la ligne au groupe existant
                    group["lines"].append(line)
                    group["x1"] = min(group["x1"], x1, x2)
                    group["y1"] = min(group["y1"], y1, y2)
                    group["x2"] = max(group["x2"], x1, x2)
                    group["y2"] = max(group["y2"], y1, y2)
                    group["angle"] = (group["angle"] * len(group["lines"]) + angle) / (len(group["lines"]) + 1)
                    found_group = True
                    break
            # Si la ligne n'appartient à aucun groupe existant, créer un nouveau groupe pour la ligne
            if not found_group:
                line_groups.append({
                    "lines": [line],
                    "x1": min(x1, x2),
                    "y1": min(y1, y2),
                    "x2": max(x1, x2),
                    "y2": max(y1, y2),
                    "angle": angle
                })
    # Supprimer les groupes qui ne contiennent qu'une seule ligne

    line_groups = [group for group in line_groups if len(group["lines"]) > 1]

    lines_to_return = []
    for group in line_groups:
        for line in group["lines"]:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            lines_to_return.append((x1, y1, x2, y2))
            break
    return lines_to_return


def filtre_orange(img):
    # Convertir l'image en float pour le traitement
    img_float = np.float32(img) / 255.0

    # Convertir l'image en espace colorimétrique HSV
    img_hsv = cv2.cvtColor(img_float, cv2.COLOR_RGB2HSV)

    # Définir les bornes de la couleur orange en HSV
    orange_min = np.array([215, 0, 0], np.uint8)
    orange_max = np.array([230, 255, 255], np.uint8)

    # Filtrer l'image pour ne garder que la couleur orange
    mask = cv2.inRange(img_hsv, orange_min, orange_max)

    # Appliquer le masque à l'image d'origine
    result = cv2.bitwise_and(img, img, mask=mask)
    return result


def filtre_noir(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mask = cv2.inRange(gray_img, 0, 60)

    # Appliquer le masque sur l'image pour ne garder que les pixels noirs
    result = cv2.bitwise_and(img, img, mask=mask)

    return result


def detect_door(image):
    img = filtre_orange(image)

    gray_image = image_to_gray(img)

    ret, thresh = cv2.threshold(gray_image, 0, 200, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.f(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #obtenir la plus grande aire
    cpt = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            approx = cv2.approxPolyDP(cnt,0.009 * cv2.arcLength(cnt, True), True)
            cv2.drawContours(image, [approx], 0, (255, 255, 255), 2)
            cpt += 1

    return cpt > 0


def zoom_max_aire(image):
    img = filtre_orange(image)

    gray_image = image_to_gray(img)

    ret, thresh = cv2.threshold(gray_image, 0, 200, cv2.THRESH_BINARY)

    # Trouver les contours dans l'image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sélectionner le plus grand contour
    cnt = max(contours, key=cv2.contourArea)

    # Obtenir les coordonnées du rectangle englobant
    x, y, w, h = cv2.boundingRect(cnt)

    # Recadrer l'image en utilisant les coordonnées du rectangle englobant
    cropped_image = image[y:y + h, x:x + w]

    # Redimensionner l'image recadrée pour l'agrandir
    coord = (x, y, w, h)

    # Afficher l'image agrandie
    return coord, cropped_image


def get_rotation_middle(coord,image):
    hauteur, largeur, nb_channels = image.shape
    x, y, w, h = coord

    #ligne au milieu
    point_milieu_bas = (int(largeur/2), 0)
    point_milieu_haut = (int(largeur/2), hauteur)
    couleur = (125, 0, 125)
    epaisseur = 2
    cv2.line(image, point_milieu_bas, point_milieu_haut, couleur, epaisseur)

    # ligne au milieu
    point_porte_bas = (x + int(w/2), y)
    point_porte_haut = (x + int(w/2), y + h)
    couleur = (255, 255, 0)
    cv2.line(image, point_porte_bas, point_porte_haut, couleur, epaisseur)

    # espace entre les deux lignes
    x_espace = point_milieu_bas[0] - point_porte_bas[0]
    point_espace_bas = (point_porte_bas[0], int(hauteur/2))
    point_espace_haut = (point_porte_bas[0] + x_espace, int(hauteur/2))
    couleur = (255, 255, 0)
    cv2.line(image, point_espace_bas, point_espace_haut, couleur, epaisseur)

    if x_espace > 0:
        return -1, x_espace
        #("gauche de ", x_espace, "pixels")
    elif x_espace < 0:
        return 1, x_espace
        #("droite de ", x_espace, "pixels")
    else:
        return 0, x_espace
        #("tout droit")


def detect_handle(coord, pts, image):
    x_moy = 0
    y_moy = 0
    x, y, w, h = coord
    if len(pts > 0):
        for point in pts:
            x_moy += point[0]
            y_moy += point[1]
        x_moy = int(x_moy/len(pts))
        y_moy = int(y_moy/len(pts))

    #point milieux de la porte:
    point_milieux_poingne = (x_moy+x, y_moy+y)

    #point pour dessiner carré
    point_poingne_start = (x_moy+x-10, y_moy+y-40)
    point_poingne_end = (x_moy+x+10, y_moy+y+40)
    couleur = (225, 0, 0)
    epaisseur = 2
    cv2.rectangle(image, point_poingne_start, point_poingne_end, couleur, epaisseur)

    return image, point_milieux_poingne


while True:
    #image = initialisation_camera(cap)
    #save_image(image)
    #image = cv2.imread("DoorIA/porte/porte.jpg")

    image = cv2.imread("myCurrentPicture.jpg")

    image_resize = resize(image, 120)


    first_image = image_resize.copy()

    TH1 = 85
    TH2 = 50
    TH3 = 100
    RHO = 0.5
    THETA = np.pi/2048

    # isoler les lignes verticales afin d'aider la réconnaissance de porte
    # on dessine les lignes sur image_resize
    line_to_draw = isoler_groupe_line_vertical(image_resize, TH1, TH2, TH3, RHO, THETA)
    for line in line_to_draw:
        x1, y1, x2, y2 = line
        cv2.line(image_resize, (x1, y1), (x2, y2), (0, 0, 0), 2)


    # détection de la porte, si on détecte une porte on va faire notre analyse
    if detect_door(image_resize):
        # on zoom sur la porte et on garde les coordonées dans l'image monde
        coord, cropped_image = zoom_max_aire(image_resize)
        # on récupère tous les points d'importance de l'image (pour rechercher la poingné)
        image, pts = points_important(cropped_image)

        cv2.imshow("image", image)
        cv2.waitKey(0)

        image, coord_pts_middle = detect_handle(coord, pts, image_resize)

        rot, x_value = get_rotation_middle(coord, image_resize)
        if rot > 0:
            print("gauche de ", x_value, "pixels")
        elif rot < 0:
            print("droite de ", x_value, "pixels")
        else:
            print("tout droit")

    cv2.imshow("image", image_resize)
    cv2.waitKey(0)

    # fermer si on press q
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


    # Afficher l'image avec les droites verticales filtrées
    cv2.waitKey(0)
    cv2.destroyAllWindows()


