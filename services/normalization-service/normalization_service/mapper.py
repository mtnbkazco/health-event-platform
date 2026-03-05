from enum import Enum


class FhirResourceMap(Enum):
    ENCOUNTER = "Encounter"
    OBSERVATION = "Observation"
    CONDITION = "Condition"

    @classmethod
    def from_event_type(cls, event_type: str) -> str:
        """Maps various event strings to a valid FHIR ResourceType string."""
        mapping = {
            "enc": cls.ENCOUNTER.value,
            "ENC": cls.ENCOUNTER.value,
            "ENCOUNTER": cls.ENCOUNTER.value,
            "obs": cls.OBSERVATION.value,
            "OBS": cls.OBSERVATION.value,
            "OBSERVATION": cls.OBSERVATION.value,
            "cond": cls.CONDITION.value,
            "COND": cls.CONDITION.value,
            "CONDITION": cls.CONDITION.value
        }
        # Use .get() to return a clean error if the type is unknown
        result = mapping.get(event_type)
        if not result:
            raise ValueError(f"Unknown event type: {event_type}")
        return result
