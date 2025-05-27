import re

def shorten_function_code(code_str: str, cutoff_lines: int = 30, exclude_last: int = 0) -> str:
    # TODO: Do this with ASTs instead of regexes, should be more reliable and easier

    # Find the function definition by locating 'def priority' and capturing until the colon
    function_match = re.search(r"def priority[\s\S]*?:", code_str)
    if not function_match:
        raise ValueError("Function definition not found.")

    # Start the shortened code with the cleaned function signature
    shortened_code = "def priority(...):\n\t"

    # Extract everything after the function definition
    function_body_start = function_match.end()
    function_body = code_str[function_body_start:].strip()

    # Remove all docstrings or triple-quoted blocks inside the function body
    function_body = re.sub(r'"""[\s\S]*?"""', '', function_body)

    # Split into lines for processing
    body_lines = function_body.splitlines()

    # Remove any stray annotation lines right after the def line
    # For JSSP:
    while body_lines and (body_lines[0].strip().endswith(",")
                          or body_lines[0].strip().startswith("blocks")
                          or body_lines[0].strip().startswith("action_mask")
                          or body_lines[0].strip().startswith(") -> np.ndarray")):
        body_lines.pop(0)
    # For FlatPack:
    # while body_lines and (
    #         body_lines[0].strip().startswith("np.") or body_lines[0].strip().endswith(") -> np.ndarray:")):
    #     body_lines.pop(0)

    # Exclude the last 'exclude_last' lines from consideration
    if exclude_last > 0:
        body_lines = body_lines[:-exclude_last]

    # Adjust cutoff to consider that lines were excluded
    adjusted_cutoff = cutoff_lines

    # If the body is too long, keep only the last 'adjusted_cutoff' lines and prepend '...'
    if len(body_lines) > adjusted_cutoff:
        kept_lines = ["...\n"] + body_lines[-adjusted_cutoff:]
    else:
        kept_lines = body_lines

    # Reconstruct the shortened body
    shortened_body = "\n".join(kept_lines)
    shortened_code += shortened_body

    return shortened_code