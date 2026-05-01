# GitHub Actions Workflows Troubleshooting Guide

## Issues Fixed ✅

### 1. **Version Mismatch in Docker Login Action**
- **Issue**: `build-docker-on-pr.yml` used `docker/login-action@v3` while `build-docker-on-tag.yml` used `v4`
- **Impact**: Inconsistent behavior and potential authentication failures
- **Fix**: Updated PR workflow to use `docker/login-action@v4` (consistent with tag workflow)
- **Status**: ✅ FIXED

### 2. **Missing Actions Permission**
- **Issue**: Workflows had insufficient permissions for interacting with GitHub Actions API
- **Impact**: Potential workflow execution failures and dependency issues
- **Fix**: Added `actions: read` permission to `build-docker-on-tag.yml` and `tag-repo-on-commit.yml`
- **Status**: ✅ FIXED

---

## Common Issues & Solutions

### Issue: "Workflows not running on tag push"
**Possible Causes:**

1. **GitHub Actions not enabled in repository**
   - Solution: Go to Settings → Actions → General → Allow all actions and reusable workflows

2. **Tag pattern not matching**
   - Check: Workflow uses `'**'` pattern which should match all tags
   - Verify: Push a test tag: `git tag v0.0.1-test && git push origin v0.0.1-test`

3. **Branch protection rules blocking workflows**
   - Solution: Check Settings → Branches → Branch protection rules
   - Verify: Rules aren't preventing required status checks

4. **Test job failing silently**
   - Check: GitHub Actions logs for the specific workflow run
   - Fix: Run `PYTHONPATH=./src python -m unittest discover tests/ -v` locally

5. **GITHUB_TOKEN permissions insufficient**
   - Solution: Ensure workflow has `packages: write` for container registry access
   - Check: Settings → Actions → General → Workflow permissions → "Read and write permissions"

### Issue: "Container push fails with authentication error"
**Solutions:**

1. **Verify PATNAME is available**
   ```bash
   # In workflow logs, check if token was properly passed
   docker login -u ${{ github.actor }} -p ${{ secrets.PATNAME }} ghcr.io
   ```

2. **Check repository visibility**
   - Private repos might have different token access
   - Solution: Verify `packages: write` permission in workflow

3. **Verify image tag case**
   - GHCR requires lowercase image names
   - Check: Workflow uses `tr '[:upper:]' '[:lower:]'` conversion ✅

### Issue: "Workflows run but don't appear in Actions tab"
**Solutions:**

1. **Check workflow enable status**
   - Go to Actions tab in GitHub
   - Verify workflows aren't disabled

2. **Verify workflow file location**
   - Files must be in `.github/workflows/` directory
   - Current workflows: ✅ All in correct location

3. **Check for workflow syntax errors**
   - GitHub will show warnings if YAML is invalid
   - Solution: Run `yamllint .github/workflows/*.yml` locally

### Issue: "Tests fail but Docker build still completes"
**Solution:**

- Check: Build job has `needs: test` dependency
- Current workflows: ✅ All have proper job dependencies
- Fix: Remove `continue-on-error: true` if you want builds to fail on test failures

---

## Workflow Execution Flow

```
tag-repo-on-commit.yml (triggered by: push to master)
  ├─ test job
  └─ tag_on_release job (needs: test)
       └─ Creates tag v*.*.* via github-tag-action
            └─ Triggers: build-docker-on-tag.yml

build-docker-on-tag.yml (triggered by: push with tag)
  ├─ test job
  └─ build_and_push_to_ghcr job (needs: test)
       └─ Builds and pushes to ghcr.io/$REPO:$TAG
```

---

## Current Workflow Configuration

### Working Workflows ✅
- `test-on-pull-request.yml` - Runs on PR creation
- `run-test-on-push.yml` - Runs on push (non-master branches)
- `build-docker-on-pr.yml` - Builds Docker image on PR
- `security-scan.yml` - Runs security checks
- `monthly-test-and-tag.yml` - Monthly automated testing

### Tag-Triggered Workflows
- `tag-repo-on-commit.yml` - Creates semantic version tags on master push
- `build-docker-on-tag.yml` - Builds and pushes to GHCR on tag creation

---

## Debugging Commands

### Check workflow locally
```bash
# Run tests
PYTHONPATH=./src python -m unittest discover tests/ -v

# Check linting
flake8 . --count --exclude=.git,.github,.venv,__pycache__,.pytest_cache,docs

# Validate YAML
pip install yamllint
yamllint .github/workflows/*.yml
```

### Check GitHub Actions settings
1. Go to repository Settings
2. Navigate to Actions > General
3. Verify:
   - ✅ Actions is enabled
   - ✅ "Allow all actions and reusable workflows" is selected
   - ✅ Workflow permissions shows "Read and write permissions"

### Manual workflow trigger (if needed)
```bash
# For development/testing:
# 1. Go to Actions tab in GitHub
# 2. Select workflow
# 3. Click "Run workflow" → Run workflow
```

---

## Recently Fixed Issues

### `build-docker-on-pr.yml`
- ✅ Updated `docker/login-action` from v3 to v4
- ✅ Consistent with `build-docker-on-tag.yml`

### `build-docker-on-tag.yml`
- ✅ Added `actions: read` permission

### `tag-repo-on-commit.yml`
- ✅ Added `actions: read` permission

---

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Login Action Docs](https://github.com/docker/login-action)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Workflow Permissions](https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs)

---

## Next Steps

1. **Verify workflows are enabled** in GitHub repository settings
2. **Push a test tag** to trigger `build-docker-on-tag.yml`:
   ```bash
   git tag v1.0.1-test
   git push origin v1.0.1-test
   ```
3. **Check Actions tab** for workflow execution
4. **Review logs** if any workflow fails
5. **Test locally** if needed using the commands above

---

## Support

If workflows still don't run after checking all above items:

1. Check GitHub status page: https://www.githubstatus.com/
2. Review Actions logs for specific error messages
3. Verify `.github/workflows/` files are committed and pushed
4. Ensure you have admin access to the repository

