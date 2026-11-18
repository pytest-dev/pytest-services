Here are the steps on how to make a new release.

1. Create a ``release-VERSION`` branch from ``upstream/main``.
2. Update ``CHANGES.rst``.
3. Push the branch to ``upstream`` and open a PR.
4. Once all tests pass, start the ``deploy`` workflow manually or via::

     gh workflow run deploy.yml --repo pytest-dev/pytest-services --ref release-VERSION -f version=VERSION

The workflow publishes the package to PyPI, pushes the ``vVERSION`` tag, creates the GitHub release, and merges the release PR.
