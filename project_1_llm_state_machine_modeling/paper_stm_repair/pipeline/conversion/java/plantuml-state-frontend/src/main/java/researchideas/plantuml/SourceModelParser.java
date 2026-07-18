package researchideas.plantuml;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

final class SourceModelParser {
    private static final Pattern ARROW = Pattern.compile("-(?:left|right|up|down)->|-->|->", Pattern.CASE_INSENSITIVE);
    private static final Pattern STATE = Pattern.compile(
            "^state\\s+(?:\"([^\"]+)\"\\s+as\\s+([A-Za-z_][A-Za-z0-9_]*)|([^\\s:{]+))(.*)$",
            Pattern.CASE_INSENSITIVE);
    private static final Pattern STM_BLOCK = Pattern.compile("^stm\\s+(.+?)\\s*\\{\\s*$", Pattern.CASE_INSENSITIVE);
    private static final Pattern STM_HEADING = Pattern.compile("^stm\\s+(.+?)\\s*$", Pattern.CASE_INSENSITIVE);
    private static final Pattern FORK_JOIN = Pattern.compile(
            "^(fork|join)\\s+([A-Za-z_][A-Za-z0-9_]*)\\s*$", Pattern.CASE_INSENSITIVE);
    private static final Pattern LIFECYCLE = Pattern.compile(
            "^(entry|enter|do|during|exit)\\s*/\\s*(.+)$", Pattern.CASE_INSENSITIVE);
    private static final Pattern PRESENTATION = Pattern.compile(
            "^(?:note\\b|legend\\b|end\\s*legend\\b|title\\b|skinparam\\b|hide\\b|show\\b|scale\\b|left\\s+to\\s+right\\s+direction\\b)",
            Pattern.CASE_INSENSITIVE);

    private static final class StateNode {
        final String id;
        final String shortName;
        String label;
        final String parent;
        String kind;
        String alias;
        boolean explicit;
        boolean declaredWithBlock;
        final List<Map<String, Object>> declarations = new ArrayList<Map<String, Object>>();
        final List<Map<String, Object>> bodyLines = new ArrayList<Map<String, Object>>();
        final List<Map<String, Object>> lifecycleActions = new ArrayList<Map<String, Object>>();

        StateNode(String id, String shortName, String label, String parent, String kind, String alias, boolean explicit) {
            this.id = id;
            this.shortName = shortName;
            this.label = label;
            this.parent = parent;
            this.kind = kind;
            this.alias = alias;
            this.explicit = explicit;
        }

        Set<String> symbols() {
            Set<String> out = new LinkedHashSet<String>();
            out.add(shortName);
            out.add(alias == null ? shortName : alias);
            return out;
        }

        Map<String, Object> toMap() {
            Map<String, Object> attributes = map(
                    "source_node", "plantuml_state",
                    "qualified_id", id,
                    "short_name", shortName,
                    "alias", alias,
                    "explicit_declaration", explicit,
                    "declared_with_block", declaredWithBlock,
                    "declarations", declarations,
                    "body_lines", bodyLines,
                    "lifecycle_actions", lifecycleActions);
            return map(
                    "id", id,
                    "label", label,
                    "kind", kind,
                    "parent", parent,
                    "raw_ref", declarations.isEmpty() ? null : declarations.get(0).get("raw_ref"),
                    "attributes", attributes);
        }
    }

    private static final class Statement {
        final int line;
        final String text;
        final String scope;

        Statement(int line, String text, String scope) {
            this.line = line;
            this.text = text;
            this.scope = scope;
        }
    }

    private static final class Frame {
        final String previousScope;

        Frame(String previousScope) {
            this.previousScope = previousScope;
        }
    }

    private final String text;
    private final String exampleId;
    private final String sourceName;
    private final LinkedHashMap<String, StateNode> states = new LinkedHashMap<String, StateNode>();
    private final List<Statement> rawTransitions = new ArrayList<Statement>();
    private final List<Statement> rawBodies = new ArrayList<Statement>();
    private final Deque<Frame> frames = new ArrayDeque<Frame>();
    private final List<Map<String, Object>> headings = new ArrayList<Map<String, Object>>();
    private final List<Map<String, Object>> ignoredPresentation = new ArrayList<Map<String, Object>>();
    private final List<Map<String, Object>> orphanLifecycle = new ArrayList<Map<String, Object>>();
    private final List<Map<String, Object>> unparsed = new ArrayList<Map<String, Object>>();
    private String currentScope;

