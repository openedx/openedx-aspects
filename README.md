# Aspects

Learner analytics for Open edX!

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. To get started:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
make install

# Serve documentation locally
make serve_docs

# Check documentation builds correctly
make check_docs

# Upgrade dependencies
make upgrade
```

## What is Aspects?

Aspects is an optional implementation of analytics for the Open edX LMS. It is the combined solution of Cairn by Overhang.io and the OARS project developed by Axim Collaborative with a huge amount of help from the Open edX community. Primarily it is intended to be a "batteries included" set of configurations and plugins to combine 3rd party tools into a powerful and flexible system for learner analytics.

## What _isn't_ Aspects?

A deployable application in-and-of itself, it helps deploy other applications together using a Tutor plugin and customizations to the Open edX platform to connect well-supported, existing, third party applications.

## Status

Aspects is in development by efforts from Axim Collaborative and Open edX community contributors. For more information, see:

* [Data Working Group issue board](https://github.com/orgs/openedx/projects/5/views/1): project design, development, and implementation
* [Aspects Documentation](https://docs.openedx.org/projects/openedx-aspects): project documentation
* [tutor-contrib-aspects](https://github.com/openedx/tutor-contrib-aspects): deploys Aspects using Tutor.
