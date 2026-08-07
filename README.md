# demos-ai-coding

Exercises for coding with AI

## Building

The build is driven by [rsconstruct](https://github.com/veltzer/rsconstruct).

```bash
rsconstruct build          # incremental build
rsconstruct build -j8      # ...with 8 parallel jobs
rsconstruct status         # show what is out of date
rsconstruct clean outputs  # remove build artifacts
```

Every `exercises/**/exercise.md` is rendered to HTML, PDF and DOCX under
`out/pandoc.exercises/`, and checked with `rumdl` (markdown lint) and `zspell`
(spelling). Configuration lives in `rsconstruct.toml` (shared across repos,
do not edit here) and `rsconstruct.local.toml` (this repo's overrides).

Spelling exceptions go in `.zspell-words`; markdown rules in `.rumdl.toml`.
