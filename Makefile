PYTHON ?= python3
PYTEST ?= pytest

.PHONY: help install test invariants chokepoint snapshot-bless smoke layer_a layer_b layer_c v1 perception extraction_params northena ci frontend-install frontend-build

help:
	@echo "RMS Intelligence System — make targets:"
	@echo "  install        Install backend Python deps."
	@echo "  invariants     Run frozen-contract snapshot tests."
	@echo "  chokepoint     Run the no-direct-LLM-calls-outside-shield guard."
	@echo "  smoke          Backend smoke + fixture roundtrip + adversarial asserts."
	@echo "  layer_a        Layer A handler round-trips."
	@echo "  layer_b        Layer B provider contracts + factory honesty."
	@echo "  layer_c        Layer C aggregator round-trip through Five Rings."
	@echo "  v1             V1 harness (Hard Rule 1, PENDING on synthetic)."
	@echo "  perception     Shield perception_router stubs + trust receipts."
	@echo "  test           Full backend test suite."
	@echo "  ci             invariants + chokepoint + smoke + layer_a + layer_b + layer_c + v1 + perception."

install:
	cd backend && pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

invariants:
	cd backend && $(PYTEST) -q tests/invariants/

chokepoint:
	cd backend && $(PYTEST) -q tests/test_no_direct_llm_calls_outside_shield.py

smoke:
	cd backend && $(PYTEST) -q tests/test_smoke.py tests/test_synthetic_fixture_roundtrip.py

layer_a:
	cd backend && $(PYTEST) -q tests/test_layer_a_handlers.py

layer_b:
	cd backend && $(PYTEST) -q tests/test_layer_b_providers.py

layer_c:
	cd backend && $(PYTEST) -q tests/test_layer_c_aggregator.py

v1:
	cd backend && $(PYTEST) -q tests/test_v1_harness.py

perception:
	cd backend && $(PYTEST) -q tests/test_perception_router.py

extraction_params:
	cd backend && $(PYTEST) -q tests/test_extraction_params_v0.py

northena:
	cd backend && $(PYTEST) -q tests/test_northena_invariants.py

g1_stamper:
	cd backend && $(PYTEST) -q tests/test_g1_stamper_and_v3.py

lift_manifest:
	cd backend && $(PYTEST) -q tests/test_lift_manifest.py

instance_fixture_a:
	cd backend && $(PYTEST) -q tests/test_instance_fixture_a_roundtrip.py

test:
	cd backend && $(PYTEST) -q

snapshot-bless:
	cd backend && $(PYTHON) scripts/bless_snapshots.py

ci: invariants chokepoint smoke layer_a layer_b layer_c v1 perception extraction_params northena g1_stamper lift_manifest instance_fixture_a
	@echo "\nG2a CI gate PASSED."

frontend-install:
	cd frontend && yarn install

frontend-build:
	cd frontend && yarn build
