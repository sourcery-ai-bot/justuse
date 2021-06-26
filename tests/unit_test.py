import os
import sys

here = os.path.split(os.path.abspath(os.path.dirname(__file__)))
src = os.path.join(here[0], "src")
sys.path.insert(0,src)

import warnings

from pathlib import Path
from unittest import TestCase
from unittest import skip

import pytest
import use

from yarl import URL

def test_other_case():
  with pytest.raises(NotImplementedError):
    use(2)

def test_simple_path():
    foo_path = Path(".tests/foo.py")
    print(f"loading foo module via use({foo_path})")
    mod = use(Path(foo_path), initial_globals={"a": 42})
    assert mod.test() == 42
    
def test_simple_url():
    import http.server
    port = 8089
    svr = http.server.HTTPServer(
      ("", port), http.server.SimpleHTTPRequestHandler
    )
    foo_uri = f"http://localhost:{port}/tests/.tests/foo.py"
    print(f"starting thread to handle HTTP request on port {port}")
    import threading
    thd = threading.Thread(target=svr.handle_request)
    thd.start()
    print(f"loading foo module via use(URL({foo_uri}))")
    with pytest.warns(use.NoValidationWarning):
      mod = use(URL(foo_uri), initial_globals={"a": 42})
      assert mod.test() == 42
    
def test_internet_url():
    foo_uri = "https://raw.githubusercontent.com/greyblue9/justuse/3f783e6781d810780a4bbd2a76efdee938dde704/tests/foo.py"
    print(f"loading foo module via use(URL({foo_uri}))")
    mod = use(
      URL(foo_uri), initial_globals={"a": 42},
      hash_algo=use.Hash.sha256, hash_value="b136efa1d0dab3caaeb68bc41258525533d9058aa925d3c0c5e98ca61200674d"
    )
    assert mod.test() == 42

class UseStr(TestCase):
  def test_module_package_ambiguity(self):
    original_cwd = os.getcwd()
    os.chdir(Path("tests/.tests"))
    with warnings.catch_warnings(record=True) as w:
      warnings.simplefilter("always")
      use("sys")
      w_filtered = [*filter(
          lambda i: i.category is not DeprecationWarning, w)]
      assert len(w_filtered) == 1
      assert issubclass(w_filtered[-1].category, use.AmbiguityWarning)
      assert "local module" in str(w_filtered[-1].message)
    os.chdir(original_cwd)
      
  def test_builtin(self):
    mod = use("sys")
    assert mod.path is sys.path