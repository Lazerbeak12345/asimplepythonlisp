# A Simple Python lisp

Once upon A time, an asipiring computer programmer heard of a distant, nigh
unapproachable land called "lisp." He was reading a book that he had purchaced
recently from the library, and at the time, only knew ECMAScript 3. He was
interested in theis book because it told of the history of early computers from
the perspective of IBM.

This book I read the entire origin story of "LISP." As I knew this book was
published not long before 1990, I suspected, and in many cases so, that all
"modern" tech mentioned in that book would now currently be residing in one of
many computer history sections in various well-known museums around the world.
And while this is somewhat true with lisp, imagine my suprise, months later,
when this same list prossessor showed up on Stack Overflow as a prominant
Artificial Intelligance programming language. What I heard, though, was that
"It's not a real language, it just makes programming easier for people who
don't know what a memory buffer is" Looking back, this is _hardly_ the case,
although it has some justification. The other thing I heard about it was "It
only uses parenthases. How are you supposed to keep track of them?" My answer
to that is this: Either using a parenthasis matcher, or using the same tools
you use to be able to do _anything at all_ in Java.

I next encountered this language when looking into how to make my programming
language, CHAML (a programming language not worth discussing in this markdown
file). Specifically, I encountered Racket, a variant of Common Lisp (correct me
if I'm wrong) that is optimized for development of Domain Specific Languages in
a paradigm known as _Language Oriented Programming_. I took a look, realised
lisp was actually pretty cool, but as it's syntax doesn't resemble C at all, I
put off learning the language untill I finished with CHAML.

Funnily enough, the syntax is so different, and I learned so much about how
programming languages work from the CHAML project, that I realised that perhaps
the only way of learning the langauge (I had been studying their docs for quite
some time) would be to write an impimentation of it. This means a few things
for this project:

1. Don't expect the code to be easy to read, as I wrote the most important code
in an hour and 30 minutes, all in one go. If that sounds like a lot, it was just
shy of 130 lines at the time.
2. Due to above reason, it's generally written in a way where if you read the
code from bottom to top, then top to bottom, then top to bottom again, it
should make sence, but if it doesn't, good luck.
3. If I do end up feeling bad enough about the code quality (likely, as I write
this) I might re-write this to be multiple files.
4. It is programmed from the perspective of someone with _no experience
whatsoever_ using the language that it mimics the functionality of. I'm sure
that although it may _seem_ to run fine, it is most likely _riddled_ with bugs
For one, right now, there are a _ton_ of scoping issues, a _ton_ of invalid
native argument issues, and a _ton_ of issues with the lazy parameter
evaluation.

But don't let this get you down! This should be a beacon of hope, that yes, not
only can a language like lisp be learned by someone who is very much used to
imperitive programming (I've learned so much already), but it can also be
written in a _very_ small amount of code. Heck, some of the functions I didn't
even need to write for it to be a lisp, but I did anyway, because I am focusing
on support for the programming language, racket.

## TLDR:

Collage student hears about lisp, then eventually writes his own version of a
lisp varient in python, cuz he was bored (sortof).

