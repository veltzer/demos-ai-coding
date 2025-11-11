##############
# parameters #
##############
# do you want to show the commands executed ?
DO_MKDBG:=0
# do you want dependency on the makefile itself ?!?
DO_ALLDEP:=1
# do you want to do 'html' from 'md'?
DO_FMT_MD_HTM:=1
# do you want to do 'pdf' from 'md'?
DO_FMT_MD_PDF:=1
# do you want to do 'docx' from 'md'?
DO_FMT_MD_DOCX:=1
# do you want to do 'pdf' from 'tex'?
DO_FMT_TEX_PDF:=1
# do you want to do 'pdf' from 'txt'?
DO_FMT_TXT_PDF:=1
# do spell check on all?
DO_MD_ASPELL:=1
# do you want to check that the md files are pure ASCII?
DO_MD_ASCII:=1
# do you want to run mdl on md files?
DO_MD_MDL:=1
# do you want to run markdownlint on md files?
DO_MD_MARKDOWNLINT:=1
# do you want to lint python files?
DO_PY_LINT:=1

########
# code #
########
ALL:=

# silent stuff
ifeq ($(DO_MKDBG),1)
Q:=
# we are not silent in this branch
else # DO_MKDBG
Q:=@
#.SILENT:
endif # DO_MKDBG

# markdown
MD_SRC:=$(shell find exercises -type f -and -name "*.md")
MD_BAS:=$(basename $(MD_SRC))
MD_HTM:=$(addprefix out/,$(addsuffix .html,$(MD_BAS)))
MD_PDF:=$(addprefix out/,$(addsuffix .pdf,$(MD_BAS)))
MD_DOCX:=$(addprefix out/,$(addsuffix .docx,$(MD_BAS)))
MD_ASPELL:=$(addprefix out/,$(addsuffix .aspell,$(MD_BAS)))
MD_ASCII:=$(addprefix out/,$(addsuffix .ascii,$(MD_BAS)))
MD_MDL:=$(addprefix out/,$(addsuffix .mdl,$(MD_BAS)))
MD_MARKDOWNLINT:=$(addprefix out/,$(addsuffix .markdownlint,$(MD_BAS)))

# python
PY_SRC:=$(shell find scripts -type f -and -name "*.py")
PY_LINT:=$(addprefix out/,$(addsuffix .lint, $(basename $(PY_SRC))))

ifeq ($(DO_MD_ASPELL),1)
ALL+=$(MD_ASPELL)
endif # DO_MD_ASPELL

ifeq ($(DO_MD_ASCII),1)
ALL+=$(MD_ASCII)
endif # DO_MD_ASCII

ifeq ($(DO_MD_MDL),1)
ALL+=$(MD_MDL)
endif # DO_MD_MDL

ifeq ($(DO_MD_MARKDOWNLINT),1)
ALL+=$(MD_MARKDOWNLINT)
endif # DO_MD_MARKDOWNLINT

ifeq ($(DO_FMT_MD_HTM),1)
ALL+=$(MD_HTM)
endif # DO_FMT_MD_HTM

ifeq ($(DO_FMT_MD_PDF),1)
ALL+=$(MD_PDF)
endif # DO_FMT_MD_PDF

ifeq ($(DO_FMT_MD_DOCX),1)
ALL+=$(MD_DOCX)
endif # DO_FMT_MD_DOCX

ifeq ($(DO_PY_LINT),1)
ALL+=$(PY_LINT)
endif # DO_PY_LINT

#########
# rules #
#########
.PHONY: all
all: $(ALL)
	@true

.PHONY: all_md
all_md: $(MD_HTM)

.PHONY: all_beamer
all_beamer: $(TEX_PDF)

.PHONY: all_slidy
all_slidy: $(TXT_PDF)

.PHONY: all_markdownlint
all_markdownlint: $(MD_MARKDOWNLINT)

.PHONY: all_py_lint
all_py_lint:  $(PY_LINT)

.PHONY: debug
debug:
	$(info doing [$@])
	$(info ALL is $(ALL))
	$(info MD_SRC is $(MD_SRC))
	$(info MD_HTM is $(MD_HTM))
	$(info MD_PDF is $(MD_PDF))
	$(info MD_DOCX is $(MD_DOCX))
	$(info MD_ASPELL is $(MD_ASPELL))
	$(info MD_ASCII is $(MD_ASCII))
	$(info MD_MDL is $(MD_MDL))
	$(info MD_MARKDOWNLINT is $(MD_MD_MARKDOWNLINT))
	$(info TXT_PDF is $(TXT_PDF))
	$(info PY_SRC is $(PY_SRC))
	$(info PY_LINT is $(PY_LINT))

.PHONY: clean
clean:
	$(info doing [$@])
	$(Q)rm -f $(ALL)

.PHONY: clean_hard
clean_hard:
	$(Q)git clean -qffxd

.PHONY: check
check:
	$(Q)git grep ' $$' -- "*.md" || true
	$(Q)git grep hours | grep -E "\.$$" || true
# $(Q)git grep '  ' -- "*.md" || true

.PHONY: subsection_stats
subsection_stats:
	$(Q)git grep -h '^## ' -- "*.md" | sort -u

.PHONY: spell_many
spell_many:
	$(info doing [$@])
	$(Q)aspell_many.sh $(MD_SRC)

############
# patterns #
############
$(MD_HTM): out/%.html: %.md
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)markdown $< > $@
$(MD_PDF): out/%.pdf: %.md
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)pandoc --from markdown --to pdf $< -o $@
$(MD_DOCX): out/%.docx: %.md
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)pandoc --from markdown --to docx $< -o $@
$(MD_ASPELL): out/%.aspell: %.md .aspell.conf .aspell.en.prepl .aspell.en.pws
	$(info doing [$@])
	$(Q)aspell --conf-dir=. --conf=.aspell.conf list < $< | pymakehelper error_on_print sort -u
	$(Q)pymakehelper touch_mkdir $@
$(MD_ASCII): out/%.ascii: %.md
	$(info doing [$@])
	$(Q)pymakehelper error_on_print grep -P -n "[^\x00-\x7F]" $<
	$(Q)pymakehelper touch_mkdir $@
$(MD_MDL): out/%.mdl: %.md .mdlrc .mdl.style.rb
	$(info doing [$@])
	$(Q)GEM_HOME=gems gems/bin/mdl $<
	$(Q)pymakehelper touch_mkdir $@
$(MD_MARKDOWNLINT): out/%.markdownlint: %.md .markdownlint.json
	$(info doing [$@])
	$(Q)node_modules/.bin/markdownlint -c .markdownlint.json $<
	$(Q)pymakehelper touch_mkdir $@
$(TEX_PDF): out/%.pdf: %.tex
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper wrapper_pdflatex --input_file $< --output_file $@
$(TXT_PDF): out/%.pdf: %.txt
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)a2x -f pdf $<
	$(Q)mv $(basename $<).pdf $@
$(PY_LINT): out/%.lint: %.py .pylintrc
	$(info doing [$@])
	$(Q)python -m pylint --reports=n --score=n $<
	$(Q)pymakehelper touch_mkdir $@

##########
# alldep #
##########
ifeq ($(DO_ALLDEP),1)
.EXTRA_PREREQS+=$(foreach mk, ${MAKEFILE_LIST},$(abspath ${mk}))
endif # DO_ALLDEP

# Why is this NOTPARALLEL here? Document the reason
# .NOTPARALLEL:
