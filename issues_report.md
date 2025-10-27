| Issue Type | Line(s) | Description | Fix Approach |
|---|---|---|---|
| Use of eval() | Security (Medium) | 59 | Bandit (B307) & Pylint (W0123) flagged eval(), which is a security risk that can execute arbitrary code. | Delete line 59 (eval("print('eval used')")). |
| Dangerous Default Value | Bug | 8 | Pylint (W0102) flagged a mutable list ([]) as a default argument. This single list is shared across all function calls. | 1. Change signature to logs=None.<br>2. Add if logs is None: logs = [] as the first line in the function. |
| Bare except / try...pass | Bug (Low) | 19-20 | Pylint (W0702), Flake8 (E722), & Bandit (B110) flagged a bare except:, which hides all errors. | Change except: on line 19 to the specific exception: except KeyError:. |
| Unused Import | Code Quality | 2 | Pylint (W0611) & Flake8 (F401) flagged import logging as unused. | Delete line 2 (import logging). |
| No with for file I/O | Code Quality | 26, 32 | Pylint (R1732) flagged open() being used without a with statement, which can lead to resource leaks. | Rewrite loadData and saveData to use with open(...) as f: and remove f.close(). |
| No file encoding specified | Code Quality | 26, 32 | Pylint (W1514) flagged open() without an explicit encoding, which can break on other systems. | Add encoding="utf-8" to both open() calls (e.g., with open(file, "r", encoding="utf-8") as f:). |
| Use of global | Code Quality | 27 | Pylint (W0603) flagged global-statement. This is discouraged in larger applications. | No fix required for this lab, but for larger projects, refactor the code into a class to manage state. |
| Old-style string formatting | Style | 12 | Pylint (C0209) flagged old % formatting instead of modern f-strings. | Change line 12 to: logs.append(f"{datetime.now()}: Added {qty} of {item}"). |
| Invalid Function Names | Style / Naming | 8, 14, 22, 25, 31, 36, 41 | Pylint (C0103) flagged function names that are not snake_case (e.g., addItem). | Rename all functions (e.g., addItem -> add_item) and update their calls in main(). |
| Missing Module Docstring | Style / Naming | 1 | Pylint (C0114) flagged that the file is missing a top-level docstring. | Add """Simple inventory management system.""" to the first line of the file. |
| Missing Function Docstrings | Style / Naming | 8, 14, 22, 25, 31, 36, 41, 48 | Pylint (C0116) flagged that all functions are missing docstrings. | Add a docstring to each function describing what it does (e.g., """Adds an item to the stock."""). |
| Missing blank lines | Style | 8, 14, 22, 25, 31, 36, 41, 48, 61 | Flake8 (E302, E305) flagged missing vertical whitespace between functions and at end of file. | Add a second blank line before each function definition and ensure two blank lines before the main() call. |
