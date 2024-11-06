package biosphere7;

/**
 * Case du plateau.
 * 
 * VOUS NE DEVEZ PAS MODIFIER CE FICHIER.
 */
public final class Case {

    /**
     * Indique l'espèce de la plante se trouvant sur cette case. 
     * L'absence de plante est indiquée par le caractère Utils.CAR_VIDE.
     */
    char espece;
    
    /**
     * Indique la couleur du propriétaire de la plante sur cette case (s'il y en
     * a une).
     * Convention : 'R' pour rouge, 'B' pour bleu.
     */
    char couleur;
    
    /**
     * Vitalité de la plante, le cas échéant.
     */
    int vitalite;
    
    /**
     * Nature d'une case.
     */
    char nature;

    /**
     * Constructeur d'une case.
     * 
     * @param uneEspece espèce de la plante sur la case
     * @param uneCouleur couleur du propriétaire de la plante sur cette case
     * @param uneVitalite vitalité de la plante sur cette case
     * @param uneNature nature de la case
     */
    public Case(char uneEspece, char uneCouleur, int uneVitalite,
            char uneNature) {
        this.espece = uneEspece;
        this.couleur = uneCouleur;
        this.vitalite = uneVitalite;
        this.nature = uneNature;
    }    
}
