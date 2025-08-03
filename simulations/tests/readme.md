# Integration Tests

Contains tests validating simulation outputs.

## Running the tests

Install dependencies and execute:

```bash
pytest simulations/tests
```

These tests check that geometry exporters create complete glTF/JSON files and
that the Blender import stubs correctly load the generated meshes.
