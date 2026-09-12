package researchideas.plantuml;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

/** Align source spans with the qualified identities produced by pinned PlantUML. */
final class OfficialIdentityReconciler {
    private static final Pattern CONCURRENT_SCOPE = Pattern.compile("CONC[0-9]+");
    private static final Pattern STM_WRAPPER = Pattern.compile("__stm_wrapper_[0-9]+");

    private OfficialIdentityReconciler() {
    }

    static Map<String, Object> reconcile(
            Map<String, Object> canonical,
            Map<String, Object> officialModel) {
        Map<String, Object> metadata = mapValue(canonical, "metadata");
        if (!"converted".equals(canonical.get("status"))) {
            Map<String, Object> audit = SourceModelParser.map(
                    "status", "not_applied",
                    "reason", "source_canonical_not_complete");
            metadata.put("official_identity_reconciliation", audit);
            return audit;
        }
        if (!"state_diagram".equals(officialModel.get("status"))) {
            Map<String, Object> audit = SourceModelParser.map(
                    "status", "not_applied",
                    "reason", "official_model_not_state_diagram",
                    "official_status", officialModel.get("status"));
            metadata.put("official_identity_reconciliation", audit);
            return audit;
        }

        Map<String, Object> model = mapValue(canonical, "model");
        List<Map<String, Object>> states = mapList(model, "states");
        List<Map<String, Object>> transitions = mapList(model, "transitions");
        List<Map<String, Object>> entities = mapList(officialModel, "entities");
        List<Map<String, Object>> links = behavioralLinks(mapList(officialModel, "links"));
        if (transitions.size() != links.size()) {
            throw new IllegalStateException(
                    "Source/official transition count mismatch: " + transitions.size()
                            + " != " + links.size());
        }

        Map<String, OfficialState> officialStates = officialStates(entities);
        Map<String, Set<String>> endpointEvidence = new LinkedHashMap<String, Set<String>>();
        List<Map<String, Object>> transitionRemaps = new ArrayList<Map<String, Object>>();
        for (int index = 0; index < transitions.size(); index++) {
            Map<String, Object> transition = transitions.get(index);
            Map<String, Object> link = links.get(index);
            Map<String, Object> attributes = mapValue(transition, "attributes");
            String rawArrow = String.valueOf(attributes.get("raw_arrow"));
            boolean reverse = rawArrow.toLowerCase(Locale.ROOT).contains("left")
                    || rawArrow.toLowerCase(Locale.ROOT).contains("up");
            String officialSourceSide = reverse ? "target" : "source";
            String officialTargetSide = reverse ? "source" : "target";
            String expectedSource = officialEndpoint(link, officialSourceSide);
            String expectedTarget = officialEndpoint(link, officialTargetSide);
            String sourceBefore = String.valueOf(transition.get("source"));
            String targetBefore = String.valueOf(transition.get("target"));
            addEndpointEvidence(endpointEvidence, sourceBefore, expectedSource);
            addEndpointEvidence(endpointEvidence, targetBefore, expectedTarget);
            transition.put("source", expectedSource);
            transition.put("target", expectedTarget);
            attributes.put("official_link_index", link.get("index"));
            attributes.put("official_link_reversed_for_layout_arrow", reverse);
            attributes.put("official_source_identity", expectedSource);
            attributes.put("official_target_identity", expectedTarget);
            if (!sourceBefore.equals(expectedSource) || !targetBefore.equals(expectedTarget)) {
                transitionRemaps.add(SourceModelParser.map(
                        "transition_id", transition.get("id"),
                        "raw_ref", transition.get("raw_ref"),
                        "source_before", sourceBefore,
                        "source_after", expectedSource,
                        "target_before", targetBefore,
                        "target_after", expectedTarget,
                        "official_link_index", link.get("index")));
            }
        }

        Map<String, String> stateRemap = new LinkedHashMap<String, String>();
        List<Map<String, Object>> stateRemaps = new ArrayList<Map<String, Object>>();
        for (Map<String, Object> state : states) {
            String oldId = String.valueOf(state.get("id"));
            String newId = resolveStateId(state, oldId, officialStates, endpointEvidence);
            stateRemap.put(oldId, newId);
            if (!oldId.equals(newId)) {
                stateRemaps.add(SourceModelParser.map(
                        "before", oldId,
                        "after", newId,
                        "raw_ref", state.get("raw_ref"),
                        "reason", endpointEvidence.containsKey(oldId)
                                ? "official_link_endpoint_identity"
                                : "unique_official_entity_identity"));
            }
        }

        LinkedHashMap<String, Map<String, Object>> merged = new LinkedHashMap<String, Map<String, Object>>();
        for (Map<String, Object> state : states) {
            String oldId = String.valueOf(state.get("id"));
            String newId = stateRemap.get(oldId);
            OfficialState official = officialStates.get(newId);
            if (official == null) {
                throw new IllegalStateException("No official state for reconciled identity " + newId);
            }
            rewriteStateIdentity(state, newId, official);
            Map<String, Object> existing = merged.get(newId);
            if (existing == null) {
                merged.put(newId, state);
            } else {
                mergeState(existing, state);
            }
        }
        if (!merged.keySet().equals(officialStates.keySet())) {
            Set<String> sourceOnly = new LinkedHashSet<String>(merged.keySet());
            sourceOnly.removeAll(officialStates.keySet());
            Set<String> officialOnly = new LinkedHashSet<String>(officialStates.keySet());
            officialOnly.removeAll(merged.keySet());
            throw new IllegalStateException(
                    "Canonical/official state identity mismatch; source_only=" + sourceOnly
                            + ", official_only=" + officialOnly);
        }
        model.put("states", new ArrayList<Map<String, Object>>(merged.values()));

        for (Map<String, Object> transition : transitions) {
            String oldScope = (String) transition.get("scope");
            String newScope = remapNullable(oldScope, stateRemap);
            if (!equal(oldScope, newScope)) {
                Map<String, Object> attributes = mapValue(transition, "attributes");
                attributes.put("raw_lexical_scope", oldScope);
                transition.put("scope", newScope);
            }
            Map<String, Object> attributes = mapValue(transition, "attributes");
            attributes.put("source_parent", endpointParent(String.valueOf(transition.get("source"))));
            attributes.put("target_parent", endpointParent(String.valueOf(transition.get("target"))));
        }
        remapRegions(model, stateRemap);
        remapSeparators(canonical, stateRemap);
        rebuildBoundaries(model, transitions);

        Map<String, Object> audit = SourceModelParser.map(
                "status", "aligned",
                "policy", "pinned_plantuml_qualified_entity_and_link_identity.v1",
                "synthetic_scope_elision", list("CONC[0-9]+", "__stm_wrapper_[0-9]+"),
                "source_state_count_before", states.size(),
                "canonical_state_count_after", merged.size(),
                "official_state_count", officialStates.size(),
                "transition_count", transitions.size(),
                "transition_identity_alignment_count", transitions.size(),
                "state_identity_remaps", stateRemaps,
                "transition_endpoint_remaps", transitionRemaps);
        metadata.put("official_identity_reconciliation", audit);
        return audit;
    }

