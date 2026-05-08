# Sample MCP Queries

Use these as manual smoke tests from an MCP-compatible client after the server is connected.

## Resources

- Read `portfolio://bio`
- Read `portfolio://projects`
- Read `portfolio://skills`
- Read `portfolio://education`

## Tool

- Call `get_project_details` with `id = "neuropathx"`
- Call `get_project_details` with `id = "breastcancer-xai-evaluation"`
- Call `get_project_details` with `id = "pulsespy"`
- Call `get_project_details` with `id = "missing-project"` and confirm the server returns `project_not_found`

## Example Natural-Language Checks

- "What is Yassien's academic background?"
- "Which projects best demonstrate medical AI?"
- "Show me the project details for NeuroPathX."
- "Which skills have evidence from embedded systems projects?"
