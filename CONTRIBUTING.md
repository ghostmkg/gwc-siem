# Contributing to gwc-siem

Thank you for your interest in contributing to gwc-siem! Whether you're fixing a bug, improving documentation, or adding a feature, your help is appreciated. This document explains how to get started and the project's expectations for contributions.

## Table of contents
- How to contribute (high-level)
- Reporting issues
- Preparing a change (fork, branch, commit messages)
- Pull request checklist
- Coding style & tests
- Documentation
- Hacktoberfest notes
- Code of Conduct

## How to contribute (high-level)

1. Find something to work on (issues, docs, or ideas).
2. Fork the repository and create a topic branch.
3. Make small, focused changes with clear commits.
4. Open a pull request (PR) with a description of the change.
5. Respond to review feedback and iterate until the PR is merged.

## Reporting issues

- Before opening a new issue, search existing issues to avoid duplicates.
- When creating an issue, include:
  - A descriptive title
  - Steps to reproduce (if applicable)
  - Expected vs actual behavior
  - Environment details (OS, versions) when relevant
  - Minimal reproducible example or logs when possible

If you want help deciding what to work on, check `Contribution_README.md` for suggested tasks and tips.

## Preparing a change (fork, branch, commit messages)

1. Fork the repository to your GitHub account.
2. Clone your fork and add the upstream remote:

   git clone <your-fork-url>
   git remote add upstream https://github.com/haris-bit/gwc-siem.git

3. Create a topic branch with a short, descriptive name:

   git checkout -b fix/clear-description

4. Keep commits small and focused. Use imperative, present-tense commit messages, for example:

   - "Fix: handle null pointer when parsing config"
   - "Docs: improve installation instructions"

5. Rebase or merge from upstream main regularly to keep your branch up to date before opening a PR:

   git fetch upstream; git rebase upstream/main

## Pull request checklist

When opening a PR, include the following in your description:

- What the change does and why
- Any relevant issue number (e.g., "Closes #123")
- How to test the change
- Screenshots or logs if the change affects UI/UX or outputs

Maintainers will review your PR. Expect requests for changes and be responsive. Once approved, a maintainer will merge it.

## Coding style & tests

- Follow the existing code style in the repository. If the project uses linters or formatters, run them before committing.
- Add unit tests for behavioral changes or new features where appropriate.
- Run tests locally and ensure they pass before opening a PR.

If you need help running tests or the project doesn't include tests yet, open an issue and we can help you get set up.

## Documentation

- Improve README sections or add new docs when you add features or change behavior.
- Keep documentation changes in the same PR as code changes when possible, or reference them clearly.

## Hacktoberfest notes

This repository participates in Hacktoberfest. To make sure your PR counts:

- Make meaningful contributions: avoid trivial changes like whitespace-only edits.
- Ensure your PR is merged or accepted before the event's deadline for it to count.
- Label your PR with relevant labels if requested by maintainers. If you want your PR to be considered for Hacktoberfest difficulty labels, ask maintainers via the PR comments.

For more Hacktoberfest guidance, see the event website and the project's `Contribution_README.md`.

## Code of Conduct

By participating in this project, you agree to follow the project's Code of Conduct. Be respectful, constructive, and inclusive.

If the repository doesn't already include a `CODE_OF_CONDUCT.md`, please open an issue or PR to add one.

---

If you have questions or need help getting started, open an issue and tag @haris-bit or any available maintainer. Thanks for contributing!