    private static List<Map<String, Object>> behavioralLinks(List<Map<String, Object>> links) {
        List<Map<String, Object>> behavioral = new ArrayList<Map<String, Object>>();
        for (Map<String, Object> link : links) {
            if (isBehaviorEndpointKind(String.valueOf(link.get("source_kind")))
                    && isBehaviorEndpointKind(String.valueOf(link.get("target_kind")))) {
                behavioral.add(link);
            }
        }
        return behavioral;
    }

    private static boolean isBehaviorEndpointKind(String kind) {
        return kind.startsWith("GROUP:")
                || kind.contains("STATE")
                || kind.contains("CIRCLE_START")
                || kind.contains("CIRCLE_END");
    }

    private static Map<String, OfficialState> officialStates(List<Map<String, Object>> entities) {
        LinkedHashMap<String, OfficialState> states = new LinkedHashMap<String, OfficialState>();
        for (Map<String, Object> entity : entities) {
            String qualified = String.valueOf(entity.get("qualified_name"));
            String kind = String.valueOf(entity.get("kind"));
            if (qualified.isEmpty()
                    || kind.contains("CIRCLE_START")
                    || kind.contains("CIRCLE_END")
                    || !isBehaviorEndpointKind(kind)) {
                continue;
            }
            String rawShortName = shortName(qualified);
            if (CONCURRENT_SCOPE.matcher(rawShortName).matches()
                    || STM_WRAPPER.matcher(rawShortName).matches()) {
                continue;
            }
            String id = normalizeQualified(qualified);
            if (id.isEmpty()) {
                continue;
            }
            String parent = normalizeQualified((String) entity.get("parent"));
            if (parent.isEmpty()) {
                parent = null;
            }
            OfficialState existing = states.get(id);
            OfficialState current = new OfficialState(id, parent, kind.startsWith("GROUP:"));
            if (existing == null) {
                states.put(id, current);
            } else if (!equal(existing.parent, current.parent)) {
                throw new IllegalStateException(
                        "Official synthetic-scope collapse changed parent for " + id + ": "
                                + existing.parent + " != " + current.parent);
            } else {
                existing.composite |= current.composite;
            }
        }
        return states;
    }

