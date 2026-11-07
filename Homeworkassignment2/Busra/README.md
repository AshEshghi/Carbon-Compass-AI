# Hometask 2 – ProcessingPipeline

**Student:** Büsra Aydın  
**Subsystem:** Web Interface  
**Project:** Carbon Compass AI

## Overview

This module implements a `ProcessingPipeline` class for an event-driven data processing system.

Its main purpose is to connect multiple processing steps using Python operator overloading.

## OOP Concept: Operator Overloading

The `ProcessingPipeline` class implements the `__or__` method, allowing processing steps to be connected with the `|` operator.

Example:

`ProcessingPipeline() | ScopeFilter((2,)) | EmissionTransformer(FACTOR_CONFIG)`

## Main Methods

- `__init__()` – Initializes the processing steps.
- `get_steps()` – Returns a copy of the processing steps.
- `__or__()` – Connects a new processing step.
- `process()` – Processes a single record through the pipeline.
- `process_stream()` – Processes records sequentially using a generator.

## Integration

The pipeline has been tested with:

- Sahra's `EnergyStream`
- Ashley's `ScopeFilter`
- Ashley's `EmissionTransformer`
- Nooshin's `InsightProcessor`

Records that do not match the selected scope are filtered out. Valid records are transformed into carbon emission results.

The pipeline also integrates Nooshin's `InsightProcessor` to generate AI-based sustainability explanations using the calculated emission data.

## UML Class Diagram

- [View UML Diagram](HA2_ProcessingPipeline_UML.png)
- [Editable UML Diagram](HA2_ProcessingPipeline_UML.drawio)

## Testing

The `test_processing_pipeline.py` script demonstrates operator overloading, record filtering, emission calculation, and stream processing.

The integration tests produced the expected results using hypothetical emission factors.

## Group Video

The five-minute group video link will be added to the final team README.
