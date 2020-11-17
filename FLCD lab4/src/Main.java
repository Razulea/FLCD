import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class Main {

    private static Map<String, Runnable> menu;
    private static FA fa;

    public static void main(String[] args) throws Exception {
        fa = new FA("FA.in");
        buildMenu();
        run();


    }

    public static void run() {
        String input;
        Scanner scanner = new Scanner(System.in);
        while (true) {
            input = scanner.nextLine();
            if (input.equals("0")) {
                return;
            } else {
                if(!(input.equals("1")||input.equals("2")||input.equals("3")||input.equals("4")||input.equals("5")||input.equals("6"))) {
                    System.out.println("Wrong command!");
                }
                else {
                    menu.get(input).run();
                }
            }
        }
    }

    public static void buildMenu() {
        menu = new HashMap<>();
        menu.put("1", Main::printStates);
        menu.put("2", Main::printAlphabet);
        menu.put("3", Main::printTransitions);
        menu.put("4", Main::printInitialStates);
        menu.put("5", Main::printFinalStates);
        menu.put("6", Main::readSequence);
        System.out.println(
                "1 - states\n" +
                "2 - alphabet\n" +
                "3 - transitions\n" +
                "4 - initial states\n" +
                "5 - final states\n" +
                "6 - read sequence\n" +
                "0 - exit\n");
    }

    public static void printStates() {
        List<String> states = fa.getStates();
        System.out.println(
                states.stream()
                        .reduce("", (s, t) -> s + " " + t)
        );
    }

    public static void printAlphabet() {
        List<String> alphabet = fa.getAlphabet();
        System.out.println(
                alphabet.stream()
                        .reduce("", (s, t) -> s + " " + t)
        );
    }

    public static void printTransitions() {
        Map<String, List<Pair<String, String>>> transitions = fa.getTransitions();
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, List<Pair<String, String>>> entry : transitions.entrySet()) {
            for (Pair<String, String> p : entry.getValue()) {
                sb.append(entry.getKey()).append(p.getFirst()).append(p.getSecond()).append("\n");
            }
        }
        System.out.println(sb.toString());
    }

    private static void printInitialStates() {
        String initialStates = fa.getInitialState();
        System.out.println(initialStates);
    }

    public static void printFinalStates() {
        List<String> finalStates = fa.getFinalStates();
        System.out.println(
                finalStates.stream()
                        .reduce("", (s, t) -> s + " " + t)
        );
    }

    private static void readSequence(){
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter sequence: ");

        String sequence = scanner.nextLine();
            if(fa.isAccepted(sequence)){
                System.out.println(sequence + " is accepted");
            }
            else {
                System.out.println(sequence + " is not accepted");
            }
    }
}




