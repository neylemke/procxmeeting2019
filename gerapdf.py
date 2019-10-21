#!  /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import re,os,glob
from titlecase import titlecase
# Constants
strlatex = """
  \\documentclass[twoside]{{article}}
  \\usepackage[affil-it]{{authblk}}
  \\usepackage{{lipsum}} % Package to generate dummy text throughout \
this template
  \\usepackage{{eurosym}}
  \\usepackage[sc]{{mathpazo}} % Use the Palatino font
  \\usepackage[T1]{{fontenc}} % Use 8-bit encoding that has 256 glyphs
  \\usepackage[utf8]{{inputenc}}
  \\linespread{{1.05}} % Line spacing-Palatino needs more space between \
lines
  \\usepackage{{microtype}} % Slightly tweak font spacing for \
aesthetics\[IndentingNewLine]
  \\usepackage[hmarginratio=1:1,top=32mm,columnsep=20pt]{{geometry}} % \
Document margins
  \\usepackage{{multicol}} % Used for the two-column layout of the \
document
  \\usepackage[hang,small,labelfont=bf,up,textfont=it,up]{{caption}} % \
Custom captions under//above floats in tables or figures
  \\usepackage{{booktabs}} % Horizontal rules in tables
  \\usepackage{{float}} % Required for tables and figures in the \
multi-column environment-they need to be placed in specific locations \
with the[H] (e.g. \\begin{{table}}[H])
  \\usepackage{{hyperref}} % For hyperlinks in the PDF
  \\usepackage{{lettrine}} % The lettrine is the first enlarged letter \
at the beginning of the text
  \\usepackage{{paralist}} % Used for the compactitem environment which \
makes bullet points with less space between them
  \\usepackage{{abstract}} % Allows abstract customization
  \\renewcommand{{\\abstractnamefont}}{{\\normalfont\\bfseries}} 
  %\\renewcommand{{\\abstracttextfont}}{{\\normalfont\\small\\itshape}} % \
Set the abstract itself to small italic text\[IndentingNewLine]
  \\usepackage{{titlesec}} % Allows customization of titles
  \\renewcommand\\thesection{{\\Roman{{section}}}} % Roman numerals for \
the sections
  \\renewcommand\\thesubsection{{\\Roman{{subsection}}}} % Roman numerals \
for subsections
  \\titleformat{{\\section}}[block]{{\\large\\scshape\\centering}}{{\\\
thesection.}}{{1em}}{{}} % Change the look of the section titles
  \\titleformat{{\\subsection}}[block]{{\\large}}{{\\thesubsection.}}{{1em}}{{}}\
 % Change the look of the section titles
  \\usepackage{{fancyhdr}} % Headers and footers
  \\pagestyle{{fancy}} % All pages have headers and footers
  \\fancyhead{{}} % Blank out the default header
  \\fancyfoot{{}} % Blank out the default footer
  \\fancyhead[C]{{X-meeting $\\bullet$ November 2017 $\\bullet$ S\\~ao \
Pedro}} % Custom header text
  \\fancyfoot[RO,LE]{{}} % Custom footer text
  %----------------------------------------------------------------------------------------
\
  % TITLE SECTION
  %\
----------------------------------------------------------------------------------------\
 
 
 \\title{{\\vspace{{-15mm}}\\fontsize{{24pt}}{{10pt}}\\selectfont\\textbf{{ {} }}}} % Article title
  
  
  \\author{{ {} }}
  
  \\affil{{ {} }}
  \\vspace{{-5mm}}
  \\date{{}}
  
  %----------------------------------------------------------------------------------------\
 
  
  \\begin{{document}}
  
  
  \\maketitle % Insert title
  
  
  \\thispagestyle{{fancy}} % All pages have headers and footers\

  %----------------------------------------------------------------------------------------\
  
  % ABSTRACT
  
  %----------------------------------------------------------------------------------------\
  
  
  \\begin{{abstract}}
  {}
  
  Funding: {} \\\\ 
  \\end{{abstract}}
  \\end{{document}} """



