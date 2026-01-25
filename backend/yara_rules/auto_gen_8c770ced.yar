rule Malware_JS_DynamicExecution_2
{
    meta:
        author = "SentinelX AI"
        date = "2023-10-27"
        description = "Detects JS script using WScript.Shell for system commands, encoded PowerShell, and eval(base64_decode) for dynamic execution."
        filename = "malicious_2_script.js"

    strings:
        $s1 = "new ActiveXObject(\"WScript.Shell\")" ascii wide nocase
        $s2 = "powershell -enc" ascii wide nocase
        $s3 = "eval(base64_decode(" ascii wide nocase

    condition:
        all of them
}