# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Changed

### Removed

## [3.5.0] - 2020-09-06
### Added
- OwnBackup status checker
- New Relic status checker

### Changed
- [dev] various CI improvements

## [3.4.0] - 2020-09-05
### Added
- Airtable status checker
- [dev] GitHub action to ensure that changelog was updated
- [dev] mypy typing check

### Changed
- Status.io status checkers handle maintenance

## [3.3.0] - 2020-09-03
### Added
- Vercel status checker

### Changed
- [Dev] Dependencies update

## [3.2.0] - 2020-08-24
### Added
- Gandi API status checker
- Twitter API status checker
- Zoom status checker

### Changed
- [Dev] httpx bump 0.14.2

## [3.1.0] - 2020-08-19
### Added
- Confluence status checker
- Coveralls status checker
- Jira status checker
- Trello status checker

### Changed
- [Dev] httpx bump 0.14.1
- [Dev] Dependencies update

## [3.0.0] - 2020-08-09
### Changed

- [Breaking change] Major refactoring of the library core and public APIs
- Unified status and summary data models (using attrs)
- Better typing hints
- Some services contain tests with mocked responses (more to come whenever we'll get more incidents)
- [Dev] Add coverage reports via coveralls.io (current coverage 96%)

## [2.9.0] - 2020-06-16
### Changed
- Add service URLs
- Dependencies update
- [Dev] Add .editorconfig

## [2.8.0] - 2020-05-24
### Changed
- [CI] Switch from Travis CI to GitHub Actions
- Dependencies update

## [2.7.0] - 2020-03-13
### Added
- Nylas status checker

## [2.6.0] - 2020-02-21
### Changed
- Add `StatusIO` outage performance status type
- Add `Heroku` maintenance status type

## [2.5.0] - 2020-02-11
### Changed
- Add `StatusIO` degraded performance status type

## [2.4.1] - 2020-02-10
### Changed
- Use `StatusIO` security type for security incidents

## [2.4.0] - 2020-02-10
### Changed
- Improve `StatusIO` check types
- Dependencies update

## [2.3.1] - 2019-10-27
### Changed
- Drop deprecated pytest-runner
- Dependencies update

## [2.3.0] - 2019-10-26
### Changed
- Handle major Salesforce incidents properly (https://github.com/amureki/statuscheck/pull/76)

## [2.2.0] - 2019-10-24
### Added
- Added CLI option to check all services (useful for debugging and/or gives you a good feeling):
`statuscheck all` (https://github.com/amureki/statuscheck/pull/74)

### Changed
- Fixed Heroku incidents verbose display (https://github.com/amureki/statuscheck/pull/74)

## [2.1.0] - 2019-10-21
### Changed
- Add name to summary, smaller clean ups (https://github.com/amureki/statuscheck/pull/73)

## [2.0.2] - 2019-10-20
### Changed
- Another attempt to fix PyPI release

## [2.0.1] - 2019-10-20
### Changed
- Fix Travis PyPI build

## [2.0.0] - 2019-10-20
### Added
- Code linters and checkers (https://github.com/amureki/statuscheck/pull/72)

### Changed
- API was redesigned to provide unified status results (https://github.com/amureki/statuscheck/pull/71)

## [1.3.0] - 2019-01-21
### Added
- Asana status checker
- CircleCI status checker

## [1.2.0] - 2019-01-21
### Added
- Codecov status checker

## [1.1.0] - 2019-01-20
### Added
- Bitbucket status checker
- Cloudflare status checker
- DigitalOcean status checker
- Mailgun status checker

## [1.0.2] - 2019-01-15
### Changed
- Fix Travis credentials mess caused by .org and .com domains

## [1.0.1] - 2019-01-15
### Changed
- Cleanup Travis config

## [1.0.0] - 2019-01-15
### Added
- Changelog file

### Changed
- Update GitHub service code, since they moved to statuspage.io
- Update dependencies

[Unreleased]: https://github.com/amureki/statuscheck/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/amureki/statuscheck/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/amureki/statuscheck/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/amureki/statuscheck/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.com/amureki/statuscheck/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/amureki/statuscheck/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/amureki/statuscheck/compare/v.0.1.0...v1.0.0