    SourceModelParser(String text, String exampleId, String sourceName) {
        this.text = text;
        this.exampleId = exampleId;
        this.sourceName = sourceName;
    }

    Map<String, Object> parse() {
        collect();
        resolveBodies();
        finalizeStateKinds();
        List<Map<String, Object>> transitions = new ArrayList<Map<String, Object>>();
        for (int i = 0; i < rawTransitions.size(); i++) {
            transitions.add(parseTransition(rawTransitions.get(i), i + 1));
        }
        List<Map<String, Object>> stateMaps = new ArrayList<Map<String, Object>>();
        boolean hierarchical = false;
        boolean concurrent = false;
        for (StateNode state : states.values()) {
            stateMaps.add(state.toMap());
            hierarchical |= state.parent != null;
            concurrent |= "fork".equals(state.kind) || "join".equals(state.kind);
        }
        List<String> initialStates = new ArrayList<String>();
        List<String> finalStates = new ArrayList<String>();
        for (Map<String, Object> transition : transitions) {
            @SuppressWarnings("unchecked")
            Map<String, Object> attributes = (Map<String, Object>) transition.get("attributes");
            if ("initial".equals(attributes.get("transition_kind"))) {
                initialStates.add((String) transition.get("target"));
            } else if ("final".equals(attributes.get("transition_kind"))) {
                finalStates.add((String) transition.get("source"));
            }
        }
        String hierarchyLevel = concurrent ? "concurrent" : (hierarchical ? "hierarchical" : "flat");
        String status = unparsed.isEmpty() ? "converted" : "partial";
        String modelName = headings.isEmpty() ? exampleId : String.valueOf(headings.get(0).get("text"));
        return map(
                "schema_version", "r4_5.plantuml_source_canonical.v1",
                "example_id", exampleId,
                "seed_id", exampleId,
                "source_format", "plantuml",
                "adapter", "plantuml_java_scope_aware_source",
                "status", status,
                "status_reason_code", unparsed.isEmpty() ? "R45.SOURCE.converted" : "R45.SOURCE.partial_unparsed_lines",
                "model", map(
                        "name", modelName,
                        "states", stateMaps,
                        "transitions", transitions,
                        "variables", new ArrayList<Object>(),
                        "initial_states", initialStates,
                        "final_states", finalStates,
                        "timing_level", "unknown",
                        "hierarchy_level", hierarchyLevel),
                "diagnostics", new ArrayList<Object>(),
                "metadata", map(
                        "source_frontend", "java_two_pass_scope_aware_plantuml_statechart_subset",
                        "source_name", sourceName,
                        "source_sha256", sha256(text),
                        "source_transition_count", rawTransitions.size(),
                        "model_headings", headings,
                        "ignored_presentation_lines", ignoredPresentation,
                        "orphan_lifecycle_actions", orphanLifecycle,
                        "unparsed_semantic_lines", unparsed,
                        "label_policy", "preserve_as_opaque_event; do not infer guard/effect/timing"));
    }

