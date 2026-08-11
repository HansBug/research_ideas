from __future__ import annotations

from paper_stm_representation.pyfcstm_names import NameRegistry


def test_name_registry_uses_pyfcstm_identifier_tools_and_stable_collision_suffix():
    registry = NameRegistry()
    first = registry.reserve(raw_text="Power On", canonical_ref="c1", object_type="event", scope="Root")
    second = registry.reserve(raw_text="Power_On", canonical_ref="c2", object_type="event", scope="Root")
    assert first == "Power_On"
    assert second == "Power_On_2"
    rows = registry.to_jsonable()["items"]
    assert rows[0]["tool_function"] == "pyfcstm.utils.to_identifier"
    assert rows[1]["collision_group"] == "Root:Power_On"
    assert rows[1]["suffix_policy"] == "stable_scope_collision_suffix_1_based"


def test_sequence_safe_path_is_recorded_for_synthetic_relay():
    registry = NameRegistry()
    relay = registry.reserve(
        raw_text="Ready scanBarcode [isValidBarcode] -> SecurityCheck",
        canonical_ref="tr_0001",
        object_type="pseudo_relay",
        scope="Root",
        use_sequence=["Ready", "scanBarcode", "isValidBarcode", "SecurityCheck", "relay"],
    )
    assert relay == "ready_scan_barcode_is_valid_barcode_security_check_relay"
    row = registry.to_jsonable()["items"][0]
    assert row["tool_function"] == "pyfcstm.utils.sequence_safe|pyfcstm.utils.to_identifier"
    assert row["tool_parameters"]["sequence_segments"][-1] == "relay"


def test_fcstm_lexer_special_token_is_suffix_adjusted():
    registry = NameRegistry()
    ident = registry.reserve(raw_text="E", canonical_ref="event-e", object_type="event", scope="Root")
    assert ident == "E_"
    row = registry.to_jsonable()["items"][0]
    assert row["is_dsl_keyword_adjusted"] is True
