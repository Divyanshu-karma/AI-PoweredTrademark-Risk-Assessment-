# src/rag/risk_engine.py

RISK_MAPPING = {
    "HIGH": [
        "1207",
        "1203",
        "1210",
        "1211",
        "1206",
        "1204",
        "1209.01(c)",  # specific override
    ],
    "MEDIUM-HIGH": [
        "1209",
        "1202",
        "1202.04",
        "1301",
        "1302",
        "1303",
        "1304",
        "1212",
    ],
    "MEDIUM": [
        "904",
        "807",
        "1213",
        "1402",
    ],
    "MEDIUM-LOW": [
        "300",
        "400",
        "600",
        "700",
    ],
    "LOW": [
        "100",
        "200",
        "304",
        "500",
    ]
}

def classify_section(section_id: str) -> str:
    """
    Determine risk level based on TMEP section prefix.
    Longest prefix match wins.
    """

    section_id = section_id.strip()

    # Build list of (risk, prefix) pairs
    rules = []
    for risk, prefixes in RISK_MAPPING.items():
        for prefix in prefixes:
            rules.append((risk, prefix))

    # Sort by prefix length descending (longest first)
    rules.sort(key=lambda x: len(x[1]), reverse=True)

    # Match prefix
    for risk, prefix in rules:
        if section_id.startswith(prefix):
            return risk

    # Conservative fallback
    return "MEDIUM-LOW"


import re


def parse_llm_output(text: str):
    """
    Extract structured issues from LLM output.
    Returns list of dictionaries.
    """

    pattern = (
        r"ISSUE:\s*(.*?)\s*"
        r"TMEP CITATION:\s*§([\d\.\(\)a-zA-Z]+)\s*"
        r"TMEP-BASED EXPLANATION:\s*(.*?)(?=\nISSUE:|\Z)"
    )

    matches = re.findall(pattern, text, re.DOTALL)

    issues = []

    for issue, citation, explanation in matches:
        issues.append({
            "issue": issue.strip(),
            "citation": citation.strip(),
            "explanation": explanation.strip(),
        })

    return issues

def apply_risk_engine(llm_text: str) -> str:
    """
    Convert LLM structured output into final risk-assigned report.
    """

    issues = parse_llm_output(llm_text)

    if not issues:
        return "NO APPLICABLE TMEP PROVISION FOUND."

    final_blocks = []

    for item in issues:
        risk = classify_section(item["citation"])

        block = (
            f"RISK CATEGORY: {risk}\n\n"
            f"ISSUE:\n{item['issue']}\n\n"
            f"TMEP CITATION:\n§{item['citation']}\n\n"
            f"REASONING:\n{item['explanation']}\n\n"
        )

        final_blocks.append(block)

    final_blocks.append(
        "Disclaimer: This assessment is generated for research and "
        "decision-support purposes only. It is not legal advice."
    )

    return "\n".join(final_blocks)

