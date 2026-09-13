import sys
from threading import RLock

from governance.approved_actions.action_models import (
    ActionStatus,
    ApprovedAction,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class ApprovedActionStore:

    def __init__(self):

        self._actions: dict[
            str,
            ApprovedAction
        ] = {}

        self._lock = RLock()

        logger.info(
            "Approved action store initialized"
        )

    # ========================================================
    # CREATE
    # ========================================================

    def save(
        self,
        action: ApprovedAction,
    ) -> None:

        try:

            with self._lock:

                if action.action_id in self._actions:

                    raise ValueError(
                        "Approved action already exists."
                    )

                self._actions[
                    action.action_id
                ] = action

                logger.info(
                    f"Approved action created: "
                    f"action_id="
                    f"{action.action_id}"
                )

        except Exception as e:

            logger.exception(
                "Failed to save approved action"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # GET
    # ========================================================

    def get(
        self,
        action_id: str,
    ) -> ApprovedAction | None:

        with self._lock:

            return self._actions.get(
                action_id
            )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        action: ApprovedAction,
    ) -> None:

        try:

            with self._lock:

                if action.action_id not in (
                    self._actions
                ):

                    raise KeyError(
                        "Approved action not found."
                    )

                self._actions[
                    action.action_id
                ] = action

        except Exception as e:

            logger.exception(
                "Failed to update approved action"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # REVOKE
    # ========================================================

    def revoke(
        self,
        action_id: str,
    ) -> None:

        try:

            with self._lock:

                action = self._actions.get(
                    action_id
                )

                if action is None:

                    raise KeyError(
                        "Approved action not found."
                    )

                action.status = (
                    ActionStatus.REVOKED
                )

                self._actions[
                    action_id
                ] = action

                logger.warning(
                    f"Approved action revoked: "
                    f"action_id={action_id}"
                )

        except Exception as e:

            logger.exception(
                "Failed to revoke approved action"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # LIST
    # ========================================================

    def list_actions(
        self,
    ) -> list[ApprovedAction]:

        with self._lock:

            return list(
                self._actions.values()
            )