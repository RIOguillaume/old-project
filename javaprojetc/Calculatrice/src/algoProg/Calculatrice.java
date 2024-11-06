package algoProg;

/**
 * Une calculatrice sur les entiers, saisis au clavier.
 */
class Calculatrice {

    /**
     * Lire un entier saisi par l'utilisateur. Vous n'avez pas à comprendre ce
     * code.
     *
     * @return l'entier saisi
     */
    static int lireUnEntier() {
        java.util.Scanner sc = new java.util.Scanner(System.in);
        int entierSaisi = 0;
        boolean saisieCorrecte = false;
        do {
            try {
                System.out.print("Entrez un nombre : ");
                entierSaisi = sc.nextInt();
                saisieCorrecte = true;
            } catch (java.util.InputMismatchException e) {
                System.err.println("Saisie incorrecte, saisissez un entier.");
                sc.next();
            }
        } while (!saisieCorrecte);
        return entierSaisi;
    }

    /**
     * Lire un opérateur arithmétique saisi par l'utilisateur. Vous n'avez pas à
     * comprendre ce code.
     *
     * @return l'opérateur saisi
     */
    static char lireUnOperateur() {
        java.util.Scanner sc = new java.util.Scanner(System.in);
        char operateurSaisi = ' ';
        boolean saisieCorrecte = false;
        do {
            try {
                System.out.print("Entrez un opérateur : ");
                String saisie = sc.next();
                operateurSaisi = saisie.charAt(0);
                if (saisie.length() == 1 && symboleOperationValide(operateurSaisi)) {
                    saisieCorrecte = true;
                }
            } catch (java.util.InputMismatchException e) {
                // traité via le booléen
            }
            if (!saisieCorrecte) {
                System.err.println("Saisie incorrecte, saisissez un opérateur.");
            }
        } while (!saisieCorrecte);
        return operateurSaisi;
    }

    /**
     * Effectuer une opération arithmétique sur les entiers.
     * 
     * @param a le premier opérande
     * @param b le second opérande
     * @param op l'opérateur
     * @return le résultat de l'opération arithmétique
     */
    static int calculer(int a, int b, char op) {
int resultat;
switch (op) {
case '+':
resultat = a + b;
break;
case '-':
resultat =  b - a;
break;
            case '*':
            resultat = a * b;
            break;
            case '%':
            resultat = a % b;
            break;
            case '/':
            resultat = a / b;
            break;
            default:
            resultat = 0;
            System.out.println("Opérateur non valide");
            }
return resultat;
    }

    /**
     * Vérifier qu'un caractère est celui d'un opérateur.
     * 
     * @param op le caractère en question
     * @return vrai ssi ce caractère est celui d'un opérateur
     */
    static boolean symboleOperationValide(char op) {
        return op=='+' || op=='-' || op=='*' || op=='/';
    }

    /**
     * Tests unitaires de la fonction symboleOperationValide.
     */
    static void testSymboleOperationValide() {
        assert(symboleOperationValide('+'));
        assert(symboleOperationValide('-'));
        assert(symboleOperationValide('*'));
        assert(symboleOperationValide('%'));
        assert(symboleOperationValide('/'));
        assert(!symboleOperationValide('='));
    }

    /**
     * Tests unitaires de la fonction calculer.
     */
    static void testCalculer() {
        assert(calculer(3, 5, '+') == 8);
        assert(calculer(3, 5, '-') == -2);
        assert(calculer(3, 5, '*') == 15);
        assert(calculer(12, 2, '%') == 0);
        assert(calculer(12, 2, '/') == 6);
    }

    /**
     * Lancement de tous les tests unitaires.
     */
    static void lancerTests() {
      System.out.println("Début des tests...");

   testSymboleOperationValide();
        testCalculer();
        System.out.println("Tests terminés avec succès");

    }

    /**
     * Lancement de la calculatrice.
     */
    static void lancerCalculatrice() {
        int premierNombre = lireUnEntier();
        char symboleOperation = lireUnOperateur();
        int secondNombre = lireUnEntier();

        System.out.print("" + premierNombre + symboleOperation + secondNombre);
        System.out.println("=" + calculer(premierNombre, secondNombre, symboleOperation));
    }

    /**
     * @param args the command line arguments
     */
public 
static 
void main(String[] args) {
//lancerTests();
lancerCalculatrice();
}

}
