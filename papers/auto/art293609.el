(TeX-add-style-hook
 "art293609"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "twoside")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("authblk" "affil-it") ("mathpazo" "sc") ("fontenc" "T1") ("inputenc" "utf8") ("geometry" "hmarginratio=1:1" "top=32mm" "columnsep=20pt") ("caption" "hang" "small" "labelfont=bf" "up" "textfont=it")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "authblk"
    "lipsum"
    "eurosym"
    "mathpazo"
    "fontenc"
    "inputenc"
    "microtype"
    "geometry"
    "multicol"
    "caption"
    "booktabs"
    "float"
    "hyperref"
    "lettrine"
    "paralist"
    "abstract"
    "titlesec"
    "fancyhdr"))
 :latex)

