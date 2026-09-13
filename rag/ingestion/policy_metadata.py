from pathlib import Path


class PolicyMetadataBuilder:

    def build(
        self,
        file_path: str | Path,
        policy_type: str,
        policy_name: str,
        version: str,
        effective_date: str,
    ) -> dict:

        file_path = Path(file_path)

        return {
            "policy_id": (
                f"{policy_type.upper()}-"
                f"{policy_name.upper()}-001"
            ),
            "policy_type": policy_type,
            "policy_name": policy_name,
            "version": version,
            "effective_date": effective_date,
            "source": file_path.name,
        }