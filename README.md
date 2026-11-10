# Informal Linear Algebra Notes

A three-chapter website of informal mathematical notes by **Harsha Vardhan Tetali**, converted from the supplied LaTeX manuscripts.

## Suggested GitHub Pages address

**https://mathyharsha.github.io/linear-algebra/**

Use a new **public** GitHub repository named `linear-algebra` in the `mathyharsha` account. It will coexist with the existing `mathyharsha.github.io` repository and the `unsupervised-learning` site.

## Publish on GitHub

1. Download and unzip the complete website package.
2. Open <https://github.com/new> and create a **public** repository named `linear-algebra` under `mathyharsha`. You may leave the new repository empty when creating it.
3. In the new repository, use **Add file → Upload files** and upload **the contents of the unzipped `linear-algebra` folder**. Do not upload only the ZIP, and do not put `index.html` in an extra nested folder.
4. Commit the files. Verify that `index.html`, `.nojekyll`, `assets/`, `chapters/`, and `source/` are at the repository root. (Some file managers hide dotfiles like `.nojekyll`; GitHub Pages works without this file in this particular project, but it is included.)
5. Go to **Settings → Pages → Build and deployment**. Choose **Deploy from a branch**, set the branch to **main** and the folder to **/(root)**, then **Save**.
6. After deployment completes, visit <https://mathyharsha.github.io/linear-algebra/>.

For command-line Git users, from **inside the extracted website folder**, you can also run:

```bash
git init
git add .
git commit -m "Publish informal linear algebra notes"
git branch -M main
git remote add origin https://github.com/mathyharsha/linear-algebra.git
git push -u origin main
```

Create the empty repository first. If the repository already has an initial commit, either upload through the GitHub website or reconcile its history before pushing.

## Navigation and content

| Chapter | Path | Content |
|---|---|---|
| 1. Spaces of a Matrix | `chapters/spaces.html` | Row, column, null spaces, rank–nullity |
| 2. Rank of a Matrix | `chapters/rank.html` | Row/column rank, factorization, proof that they agree |
| 3. Singular Value Decomposition | `chapters/svd.html` | Null spaces, Gram matrices, bases, SVD derivation |

All mathematical content from the original LaTeX documents is included. Display equations have stable identifiers such as `#eq-svd-42`. The original `\ref{...}` references are clickable, and equations are numbered independently by chapter, e.g. `(3.17)`.

### Source files

- `source/original/` — untouched uploaded LaTeX files.
- `source/edited/` — lightly copy-edited LaTeX files used for the website. Obvious notation mistakes were corrected (for example, using `\in` rather than `\subseteq` for vector membership in an SVD proof, and correcting two subscripted square roots). Mathematics has **not** undergone independent formal peer review.
- `tools/build.py` — converts edited manuscripts to HTML using Pandoc and BeautifulSoup, reapplies the navigation and layout, and builds the client-side search index.

To rebuild after modifying the source, change `source/original/{spaces,rank,svd}.tex` and, if necessary, the editorial rules or design in `tools/build.py`, then run:

```bash
python -m pip install beautifulsoup4
# Install pandoc separately: https://pandoc.org/installing.html
python tools/build.py
```

**Direct editing:** For quick website corrections without rebuilding, edit `chapters/spaces.html`, `chapters/rank.html`, or `chapters/svd.html` on GitHub and commit the changes. The `index.html` file is the landing page, `assets/styles.css` controls appearance, and `assets/app.js` controls navigation and search.

### Practical notes

- GitHub Pages supports plain HTML/CSS/JS, so you do **not** need Jekyll, Node.js, Python, or any build step to deploy the ready-made files.
- MathJax loads from a CDN to render LaTeX in browsers. An internet connection is needed for nicely typeset mathematics, even when previewing the site locally.
- The website uses Google Fonts; the fallback fonts will be used if Google Fonts are unavailable.
- Search matches chapter titles and section headings, not the full text of every paragraph.
- No additional figures were present in the three uploaded ZIPs, which contained only `main.tex`.
- The website does not modify your pre-existing homepage or other GitHub repositories.