    private static String resolveStateId(
            Map<String, Object> state,
            String oldId,
            Map<String, OfficialState> officialStates,
            Map<String, Set<String>> endpointEvidence) {
        Set<String> evidence = endpointEvidence.get(oldId);
        if (evidence != null) {
            if (evidence.size() != 1) {
                throw new IllegalStateException(
                        "One source state maps to multiple official identities: " + oldId + " -> " + evidence);
            }
            return evidence.iterator().next();
        }
        if (officialStates.containsKey(oldId)) {
            return oldId;
        }
        Map<String, Object> attributes = mapValue(state, "attributes");
        String shortName = String.valueOf(attributes.get("short_name"));
        List<String> candidates = new ArrayList<String>();
        for (String officialId : officialStates.keySet()) {
            if (shortName.equals(shortName(officialId))) {
                candidates.add(officialId);
            }
        }
        if (candidates.size() != 1) {
            throw new IllegalStateException(
                    "Cannot uniquely align source state " + oldId + " with official entities " + candidates);
        }
        return candidates.get(0);
    }

    private static void addEndpointEvidence(
            Map<String, Set<String>> evidence,
            String sourceIdentity,
            String officialIdentity) {
        if (sourceIdentity.startsWith("@")) {
            return;
        }
        Set<String> targets = evidence.get(sourceIdentity);
        if (targets == null) {
            targets = new LinkedHashSet<String>();
            evidence.put(sourceIdentity, targets);
        }
        targets.add(officialIdentity);
    }

    private static String officialEndpoint(Map<String, Object> link, String side) {
        String qualified = String.valueOf(link.get(side));
        String kind = String.valueOf(link.get(side + "_kind"));
        if (kind.contains("CIRCLE_START")) {
            return "@initial:" + scopeKey(normalizeQualified(parentOf(qualified)));
        }
        if (kind.contains("CIRCLE_END")) {
            return "@final:" + scopeKey(normalizeQualified(parentOf(qualified)));
        }
        return normalizeQualified(qualified);
    }

    private static void rewriteStateIdentity(
            Map<String, Object> state,
            String id,
            OfficialState official) {
        state.put("id", id);
        state.put("parent", official.parent);
        if (official.composite) {
            state.put("kind", "composite");
        }
        Map<String, Object> attributes = mapValue(state, "attributes");
        attributes.put("qualified_id", id);
        attributes.put("short_name", shortName(id));
        attributes.put("official_identity_aligned", true);
        attributes.put("official_parent", official.parent);
    }

    private static void mergeState(Map<String, Object> target, Map<String, Object> source) {
        Map<String, Object> targetAttributes = mapValue(target, "attributes");
        Map<String, Object> sourceAttributes = mapValue(source, "attributes");
        boolean targetExplicit = Boolean.TRUE.equals(targetAttributes.get("explicit_declaration"));
        boolean sourceExplicit = Boolean.TRUE.equals(sourceAttributes.get("explicit_declaration"));
        if ((!targetExplicit && sourceExplicit)
                || String.valueOf(target.get("label")).equals(shortName(String.valueOf(target.get("id"))))) {
            target.put("label", source.get("label"));
            target.put("raw_ref", source.get("raw_ref"));
        }
        if ("composite".equals(source.get("kind"))) {
            target.put("kind", "composite");
        } else if ("state".equals(target.get("kind")) && !"state".equals(source.get("kind"))) {
            target.put("kind", source.get("kind"));
        }
        targetAttributes.put("explicit_declaration", targetExplicit || sourceExplicit);
        targetAttributes.put(
                "declared_with_block",
                Boolean.TRUE.equals(targetAttributes.get("declared_with_block"))
                        || Boolean.TRUE.equals(sourceAttributes.get("declared_with_block")));
        if (targetAttributes.get("alias") == null && sourceAttributes.get("alias") != null) {
            targetAttributes.put("alias", sourceAttributes.get("alias"));
        }
        mergeList(targetAttributes, sourceAttributes, "declarations");
        mergeList(targetAttributes, sourceAttributes, "body_lines");
        mergeList(targetAttributes, sourceAttributes, "lifecycle_actions");
        mergeUniqueList(targetAttributes, sourceAttributes, "parent_region_indices");
    }

