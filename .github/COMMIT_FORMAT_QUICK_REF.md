# Quick Reference: Workflow Commits & Tagging

## TL;DR - Commit Message Format

Use one of these prefixes in your commit messages to trigger automatic version tags:

```bash
# PATCH version bump (v1.0.0 → v1.0.1)
git commit -m "fix: description of bug fix"

# MINOR version bump (v1.0.0 → v1.1.0)
git commit -m "feat: description of new feature"

# MAJOR version bump (v1.0.0 → v2.0.0) - Include breaking change notice
git commit -m "refactor: major API changes

BREAKING CHANGE: old API no longer supported"
```

## Complete Examples

### Example 1: Bug Fix (Patch)
```bash
git commit -m "fix: resolve weather data parsing issue with decimal values"
# Result: v1.2.3 → v1.2.4
```

### Example 2: New Feature (Minor)
```bash
git commit -m "feat: add support for multiple weather station types"
# Result: v1.2.4 → v1.3.0
```

### Example 3: Breaking Change (Major)
```bash
git commit -m "refactor: restructure API endpoints

BREAKING CHANGE: /weather endpoint returns different JSON format"
# Result: v1.3.0 → v2.0.0
```

### Example 4: Documentation (No Bump)
```bash
git commit -m "docs: update README with new API examples"
# Result: No tag created
```

## Commit Types That Create Tags

| Type | Bump | Example |
|------|------|---------|
| `feat:` | Minor | New functionality |
| `fix:` | Patch | Bug fixes |
| `BREAKING CHANGE:` | Major | Incompatible changes |

## Commit Types That DON'T Create Tags

| Type | Reason |
|------|--------|
| `docs:` | Documentation only |
| `style:` | Code formatting |
| `refactor:` | Code restructure (unless breaking) |
| `test:` | Test additions |
| `chore:` | Maintenance |

## The Automatic Process

```
You push to master
    ↓
Workflow runs tests
    ↓
Tests pass
    ↓
Analyzes your commit message
    ↓
Finds feat:, fix:, or BREAKING CHANGE
    ↓
Calculates new version (semantic versioning)
    ↓
Creates git tag (v1.2.3)
    ↓
Creates GitHub Release with release notes
    ↓
✓ Done!
```

## What Gets Generated Automatically

- **Version Tag**: `v1.2.3` (semantic versioning)
- **GitHub Release**: With changelog and release notes
- **Release Notes**: Auto-generated from commit messages
- **Timestamp**: Current date/time

## To Manually Check Workflow

1. Go to: GitHub Repository → Actions tab
2. Select: "Tag on Commit to Master"
3. View the latest run with full logs
4. Look for "New tag" output in logs

## Safety Features

✅ **Only on master branch** - Other branches don't create tags
✅ **Only if tests pass** - Tests must succeed first
✅ **Conventional commits only** - Prevents random tags
✅ **Semantic versioning** - Automated version calculation
✅ **Annotated tags** - Proper git history tracking

## Need to Create Tag Manually?

```bash
# Create and push annotated tag
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3

# This triggers: build-docker-on-tag.yml workflow
# Result: Docker image pushed to GHCR
```

## Workflow Triggers

| Event | Workflow | Action |
|-------|----------|--------|
| Push to master | tag-repo-on-commit | Create tag + release |
| Tag created | build-docker-on-tag | Build + push Docker |
| Pull request | test-on-pull-request | Run tests |
| Push (non-master) | run-test-on-push | Run tests |

---

**Need more details?** See `.github/TAG_ON_COMMIT_TROUBLESHOOTING.md`