    private void collect() {
        String[] lines = text.split("\\r?\\n", -1);
        for (int i = 0; i < lines.length; i++) {
            int lineNumber = i + 1;
            String stripped = lines[i].trim();
            String lowered = stripped.toLowerCase(Locale.ROOT);
            if (stripped.isEmpty() || "@startuml".equals(lowered) || "@enduml".equals(lowered)) {
                continue;
            }
            if (stripped.startsWith("'") || stripped.startsWith("//")) {
                continue;
            }
            if ("}".equals(stripped)) {
                if (frames.isEmpty()) {
                    unparsed.add(map("line", lineNumber, "raw", stripped, "reason", "unmatched_closing_brace"));
                } else {
                    currentScope = frames.pop().previousScope;
                }
                continue;
            }
            Matcher stmBlock = STM_BLOCK.matcher(stripped);
            if (stmBlock.matches()) {
                headings.add(map("line", lineNumber, "text", stmBlock.group(1).trim(), "block", true));
                frames.push(new Frame(currentScope));
                continue;
            }
            Matcher stmHeading = STM_HEADING.matcher(stripped);
            if (stmHeading.matches()) {
                headings.add(map("line", lineNumber, "text", stmHeading.group(1).trim(), "block", false));
                continue;
            }
            if (PRESENTATION.matcher(stripped).find()) {
                ignoredPresentation.add(map("line", lineNumber, "raw", stripped));
                continue;
            }
            if (ARROW.matcher(stripped).find()) {
                rawTransitions.add(new Statement(lineNumber, stripped, currentScope));
                continue;
            }
            Matcher forkJoin = FORK_JOIN.matcher(stripped);
            if (forkJoin.matches()) {
                declareState(forkJoin.group(2), forkJoin.group(2), currentScope, lineNumber, stripped,
                        forkJoin.group(1).toLowerCase(Locale.ROOT), null, true);
                continue;
            }
            Matcher lifecycle = LIFECYCLE.matcher(stripped);
            if (lifecycle.matches()) {
                if (currentScope == null) {
                    orphanLifecycle.add(map(
                            "line", lineNumber,
                            "raw", stripped,
                            "kind", normalizedLifecycleKind(lifecycle.group(1)),
                            "text", lifecycle.group(2).trim(),
                            "raw_ref", rawRef(lineNumber),
                            "mapping_status", "blocked_ambiguous_owner"));
                } else {
                    attachLifecycle(states.get(currentScope), lifecycle.group(1), lifecycle.group(2), lineNumber, stripped);
                }
                continue;
            }
            if (parseStateDeclaration(lineNumber, stripped)) {
                continue;
            }
            if (stripped.contains(":")) {
                rawBodies.add(new Statement(lineNumber, stripped, currentScope));
                continue;
            }
            if ("--".equals(stripped)) {
                unparsed.add(map("line", lineNumber, "raw", stripped, "reason", "concurrent_region_separator_unsupported"));
                continue;
            }
            unparsed.add(map("line", lineNumber, "raw", stripped, "reason", "unrecognized_semantic_line"));
        }
    }

    private boolean parseStateDeclaration(int line, String stripped) {
        Matcher matcher = STATE.matcher(stripped);
        if (!matcher.matches()) {
            return false;
        }
        String display = matcher.group(1);
        String alias = matcher.group(2);
        String plain = matcher.group(3);
        String shortName = alias != null ? alias : plain;
        String label = display != null ? display : plain;
        String rest = matcher.group(4) == null ? "" : matcher.group(4).trim();
        boolean opens = rest.endsWith("{");
        if (opens) {
            rest = rest.substring(0, rest.length() - 1).trim();
        }
        String kind = opens ? "composite" : "state";
        String restLower = rest.toLowerCase(Locale.ROOT);
        if (restLower.contains("<<fork>>")) {
            kind = "fork";
        } else if (restLower.contains("<<join>>")) {
            kind = "join";
        } else if (restLower.contains("<<choice>>")) {
            kind = "choice";
        }
        StateNode state = declareState(shortName, label, currentScope, line, stripped, kind, alias, true);
        state.declaredWithBlock |= opens;
        if (rest.startsWith(":")) {
            rawBodies.add(new Statement(line, shortName + " " + rest, currentScope));
        } else if (!rest.isEmpty() && !rest.startsWith("<<")) {
            state.bodyLines.add(map("line", line, "text", rest, "raw", stripped, "raw_ref", rawRef(line)));
        }
        if (opens) {
            state.kind = "composite";
            frames.push(new Frame(currentScope));
            currentScope = state.id;
        }
        return true;
    }

    private StateNode declareState(String shortName, String label, String parent, int line, String raw,
                                   String kind, String alias, boolean explicit) {
        String id = qualified(parent, shortName);
        StateNode state = states.get(id);
        if (state == null) {
            state = new StateNode(id, shortName, label == null ? shortName : label, parent, kind, alias, explicit);
            states.put(id, state);
        } else {
            if (label != null && (state.label.equals(state.shortName) || alias != null)) {
                state.label = label;
            }
            if (alias != null) {
                state.alias = alias;
            }
            state.explicit |= explicit;
            if (!"state".equals(kind)) {
                state.kind = kind;
            }
        }
        state.declarations.add(map("line", line, "raw", raw, "raw_ref", rawRef(line)));
        return state;
    }

