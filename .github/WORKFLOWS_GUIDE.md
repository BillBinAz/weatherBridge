# GitHub Actions Workflow Guide

This document explains all GitHub Actions workflows in the weatherBridge project and how to use them.

## 📋 Workflow Overview

### Testing & CI/CD Workflows

#### 1. **Test on Pull Request** (`test-on-pull-request.yml`)
- **Trigger:** Pull requests to `develop`, `dev`, `feature/*`, and `master` branches
- **What it does:**
  - Runs Python tests (3.13, 3.14)
  - Lint with flake8 (critical + non-blocking)
  - Coverage reporting to Codecov
  - Adds coverage comment to PR
- **Status Badge:** See PR for test results
- **On failure:** PR cannot be merged until tests pass

#### 2. **Run Tests on Push** (`run-test-on-push.yml`)
- **Trigger:** Pushes to all branches except `master`
- **What it does:**
  - Runs tests on feature branches
  - Provides fast feedback during development
- **Status Badge:** Check branch status in Actions tab
- **On failure:** Non-blocking, doesn't prevent merging

#### 3. **Tag Repo on Commit** (`tag-repo-on-commit.yml`)
- **Trigger:** Pushes to `master` branch
- **What it does:**
  - Runs full test suite
  - Automatically bumps version tag
  - Creates GitHub release with changelog
- **Version scheme:** Semantic versioning (v1.0.0)
- **Release notes:** Auto-generated from commit messages

#### 4. **Monthly Test and Tag** (`monthly-test-and-tag.yml`)
- **Trigger:** Scheduled monthly (1st at 4 AM UTC)
- **What it does:**
  - Runs full test suite
  - Creates monthly release tag
  - Generates release notes
- **Purpose:** Ensures compatibility across Python versions monthly
- **Schedule:** 1st of each month at 4 AM UTC

---

### Docker Build Workflows

#### 5. **Build Docker on PR** (`build-docker-on-pr.yml`)
- **Trigger:** Pull requests to `master`
- **What it does:**
  - Runs full test suite
  - Builds Docker image
  - Pushes with PR-specific tag
- **Image tag format:** `billbinaz/weatherbridge:pr-XX`, `billbinaz/weatherbridge:sha-XXXXX`
- **Purpose:** Verify Docker build before merge

#### 6. **Build Docker on Tag** (`build-docker-on-tag.yml`)
- **Trigger:** Git tags matching `v*` (e.g., v1.0.0)
- **What it does:**
  - Runs full test suite
  - Builds Docker image
  - Pushes to GHCR (GitHub Container Registry)
  - Pushes to Docker Hub
  - Creates semantic version tags
- **Tags:**
  - `ghcr.io/billbinaz/weatherbridge:v1.0.0`
  - `ghcr.io/billbinaz/weatherbridge:latest`
  - `billbinaz/weatherbridge:v1.0.0`
  - `billbinaz/weatherbridge:latest`
- **Purpose:** Release-quality Docker images

---

### Security & Quality Workflows

#### 7. **Security Scanning** (`security-scan.yml`)
- **Trigger:**
  - Push to `master`/`develop`
  - Pull requests to `master`/`develop`
  - Weekly schedule (Monday 2 AM UTC)
- **Scanners:**
  - **Trivy:** Container/filesystem vulnerability scanning
  - **Safety:** Python dependency vulnerability database
  - **Bandit:** Python code security issues
  - **CodeQL:** Advanced code analysis
- **Results:** Published to GitHub Security tab (Vulnerabilities)
- **On failure:** Non-blocking, allows PR to merge

#### 8. **Code Quality** (`code-quality.yml`)
- **Trigger:**
  - Push to `master`/`develop`
  - Pull requests to `master`/`develop`
- **Checks:**
  - **Black:** Code formatting
  - **isort:** Import sorting
  - **Pylint:** Code style (non-blocking)
  - **mypy:** Type checking (non-blocking)
  - **Radon:** Code complexity analysis
- **Results:** Comments added to PR with quality report
- **On failure:** Non-blocking, allows PR to merge

#### 9. **Stale Issues** (`stale-issues.yml`)
- **Trigger:** Daily (2 AM UTC)
- **What it does:**
  - Marks issues as stale after 60 days of inactivity
  - Closes stale issues after 7 more days
  - Closes stale PRs after 7 days of inactivity
