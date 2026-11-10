#!/usr/bin/env python3
"""Build the chapter HTML from lightly corrected original LaTeX.
Requires pandoc and beautifulsoup4. Run from anywhere: python tools/build.py
"""
from pathlib import Path
import re
import subprocess
import html
import json
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [
    ('spaces','01','Spaces of a Matrix', 'Rows, columns, null spaces, and the rank–nullity relationship', 'Start with a matrix as a linear map and build its fundamental subspaces from first principles.', '01 · Foundations'),
    ('rank','02','Rank of a Matrix', 'Linear independence, rank inequalities, and row–column rank equality', 'Understand why the number of independent rows and columns must agree.', '02 · Dimension'),
    ('svd','03','Singular Value Decomposition', 'Null spaces, Gram matrices, eigenvectors, and a constructive SVD', 'Derive the singular value decomposition from the geometry of the fundamental spaces.', '03 · Decomposition'),
]

# Conservative copy edits: no mathematical arguments are rewritten.
EDIT = {
'spaces': [
 ('In this article the Row, Column and Null Spaces of a Matrix are defined in an informal and intuitive way. Further an equality relating the rank of a matrix and its nullity is explained so that the reader is well acquainted with these fundamental spaces of a matrix.', 'In these notes, the row, column, and null spaces of a matrix are introduced informally and intuitively. We then explain the relationship between the rank and nullity of a matrix to develop a clearer understanding of these fundamental spaces.'),
 ('Let us define certain conventions, to follow in this article, about $A$ and $A^{\\top}$.','We begin by establishing notation for $A$ and $A^{\\top}$.'),
 (r'R(A) = \{ u : u = A^{\top}y, \forall y \in \mathbb{R}^m  \}', r'R(A) = \{ A^{\top}\boldsymbol{y} : \boldsymbol{y} \in \mathbb{R}^m \}'),
 ('We notate matrix $A$ with its columns as:', 'We write the matrix $A$ in terms of its columns as:'),
 ('we notate:', 'we write:'),
 ('We can always see the matrix $A$ as an operator which transforms vectors in $\\mathbb{R}^{n}$ space to vectors in $\\mathbb{R}^{m}$ space, as for any', 'We can view $A$ as a linear map from $\\mathbb{R}^{n}$ to $\\mathbb{R}^{m}$: for any'),
 ('Let us plug in all possible $\\boldsymbol{y} \\in \\mathbb{R}^m$ and put them in a set, let us call this set $R(A)$ for reasons that will be clear as we proceed. Thus,','Collecting all possible vectors $A^{\\top}\\boldsymbol{y}$, with $\\boldsymbol{y} \\in \\mathbb{R}^m$, gives a set that we denote by $R(A)$. Thus,'),
 ('If this is seeming incomprehensible, it is easy to define the above set as the set of all vectors that are orthogonal to all linear combinations formed by the rows of matrix $A$.','Equivalently, this is the set of all vectors orthogonal to every linear combination of the rows of $A$.'),
 ('We name it the \\textbf{Null Space} of $A$. And we also have that the \\textbf{Null Space} of $A$ is orthogonal to the \\textbf{Row Space} of $A$.','We call it the \\textbf{null space} of $A$. The null space of $A$ is orthogonal to the row space of $A$.'),
 ('On similar lines we can define', 'Similarly, we can define'),
 ('Now let us assume that the dimension of null space', 'Now suppose that the dimension of the null space'),
 ('Let the complete basis set of $\\mathbb{R}^n$ be,','Let a complete basis for $\\mathbb{R}^n$ be'),
 ('Any element $\\boldsymbol{a} \\in$ range-space of $A$, or equivalently $C(A)$, we have,','For any element $\\boldsymbol{a}$ in the range of $A$, equivalently in $C(A)$, we have'),
 ('(since, $\\boldsymbol{g}_i$ are basis of null space of $A$, we have,', '(Since the $\\boldsymbol{g}_i$ form a basis for the null space of $A$, we have'),
 ('From here we say that the the \\textbf{Linear Span} of the above set is $C(A)$.','Thus, the \\textbf{linear span} of this set is $C(A)$.'),
 ('Since the above set is linearly independent and is a linear span of $\\mathbb{R}^n$, it is a basis for the space $C(A)$.','Since the set is linearly independent and spans $C(A)$, it is a basis for $C(A)$.'),
 ('Thus, $n = dim(N(A)) + dim(C(A))$.','Thus, $n = \\dim(N(A)) + \\dim(C(A))$.'),
 ('In the above the Column space can be replaced by Row space as the rank is the same.','In the rank–nullity identity, the column-space dimension can be replaced by the row-space dimension, since both equal the rank.'),
 ],
'rank': [
 ('Let $A$ be a matrix of m rows and n columns with real entries', 'Let $A$ be a matrix with $m$ rows and $n$ columns and real entries'),
 ('two quantities called the \\textbf{Row rank} and \\textbf{Column Rank}', 'two quantities called the \\textbf{row rank} and \\textbf{column rank}'),
 ('is looked as a vector', 'is viewed as a vector'),
 ('We know from matrix vector multiplication that pre-multiplying a matrix with a row vector gives a row vector which is a linear combination of the rows of the matrix.', 'Premultiplying a matrix by a row vector produces a linear combination of the rows of that matrix.'),
 ('Let us follow the following convention for each of them:', 'We use the following notation for each vector:'),
 ('Elaborating further (for lucidity) we can write,','More explicitly, we can write'),
 ('Naming the first matrix in the left hand side above, as', 'Denoting the first matrix on the left-hand side by'),
 ('is utmost the rank of matrix', 'is at most the row rank of matrix'),
 ('pre-multiplication can either reduce or utmost maintain the rank of a matrix.', 'premultiplication can reduce the row rank of a matrix or leave it unchanged.'),
 ('Now placing these above vectors in the columns of a new matrix we get,','Placing these vectors in the columns of a new matrix gives'),
 ('To represent the above in lucid way, we write,','Equivalently, we write'),
 ('In an elaborate way we have,', 'More explicitly, we have'),
 ('is utmost the column rank of', 'is at most the column rank of'),
 ('We call a matrix to have deficient row rank if the row-rank is less than the number of rows in the matrix.', 'A matrix has deficient row rank if its row rank is smaller than its number of rows.'),
 ('row convection', 'row convention'),
 ('Thus we can write matrix $A$ as,','Thus, we can write $A$ as'),
 ('Using intuitions obtained in the subsection of row-rank, we can factorize the above matrix as:', 'Using the intuition developed in the subsection on row rank, we can factorize this matrix as follows:'),
 ('Observe that each of the matrices $S$ and $R$ above have row-rank $r$ since both have $r$ independent rows.', 'Both $S$ and $R$ have rank $r$: the columns of $S$ are linearly independent, and the rows of $R$ are linearly independent.'),
 ('Note that the above result to hold, the matrix need not be rank deficient, as in such a case, the values $a_{i,j}$ are all zeros.', 'The equality also holds for matrices of full row rank; when $r=m$, there are no dependent rows to express.'),
 ('Thus, we finally arrive a point where we see the two notions', 'Thus, we conclude that the two notions'),
 ('From this, we define the rank of matrix which is equal to its row-rank and the column-rank.', 'We define the rank of a matrix to be this common value.'),
 ],
'svd': [
 ('In this article we consider finding the basis elements for the column space and row space of a matrix', 'In these notes, we construct bases for the column and row spaces of a matrix'),
 ('Towards this objective, we first build positive-semi definite matrices which have row or column spaces equivalent to row and column spaces of $A$.', 'To do so, we first construct positive semidefinite matrices whose row or column spaces coincide with those of $A$.'),
 ('We select positive semi-definite matrices for this task because positive semi-definite matrices are symmetric and can have an orthonormal eigen-basis which can span the required space.', 'Positive semidefinite matrices are symmetric, so their orthonormal eigenvectors can provide bases for the spaces of interest.'),
 ('Let us start from the null space of matrix $A$.', 'We begin with the null space of $A$.'),
 ('Now let us say,', 'Now suppose'),
 ('Now pre-multiplying both sides by', 'Premultiplying both sides by'),
 ('The above can be seen as a norm, therefore,', 'Recognizing the squared Euclidean norm, we obtain'),
 ('\\boldsymbol{y} \\subseteq null(A)', '\\boldsymbol{y} \\in null(A)'),
 ('Now playing the above tricks with', 'Repeating the argument with'),
 ('the same as null space of', 'the same as the null space of'),
 ('where $R(A)$ is the row-space of $A$.', 'where $R(A)$ denotes the row space of $A$.'),
 ('where $C(A)$ is the column-space of $A$.', 'where $C(A)$ denotes the column space of $A$.'),
 ('Therefore, the column-space of $A$ is the same as the column-space of $AA^{\\top}$. On similar lines, row-space of $A$ is same as the row-space of $A^{\\top}A$.', 'Thus, $A$ and $AA^{\\top}$ have the same column space. Similarly, $A$ and $A^{\\top}A$ have the same row space.'),
 ('In this we have the domain set as the n-dimensional vector space', 'The domain is the $n$-dimensional vector space'),
 ('and the co-domain set as the m-dimensional vector space', 'and the codomain is the $m$-dimensional vector space'),
 ('Since it is in the column space of $A$ it can be represented by the basis elements of the column space of $A$. This basis set can be easily found from the matrix $AA^{\\top}$ since, it is a symmetric matrix we can find orthonormal basis by finding the eigenvectors of the symmetric matrix $AA^{\\top}$.', 'An orthonormal basis for $C(A)$ can be constructed from eigenvectors of the symmetric matrix $AA^{\\top}$ associated with its positive eigenvalues.'),
 ('Let the orthonormal basis be', 'Let this orthonormal basis be'),
 ('Since each is an eigenvector of $AA^{\\top}$, we have', 'Since each $\\boldsymbol{u}_i$ is an eigenvector of $AA^{\\top}$, we have'),
 ('so as to normalize each', 'to normalize each'),
 ('columns space', 'column space'),
 ('From similar reasons, we can extend', 'For similar reasons, we can extend'),
 ('\\sqrt{\\lambda}_1', '\\sqrt{\\lambda_1}'),
 ('\\sqrt{\\lambda}_2', '\\sqrt{\\lambda_2}'),
 ('using Gram-Schmidt Process', 'using the Gram–Schmidt process'),
 ('contains Singular Values', 'contains the singular values'),
 ]
}

