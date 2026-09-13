import json
import sys

from pathlib import Path
from threading import RLock
from uuid import uuid4
from decimal import Decimal

from logging.handlers import RotatingFileHandler
import logging

from governance.audit.audit_config import (
    AUDIT_DIR,
    AUDIT_FILE,
    MAX_AUDIT_FILE_SIZE,
    BACKUP_COUNT,
)

from governance.audit.audit_models import (
    AuditEvent,
    AuditEventType,
    AuditSeverity,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class AuditLogger:

    def __init__(
        self,
        audit_file: Path = AUDIT_FILE,
    ):

        try:

            self.audit_file = Path(
                audit_file
            )

            self.audit_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self._lock = RLock()

            self._logger = (
                logging.getLogger(
                    "AI-Banking-Audit"
                )
            )

            self._logger.setLevel(
                logging.INFO
            )

            self._logger.propagate = False

            self._configure_handler()

            logger.info(
                "Governance audit logger initialized"
            )

        except Exception as e:

            logger.exception(
                "Failed to initialize "
                "audit logger"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # LOGGER CONFIGURATION
    # ========================================================

    def _configure_handler(self):

        if self._logger.handlers:

            return

        handler = RotatingFileHandler(

            filename=self.audit_file,

            maxBytes=MAX_AUDIT_FILE_SIZE,

            backupCount=BACKUP_COUNT,

            encoding="utf-8",
        )

        self._logger.addHandler(
            handler
        )

    # ========================================================
    # WRITE AUDIT EVENT
    # ========================================================

    def log(
        self,
        event_type: AuditEventType,
        request_id: str,
        severity: AuditSeverity = (
            AuditSeverity.INFO
        ),
        **kwargs,
    ) -> AuditEvent:

        try:

            event = AuditEvent(

                event_id=str(
                    uuid4()
                ),

                event_type=event_type,

                severity=severity,

                request_id=request_id,

                **kwargs,
            )

            serialized = (
                event.model_dump(
                    mode="json"
                )
            )

            payload = json.dumps(
                serialized,
                separators=(
                    ",",
                    ":"
                ),
                ensure_ascii=False,
            )

            with self._lock:

                self._logger.info(
                    payload
                )

            return event

        except Exception as e:

            logger.exception(
                "Failed to write audit event"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # PERMISSION EVENT
    # ========================================================

    def log_permission_check(
        self,
        request_id: str,
        agent_id: str,
        agent_name: str,
        agent_type: str,
        action: str,
        resource: str,
        decision: str,
        reason: str,
        user_id: str | None = None,
        metadata: dict | None = None,
    ):

        return self.log(

            event_type=(
                AuditEventType.PERMISSION_CHECK
            ),

            request_id=request_id,

            agent_id=agent_id,

            agent_name=agent_name,

            agent_type=agent_type,

            user_id=user_id,

            action=action,

            resource=resource,

            decision=decision,

            reason=reason,

            metadata=metadata or {},
        )

    # ========================================================
    # POLICY EVENT
    # ========================================================

    def log_policy_evaluation(
        self,
        request_id: str,
        agent_id: str,
        agent_name: str,
        action: str,
        decision: str,
        reason: str,
        policy_name: str | None = None,
        policy_version: str | None = None,
        metadata: dict | None = None,
    ):

        return self.log(

            event_type=(
                AuditEventType.POLICY_EVALUATION
            ),

            request_id=request_id,

            agent_id=agent_id,

            agent_name=agent_name,

            action=action,

            decision=decision,

            reason=reason,

            policy_name=policy_name,

            policy_version=policy_version,

            metadata=metadata or {},
        )

    # ========================================================
    # RISK EVENT
    # ========================================================

    def log_risk_assessment(
        self,
        request_id: str,
        agent_id: str,
        agent_name: str,
        decision: str,
        reason: str,
        risk_level: str,
        fraud_probability: float,
        risk_score: float,
        model_name: str,
        model_version: str | None = None,
        metadata: dict | None = None,
    ):

        return self.log(

            event_type=(
                AuditEventType.RISK_ASSESSMENT
            ),

            request_id=request_id,

            agent_id=agent_id,

            agent_name=agent_name,

            decision=decision,

            reason=reason,

            risk_level=risk_level,

            fraud_probability=(
                fraud_probability
            ),

            risk_score=risk_score,

            metadata={
                **(metadata or {}),
                "model_name": model_name,
                "model_version": model_version,
            },
        )

    # ========================================================
    # BUDGET EVENT
    # ========================================================

    def log_budget_evaluation(
        self,
        request_id: str,
        agent_id: str,
        agent_name: str,
        agent_type: str,
        decision: str,
        reason: str,
        amount: Decimal,
        budget_limit: Decimal,
        remaining_budget: Decimal,
        currency: str = "INR",
        metadata: dict | None = None,
    ):

        return self.log(

            event_type=(
                AuditEventType.BUDGET_EVALUATION
            ),

            request_id=request_id,

            agent_id=agent_id,

            agent_name=agent_name,

            agent_type=agent_type,

            decision=decision,

            reason=reason,

            amount=amount,

            budget_limit=budget_limit,

            remaining_budget=remaining_budget,

            currency=currency,

            metadata=metadata or {},
        )

    # ========================================================
    # GOVERNANCE DECISION
    # ========================================================

    def log_governance_decision(
        self,
        request_id: str,
        agent_id: str,
        agent_name: str,
        decision: str,
        reason: str,
        action: str,
        resource: str,
        user_id: str | None = None,
        amount: Decimal | None = None,
        currency: str | None = None,
        metadata: dict | None = None,
    ):

        severity = (
            AuditSeverity.INFO
        )

        if decision.lower() == "deny":

            severity = (
                AuditSeverity.WARNING
            )

        elif decision.lower() == "escalate":

            severity = (
                AuditSeverity.HIGH
            )

        return self.log(

            event_type=(
                AuditEventType.GOVERNANCE_DECISION
            ),

            request_id=request_id,

            severity=severity,

            agent_id=agent_id,

            agent_name=agent_name,

            user_id=user_id,

            action=action,

            resource=resource,

            amount=amount,

            currency=currency,

            decision=decision,

            reason=reason,

            metadata=metadata or {},
        )

    # ========================================================
    # MCP EVENT
    # ========================================================

    def log_mcp_execution(
        self,
        request_id: str,
        agent_id: str,
        agent_name: str,
        mcp_server: str,
        mcp_tool: str,
        success: bool,
        action: str | None = None,
        resource: str | None = None,
        reason: str | None = None,
        metadata: dict | None = None,
    ):

        event_type = (
            AuditEventType.MCP_EXECUTION
            if success
            else AuditEventType.MCP_FAILURE
        )

        severity = (
            AuditSeverity.INFO
            if success
            else AuditSeverity.HIGH
        )

        return self.log(

            event_type=event_type,

            request_id=request_id,

            severity=severity,

            agent_id=agent_id,

            agent_name=agent_name,

            action=action,

            resource=resource,

            mcp_server=mcp_server,

            mcp_tool=mcp_tool,

            success=success,

            reason=reason,

            metadata=metadata or {},
        )

    # ========================================================
    # EMERGENCY STOP
    # ========================================================

    def log_emergency_stop(
        self,
        request_id: str,
        agent_id: str,
        agent_name: str,
        reason: str,
        metadata: dict | None = None,
    ):

        return self.log(

            event_type=(
                AuditEventType.EMERGENCY_STOP
            ),

            request_id=request_id,

            severity=(
                AuditSeverity.CRITICAL
            ),

            agent_id=agent_id,

            agent_name=agent_name,

            decision="blocked",

            reason=reason,

            metadata=metadata or {},
        )