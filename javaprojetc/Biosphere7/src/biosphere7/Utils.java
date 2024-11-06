package biosphere7;

import java.util.Arrays;
import java.util.stream.Collectors;

/**
 * Quelques fonctions utiles au projet. Vous devez comprendre ce que font ces
 * méthodes (voir leur documentation), mais pas comment elles le font (leur
 * code).
 * 
 * À faire évoluer en fonction des nouvelles natures de case, des nouvelles
 * espèces de plantes, etc.
 */
public class Utils {
    
    /**
     * Caractère pour indiquer une plante possédée par les rouges.
     */
    public final static char CAR_ROUGE = 'R';

    /**
     * Caractère pour indiquer une plante possédée par les bleus.
     */
    public final static char CAR_BLEU = 'B';

    /**
     * Caractère indiquant la nature "Terre" de la case.
     */
    public final static char CAR_TERRE = ' ';

    /**
     * Caractère pour indiquer une case sans plante.
     */
    public final static char CAR_VIDE = ' ';

    /**
     * Caractère pour indiquer une case avec un pommier.
     */
    public final static char CAR_POMMIER = 'P';

    /**
     * Fonction qui renvoie une copie du tableau sans les cases non utilisées,
     * c'est-à-dire contenant null ou la chaîne vide. Par exemple {"Coucou", "",
     * null, "Hello", null} renvoie {"Coucou", "Hello"}.
     *
     * @param actions le tableau à nettoyer
     * @return le tableau nettoyé
     */
    public static String[] nettoyerTableau(final String[] actions) {
        return Arrays.stream(actions)
                .filter(a -> ((a != null) && (!"".equals(a))))
                .collect(Collectors.toList())
                .toArray(new String[0]);
    }

    /**
     * Construit un plateau à partir de sa représentation sour forme texte,
     * comme renvoyé par formatTexte(), avec coordonnées et séparateurs.
     *
     * @param texteOriginal le texte du plateau
     * @return le plateau
     */
    public static Case[][] plateauDepuisTexte(final String texteOriginal) {
        final Case[][] plateau = new Case[Coordonnees.NB_LIGNES][Coordonnees.NB_COLONNES];
        final String[] lignes = texteOriginal.split("\n");
        for (int lig = 0; lig < Coordonnees.NB_LIGNES; lig++) {
            final String ligne1 = lignes[2 * lig + 1];
            final String ligne2 = lignes[2 * lig + 2];
            for (int col = 0; col < Coordonnees.NB_COLONNES; col++) {
                final String codageLigne1 = ligne1.substring(2 + 4 * col, 2 + 4 * col + 3);
                final String codageLigne2 = ligne2.substring(2 + 4 * col, 2 + 4 * col + 3);
                plateau[lig][col] = caseDepuisCodage(codageLigne1, codageLigne2);
            }
        }
        return plateau;
    }

    /**
     * Construit une case depuis son codage.
     *
     * @param ligne1 codage de la case, première ligne
     * @param ligne2 codage de la case, deuxième ligne
     * @return case correspondante
     */
    public static Case caseDepuisCodage(final String ligne1, final String ligne2) {
        // vérification des arguments
        if (ligne1.length() != 3 || ligne2.length() != 3) {
            throw new IllegalArgumentException(
                    "Un codage de ligne doit être sur 3 caractères par ligne.");
        }
        Case laCase = new Case(CAR_VIDE, CAR_ROUGE, 0, CAR_TERRE);
        //
        // ligne 1
        //
        // 1er caractère : nature
        char carNature = ligne1.charAt(0);
        if (carNature == '-') {
            laCase.nature = Utils.CAR_TERRE;
        } else {
            laCase.nature = carNature;
        }
        // 2ème caractère : rien
        // 3ème caractère : rien
        //
        // ligne 2
        //
        // 1er caractère : espèce
        laCase.espece = ligne2.charAt(0);
        // 2ème caractère : couleur
        char carCouleur = ligne2.charAt(1);
        if (laCase.espece == CAR_VIDE) {
            if (carCouleur != CAR_VIDE) {
                throw new IllegalArgumentException("Cette case ne contient pas de plante,"
                        + " donc ne devrait pas avoir de couleur associée.");
            }
        } else {
            if (carCouleur != CAR_BLEU && carCouleur != CAR_ROUGE) {
                throw new IllegalArgumentException(
                        "Caractère couleur non admis : " + carCouleur);
            }
            laCase.couleur = carCouleur;
        }
        // 3ème caractère : vitalité
        char carVitalite = ligne2.charAt(2);
        if (laCase.espece == CAR_VIDE) {
            if (carVitalite != CAR_VIDE) {
                throw new IllegalArgumentException("Cette case ne contient pas de plante,"
                        + " donc ne devrait pas avoir de vitalité associée.");
            }
            laCase.vitalite = 0;
        } else {
            laCase.vitalite = Integer.parseInt("" + carVitalite);
        }
        return laCase;
    }

    /**
     * Afficher les action possibles déjà calculées.
     *
     * @param actionsPossibles les actions possibles calculées
     */
    static void afficherActionsPossibles(String[] actionsPossibles) {
        System.out.println(Arrays.deepToString(actionsPossibles));
    }

    /**
     * Indique si une action est présente parmi les actions possibles calculées.
     *
     * @param actionsPossibles actions possibles calculées
     * @param action l'action à tester
     * @return vrai ssi l'action est présente parmi les actions possibles
     */
    static boolean actionsPossiblesContient(String[] actionsPossibles,
            String action) {
        return Arrays.asList(actionsPossibles).contains(action);
    }
}
