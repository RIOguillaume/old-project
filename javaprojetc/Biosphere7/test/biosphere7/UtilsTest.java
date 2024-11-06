package biosphere7;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests sur la classe Utils.
 */
public class UtilsTest {

    /**
     * Test de la fonction caseDepuisCodage.
     */
    @Test
    public void testCaseDepuisCodage() {
        Case laCase;
        // case vide
        laCase = Utils.caseDepuisCodage("---", "   ");
        assertEquals(Utils.CAR_TERRE, laCase.nature);
        assertEquals(Utils.CAR_VIDE, laCase.espece);
        // un pommier possédé par les rouges
        laCase = Utils.caseDepuisCodage("---", "PR4");
        assertEquals(Utils.CAR_TERRE, laCase.nature);
        assertEquals(Utils.CAR_POMMIER, laCase.espece);
        assertEquals(Utils.CAR_ROUGE, laCase.couleur);
        assertEquals(4, laCase.vitalite);
        // un pommier possédé par les bleus
        laCase = Utils.caseDepuisCodage("---", "PB9");
        assertEquals(Utils.CAR_TERRE, laCase.nature);
        assertEquals(Utils.CAR_POMMIER, laCase.espece);
        assertEquals(Utils.CAR_BLEU, laCase.couleur);
        assertEquals(9, laCase.vitalite);
    }

    /**
     * Test de la fonction plateauDepuisTexte().
     */
    @Test
    public void testPlateauDepuisTexte() {
        Case[][] plateau = Utils.plateauDepuisTexte(PLATEAU1);
        Case laCase;
        // une case avec un pommier bleu
        laCase = plateau[0][0];
        assertEquals(Utils.CAR_TERRE, laCase.nature);
        assertEquals(Utils.CAR_POMMIER, laCase.espece);
        assertEquals(Utils.CAR_BLEU, laCase.couleur);
        assertEquals(4, laCase.vitalite);
        // une case avec un pommier rouge
        laCase = plateau[13][13];
        assertEquals(Utils.CAR_TERRE, laCase.nature);
        assertEquals(Utils.CAR_POMMIER, laCase.espece);
        assertEquals(Utils.CAR_ROUGE, laCase.couleur);
        assertEquals(1, laCase.vitalite);
        // une case vide
        laCase = plateau[0][1];
        assertEquals(Utils.CAR_TERRE, laCase.nature);
        assertEquals(Utils.CAR_VIDE, laCase.espece);
    }

    /**
     * Test de la fonction nettoyerTableau().
     */
    @Test
    public void testNettoyerTableau() {

        String tab[], tabNettoye[];

        // tableau de taille 0
        tab = new String[0];
        tabNettoye = Utils.nettoyerTableau(tab);
        assertEquals(0, tabNettoye.length);

        // tableau de taille 1 avec 1 élément
        tab = new String[1];
        tab[0] = "coucou";
        tabNettoye = Utils.nettoyerTableau(tab);
        assertEquals(1, tabNettoye.length);
        assertEquals("coucou", tabNettoye[0]);

        // tableau de taille 1 avec 0 élément (null)
        tab = new String[1];
        tab[0] = null;
        tabNettoye = Utils.nettoyerTableau(tab);
        assertEquals(0, tabNettoye.length);

        // tableau de taille 1 avec 0 élément ("")
        tab = new String[1];
        tab[0] = "";
        tabNettoye = Utils.nettoyerTableau(tab);
        assertEquals(0, tabNettoye.length);

        // tableau de taille 2 avec 1 élément ("")
        tab = new String[2];
        tab[0] = "";
        tab[1] = "hello";
        tabNettoye = Utils.nettoyerTableau(tab);
        assertEquals(1, tabNettoye.length);
        assertEquals("hello", tabNettoye[0]);

        // un cas plus complet
        tab = new String[7];
        tab[0] = "";
        tab[1] = "hello";
        tab[2] = null;
        tab[3] = "";
        tab[4] = "hello";
        tab[5] = "";
        tab[6] = null;
        tabNettoye = Utils.nettoyerTableau(tab);
        assertEquals(2, tabNettoye.length);
        assertEquals("hello", tabNettoye[0]);
        assertEquals("hello", tabNettoye[1]);
    }

    final String PLATEAU1
            = "   A   B   C   D   E   F   G   H   I   J   K   L   M   N \n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "a|PB4|   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "b|PR9|   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "c|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "d|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "e|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "f|   |PR3|   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "g|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "h|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "i|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "j|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "k|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "l|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "m|   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            + "n|   |   |   |   |   |   |   |   |   |   |   |   |   |PR1|\n"
            + " +---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n";
}
