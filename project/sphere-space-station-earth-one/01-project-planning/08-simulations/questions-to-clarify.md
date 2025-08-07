# Questions to Clarify

1. Should `SceneConfiguration` default all modules to `false`, or are some modules considered core and enabled by default?
2. Will module-specific parameters (e.g. number of elevators or reactor output) be stored in the same configuration file or in separate module configs?
3. Where should `full_scene.toml` reside in the repository, and are multiple example configs (minimal/full) expected?
4. Are there additional optional modules beyond the six listed in Sprint L4 that we should account for in an extensible schema?
5. Should the `SceneModel` expose modules via a collection object instead of boolean flags to better support future module metadata?