    private static void remapRegions(Map<String, Object> model, Map<String, String> stateRemap) {
        List<Map<String, Object>> regions = mapList(model, "concurrent_regions");
        for (Map<String, Object> region : regions) {
            String oldOwner = (String) region.get("owner_scope");
            String owner = remapNullable(oldOwner, stateRemap);
            region.put("owner_scope", owner);
            region.put("id", scopeKey(owner) + ":region:" + region.get("region_index"));
            List<Object> remapped = new ArrayList<Object>();
            Set<String> seen = new LinkedHashSet<String>();
            for (Object raw : objectList(region.get("state_ids"))) {
                String id = stateRemap.containsKey(String.valueOf(raw))
                        ? stateRemap.get(String.valueOf(raw)) : String.valueOf(raw);
                if (seen.add(id)) {
                    remapped.add(id);
                }
            }
            region.put("state_ids", remapped);
        }
    }

    private static void remapSeparators(
            Map<String, Object> canonical,
            Map<String, String> stateRemap) {
        Map<String, Object> metadata = mapValue(canonical, "metadata");
        List<Map<String, Object>> separators = mapList(metadata, "concurrent_region_separators");
        for (Map<String, Object> separator : separators) {
            separator.put(
                    "owner_scope",
                    remapNullable((String) separator.get("owner_scope"), stateRemap));
        }
    }

    private static void rebuildBoundaries(
            Map<String, Object> model,
            List<Map<String, Object>> transitions) {
        List<String> initial = new ArrayList<String>();
        List<String> finals = new ArrayList<String>();
        for (Map<String, Object> transition : transitions) {
            Map<String, Object> attributes = mapValue(transition, "attributes");
            if ("initial".equals(attributes.get("transition_kind"))) {
                initial.add(String.valueOf(transition.get("target")));
            } else if ("final".equals(attributes.get("transition_kind"))) {
                finals.add(String.valueOf(transition.get("source")));
            }
        }
        model.put("initial_states", initial);
        model.put("final_states", finals);
    }

    private static String endpointParent(String endpoint) {
        if (endpoint.startsWith("@initial:") || endpoint.startsWith("@final:")) {
            String scope = endpoint.substring(endpoint.indexOf(':') + 1);
            return "__root__".equals(scope) ? null : scope;
        }
        return parentOf(endpoint);
    }

    private static String normalizeQualified(String qualified) {
        if (qualified == null || qualified.isEmpty()) {
            return "";
        }
        StringBuilder out = new StringBuilder();
        for (String segment : qualified.split("\\.")) {
            if (segment.isEmpty()
                    || CONCURRENT_SCOPE.matcher(segment).matches()
                    || STM_WRAPPER.matcher(segment).matches()) {
                continue;
            }
            if (out.length() > 0) {
                out.append('.');
            }
            out.append(segment);
        }
        return out.toString();
    }

    private static String parentOf(String id) {
        int dot = id.lastIndexOf('.');
        return dot < 0 ? null : id.substring(0, dot);
    }

    private static String shortName(String id) {
        int dot = id.lastIndexOf('.');
        return dot < 0 ? id : id.substring(dot + 1);
    }

    private static String scopeKey(String scope) {
        return scope == null || scope.isEmpty() ? "__root__" : scope;
    }

    private static String remapNullable(String value, Map<String, String> remap) {
        return value != null && remap.containsKey(value) ? remap.get(value) : value;
    }

    private static boolean equal(Object left, Object right) {
        return left == null ? right == null : left.equals(right);
    }

    private static List<Object> list(Object... values) {
        List<Object> out = new ArrayList<Object>();
        for (Object value : values) {
            out.add(value);
        }
        return out;
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> mapValue(Map<String, Object> owner, String key) {
        return (Map<String, Object>) owner.get(key);
    }

    @SuppressWarnings("unchecked")
    private static List<Map<String, Object>> mapList(Map<String, Object> owner, String key) {
        Object value = owner.get(key);
        if (value == null) {
            return new ArrayList<Map<String, Object>>();
        }
        return (List<Map<String, Object>>) value;
    }

    @SuppressWarnings("unchecked")
    private static List<Object> objectList(Object value) {
        return value == null ? new ArrayList<Object>() : (List<Object>) value;
    }

    private static void mergeList(
            Map<String, Object> target,
            Map<String, Object> source,
            String key) {
        List<Object> targetValues = objectList(target.get(key));
        targetValues.addAll(objectList(source.get(key)));
        target.put(key, targetValues);
    }

    private static void mergeUniqueList(
            Map<String, Object> target,
            Map<String, Object> source,
            String key) {
        LinkedHashSet<Object> values = new LinkedHashSet<Object>(objectList(target.get(key)));
        values.addAll(objectList(source.get(key)));
        target.put(key, new ArrayList<Object>(values));
    }

    private static final class OfficialState {
        final String id;
        final String parent;
        boolean composite;

        OfficialState(String id, String parent, boolean composite) {
            this.id = id;
            this.parent = parent;
            this.composite = composite;
        }
    }
}
