![](meta/repo-banner.png)

### Python Library and CLI for the Pwned Password v2 API

[![CI Status][ci-badge]][travis-repo-url]
[![Version][version-badge]][pypi-url]
[![Python Versions][versions-badge]][pypi-url]

## About

From https://haveibeenpwned.com/API/v2#PwnedPasswords:

> Pwned Passwords are more than half a billion passwords which have previously been exposed in data breaches. The service is detailed in the [launch blog post](https://www.troyhunt.com/introducing-306-million-freely-downloadable-pwned-passwords/) then [further expanded on with the release of version 2](https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2). The entire data set is [both downloadable and searchable online via the Pwned Passwords page](https://haveibeenpwned.com/Passwords).

`pwnedpasswords` is a small Python wrapper and command line utility that exposes the functionality of the Pwned Passwords API.

## Installation

pwnedpasswords is available for download through [PyPi][pypi-url]. You can install it right away using pip.

```bash
pip install pwnedpasswords
```

## Usage

```python
import pwnedpasswords
password = pwnedpasswords.Password("testing 123")

# Return the number of times `testing 123` appears in the Pwned Passwords database.
password.check()
```

And that's it! :tada:

#### Notes

pwnedpasswords will automatically check to see if your provided input looks like a SHA-1 hash. If it looks like plain text, it'll automatically hash it before sending it to the Pwned Passwords API.

If you'd like to provide an already-hashed password as input, you don't need to do anything special--pwnedpasswords will detect that it looks like a SHA-1 hash and will not hash it again before providing it as input to the Pwned Passwords API.

```python
password = pwnedpasswords.Password("b8dfb080bc33fb564249e34252bf143d88fc018f")
```

Likewise, if a password *looks* like a SHA-1 hash, but is actually a user-provided password, set `plain_text` to `True`, so that the library knows to hash it before checking it against the database.

```python
password = pwnedpasswords.Password("1231231231231231231231231231231231231231", plain_text=True)
```

## Details

### `check`

This is the preferred method. By default, the `check` method uses the `https://api.pwnedpasswords.com/range/` endpoint, which is [k-anonymous][k-anonymous-url].

```python
password = pwnedpasswords.Password("username")
password.check()
# 8340
```

If you'd like to force pwnedpasswords to use the search endpoint instead (https://api.pwnedpasswords.com/pwnedpassword/), set the `anonymous` parameter to `False`.

```python
password = pwnedpasswords.Password("password")
password.check(anonymous=False)
# 3303003
```

You might want to do this if you'd prefer faster response times, and aren't that worried about leaking passwords you're searching for over the network.

If you'd like direct access to the search and range endpoints, you can also call them directly.

### `search`

```python
password = pwnedpasswords.Password("testing 123")
password.search()
# outputs 1
```

### `range`

```python
password = pwnedpasswords.Password("098765")
password.range()
# outputs a dictionary mapping SHA-1 hash suffixes to frequency counts
```

## Command Line Utility

pwnedpasswords comes bundled with a handy command line utility for checking passwords against the Pwned Passwords database.

```bash
$ pwnedpasswords 123456password
240
```

The output is simply the number of entries returned from the Pwned Passwords database.

The CLI returns an exit code equal to the base-10 log of the result count, plus 1. If there are no matches in the API, the exit status will be `0`. While returning the base-10 log might seem odd, note that most systems require exit status codes to be in the range 0-127, and I wanted the status code to provide *some* indication for severity. log(N) seemed to be a good tradeoff. The exit status is log(N)+1 since there are plenty of matches in the database with 1 match.

If you'd like to take a look under the hood to make sure things are working as they should, set the `--verbose` flag.

```bash
$ pwnedpasswords 123456password --verbose
INFO:pwnedpasswords.pwnedpasswords:https://api.pwnedpasswords.com/range/5052C
INFO:pwnedpasswords.pwnedpasswords:Entry found
240
```

## Thanks

Special thanks to [Troy Hunt](https://www.troyhunt.com) for collecting this data and providing this service.

## Authors

Dan Loewenherz / ([@dlo](https://github.com/dlo))

## License

Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

[ci-badge]: https://img.shields.io/travis/lionheart/pwnedpasswords.svg?style=flat
[version-badge]: https://img.shields.io/pypi/v/pwnedpasswords.svg?style=flat
[versions-badge]: https://img.shields.io/pypi/pyversions/pwnedpasswords.svg?style=flat

[travis-repo-url]: https://travis-ci.org/lionheart/pwnedpasswords
[k-anonymous-url]: https://en.wikipedia.org/wiki/K-anonymity
[semver-url]: http://www.semver.org
[pypi-url]: https://pypi.python.org/pypi/pwnedpasswords

