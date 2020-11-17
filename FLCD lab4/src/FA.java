import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

public class FA {

    private final List<String> states;
    private final List<String> alphabet;
    private final Map<String, List<Pair<String, String>>> transitions;
    private final String initialState;
    private final List<String> finalStates;

    public FA(String inputFile) throws IOException {
        states = new ArrayList<>();
        alphabet = new ArrayList<>();
        transitions = new HashMap<>();
        finalStates = new ArrayList<>();

        BufferedReader reader = new BufferedReader(new FileReader(new File(inputFile)));
        String line = reader.readLine();
        states.addAll(Arrays.asList(line.split(" ")));
        for (String state : states) {
            transitions.put(state, new ArrayList<>());
        }
        line = reader.readLine();
        alphabet.addAll(Arrays.asList(line.split(" ")));

        initialState = reader.readLine();

        line = reader.readLine();
        finalStates.addAll(Arrays.asList(line.split(" ")));

        line = reader.readLine();
        while (line != null) {
            String[] parts = line.split(" ");
            String sourceState = parts[0];
            String destinationsState = parts[parts.length - 1];
            for (String transition : Arrays.asList(parts).subList(1, parts.length - 1)) {
                transitions.get(sourceState).add(new Pair<>(transition, destinationsState));
            }
            line = reader.readLine();
        }
    }

    public List<String> getStates() {
        return states;
    }

    public List<String> getAlphabet() {
        return alphabet;
    }

    public Map<String, List<Pair<String, String>>> getTransitions() {
        return transitions;
    }

    public String getInitialState() {
        return initialState;
    }

    public List<String> getFinalStates() {
        return finalStates;
    }

    public boolean isDeterministic() {
        for (String state : states) {
            List<Pair<String, String>> trans = transitions.get(state);
            List<String> uniqueTrans = trans.stream()
                    .map(Pair::getFirst)
                    .distinct()
                    .collect(Collectors.toList());
            if (trans.size() != uniqueTrans.size()) {
                return false;
            }
        }
        return true;
    }

    public boolean isAccepted(String sequence){
        String currentState = initialState;
        while (!sequence.isEmpty()) {
            List<Pair<String, String>> trans = transitions.get(currentState);
            String firstChar = String.valueOf(sequence.charAt(0));
            Optional<String> nextState = trans.stream()
                    .filter(p -> p.getFirst().equals(firstChar))
                    .map(Pair::getSecond)
                    .findFirst();
            if (nextState.isEmpty()) {
                return false;
            } else {
                currentState = nextState.get();
            }
            sequence = sequence.substring(1);
        }
        return finalStates.contains(currentState);
    }

    @Override
    public String toString() {
        return "FA{" +
                ", states=" + states +
                ", alphabet=" + alphabet +
                ", transitions=" + transitions +
                ", initialState='" + initialState + '\'' +
                ", finalStates=" + finalStates +
                '}';
    }

}
