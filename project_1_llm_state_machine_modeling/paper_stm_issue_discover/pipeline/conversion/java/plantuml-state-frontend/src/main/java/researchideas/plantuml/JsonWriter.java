package researchideas.plantuml;

import java.lang.reflect.Array;
import java.util.Iterator;
import java.util.Map;

final class JsonWriter {
    private JsonWriter() {
    }

    static String write(Object value) {
        StringBuilder out = new StringBuilder();
        append(out, value);
        return out.toString();
    }

    private static void append(StringBuilder out, Object value) {
        if (value == null) {
            out.append("null");
        } else if (value instanceof String || value instanceof Character) {
            appendString(out, value.toString());
        } else if (value instanceof Number || value instanceof Boolean) {
            out.append(value.toString());
        } else if (value instanceof Map<?, ?>) {
            appendMap(out, (Map<?, ?>) value);
        } else if (value instanceof Iterable<?>) {
            appendIterable(out, (Iterable<?>) value);
        } else if (value.getClass().isArray()) {
            out.append('[');
            for (int i = 0; i < Array.getLength(value); i++) {
                if (i > 0) {
                    out.append(',');
                }
                append(out, Array.get(value, i));
            }
            out.append(']');
        } else {
            appendString(out, value.toString());
        }
    }

    private static void appendMap(StringBuilder out, Map<?, ?> values) {
        out.append('{');
        Iterator<? extends Map.Entry<?, ?>> iterator = values.entrySet().iterator();
        boolean first = true;
        while (iterator.hasNext()) {
            Map.Entry<?, ?> entry = iterator.next();
            if (!first) {
                out.append(',');
            }
            first = false;
            appendString(out, String.valueOf(entry.getKey()));
            out.append(':');
            append(out, entry.getValue());
        }
        out.append('}');
    }

    private static void appendIterable(StringBuilder out, Iterable<?> values) {
        out.append('[');
        boolean first = true;
        for (Object value : values) {
            if (!first) {
                out.append(',');
            }
            first = false;
            append(out, value);
        }
        out.append(']');
    }

    private static void appendString(StringBuilder out, String value) {
        out.append('"');
        for (int i = 0; i < value.length(); i++) {
            char ch = value.charAt(i);
            switch (ch) {
                case '"':
                    out.append("\\\"");
                    break;
                case '\\':
                    out.append("\\\\");
                    break;
                case '\b':
                    out.append("\\b");
                    break;
                case '\f':
                    out.append("\\f");
                    break;
                case '\n':
                    out.append("\\n");
                    break;
                case '\r':
                    out.append("\\r");
                    break;
                case '\t':
                    out.append("\\t");
                    break;
                default:
                    if (ch < 0x20) {
                        out.append(String.format("\\u%04x", (int) ch));
                    } else {
                        out.append(ch);
                    }
            }
        }
        out.append('"');
    }
}
