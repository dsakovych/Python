1. Matches the beginning of a line - ^
2. Matches the end of the line - $
3. Matches any character - .
4. Matches whitespace - \s
5. Matches any non-whitespace character - \S
6. Repeats a character zero or more times - *
7. Repeats a character zero or more times (non-greedy) - *?
8. Repeats a character one or more times - +
9. Repeats a character one or more times (non-greedy) - +?
10. Matches a single character in the listed set - [aeiou]
11.	Matches a single character not in the listed set - [^XYZ]
12. The set of characters can include a range - [a-z0-9]
13. Indicates where string extraction is to start - (
14.	Indicates where string extraction is to end - )

For more information about using regular expressions in Python, see https://docs.python.org/2/howto/regex.html
