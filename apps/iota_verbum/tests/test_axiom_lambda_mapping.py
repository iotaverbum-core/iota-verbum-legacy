# tests/test_axiom_lambda_mapping.py

from engine.axiom_lambda import AxiomLambdaFlags
from engine.axiom_lambda_mapping import LamentContext, derive_flags_from_context


def test_mapping_basic_christian_lament():
    context = LamentContext(
        subject_type="human",
        canonical_epoch="post-incarnation",
        developmental_stage="adult",
        god_addressed_as="Jesus",
        explicit_trinity_confessed=True,
        explicit_christ_union=True,
        soteriology_phrases=["Jesus died for us on the cross"],
        eschatology_phrases=["bodily resurrection and new creation"],
        suffering_kind="illness",
        posture_markers=["repent", "trust"],
    )

    flags: AxiomLambdaFlags = derive_flags_from_context(context)

    assert flags.image_bearer is True
    assert flags.pre_incarnation_context is False
    assert flags.pre_rational_subject is False

    assert flags.triune_confessed is True
    assert flags.explicit_christ_union is True
    assert flags.christ_event_present is True
    assert flags.bodily_resurrection_confessed is True
    assert flags.new_creation_confessed is True

    assert flags.genuine_suffering is True
    assert flags.cheap_lament_indicators is False
    assert flags.oriented_to_repentance_trust is True

    assert flags.ambiguous_religious_context is False
    assert flags.gnostic_language_present is False
    assert flags.universalist_language_present is False


def test_mapping_entitlement_marks_cheap_lament():
    context = LamentContext(
        subject_type="human",
        suffering_kind="entitlement",
        posture_markers=["complain"],
    )

    flags = derive_flags_from_context(context)

    assert flags.image_bearer is True
    assert flags.genuine_suffering is False
    assert flags.cheap_lament_indicators is True


def test_mapping_pre_incarnation_and_pre_rational_notes():
    context = LamentContext(
        subject_type="human",
        canonical_epoch="pre-incarnation",
        developmental_stage="pre-rational",
        god_addressed_as="God",
    )

    flags = derive_flags_from_context(context)

    assert flags.pre_incarnation_context is True
    assert flags.pre_rational_subject is True
    # notes should contain at least two explanatory entries
    assert len(flags.notes) >= 2