def edit_text(slug, source):
    for a,b in EDIT[slug]:
        if a not in source:
            print('WARN unmatched edit',slug,repr(a[:70]))
        source=source.replace(a,b)
    # Convert plain roman words that appear as unstyled math into readable operators.
    if slug=='svd':
        source=re.sub(r'(?<![\\a-zA-Z])null\(',r'\\operatorname{null}(',source)
    return source

def to_html(slug,body):
    proc=subprocess.run(['pandoc','-f','latex','-t','html5','--mathjax','--wrap=none'],input=body,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    return BeautifulSoup(proc.stdout,'html.parser')

HEADINGS = {}
ENTRIES=[]
BUILD_STATS={}
for idx,(slug,number,title,subtitle,lead,kicker) in enumerate(CHAPTERS,1):
    source_path=ROOT/'source'/'original'/f'{slug}.tex'
    original=source_path.read_text(encoding='utf-8')
    edited=edit_text(slug,original)
    (ROOT/'source'/'edited'/f'{slug}.tex').write_text(edited,encoding='utf-8')
    body=edited[edited.find('\\section{Introduction}'):edited.rfind('\\end{document}')]
    soup=to_html(slug,body)
    main=soup.new_tag('div',attrs={'class':'article-body'})
    main.extend(list(soup.contents))
    heading_links=[]
    for h in main.find_all(['h1','h2']):
        h.name='h2' if h.name=='h1' else 'h3'
        heading_links.append({'id':h.get('id',''),'title':h.get_text(' ',strip=True),'depth':2 if h.name=='h2' else 3})
        anchor=soup.new_tag('a',href='#'+h.get('id',''),attrs={'class':'heading-anchor','aria-label':'Link to this section'})
        anchor.string='#'
        h.append(anchor)
    HEADINGS[slug]=heading_links
    # MathJax-friendly expression cards and stable numbered anchors.
    label_mapping={}
    eq_count=0
    for el in main.select('span.math.display'):
        eq_count+=1
        num=f'{number}.{eq_count}'
        eq_id=f'eq-{slug}-{eq_count}'
        math=el.get_text()
        labels=re.findall(r'\\label\{([^}]+)\}',math)
        math=re.sub(r'\\label\{[^}]+\}','',math).strip()
        for label in labels: label_mapping[label]=(num,eq_id)
        el.clear()
        el['id']=eq_id
        el['class']=['equation-block']
        math_el=soup.new_tag('span',attrs={'class':'equation-math'})
        math_el.append(NavigableString(math))
        num_el=soup.new_tag('a',href=f'#{eq_id}',attrs={'class':'eq-number','title':f'Link to equation {num}','aria-label':f'Equation {num}; copy link'})
        num_el.string=f'({num})'
        el.append(math_el)
        el.append(num_el)
    for el in main.select('a[data-reference-type="ref"]'):
        label=el.get('data-reference','')
        if label in label_mapping:
            num,eq_id=label_mapping[label]
            el['href']='#'+eq_id
            el['class']=['eq-ref']
            el.clear()
            el.string=num
    # Change occasional Pandoc line break leftovers into normal text flow.
    for br in main.find_all('br'):
        br.replace_with(NavigableString(' '))
    # Unwrap empty paragraphs.
    for p in main.find_all('p'):
        if not p.get_text(' ',strip=True) and not p.find('span',class_='math'):
            p.decompose()
    OUT=ROOT/'chapters'/f'{slug}.html'
    # Section headings in article appear only once; split intro and content naturally.
    toc='\n'.join(f'<a class="toc-link {"toc-sub" if h["depth"]==3 else ""}" href="#{h["id"]}">{html.escape(h["title"])}</a>' for h in heading_links)
    previous=CHAPTERS[idx-2] if idx>1 else None
    following=CHAPTERS[idx] if idx<len(CHAPTERS) else None
    bottom_links=''
    if previous:
        bottom_links+=f'<a class="chapter-step previous" href="{previous[0]}.html"><span>← Previous chapter</span><strong>{html.escape(previous[2])}</strong></a>'
    if following:
        bottom_links+=f'<a class="chapter-step next" href="{following[0]}.html"><span>Next chapter →</span><strong>{html.escape(following[2])}</strong></a>'
    if not following:
        bottom_links+=f'<a class="chapter-step next" href="../index.html"><span>Back to overview →</span><strong>All chapters</strong></a>'
    content=f'''<div class="reading-progress" id="reading-progress"></div>
<div class="page-wrap"><div class="breadcrumb"><a href="../index.html">Notes</a><span>/</span><a href="../index.html#chapters">Linear algebra</a><span>/</span><strong>{html.escape(title)}</strong></div>
<section class="chapter-header">
<span class="eyebrow">{html.escape(kicker)} <span class="eyebrow-dot">·</span> Informal linear algebra notes</span>
<h1>{html.escape(title)}</h1><p class="chapter-lead">{html.escape(subtitle)}</p>
<div class="chapter-meta"><span><span class="meta-swatch"></span> Written by Harsha Vardhan Tetali</span><span>{eq_count} numbered equations</span><a href="../source/edited/{slug}.tex" download>View LaTeX source ↗</a></div>
</section>
<div class="chapter-layout"><aside class="chapter-sidebar" id="chapter-sidebar"><div class="sidebar-top"><span>ON THIS PAGE</span><button type="button" id="toc-collapse" aria-expanded="true">Sections <span>⌄</span></button></div><nav class="toc-list" aria-label="Table of contents">{toc}</nav><div class="sidebar-return"><a href="../index.html#chapters">← All chapters</a></div></aside>
<main id="main-content" class="article"><div class="chapter-intro-callout"><span class="note-icon">✦</span><p><strong>The idea.</strong> {html.escape(lead)}</p></div>{str(main)}
<div class="chapter-ending"><span>CHAPTER {number} OF 03</span><p>Continue reading</p><div class="chapter-pager">{bottom_links}</div></div>
</main></div></div>'''
    OUT.write_text(build_page(title, content, nested=True, description=subtitle, chapter=slug) if 'build_page' in globals() else content,encoding='utf-8')
    ENTRIES.append({'title':title,'description':subtitle,'href':f'chapters/{slug}.html','keywords': f'{title} {subtitle} matrix linear algebra '+ ' '.join(h['title'] for h in heading_links).lower()})
    ENTRIES+= [{'title': h['title'], 'description': f'{title} · Section', 'href': f'chapters/{slug}.html#{h["id"]}', 'keywords':f'{h["title"]} {title} {subtitle}'} for h in heading_links]
    BUILD_STATS[slug]={'equations':eq_count,'sections':len(heading_links),'references':len(label_mapping)}
    print(slug,BUILD_STATS[slug])

# This script is intentionally a self-contained renderer: replace provisional
# chapter bodies with the common shell, after all chapters have been parsed.
def build_page(title, content, nested=False, description='', chapter=None):
    prefix='../' if nested else ''
    nav=''.join(f'<a class="nav-link {"is-current" if chapter==s else ""}" href="{prefix}chapters/{s}.html">{n} · {html.escape(t)}</a>' for (s,n,t,_,_,_) in CHAPTERS)
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="theme-color" content="#f6f4ef"/>
<title>{html.escape(title)} | Linear Algebra Notes · Harsha Vardhan Tetali</title>
<meta name="description" content="{html.escape(description,quote=True)}"/>
<meta property="og:title" content="{html.escape(title,quote=True)} | Informal Linear Algebra Notes"/>
<meta property="og:description" content="{html.escape(description,quote=True)}"/>
<meta property="og:type" content="website"/>
<link rel="canonical" href="https://mathyharsha.github.io/linear-algebra/{'chapters/'+chapter+'.html' if chapter else ''}"/>
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap" rel="stylesheet"/>
<script>try{{if(localStorage.getItem('matrix-notes-theme')==='dark')document.documentElement.dataset.theme='dark'}}catch(e){{}}</script>
<link rel="stylesheet" href="{prefix}assets/styles.css"/>
<script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}},startup:{{typeset:true}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<script defer src="{prefix}assets/search-index.js"></script>
<script defer src="{prefix}assets/app.js"></script>
</head><body data-chapter="{chapter or 'home'}">
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header"><div class="site-nav"><a class="site-brand" href="{prefix}index.html"><span class="brand-mark">H<span>·</span></span><span class="brand-name">Harsha's <em>notes</em></span></a>
<nav class="desktop-nav" aria-label="Chapters"><a href="{prefix}index.html#chapters" class="nav-link">Chapters</a>{nav}</nav>
<div class="nav-actions"><button class="icon-button" type="button" id="search-button" aria-label="Search notes" title="Search notes (/)" data-icon="search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.6"/><path d="M16 16l5 5"/></svg><span class="search-hint">Search</span><kbd>/</kbd></button>
<button class="icon-button theme-toggle" type="button" id="theme-button" aria-label="Toggle light or dark theme" title="Toggle theme"><svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.4A8.5 8.5 0 0 1 9.6 3.5a8.5 8.5 0 1 0 10.9 10.9Z"/></svg></button>
<button class="icon-button mobile-menu-button" type="button" id="menu-button" aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></div></div>
<nav class="mobile-nav" id="mobile-nav" aria-label="Mobile chapters">{nav}<a href="{prefix}index.html">All chapters</a></nav>
</header>
{content}
<footer class="site-footer"><div class="footer-inner"><div><span class="footer-logo">H<span>·</span></span><strong>Informal Linear Algebra Notes</strong><p>Working through matrix theory, one idea at a time.</p></div><div class="footer-links"><a href="{prefix}index.html">Overview</a><a href="https://mathyharsha.github.io/" target="_blank" rel="noopener">Academic website ↗</a><a href="{prefix}source/edited/{chapter or 'spaces'}.tex">LaTeX source ↗</a></div></div><div class="footer-bottom">© Harsha Vardhan Tetali · These notes are informal educational material; corrections are welcome.</div></footer>
<div class="search-modal" id="search-modal" hidden><div class="search-backdrop" data-close-search></div><section class="search-dialog" role="dialog" aria-modal="true" aria-label="Search the notes"><div class="search-field"><svg viewBox="0 0 24 24"><circle cx="10" cy="10" r="6.5"/><path d="m15 15 6 6"/></svg><input id="search-input" type="search" placeholder="Search for rank, null space, eigenvectors…" aria-label="Search query" autocomplete="off"/><button type="button" data-close-search aria-label="Close search">Esc</button></div><div class="search-results" id="search-results"><p>Search across all chapters and section titles.</p></div></section></div>
</body></html>'''

for slug,number,title,subtitle,lead,kicker in CHAPTERS:
    outfile=ROOT/'chapters'/f'{slug}.html'
    outfile.write_text(build_page(title,outfile.read_text(encoding='utf-8'),nested=True,description=subtitle,chapter=slug),encoding='utf-8')

# A zero-JS, static homepage (apart from search/theme enhancements).
chapter_cards=''
for slug,number,title,subtitle,lead,kicker in CHAPTERS:
    formulas={'spaces':'R(A) \\perp N(A)','rank':'\\operatorname{rank}(A)=\\operatorname{rank}(A^\\top)','svd':'A=U\\Sigma V^\\top'}
    section_count=len(HEADINGS[slug]); eq_count=BUILD_STATS[slug]['equations']
    chapter_cards+=f'''<a class="chapter-card" href="chapters/{slug}.html"><div class="card-top"><span class="chapter-index">{number} / 03</span><span class="card-arrow">↗</span></div><div class="card-formula">\\({formulas[slug]}\\)</div><h3>{html.escape(title)}</h3><p>{html.escape(subtitle)}</p><div class="card-bottom"><span>{section_count} sections · {eq_count} equations</span><span>Read chapter <span aria-hidden="true">→</span></span></div></a>'''

home=f'''<main id="main-content"><section class="hero"><div class="hero-grid"><div class="hero-copy"><span class="eyebrow"><span class="eyebrow-line"></span> AN INFORMAL COURSE IN MATRIX THEORY</span><h1>Linear algebra,<br/><em>from the inside out.</em></h1><p>Three sets of notes on the structure behind matrices: their fundamental spaces, rank, and singular value decomposition. Built from definitions, intuition, and step-by-step derivations.</p><div class="hero-actions"><a class="primary-button" href="chapters/spaces.html">Start reading <span>↗</span></a><a class="secondary-link" href="#chapters">Browse the chapters <span>↓</span></a></div><div class="hero-credit"><span class="avatar-initial">HT</span><div><span>Prepared by</span><strong>Harsha Vardhan Tetali</strong></div></div></div>
<div class="hero-visual" aria-label="A matrix transformation illustration"><div class="visual-top"><span>THE STRUCTURE OF A MATRIX</span><span>Fig. 01</span></div><div class="visual-grid"><div class="vector-column"><span class="vec-label">INPUT SPACE</span><span class="vec-big">ℝⁿ</span><div class="vector-swatch"><i></i><i></i><i></i><i></i></div><span class="vector-caption">row + null spaces</span></div><div class="map-arrow"><span class="arrow-a">A</span><div class="arrow-stroke"></div><span class="arrow-sub">linear map</span></div><div class="vector-column"><span class="vec-label">OUTPUT SPACE</span><span class="vec-big">ℝᵐ</span><div class="vector-swatch output"><i></i><i></i><i></i></div><span class="vector-caption">column + left-null spaces</span></div></div><div class="visual-equation"><span>A FUNDAMENTAL IDENTITY</span><strong>\\(\\dim N(A)+\\operatorname{{rank}}(A)=n\\)</strong></div></div></div></section>
<section id="chapters" class="chapters-section"><div class="section-intro"><div><span class="eyebrow">READING PATH / 01 — 03</span><h2>Start with the spaces.<br/><em>Build toward the decomposition.</em></h2></div><p>Each chapter stands on its own, but they work best in order. The mathematical proofs are adapted from the original LaTeX notes, with only light copy-editing.</p></div><div class="chapter-cards">{chapter_cards}</div></section>
<section class="connection-section"><div class="connection-text"><span class="eyebrow">HOW THE IDEAS FIT TOGETHER</span><h2>Three ways to understand<br/><em>the same matrix.</em></h2><p>The four fundamental spaces describe what a matrix can produce and what it annihilates. Rank counts the independent directions. SVD then chooses orthonormal coordinates that make the action of the matrix transparent.</p><a href="chapters/svd.html">See the SVD derivation <span>↗</span></a></div><div class="identity-list"><div class="identity-item"><span>01 <strong>Fundamental spaces</strong></span><div>\\(R(A)=N(A)^\\perp\\)</div></div><div class="identity-item"><span>02 <strong>Rank & nullity</strong></span><div>\\(\\operatorname{{rank}}(A)+\\dim N(A)=n\\)</div></div><div class="identity-item"><span>03 <strong>Singular values</strong></span><div>\\(A=U\\Sigma V^\\top\\)</div></div></div></section>
<section class="about-section"><span class="eyebrow">ABOUT THESE NOTES</span><h2>Written to understand,<br/><em>not just to memorize.</em></h2><p>These are informal mathematical notes prepared by Harsha Vardhan Tetali. The focus is on deriving familiar results carefully from the properties of linear maps and vector spaces. The original LaTeX files and lightly edited versions are included for reference.</p><div class="about-links"><a href="source/edited/spaces.tex" download>Download chapter 1 source ↗</a><a href="source/edited/rank.tex" download>Download chapter 2 source ↗</a><a href="source/edited/svd.tex" download>Download chapter 3 source ↗</a></div></section></main>'''
(ROOT/'index.html').write_text(build_page('Overview',home,description='Informal notes on matrix spaces, rank, and singular value decomposition, by Harsha Vardhan Tetali.'),encoding='utf-8')

(ROOT/'assets'/'search-index.js').write_text('window.NOTES_SEARCH_INDEX = '+json.dumps(ENTRIES,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
print('Created',len(ENTRIES),'search index entries; rendered chapters and homepage')
