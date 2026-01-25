rule JS_Malware_WScriptShell_PowerShellEnc_EvalB64
{
    meta:
        author = "SentinelX AI"
        date = "2023-10-27"
        description = "Detects JavaScript using WScript.Shell to run encoded PowerShell via cmd.exe, followed by an eval(base64_decode()) call."
        filename = "malicious_2_script.js"
        malware_family = "JS.ObfuscatedCommand"

    strings:
        $s1 = "WScript.Shell" ascii wide
        $s2 = "cmd.exe /c powershell -enc" ascii wide
        $s3 = "eval(base64_decode(" ascii wide

    condition:
        all of them
}