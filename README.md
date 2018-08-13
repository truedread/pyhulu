# pyhulu
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Python library for interacting with the E2E encrypted Hulu API

# Usage

First, initialize the `HuluClient` class with a device code, device key, and cookies:

```python
client = pyhulu.HuluClient(device_code, device_key, cookies)
```

`device_code` is a three-digit string or integer (doesn't matter) denoting the device you will make requests as.

`device_key` is a 16-byte AES key that corresponds to the device code you're using. This is used to decrypt the device config response.

`cookies` can either be a cookie jar object or a dict of cookie key / value pairs. This is passed to the `requests` library, so whatever it takes will work. Examples here: http://docs.python-requests.org/en/master/user/quickstart/#cookies.

With the initialized `client` object, you can use the `load_playlist()` method:

```python
client.load_playlist(video_id)
```

`video_id` is either a string or integer denoting the video ID to request a playlist for. This is NOT the ID in the `/watch/` URL! If you view the page source of a `/watch/` page, you'll find `\"content_id\"` which has the actual video ID used by the API.

This method returns a dict of the playlist response, which contains stream and license URLs.

# Installation

To install, clone the repository and run `python setup.py install`.

# To-Do

- [ ] Add to PyPI
- [ ] Add unit tests
- [x] Add documentation
