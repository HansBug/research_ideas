package researchideas.plantuml;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import net.sourceforge.plantuml.BlockUml;
import net.sourceforge.plantuml.SourceStringReader;
import net.sourceforge.plantuml.abel.Entity;
import net.sourceforge.plantuml.abel.Link;
import net.sourceforge.plantuml.core.Diagram;
import net.sourceforge.plantuml.statediagram.StateDiagram;
import net.sourceforge.plantuml.version.Version;

public final class PlantUmlStateFrontend {
    private PlantUmlStateFrontend() {
    }

    public static void main(String[] args) throws Exception {
        Map<String, String> options = parseArgs(args);
        Path sourcePath = requiredPath(options, "source");
        String exampleId = required(options, "example-id");
        String sourceName = options.containsKey("source-name")
                ? options.get("source-name") : sourcePath.getFileName().toString();
        Path officialPath = options.containsKey("official-source")
                ? Paths.get(options.get("official-source")) : sourcePath;

        String source = read(sourcePath);
        String officialSource = read(officialPath);
        OfficialValidationNormalizer.Result normalized = OfficialValidationNormalizer.normalize(officialSource);
        Map<String, Object> output = SourceModelParser.map(
                "schema_version", "r4_5.plantuml_java_frontend.v1",
                "tool", SourceModelParser.map(
                        "implementation", PlantUmlStateFrontend.class.getName(),
                        "plantuml_version", Version.versionString(),
                        "java_version", System.getProperty("java.version")),
                "canonical", new SourceModelParser(source, exampleId, sourceName).parse(),
                "official_model", inspectOfficial(officialSource, officialPath.getFileName().toString()),
                "official_validation", SourceModelParser.map(
                        "normalizations", normalized.changes,
                        "model", inspectOfficial(normalized.source, "normalized:" + officialPath.getFileName().toString())));
        System.out.println(JsonWriter.write(output));
    }

    private static Map<String, Object> inspectOfficial(String source, String sourceName) {
        Map<String, Object> output = new LinkedHashMap<String, Object>();
        output.put("source_name", sourceName);
        try {
            SourceStringReader reader = new SourceStringReader(source);
            List<BlockUml> blocks = reader.getBlocks();
            output.put("block_count", blocks.size());
            if (blocks.size() != 1) {
                output.put("status", "not_single_block");
                output.put("entities", new ArrayList<Object>());
                output.put("links", new ArrayList<Object>());
                return output;
            }
            Diagram parsed = blocks.get(0).getDiagram();
            output.put("diagram_class", parsed.getClass().getName());
            output.put("description", String.valueOf(parsed.getDescription()));
            if (!(parsed instanceof StateDiagram)) {
                output.put("status", "not_state_diagram");
                output.put("warning_or_error", String.valueOf(parsed.getWarningOrError()));
                output.put("entities", new ArrayList<Object>());
                output.put("links", new ArrayList<Object>());
                return output;
            }
            StateDiagram diagram = (StateDiagram) parsed;
            output.put("status", "state_diagram");
            output.put("final_error", String.valueOf(diagram.checkFinalError()));
            output.put("warning_or_error", String.valueOf(diagram.getWarningOrError()));

            List<Entity> groups = new ArrayList<Entity>(diagram.groupsAndRoot());
            List<Entity> leaves = new ArrayList<Entity>(diagram.leafs());
            Comparator<Entity> byQualifiedName = new Comparator<Entity>() {
                @Override
                public int compare(Entity left, Entity right) {
                    return qualifiedName(left).compareTo(qualifiedName(right));
                }
            };
            Collections.sort(groups, byQualifiedName);
            Collections.sort(leaves, byQualifiedName);
            List<Map<String, Object>> entities = new ArrayList<Map<String, Object>>();
            for (Entity entity : groups) {
                entities.add(entityMap("group", entity));
            }
            for (Entity entity : leaves) {
                entities.add(entityMap("leaf", entity));
            }
            List<Map<String, Object>> links = new ArrayList<Map<String, Object>>();
            int index = 0;
            for (Link link : diagram.getLinks()) {
                links.add(SourceModelParser.map(
                        "index", index++,
                        "source", qualifiedName(link.getEntity1()),
                        "source_kind", entityKind(link.getEntity1()),
                        "target", qualifiedName(link.getEntity2()),
                        "target_kind", entityKind(link.getEntity2()),
                        "label", String.valueOf(link.getLabel()),
                        "type", String.valueOf(link.getType()),
                        "length", link.getLength()));
            }
            output.put("entities", entities);
            output.put("links", links);
            output.put("counts", SourceModelParser.map(
                    "groups", groups.size(),
                    "leaves", leaves.size(),
                    "links", links.size()));
            return output;
        } catch (Throwable error) {
            output.put("status", "official_parser_exception");
            output.put("exception_class", error.getClass().getName());
            output.put("exception_message", String.valueOf(error.getMessage()));
            output.put("entities", new ArrayList<Object>());
            output.put("links", new ArrayList<Object>());
            return output;
        }
    }

    private static Map<String, Object> entityMap(String collection, Entity entity) {
        Entity parent = entity.getParentContainer();
        List<String> body = new ArrayList<String>();
        if (entity.getBodier() != null) {
            for (Object line : entity.getBodier().getRawBody()) {
                body.add(String.valueOf(line));
            }
        }
        String kind = entityKind(entity);
        return SourceModelParser.map(
                "collection", collection,
                "qualified_name", qualifiedName(entity),
                "name", String.valueOf(entity.getName()),
                "display", String.valueOf(entity.getDisplay()),
                "kind", kind,
                "parent", parent == null ? null : qualifiedName(parent),
                "concurrent_separator", String.valueOf(entity.getConcurrentSeparator()),
                "raw_body", body);
    }

    private static String qualifiedName(Entity entity) {
        return entity.getQuark().getQualifiedName();
    }

    private static String entityKind(Entity entity) {
        return entity.isGroup()
                ? "GROUP:" + String.valueOf(entity.getGroupType())
                : "LEAF:" + String.valueOf(entity.getLeafType());
    }

    private static String read(Path path) throws Exception {
        return new String(Files.readAllBytes(path), StandardCharsets.UTF_8);
    }

    private static Map<String, String> parseArgs(String[] args) {
        Map<String, String> options = new LinkedHashMap<String, String>();
        for (int i = 0; i < args.length; i++) {
            String arg = args[i];
            if (!arg.startsWith("--") || i + 1 >= args.length) {
                throw new IllegalArgumentException("Expected --key value, got: " + arg);
            }
            options.put(arg.substring(2), args[++i]);
        }
        return options;
    }

    private static String required(Map<String, String> options, String key) {
        String value = options.get(key);
        if (value == null || value.trim().isEmpty()) {
            throw new IllegalArgumentException("Missing --" + key);
        }
        return value;
    }

    private static Path requiredPath(Map<String, String> options, String key) {
        Path path = Paths.get(required(options, key));
        if (!Files.isRegularFile(path)) {
            throw new IllegalArgumentException("Not a file: " + path);
        }
        return path;
    }
}
