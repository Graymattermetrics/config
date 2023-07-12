# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1]

### Changed
- Renamed and moved `machine_paced.incorrect.initial_duration` to `machine_paced.initial_speedup_duration`

### Removed
- Useless `machine_paced.max_count`
- Useless `machine_paced.not_there`
- Useless `machine_paced.not_there_disabled`

## [0.1.0]

### Added
- Max speedup amount in `machine_paced.correct` set to 100ms
- Max slowdown amount in `machine_paced.correct` set to 100ms

### Changed
- `machine_paced.slowdown` has been renamed to `machine_paced.incorrect`
- `machine_paced.speedup` has been renamed to `machine_paced.correct`

[0.1.0]: https://github.com/graymattermetrics/config/commit/d2fcc9008e072c8cc87fe8131ad19ead879af48a#diff-d8d0422389f03d783e32e627250fe29834bd09c6361640d1ff00661dd6820034
[0.1.1]: https://github.com/graymattermetrics/config/commit/86d1f38df049014d84e6c7da92cc0919e00b107d#diff-d8d0422389f03d783e32e627250fe29834bd09c6361640d1ff00661dd6820034