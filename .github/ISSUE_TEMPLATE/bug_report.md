---
name: Bug Report
description: Report a bug in weatherBridge
title: "[BUG] "
labels: ["bug"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: description
    attributes:
      label: Describe the bug
      description: A clear and concise description of what the bug is.
      placeholder: When I do X, Y happens unexpectedly...
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to reproduce
      description: Steps to reproduce the behavior
      value: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: A clear and concise description of what you expected to happen.
      placeholder: I expected X to happen...
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: |
        examples:
          - **OS**: Ubuntu 22.04 / Windows 10 / macOS 13
          - **Python**: 3.13 / 3.14
          - **Docker**: yes/no
      value: |
        - **OS**: 
        - **Python Version**: 
        - **Installation Method**: 
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant logs/output
      description: Please copy and paste any relevant log output or error messages
      render: shell

  - type: textarea
    id: context
    attributes:
      label: Additional context
      description: Add any other context about the problem here.

