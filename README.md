# Scientific Calculator: LL(1) Parser (Python)

A calculator that **reads and evaluates arithmetic expressions** with a hand-written lexer and a **recursive-descent parser for an attributed LL(1) grammar**: values are computed during parsing, with no intermediate syntax tree. Project for the ENSIMAG *Language Theory* course (LL(1) parsing), 2025-2026. Requires Python 3.10+.

## Supported syntax

| Feature | Syntax | Example |
|---|---|---|
| Numbers | integers and decimals | `12`, `3.5` |
| Operators | `+  -  *  /  ^` | `2+3*4` |
| Power | `^`, right-associative | `2^3^2` gives `512.0` |
| Factorial | `!` | `5!` gives `120` |
| Unary minus | `-` | `-(2+3)` |
| Parentheses | `( )` | `(4-1)^2` |
| Several calculations | separated by `;` | `1+2*3; (4-1)^2;` |
| Result references | `#n` is the value of the n-th previous calculation | `1; 2; #1+#2;` |

Each calculation ends with `;` and the input ends with a newline. The program returns the list of results:

```bash
$ printf '1+2*3;(4-1)^2;#1+#2;5!;\n' | python3 calc.py
@ init parser on 'NUM:1.0'
@ result =  [7.0, 9.0, 16.0, 120]
```

## How it works

1. **Lexer** (`lexer.py`): reads the stream character by character with a three-character look-ahead and builds the tokens. Numbers are recognised with small state machines; unsupported characters raise a `LexerError`.
2. **Grammar** (`calc.py`): the expression grammar is layered by priority, from `exp_5` (addition, subtraction) down to `exp_0` (number, `#n`, parenthesised expression). Left recursion is removed and the grammar is factored so that one token of look-ahead is enough.
3. **Attributes**: each parsing function returns the value of its sub-expression, so the result is computed on the fly.
4. **Syntax errors**: an unexpected token raises a `ParserError` that names the token found and the one expected.
5. **Error-recovery variant** (`rattrapage.py`): on a syntax error, the parser skips tokens up to a synchronisation token (computed from the grammar's follow sets) before reporting the error.

## Repository content

| File | Content |
|---|---|
| `archive/definitions.py` | Characters, token types and their display |
| `archive/lexer.py` | Lexer |
| `archive/calc.py` | Parser and evaluator |
| `archive/rattrapage.py` | Parser with error recovery |
| `archive/test_lexer.py`, `test_parser.py`, `test_calc.py`, `test_ratt.py` | Test suites (valid expressions, `#n` references, binomial-coefficient computations, error cases) |

## Run the tests

```bash
cd archive
python3 test_lexer.py
python3 test_parser.py
python3 test_calc.py
python3 test_ratt.py
```

## Author
[Ayoub Bkhach](https://github.com/Bkhach-Ayoub) · [LinkedIn](https://www.linkedin.com/in/bkhach-ayoub/) · [Portfolio](https://bkhach-ayoub.github.io)
