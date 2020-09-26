from __future__ import unicode_literals

import unicodedata
import sys

PY2 = sys.version_info[0] == 2

if PY2:
    from urlparse import (
        ParseResult,
        SplitResult,
        _splitnetloc,
        _splitparams,
        scheme_chars,
        uses_params,
    )

    _coerce_args = None
else:
    from urllib.parse import (
        ParseResult,
        SplitResult,
        _coerce_args,
        _splitnetloc,
        _splitparams,
        scheme_chars,
        uses_params,
    )


class CustomUnicodeDecodeError(UnicodeDecodeError):
    def __init__(self, obj, *args):
        self.obj = obj
        UnicodeDecodeError.__init__(self, *args)

    def __str__(self):
        original = UnicodeDecodeError.__str__(self)
        return "%s. You passed in %r (%s)" % (original, self.obj, type(self.obj))


# Derived from Django 1.11.16. Only used in a Python2 branch.
def force_text(s):
    """
    Similar to smart_text, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    encoding = "utf-8"
    errors = "strict"
    # Handle the common case first for performance reasons.
    if issubclass(type(s), unicode):
        return s
    try:
        if not issubclass(type(s), basestring):
            if hasattr(s, "__unicode__"):
                s = unicode(s)
            else:
                s = unicode(bytes(s), encoding, errors)
        else:
            # Note: We use .decode() here, instead of six.text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise CustomUnicodeDecodeError(s, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = " ".join(force_text(arg, encoding, errors) for arg in s)
    return s


# Based on Django 1.11.16 and 2.1.2
# Copied from urllib.parse.urlsplit() with
# https://github.com/python/cpython/pull/661 applied.
def _urlsplit(url, scheme="", allow_fragments=True):
    """
    Parse a URL into 5 components:
    <scheme>://<netloc>/<path>?<query>#<fragment>
    Return a 5-tuple: (scheme, netloc, path, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes.
    """
    if _coerce_args:
        url, scheme, _coerce_result = _coerce_args(url, scheme)
    allow_fragments = bool(allow_fragments)
    netloc = query = fragment = ""
    i = url.find(":")
    if i > 0:
        for c in url[:i]:
            if c not in scheme_chars:
                break
        else:
            start = i + 1
            scheme, url = url[:i].lower(), url[start:]

    if url[:2] == "//":
        netloc, url = _splitnetloc(url, 2)
        if ("[" in netloc and "]" not in netloc) or (
            "]" in netloc and "[" not in netloc
        ):
            raise ValueError("Invalid IPv6 URL")
    if allow_fragments and "#" in url:
        url, fragment = url.split("#", 1)
    if "?" in url:
        url, query = url.split("?", 1)
    v = SplitResult(scheme, netloc, url, query, fragment)
    return _coerce_result(v) if _coerce_args else v


# Based on Django 1.11.16 and 2.1.2
# Copied from urllib.parse.urlparse() but uses fixed urlsplit() function.
def _urlparse(url, scheme="", allow_fragments=True):
    """
    Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes.
    """
    if _coerce_args:
        url, scheme, _coerce_result = _coerce_args(url, scheme)
    splitresult = _urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = splitresult
    if scheme in uses_params and ";" in url:
        url, params = _splitparams(url)
    else:
        params = ""
    result = ParseResult(scheme, netloc, url, params, query, fragment)
    return _coerce_result(result) if _coerce_args else result


# Based on Django 2.1.2
def _is_safe_url(url, allowed_hosts, require_https=False):
    # Chrome considers any URL with more than two slashes to be absolute, but
    # urlparse is not so flexible. Treat any url with three slashes as unsafe.
    if url.startswith("///"):
        return False
    try:
        url_info = _urlparse(url)
    except ValueError:  # e.g. invalid IPv6 addresses
        return False
    # Forbid URLs like http:///example.com - with a scheme, but without a hostname.
    # In that URL, example.com is not the hostname but, a path component. However,
    # Chrome will still consider example.com to be the hostname, so we must not
    # allow this syntax.
    if not url_info.netloc and url_info.scheme:
        return False
    # Forbid URLs that start with control characters. Some browsers (like
    # Chrome) ignore quite a few control characters at the start of a
    # URL and might consider the URL as scheme relative.
    if unicodedata.category(url[0])[0] == "C":
        return False
    scheme = url_info.scheme
    # Consider URLs without a scheme (e.g. //example.com/p) to be http.
    if not url_info.scheme and url_info.netloc:
        scheme = "http"
    valid_schemes = ["https"] if require_https else ["http", "https"]
    return (not url_info.netloc or url_info.netloc in allowed_hosts) and (
        not scheme or scheme in valid_schemes
    )


# Based on Django 1.11.16 and d22b90b4eabc1fe9b7b35aada441e0edf5ebd6d8
def is_safe_url(url, allowed_hosts, require_https=False):
    """
    Return ``True`` if the url is a safe redirection (i.e. it doesn't point to
    a different host and uses a safe scheme).

    Always return ``False`` on an empty url.

    If ``require_https`` is ``True``, only 'https' will be considered a valid
    scheme, as opposed to 'http' and 'https' with the default, ``False``.
    """
    if url is not None:
        url = url.strip()
    if not url:
        return False
    if PY2:
        try:
            url = force_text(url)
        except UnicodeDecodeError:
            return False
    if allowed_hosts is None:
        allowed_hosts = set()
    elif (
        PY2 and isinstance(allowed_hosts, basestring) or isinstance(allowed_hosts, str)
    ):
        allowed_hosts = {allowed_hosts}
    # Chrome treats \ completely as / in paths but it could be part of some
    # basic auth credentials so we need to check both URLs.
    return _is_safe_url(
        url, allowed_hosts, require_https=require_https
    ) and _is_safe_url(
        url.replace("\\", "/"), allowed_hosts, require_https=require_https
    )
