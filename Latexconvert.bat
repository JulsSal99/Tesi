```` {.bash}
     pandoc -f markdown -t latex --wrap=none --table-of-contents --toc-depth=2 --listings --number-sections --standalone -o TEST.tex TEST.md
````