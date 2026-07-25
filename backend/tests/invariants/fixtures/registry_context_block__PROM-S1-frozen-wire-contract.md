## Registry context · promises in force on this task

### Function: PROM-S1-frozen-wire-contract
**Mandate:** Frozen wire contracts land as Pydantic BaseModel envelopes at backend/contracts/<name>.py with model_config extra=forbid.

**Promise:** Landed frozen wire contracts remain byte-identical; changes ride additive versioning (v0 → v1) never in-place mutation.

**Service trace:**
- governance:tiered_ruling_model.md
- governance:registry_doctrine_v1.md
- contract:backend/contracts/service_1_refusal_v1.py