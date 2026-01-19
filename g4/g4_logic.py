import re
import config

def contains_keyword(text, keywords):
    text = text.lower()
    return any(k in text for k in keywords)

def is_register_requirement(text):
    return contains_keyword(text, config.REGISTER_KEYWORDS)

def is_communication_requirement(text):
    return contains_keyword(text, config.COMMUNICATION_KEYWORDS)

def is_fault_requirement(text):
    return contains_keyword(text, config.FAULT_KEYWORDS)

def is_io_requirement(text):
    return contains_keyword(text, config.IO_KEYWORDS)

def is_functional_requirement(text):
    return contains_keyword(text, config.FUNCTIONAL_KEYWORDS)

def check_g41_testability(text):
    if is_register_requirement(text):
        return "Analysis"

    if (
        is_communication_requirement(text)
        or is_fault_requirement(text)
        or is_io_requirement(text)
        or is_functional_requirement(text)
    ):
        return "Test"

    return "Manual"

def extract_verification_method(text):
    match = re.search(config.VERIFICATION_METHOD_REGEX, text, re.IGNORECASE)
    return match.group(1).capitalize() if match else "NA"

def check_g45(text):
    return "PASS" if re.search(config.MANDATORY_WORD_REGEX, text, re.IGNORECASE) else "FAIL"