strlatex2 = """\\procpaper[switch=45,
    title={{{}}}, 
    author={{{}}}, 
    index={{{{{}}}}}]
    {{{}}} \n\n """

replacements={"Î¦" : "$\\Phi$ ", "\'" : "'", "ﬁ" : "fi", "á" : "\\'a", 
 "\[Gamma]" : "$\\gamma$", "ï\[Not]" : "fi", 
 "\[RightArrow]" : "$\\rightarrow$", " Î\.b3" : "$ \\gamma$", 
 " â â" : " $\\rightarrow$", "â\.b2" : "'", 
 "Â\[PlusMinus]" : "$\\pm$", "â¤" : "$\\leq$",
 "Â\[Degree]" :  "$^o$", "\Âº" : "$^o$", " \â¢ CL" : " ", 
 "Â\.b4" : "'", "â¥" : "$\\leq$", "ââ" : " ", "¹" : "1", 
 "â" : "\\^a", "\[OpenCurlyDoubleQuote]" : "``", 
 "\[CloseCurlyDoubleQuote]" : "''", "ã" : "\\~a", "á" : "\\'a", 
 "ê" : "\\^e", "é" : "\\'e", "õ" : "\\~o", "ó" : "\\'o", 
 "ô" : "\\^o", "ú" : "\\'u", "ç" : "\\c{c}", "í" : "\\'{\\i}",
 "Ã" : "\\~A", "Á" : "\\'A", "Ê" : "\\^E", "É" : "\\'E", 
 "Õ" : "\\~O", "Ó" : "\\'O", "Ô" : "\\^O", "Ú" : "\\'U", 
 "Ç" : "\\c{C}", "Í" : "\\'I", "Å" : "$\\AA$", "ß" : "$\\beta$", 
 "\[CloseCurlyQuote]" : "'", "\[OpenCurlyQuote]" : "'", "%" : "\\%",
  "ß" : "$\\beta$",  "_" : "\\_", 
 "ö" : "\\\"o", "ü" : "\\\"u",
 "à" : "\\`a", "À" : "\\`A", "€": "\\euro",
 "®" : "\\textsuperscript{\\textcopyright}", "¾" : "3/4", 
 "ñ" : "\\~n", "ï" : "\\\"{\\i}", "I'" : "\\'I", "#" : "\\#",
 "i\.b4" : "\\'{\\i}", 
 " " : " ",  "°" : "$^o$"}
prefix=""


# ## Funções Gerais


def namecase(str):
    """Converte Strings para Capitalização Brasileira"""
    lissubs=[(" De "," de "),(" Do "," do "), (" Da ", " da "), (" Das ", " das "),
             (" Dos "," dos ")]
    str2=titlecase(str)
    for subs in lissubs:
        str2=str2.replace(subs[0],subs[1])
    return str2




def brnames(str):
    """Gera Nomes para a regra ABNT"""
    lis=str.split(" ")
    str2=lis[-1]+ ", "
    for word in lis[0:-1]:
        str2=str2+" "+word
    return str2



def orderedunion(lis):
    """Elimina Repetições e mantém a ordem"""
    lis2=[]
    for elem in lis:
        if not (elem in lis2):
            lis2.append(elem)
    return lis2




def fixbin(string,replacements):
    """ Fix Binary Characters"""
    for k, v in replacements.items():
        string=string.replace(k, v)
    return string


# ## Funções Específicas
# 


def geraAuthors(str):
    """Gera uma Lista de Autores"""
    m = re.findall('[^(),]+\([^()]+[^()]+\)', str)
    return [namecase(word.split("(")[0].strip()) for word in m]

def geraAfil(str):
    """Gera uma lista de Afiliações"""
    m = re.findall('\([^()]+[^()]+\)', str)
    return [inst[1:-1] for inst in m]



