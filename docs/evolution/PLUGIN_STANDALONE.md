# Standalone Plugin Integration

To use the Innovation & Evolution Gating system as a standalone remote repo plugin:

1. **Repository Structure**:
   Ensure your remote repository contains the `.claude-plugin/` or equivalent marketplace definitions pointing to this framework.

2. **Triggering**:
   Users can invoke the capability by interacting with their agent:
   `@agent run innovation search on this repository`

3. **Remote Execution**:
   The agent will:
   - Clone the target remote repository into a secure sandbox.
   - Inject the `autoresearch-superpowers` skills (specifically `innovation-searching`, `systematic-debugging`, and `test-driven-development`).
   - Run the V&V baselining.
   - Execute the search loop.
   - Push the winning branch back to the remote as a Pull Request, complete with the Evolution Gate pass report.

4. **Continuous Evolution (Cron/Webhooks)**:
   This plugin can be hooked into GitHub Actions or GitLab CI to run periodically, constantly searching for dependency updates or architectural improvements and submitting them only if they pass the Evolution Gate.
