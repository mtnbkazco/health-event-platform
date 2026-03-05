import pytest
from fake_ehr_producer.resource_generator import ResourceGenerator


def test_generate_resource_contains_required_fields():
    generator = ResourceGenerator()
    resource = generator.fhir_generated_resource()

    assert "id" in resource
    assert "resourceType" in resource
    assert "subject" in resource


def test_patient_id_is_string():
    generator = ResourceGenerator()
    resource = generator.fhir_generated_resource()
    assert isinstance(resource["id"], str)


def test_event_type_is_valid():
    generator = ResourceGenerator()
    resource = generator.fhir_generated_resource()
    assert resource["resourceType"] in [
        "Observation",
        "Encounter",
        "Condition"
    ]