<!-- <p align="center">
  <img width="344" height="225" src="meta/repo-banner-small.png" />
</p> -->

![](meta/repo-banner.png)
[![](meta/repo-banner-bottom.png)][lionheart-url]

[![CI Status][ci-badge]][travis-repo-url]
[![Version][version-badge]][pypi-url]
[![Python Versions][versions-badge]][pypi-url]

`pwnedpasswords` is a small Python wrapper and command line utility that lets you check if a passphrase has been pwned using the [Pwned Passwords v2 API](https://haveibeenpwned.com/API/v2#PwnedPasswords). All provided password data is [k-anonymized][k-anonymous-url] before sending to the API, so plaintext passwords never leave your computer.

From https://haveibeenpwned.com/API/v2#PwnedPasswords:

> Pwned Passwords are more than half a billion passwords which have previously been exposed in data breaches. The service is detailed in the [launch blog post](https://www.troyhunt.com/introducing-306-million-freely-downloadable-pwned-passwords/) then [further expanded on with the release of version 2](https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2). The entire data set is [both downloadable and searchable online via the Pwned Passwords page](https://haveibeenpwned.com/Passwords).

### Installation

pwnedpasswords is available for download through [PyPi][pypi-url]. You can install it right away using pip.

```bash
pip install pwnedpasswords
```

### Usage

```python
import pwnedpasswords

pwnedpasswords.check("testing 123")
# Returns 1
```

#### Security Note

No plaintext passwords ever leave your machine using pwnedpasswords.

How does that work? Well, the Pwned Passwords v2 API has a pretty cool [k-anonymity][k-anonymous-url] implementation.

From https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/:

> Formally, a data set can be said to hold the property of k-anonymity, if for every record in a released table, there are k − 1 other records identical to it.

This allows us to only provide the first 5 characters of the SHA-1 hash of the password in question. The API then responds with a list of SHA-1 hash suffixes with that prefix. On average, that list contains 478 results.

People smarter than I am have used [math](https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/) to show that 5-character prefixes are sufficient to maintain k-anonmity.

In short: your plaintext passwords are protected if you use this library. You won't leak enough data to identity which passwords you're searching for.

#### Notes

pwnedpasswords automatically checks if your provided input looks like a SHA-1 hash. If it does, it won't do any further processing. If it looks like plain text, it'll automatically hash it before sending it to the Pwned Passwords API.

If you'd like to provide an already-hashed password as input to pwnedpasswords, you don't need to do anything--pwnedpasswords will detect that it looks like a SHA-1 hash and won't hash it again before sending it to the `range` endpoint.

```python
pwnedpasswords.check("b8dfb080bc33fb564249e34252bf143d88fc018f")
```

Likewise, if a password looks like a SHA-1 hash (i.e., matches the regex `[0-9a-fA-F]{40}`) but is actually a user-provided password, set `plain_text` to `True`, so that the library knows to hash it before sending it to the API.

```python
pwnedpasswords.check("1231231231231231231231231231231231231231", plain_text=True)
```

## Details

### `check`

This is the preferred method. By default, the `check` method uses the `https://api.pwnedpasswords.com/range/` endpoint, which is [k-anonymous][k-anonymous-url].

```python
pwnedpasswords.check("mypassword")
# 34729
```

If you'd like to force pwnedpasswords to use the search endpoint instead (https://api.pwnedpasswords.com/pwnedpassword/), set the `anonymous` parameter to `False`.

```python
pwnedpasswords.check("password", anonymous=False)
# 3303003
```

You might want to do this if you'd prefer faster response times, and aren't that worried about leaking passwords you're searching for over the network.

If you'd like direct access to the search and range endpoints, you can also call them directly.

### `search`

```python
pwnedpasswords.search("testing 123")
# outputs 1
```

### `range`

```python
pwnedpasswords.range("098765")
# outputs a dictionary mapping SHA-1 hash suffixes to frequency counts
```

## Command Line Utility

pwnedpasswords comes bundled with a handy command line utility. Usage is pretty straightforward--just provide the password in question as the first argument:

```bash
$ pwnedpasswords 123456password
240
```

The output is simply the number of entries found in the Pwned Passwords database.

For help, just provide `-h` as a command-line argument.

```bash
$ pwnedpasswords -h
usage: pwnedpasswords [-h] [--plain-text] [--verbose] password

positional arguments:
  password      The password or hashed password to search for.

optional arguments:
  -h, --help    show this help message and exit
  --plain-text  Specify that the provided input is plain text, even if it
                looks like a SHA-1 hash.
  --verbose     Display verbose output.
```

#### Note

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

## See also

[django-pwnedpasswords-validator](https://github.com/lionheart/django-pwnedpasswords-validator), a validator that checks user passwords against the Pwned Passwords API using this library.

## License

Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

[ci-badge]: https://img.shields.io/travis/lionheart/pwnedpasswords.svg?style=flat
[version-badge]: https://img.shields.io/pypi/v/pwnedpasswords.svg?style=flat
[versions-badge]: https://img.shields.io/pypi/pyversions/pwnedpasswords.svg?style=flat

[travis-repo-url]: https://travis-ci.org/lionheart/pwnedpasswords
[k-anonymous-url]: https://en.wikipedia.org/wiki/K-anonymity
[semver-url]: http://www.semver.org
[pypi-url]: https://pypi.python.org/pypi/pwnedpasswords
[lionheart-url]: https://lionheartsw.com/

