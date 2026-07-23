package researchideas.plantuml;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

final class OfficialValidationNormalizer {
    private static final Pattern STM_BLOCK = Pattern.compile("^(\\s*)stm\\s+(.+?)\\s*\\{\\s*$", Pattern.CASE_INSENSITIVE);
    private static final Pattern STM_HEADING = Pattern.compile("^(\\s*)stm\\s+(.+?)\\s*$", Pattern.CASE_INSENSITIVE);
    private static final Pattern BARE_ACTION = Pattern.compile("^(\\s*)(entry|enter|do|during|exit)\\s*/", Pattern.CASE_INSENSITIVE);
    private static final Pattern FORK_JOIN = Pattern.compile("^(\\s*)(fork|join)\\s+([A-Za-z_][A-Za-z0-9_]*)\\s*$", Pattern.CASE_INSENSITIVE);
    private static final Pattern ARROW = Pattern.compile("-(?:left|right|up|down)->|-->|->", Pattern.CASE_INSENSITIVE);
    private static final Pattern QUOTED_DELIMITER = Pattern.compile(
            "^(\\s*@(start|end)uml)\\x22+\\s*$", Pattern.CASE_INSENSITIVE);
    private static final Pattern DOUBLED_QUOTED_STATE = Pattern.compile(
            "^(\\s*state\\s+)\\x22{2}([^\\x22]+)\\x22{2}(\\s+as\\s+[A-Za-z_][A-Za-z0-9_]*.*)$",
            Pattern.CASE_INSENSITIVE);

    static final class Result {
        final String source;
        final List<Map<String, Object>> changes;

        Result(String source, List<Map<String, Object>> changes) {
            this.source = source;
            this.changes = changes;
        }
    }

    private OfficialValidationNormalizer() {
    }

    static Result normalize(String source) {
        String[] lines = source.split("\\r?\\n", -1);
        List<String> output = new ArrayList<String>();
        List<Map<String, Object>> changes = new ArrayList<Map<String, Object>>();
        for (int i = 0; i < lines.length; i++) {
            int lineNumber = i + 1;
            String line = lines[i];
            String rewritten = line;
            String rule = null;
            Matcher stmBlock = STM_BLOCK.matcher(line);
            Matcher stmHeading = STM_HEADING.matcher(line);
            Matcher bareAction = BARE_ACTION.matcher(line);
            Matcher forkJoin = FORK_JOIN.matcher(line);
            Matcher quotedDelimiter = QUOTED_DELIMITER.matcher(line);
            Matcher doubledQuotedState = DOUBLED_QUOTED_STATE.matcher(line);
            if (doubledQuotedState.matches()) {
                rewritten = doubledQuotedState.group(1) + "\"" + doubledQuotedState.group(2)
                        + "\"" + doubledQuotedState.group(3);
                rule = "official_validation.plantuml_state_display_doubled_quotes";
            } else if (quotedDelimiter.matches()) {
                rewritten = quotedDelimiter.group(1);
                rule = "official_validation.plantuml_delimiter_trailing_quote";
            } else if (stmBlock.matches()) {
                String alias = "__stm_wrapper_" + lineNumber;
                String label = stmBlock.group(2).replace("\"", "'");
                rewritten = stmBlock.group(1) + "state \"" + label + "\" as " + alias + " {";
                rule = "official_validation.stm_block_wrapper";
            } else if (stmHeading.matches() && !line.trim().toLowerCase(Locale.ROOT).startsWith("state ")) {
                rewritten = stmHeading.group(1) + "' official-validation ignored non-PlantUML heading: " + line.trim();
                rule = "official_validation.stm_heading_comment";
            } else if (bareAction.find()) {
                rewritten = bareAction.group(1) + "' official-validation preserves action in Java source canonical: " + line.trim();
                rule = "official_validation.bare_action_comment";
            } else if (forkJoin.matches()) {
                rewritten = forkJoin.group(1) + "state " + forkJoin.group(3) + " <<" + forkJoin.group(2).toLowerCase(Locale.ROOT) + ">>";
                rule = "official_validation.fork_join_stereotype";
            } else if (ARROW.matcher(line).find()) {
                rewritten = normalizeTransition(line);
                if (!rewritten.equals(line)) {
                    rule = "official_validation.transition_syntax";
                }
            }
            output.add(rewritten);
            if (rule != null) {
                changes.add(SourceModelParser.map(
                        "line", lineNumber,
                        "rule_id", rule,
                        "before", line,
                        "after", rewritten));
            }
        }
        return new Result(joinLines(output), changes);
    }

    private static String normalizeTransition(String line) {
        Matcher arrow = ARROW.matcher(line);
        if (!arrow.find()) {
            return line;
        }
        String indent = line.substring(0, line.length() - line.replaceFirst("^\\s+", "").length());
        String source = line.substring(0, arrow.start()).trim();
        String remainder = line.substring(arrow.end()).trim();
        String target;
        String suffix = "";
        Matcher when = Pattern.compile("^(.+?)\\s+when\\s*:\\s*(.*)$", Pattern.CASE_INSENSITIVE).matcher(remainder);
        if (when.matches()) {
            target = when.group(1).trim();
            suffix = " : when" + (when.group(2).trim().isEmpty() ? "" : " " + when.group(2).trim());
        } else {
            int colon = remainder.indexOf(':');
            if (colon >= 0) {
                target = remainder.substring(0, colon).trim();
                String label = remainder.substring(colon + 1).trim();
                suffix = label.isEmpty() ? "" : " : " + label;
            } else {
                target = remainder;
            }
        }
        source = unbracket(source);
        target = unbracket(target);
        return indent + source + " " + arrow.group() + " " + target + suffix;
    }

    private static String unbracket(String endpoint) {
        String value = endpoint.trim();
        if (value.startsWith("[") && value.endsWith("]") && !"[*]".equals(value)) {
            return value.substring(1, value.length() - 1).trim();
        }
        return value;
    }

    private static String joinLines(List<String> lines) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < lines.size(); i++) {
            if (i > 0) {
                out.append('\n');
            }
            out.append(lines.get(i));
        }
        return out.toString();
    }
}
