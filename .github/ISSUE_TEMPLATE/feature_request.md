---
name: Feature Request
description: Suggest an idea for weatherBridge
title: "[FEATURE] "
labels: ["enhancement"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting an improvement to weatherBridge!

  - type: textarea
    id: description
    attributes:
      label: Is your feature request related to a problem?
      description: Describe the problem you're trying to solve
      placeholder: I'm always frustrated when...
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
      description: Describe the solution you'd like
      placeholder: One solution would be to...
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative solutions
      description: Describe alternative solutions or approaches
      placeholder: Another approach would be to...

  - type: textarea
    id: context
    attributes:
      label: Additional context
      description: Add any other context about the feature request here
      placeholder: This feature would be particularly useful when...

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Low
        - Medium
        - High
        - Critical
    validations:
      required: false

