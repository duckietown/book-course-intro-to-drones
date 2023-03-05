# Template: template-book

This template provides a boilerplate repository for books in Duckietown.


## What to change

These are the fields you **must** update to create your book.


### Placeholders in `src/_config.yml`

This file configures the build of the book.
Replace the placeholder string `BOOK_NAME_HERE` (there should be two separate instances of it) with
the name of the repository hosting your book (e.g., `book-devmanual-docs`).


### Structure in `src/_toc.yml`

Use the instructions [here](https://jupyterbook.org/en/stable/structure/toc.html#structure-of-a-book)
to learn how to structure your book using the Table of Contents file `_toc.yml`.
A simple example is already provided by this template. Adapt it to your needs.


### Logo in `src/logo.png`

There is a default logo in `src/logo.png`. This is the book's logo, change it with something that 
reflects the scope of your book. Transparent PNGs are recommended.


## Build

You can build this book by running the command,

```shell
dts docs build
```
