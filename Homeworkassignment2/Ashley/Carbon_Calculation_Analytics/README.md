# HA2 — Carbon Calculation & Analytics (Ashley)

## What is included

| File | Purpose |
| --- | --- |
| `processor_base.py` | Local ABC `CarbonProcessor` with an abstract `process()` method. |
| `scope_filter.py` | `ScopeFilter`, a concrete processor selecting Scope 1/2/3 events. |
| `emission_transformer.py` | `EmissionTransformer`, a concrete processor calculating kg and metric tonnes CO2e. |
| `demo_ashley.py` | Standalone demonstration using two hypothetical electricity events. |
| `test_ashley_ha2.py` | Automated independent tests, including a dictionary/iterator compatibility test. |

The source files use only Python's standard library. There is **no** import from `shared`, `Sahra`, `Nooshin`, or `Busra`. Both processors inherit from the local `CarbonProcessor` and use a consistent `.process(record)` interface.

## Run

From the repository root:

```powershell
python Homeworkassignment2/Ashley/demo_ashley.py
python -m unittest discover -s Homeworkassignment2/Ashley -p "test_*.py" -v
```

Running `demo_ashley.py` directly through the VS Code *Run Python File* button also works.

Expected demonstration output:

```text
Record 1: 0.04800 t CO2e
Record 2: 0.06000 t CO2e
```

## Input / output contract

`ScopeFilter.process(record)` accepts an event mapping (usually a dictionary) that includes `scope` or `scope_tag`. It returns a **new** dictionary for matching records and `None` otherwise.

`EmissionTransformer.process(record)` accepts a scoped dictionary, finds its activity-specific factor, checks quantity, units, scope and factor year, and adds calculated emissions. It returns another **new** dictionary without mutating the input.

The demo uses an electricity record containing `record_id`, `building_id`, `timestamp`, and `electricity_kwh`, plus an adapter that sets `scope=2` without changing Sahra's original data. For other activities, use `activity_type`, `quantity`, `unit`, `scope`, and a matching factor configuration.

## Team integration

Sahra's `EnergyStream` can supply dictionaries, Nooshin's `InsightProcessor` can receive the transformed dictionaries, and Büşra's `ProcessingPipeline` can call `.process(record)` on each stage. A pipeline should skip `None` results. It should not require all steps to have exactly the same Python parent type unless the team later agrees to refactor into a single shared hierarchy.

The end-to-end team pipeline has **not** been integrated into this standalone package. Tests use simulated dictionaries compatible with Sahra's agreed format.

## Notes on emissions factors

Example factor `0.4 kg CO2e/kWh` is hypothetical and must not be used as if sourced for formal GHG reporting. This code checks factor value, activity, scope, year, and unit, not full jurisdiction or accounting-boundary applicability.

## UML

See `docs/ASHLEY_HA2_UML.md` in the package for the Mermaid class diagram. For HA2 submission, the team README should also include the other three members' UML diagrams and the team video link.
