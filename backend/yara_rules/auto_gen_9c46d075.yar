rule malicious_3_shell_python
{
  meta:
    author = "SentinelX AI"
    date = "2023-10-27"
    description = "Detects a Python script using os.system to launch a Netcat reverse shell to a specific IP and port."
    malware_family = "ReverseShell"
    filename = "malicious_3_shell.py"

  strings:
    $s1 = "import os"
    $s2 = "os.system"
    $s3 = "nc -e /bin/sh"
    $s4 = "10.0.0.1"
    $s5 = "1234"

  condition:
    all of them
}