    private void resolveBodies() {
        for (Statement statement : rawBodies) {
            int colon = statement.text.indexOf(':');
            String name = cleanEndpoint(statement.text.substring(0, colon));
            String body = statement.text.substring(colon + 1).trim();
            StateNode state = null;
            if (statement.scope != null) {
                StateNode owner = states.get(statement.scope);
                if (owner != null && owner.symbols().contains(name)) {
                    state = owner;
                }
            }
            if (state == null) {
                for (String parent : ancestors(statement.scope)) {
                    state = directMatch(name, parent, true);
                    if (state != null) {
                        break;
                    }
                }
            }
            if (state == null) {
                List<StateNode> aliasMatches = new ArrayList<StateNode>();
                for (StateNode candidate : states.values()) {
                    if (candidate.explicit && name.equals(candidate.alias)) {
                        aliasMatches.add(candidate);
                    }
                }
                if (aliasMatches.size() == 1) {
                    state = aliasMatches.get(0);
                }
            }
            if (state == null) {
                state = declareState(name, name, statement.scope, statement.line, statement.text, "state", null, false);
            }
            Matcher lifecycle = LIFECYCLE.matcher(body);
            if (lifecycle.matches()) {
                attachLifecycle(state, lifecycle.group(1), lifecycle.group(2), statement.line, statement.text);
            } else {
                state.bodyLines.add(map(
                        "line", statement.line,
                        "text", body,
                        "raw", statement.text,
                        "raw_ref", rawRef(statement.line)));
            }
        }
    }

    private void finalizeStateKinds() {
        for (StateNode state : states.values()) {
            if (!"composite".equals(state.kind)) {
                continue;
            }
            boolean hasChild = false;
            for (StateNode candidate : states.values()) {
                if (state.id.equals(candidate.parent)) {
                    hasChild = true;
                    break;
                }
            }
            if (!hasChild) {
                state.kind = "state";
            }
        }
    }

    private void attachLifecycle(StateNode state, String rawKind, String actionText, int line, String raw) {
        String kind = normalizedLifecycleKind(rawKind);
        state.lifecycleActions.add(map(
                "kind", kind,
                "text", actionText.trim(),
                "line", line,
                "raw", raw,
                "raw_ref", rawRef(line)));
    }

    private static String normalizedLifecycleKind(String rawKind) {
        String kind = rawKind.toLowerCase(Locale.ROOT);
        if ("enter".equals(kind)) {
            return "entry";
        }
        if ("during".equals(kind)) {
            return "do";
        }
        return kind;
    }

    private StateNode resolveExplicit(String name, String scope) {
        if (scope != null) {
            StateNode owner = states.get(scope);
            if (owner != null && owner.symbols().contains(name)) {
                return owner;
            }
        }
        for (String parent : ancestors(scope)) {
            StateNode direct = directMatch(name, parent, true);
            if (direct != null) {
                return direct;
            }
        }
        List<StateNode> explicitMatches = matching(name, true);
        return explicitMatches.size() == 1 ? explicitMatches.get(0) : null;
    }

    private StateNode resolveEndpoint(String rawName, String scope, int line) {
        String name = cleanEndpoint(rawName);
        StateNode explicit = resolveExplicit(name, scope);
        if (explicit != null) {
            return explicit;
        }
        for (String parent : ancestors(scope)) {
            StateNode direct = directMatch(name, parent, false);
            if (direct != null) {
                return direct;
            }
        }
        if (scope != null) {
            String prefix = scope + ".";
            List<StateNode> descendants = new ArrayList<StateNode>();
            for (StateNode state : matching(name, false)) {
                if (state.id.startsWith(prefix)) {
                    descendants.add(state);
                }
            }
            if (descendants.size() == 1) {
                return descendants.get(0);
            }
        }
        return declareState(name, name, scope, line, "implicit from transition endpoint " + rawName,
                "state", null, false);
    }

    private List<StateNode> matching(String name, boolean explicitOnly) {
        List<StateNode> out = new ArrayList<StateNode>();
        for (StateNode state : states.values()) {
            if (state.symbols().contains(name) && (!explicitOnly || state.explicit)) {
                out.add(state);
            }
        }
        return out;
    }

    private StateNode directMatch(String name, String parent, boolean explicitOnly) {
        StateNode result = null;
        for (StateNode state : states.values()) {
            if (equal(parent, state.parent) && state.symbols().contains(name) && (!explicitOnly || state.explicit)) {
                if (result != null) {
                    return null;
                }
                result = state;
            }
        }
        return result;
    }