- **Exempt labels:** `bug`, `enhancement`, `help-wanted`, `security`
- **Purpose:** Keep repository clean and active

---

## 🚀 How to Use

### Creating a Pull Request
1. Create your feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Push to GitHub: `git push origin feature/my-feature`
4. Create PR via GitHub UI
5. **Workflows will automatically run:**
   - ✅ Tests on PR (required to pass before merge)
   - ✅ Code quality checks (non-blocking)
   - ✅ Security scans (if on master/develop)
   - ✅ Docker build (if PR to master)

### Merging to Master
1. Ensure all checks pass (green checkmarks)
2. Get code review approval
3. Merge PR
4. **Workflows will automatically:**
   - ✅ Run full test suite
   - ✅ Bump version tag (auto-detect release type)
   - ✅ Create GitHub release
   - Email notification on success/failure

### Creating a Manual Release
1. Push code to `master`
2. Wait for release automation
3. Or manually create a tag: `git tag v1.0.0 && git push --tags`
4. **Workflow will automatically:**
   - ✅ Run tests
   - ✅ Build Docker images
   - ✅ Push to registries
   - ✅ Create GitHub release

---

## 📊 Dependency Management (Dependabot)

### Automated Updates
Dependabot automatically creates PRs for:
- Python package updates (weekly Monday 3 AM UTC)
- GitHub Actions updates (weekly Monday 4 AM UTC)

### How It Works
1. Dependabot detects outdated dependencies
2. Creates automatic PR with updated versions
3. Runs full test suite on the PR
4. If tests pass, you can merge automatically or review first
5. Commit message includes type and scope: `chore(deps): package@newversion`

### Labels
- Dependencies from pip: `dependencies`, `python`
- GitHub Actions: `ci/cd`, `github-actions`

---

## ⚙️ Configuration Files

### `.github/dependabot.yml`
Controls automated dependency updates
- Pip updates: Weekly Monday 3 AM UTC
- GitHub Actions: Weekly Monday 4 AM UTC
- Max 5 open PRs at once to avoid overwhelming

### `.github/ISSUE_TEMPLATE/`
Templates for:
- `bug_report.md` - Report bugs
- `feature_request.md` - Request features

### `.github/pull_request_template.md`
Template for PR descriptions and checklist

---

## 🔍 Monitoring & Status

### Check Workflow Status
1. Go to Actions tab in GitHub
2. See all workflow runs
3. Click on specific workflow for logs
4. Each job has detailed output

### Viewing Test Results
- PR checks: Shows above merge button
- Coverage: Codecov badge and comments
- Security: GitHub Security tab

### Getting Notifications
- Failed workflow: Email notification
- PR comments: @mention notifications
- Security alerts: GitHub Alerts tab

---

## 🐛 Troubleshooting

### Tests fail locally but pass in GitHub
- Check Python version: `python --version` (should be 3.13 or 3.14)
- Check dependencies: `pip install -r requirements.txt`
- Check PYTHONPATH: Should include `./src`

### Workflow takes too long
- First run: Longer (downloading dependencies, caching)
- Subsequent runs: Faster (using cache)
- Check Actions tab for bottleneck step

### Docker build fails
- Ensure Dockerfile exists and is valid
- Check build log in Actions tab for specific error
- Verify secrets if pushing to registry

### Dependabot PRs fail tests
1. Review the version changes
2. Check for breaking changes
3. Run tests locally first: `python -m pytest`
4. Update code if necessary
5. Re-run workflow if infrastructure issue

---

## 📈 Performance Tips

1. **Caching:** Pip dependencies cached automatically
2. **Parallel jobs:** Some workflows run jobs in parallel
3. **Branch protection:** Only required workflows block merge
4. **Scheduled tasks:** Off-peak hours (UTC) to reduce congestion

---

## 🔐 Security Notes

- Workflows use `secrets.GITHUB_TOKEN` (minimum required permissions)
- No credentials stored in workflow files
- Security scans check for vulnerabilities
- Dependabot updates include security patches
- Never commit sensitive data to `.github/`

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Workflow Syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [Dependabot Docs](https://docs.github.com/dependabot)
- [CodeQL Documentation](https://codeql.github.com/)

---

**Last Updated:** April 30, 2026
**Maintained by:** weatherBridge Team