def geraStringAfil(lis):
    lisafil=orderedunion(lis)
    stringafil="" 
    i=1
    for inst in lisafil:
        stringafil=stringafil+str(i)+" "+inst+"\n\n"
        i=i+1
    return stringafil
    

def geraStringAuthors(record):
    lisafil=record["Afil"]
    lisauthors=record["Authors"]
    dictauthors={}
    dictafil={}
    lisafilorder=orderedunion(lisafil)
    for i in range(len(lisauthors)):
        dictauthors[lisauthors[i]]=lisafil[i]
    for i in range(len(lisafilorder)):
        dictafil[lisafilorder[i]]=i
    strsaida=""
    for author in lisauthors:
        num=dictafil[dictauthors[author]]
        strsaida=strsaida+author+"$^{"+str(num+1)+"}$, "
    return strsaida[:-1]
    

def gerastringindex(record):
    title=record["Título"]
    author=", ".join(record["Authors"])
    file="art"+str(index)
    indexstr=",".join(["\\index{"+brnames(aut)+"}" for aut in record["Authors"]])
    return strlatex2.format(title,author,indexstr,file)

def readpapers(file):
    artsds=pd.read_excel(prefix+'trabalhos2017v5.xlsx',index_col=0)
# Insere duas colunas no lugar da Coluna de Autores
    artsds["Afil"]=[geraAfil(record) for record in artsds["Autores"]]
    artsds["Authors"]=[geraAuthors(record) for record in artsds["Autores"]]
    return artsds

def gerastringabstract(record,strlatex):
    author=geraStringAuthors(record)
    title=fixbin(record["Título"],replacements)
    afiliation=geraStringAfil(record["Afil"])
    print(index)
    if record["Modalidade"]=="Poster":
        abstract=fixbin(record["Resumo"],replacements)
    else:
        abstract=""
    funding=fixbin(record["Funding"],replacements)
    return strlatex.format(title,author,afiliation,abstract,funding)


if __name__ == "__main__":
# Entrada dos Dados
    artsds=readpapers(prefix+'trabalhos2017v5.xlsx')
# ## Separação em Grupos
    artsdsgrouped=artsds.groupby(["Modalidade"],axis=0)
    artsdsposter=artsdsgrouped.get_group('Poster')
    artsdsHT=artsdsgrouped.get_group('HighLight Tracks')

# ## Gera os arquivos com os abstracts

    print("gerando os arquivos com os Abstratcs")
    for index, record in artsds.iterrows():
        stringfileresumo=gerastringabstract(record,strlatex)
        f = open('papers/art'+str(index)+".tex", 'w')
        f.write(stringfileresumo)
        f.close()


# ## Gera os arquivos com os índices 
    print("gerando os arquivos com os índices")
    areas = sorted(list(set(artsdsposter["Área Temática"])))
    groupareas=artsdsposter.groupby(["Área Temática"],axis=0)
    compstr = "";
    for area in areas:
        print(area)
        ds=groupareas.get_group(area)
        ds=ds.sort_values("Poster Code")
        sessionstr = "\\chapter{" + area + "}\n";
        for index, record in ds.iterrows():
            sessionstr=sessionstr+gerastringindex(record)
        compstr = compstr + sessionstr
        f = open('posters.tex', 'w')
        f.write(compstr)
        f.close()

    print("gerando os arquivos com os índices dos HT")
    compstr = "";
    ds=artsdsHT
    sessionstr=""
    ds=ds.sort_values("Poster Code")
    for index, record in ds.iterrows():
        sessionstr=sessionstr+gerastringindex(record)
    compstr = compstr + sessionstr
    f = open('papers.tex', 'w')
    f.write(compstr)
    f.close()

    print("Compilando")
    os.chdir("papers")
    for file in glob.glob("*.tex"):
        os.system("pdflatex "+file)
    os.chdir("..")
    os.system("pdflatex procxmeeting2017; makeindex procxmeeting2017;pdflatex procxmeeting2017")
