package researchideas.plantuml;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Narrow, ledgered repairs for transport damage in the author workbook cells. */
final class SourceInputNormalizer {
    private static final Pattern DOUBLED_QUOTED_STATE = Pattern.compile(
            "^(\\s*state\\s+)\"\"([^\"]+)\"\"(\\s+as\\s+[A-Za-z_][A-Za-z0-9_]*(?:\\s+.*)?\\s*)$",
            Pattern.CASE_INSENSITIVE);
    private static final Pattern TRAILING_QUOTED_END = Pattern.compile("^(\\s*@enduml)\"(\\s*)$", Pattern.CASE_INSENSITIVE);

    static final class Result {
        final String source;
        final List<Map<String, Object>> changes;

        Result(String source, List<Map<String, Object>> changes) {
            this.source = source;
            this.changes = changes;
        }
    }

    private SourceInputNormalizer() {
    }

    static Result normalize(String source, String sourceName) {
        String[] lines = source.split("\\r?\\n", -1);
        List<String> output = new ArrayList<String>();
        List<Map<String, Object>> changes = new ArrayList<Map<String, Object>>();
        for (int i = 0; i < lines.length; i++) {
            int lineNumber = i + 1;
            String before = lines[i];
            String after = before;
            String ruleId = null;

            Matcher doubledState = DOUBLED_QUOTED_STATE.matcher(before);
            Matcher trailingEnd = TRAILING_QUOTED_END.matcher(before);
            if (doubledState.matches()) {
                after = doubledState.group(1) + "\"" + doubledState.group(2) + "\"" + doubledState.group(3);
                ruleId = "source_input.workbook_doubled_state_quotes";
            } else if (trailingEnd.matches()) {
                after = trailingEnd.group(1) + trailingEnd.group(2);
                ruleId = "source_input.workbook_trailing_end_quote";
            }
            output.add(after);
            if (ruleId != null) {
                changes.add(SourceModelParser.map(
                        "line", lineNumber,
                        "raw_ref", sourceName + ":line:" + lineNumber,
                        "rule_id", ruleId,
                        "before", before,
                        "after", after));
            }
        }
        return new Result(joinLines(output), changes);
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
