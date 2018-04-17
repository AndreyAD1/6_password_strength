# Password Strength Calculator

This script evaluates a strength of password from 1 to 10 points.

**Evaluation rules**

| Criterion | Mark |
| --------- | ---- |
| Upper and lower case letters | +2 |
| Digits | +2 |
| Special characters | +2 |
| Underlines, minuses and brackets | +2 |
| Password length > 8 symbols | +1 |
| Password length > 12 symbols | +2 |
| More than 4 numbers in a row | -1 |
| Date and time | -1 |
| Password from blacklist | -1 | 

# Quickstart

The script requires Python v3.5.

*Requirements:*
- dateparser==0.7.0
- python-dateutil==2.7.2
- pytz==2018.4
- regex==2018.2.21
- six==1.11.0
- tzlocal==1.5.1


A path of file containing a text is the optional argument of the script. 

To run script on Linux:
```
$ python password_strength.py -b password_blacklist.txt
Password: ******
Your password gets 1 point(s) out of 10.
```

Windows usage is the same.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
