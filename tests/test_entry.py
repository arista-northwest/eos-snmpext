

import sys
import io

from eos_snmpext.entry import run, BASE_OID
from eos_snmpext.contrib import snmp_passpersist as snmp

import pytest

SNMP_EXTENSION = 'hello'

extensions = []

# @pytest.fixture(scope="module", autouse=True)
# def t_stdin(request):
#     stdin = sys.stdin

#     def cleanup():
#         sys.stdin = stdin

#     request.addfinalizer(cleanup)
#     sys.stdin = io.StringIO()

@pytest.fixture(scope="module", autouse=True)
def t_stdouts(request):
    stderr = sys.stderr
    stdout = sys.stdout

    def cleanup():
        sys.stderr = stderr
        sys.stdout = stdout

    request.addfinalizer(cleanup)
    sys.stderr = io.StringIO()
    sys.stdout = io.StringIO()

def test_ping(monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", io.StringIO(u"PING\n"))
    code = run(extensions)
    assert code  == 0
    assert capsys.readouterr().out == "PONG\n"

# def test_hello(monkeypatch, capsys):
#     monkeypatch.setattr(sys, "stdin", io.StringIO(u"get\n.1.3.6.1.4.1.8072.1.3.1.5.255.0\n"))
#     code = run(extensions)
#     assert code  == 0
#     outerr = capsys.readouterr()
#     assert outerr == ".1.3.6.1.4.1.8072.1.3.1.5.255.0"

def test_ext():
    pp = snmp.PassPersist(BASE_OID)
    
    
