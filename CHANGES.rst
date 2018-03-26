Changelog
=========

1.3.0
-----

- Add `request` param to watcher_getter to have proper execution order
  of finalizers (youtux).

1.2.1
-----

- Swap kill and terminate in watcher_getter finalization, allowing
  for a more polite SIGTERM for terminating child procs on Unix. See
  #15 for details (jaraco)

1.2.0
-----

- Make pylibmc an optional dependency, available as an extra (jaraco)

1.1.15
------

- Fixed hang with updated netcat-openbsd>=1.130.3 (joepvandijken)

1.1.14
------

- Use a different strategy to determine whether xvfb supports (youtux )

1.1.12
------

- use realpath for mysql base dir (bubenkoff)

1.1.11
------

- exclude locked displays for xvfb (bubenkoff)

1.1.7
-----

- django settings fix (olegpidsadnyi)

1.1.3
-----

- django 1.8 support (bubenkoff)

1.1.2
-----

- old django support fix (olegpidsadnyi)

1.1.0
-----

- django 1.7+ support (bubenkoff)

1.0.10
------

- removed auto artifacts cleanup (bubenkoff)

1.0.8
-----

- fixed popen arguments (bubenkoff)

1.0.2
-----

- added port and display getters (bubenkoff)

1.0.1
-----

- Improved documentation (bubenkoff)

1.0.0
-----

- Initial public release