    private Map<String, Object> parseTransition(Statement statement, int index) {
        Matcher arrow = ARROW.matcher(statement.text);
        if (!arrow.find()) {
            throw new IllegalStateException("Transition lost arrow at line " + statement.line);
        }
        String sourceRaw = statement.text.substring(0, arrow.start()).trim();
        String remainder = statement.text.substring(arrow.end()).trim();
        String targetRaw;
        String label = null;
        boolean labelPresent = false;
        Matcher when = Pattern.compile("^(.+?)\\s+when\\s*:\\s*(.*)$", Pattern.CASE_INSENSITIVE).matcher(remainder);
        if (when.matches()) {
            targetRaw = when.group(1).trim();
            label = "when" + (when.group(2).trim().isEmpty() ? "" : " " + when.group(2).trim());
            labelPresent = true;
        } else {
            int colon = remainder.indexOf(':');
            if (colon >= 0) {
                targetRaw = remainder.substring(0, colon).trim();
                label = emptyToNull(remainder.substring(colon + 1).trim());
                labelPresent = true;
            } else {
                targetRaw = remainder.trim();
            }
        }
        boolean sourceInitial = "[*]".equals(sourceRaw.replace(" ", ""));
        boolean targetFinal = "[*]".equals(targetRaw.replace(" ", ""));
        StateNode sourceState = null;
        StateNode targetState = null;
        String kind = "normal";
        String source;
        String target;
        if (sourceInitial) {
            source = "@initial:" + scopeKey(statement.scope);
            kind = "initial";
        } else {
            sourceState = resolveEndpoint(sourceRaw, statement.scope, statement.line);
            source = sourceState.id;
        }
        if (targetFinal) {
            target = "@final:" + scopeKey(statement.scope);
            kind = "final";
        } else {
            targetState = resolveEndpoint(targetRaw, statement.scope, statement.line);
            target = targetState.id;
        }
        Map<String, Object> attributes = map(
                "source_node", "plantuml_transition",
                "transition_kind", kind,
                "raw_line", statement.text,
                "raw_line_number", statement.line,
                "raw_source", sourceRaw,
                "raw_target", targetRaw,
                "raw_arrow", arrow.group(),
                "raw_label_present", labelPresent,
                "raw_label", label,
                "label_semantics", label == null ? "unlabeled" : "opaque_plantuml_display_label",
                "source_parent", sourceState == null ? statement.scope : sourceState.parent,
                "target_parent", targetState == null ? statement.scope : targetState.parent);
        return map(
                "id", String.format(Locale.ROOT, "tr_%04d", index),
                "source", source,
                "target", target,
                "event", label,
                "guard", null,
                "action", null,
                "label", label,
                "scope", statement.scope,
                "raw_ref", rawRef(statement.line),
                "attributes", attributes);
    }

    private String rawRef(int line) {
        return sourceName + ":line:" + line;
    }

    private static String qualified(String parent, String shortName) {
        return parent == null ? shortName : parent + "." + shortName;
    }

    private static String cleanEndpoint(String raw) {
        String out = raw.trim();
        if (out.length() >= 2 && out.startsWith("\"") && out.endsWith("\"")) {
            out = out.substring(1, out.length() - 1).trim();
        }
        if (out.length() >= 2 && out.startsWith("[") && out.endsWith("]") && !"[*]".equals(out)) {
            out = out.substring(1, out.length() - 1).trim();
        }
        return out;
    }

    private static List<String> ancestors(String scope) {
        List<String> out = new ArrayList<String>();
        String current = scope;
        while (current != null) {
            out.add(current);
            int dot = current.lastIndexOf('.');
            current = dot < 0 ? null : current.substring(0, dot);
        }
        out.add(null);
        return out;
    }

    private static String scopeKey(String scope) {
        return scope == null ? "__root__" : scope;
    }

    private static boolean equal(Object left, Object right) {
        return left == null ? right == null : left.equals(right);
    }

    private static String emptyToNull(String value) {
        return value.isEmpty() ? null : value;
    }

    private static String sha256(String value) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] encoded = digest.digest(value.getBytes(StandardCharsets.UTF_8));
            StringBuilder out = new StringBuilder();
            for (byte item : encoded) {
                out.append(String.format(Locale.ROOT, "%02x", item & 0xff));
            }
            return out.toString();
        } catch (Exception error) {
            throw new IllegalStateException(error);
        }
    }

    static Map<String, Object> map(Object... values) {
        if (values.length % 2 != 0) {
            throw new IllegalArgumentException("map requires key/value pairs");
        }
        Map<String, Object> out = new LinkedHashMap<String, Object>();
        for (int i = 0; i < values.length; i += 2) {
            out.put(String.valueOf(values[i]), values[i + 1]);
        }
        return out;
    }
}
