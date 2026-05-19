# Deploying to Streamlit Community Cloud

A step-by-step guide for getting *The Confidence Trap* online with a public URL
you can put in your dissertation and demo in the video.

**Total time:** ~15 minutes the first time.
**Cost:** Free.
**End result:** A public URL like `https://amina-confidence-trap.streamlit.app`
that you can share with anyone.

---

## What you need before starting

- A **GitHub account** (sign up at github.com if you don't have one — free).
- A **Streamlit Community Cloud account** (sign up at share.streamlit.io — free,
  uses your GitHub login).
- The three files in this folder: `app.py`, `requirements.txt`, `README.md`,
  plus the hidden `.gitignore`.

---

## Step 1 — Create a new GitHub repository

1. Go to <https://github.com/new>
2. Fill in:
   - **Repository name**: `the-confidence-trap` (or whatever you prefer — this
     becomes part of your URL).
   - **Description**: *Interactive policy brief on AI-generated healthcare chart
     explanations* (or similar).
   - **Public** — Streamlit Community Cloud's free tier requires the repo to be
     public. (If you need it private for marking reasons, see "Private repo
     deployment" at the bottom.)
   - **Do NOT** tick "Add a README file" — you already have one.
   - **Do NOT** add a .gitignore or licence yet.
3. Click **Create repository**.

GitHub will show you a page with setup instructions. Keep that tab open — you'll
copy the repository URL from it in step 2.

---

## Step 2 — Upload your files

You have two options depending on how comfortable you are with git on the
command line.

### Option A — Web upload (simplest, no terminal)

1. On the empty repo page, click **"uploading an existing file"** (it's a link
   in the quick-setup instructions).
2. Drag and drop these four files from your computer into the upload area:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore` (this file may be hidden in your file manager — on macOS press
     `Cmd+Shift+.` to show hidden files; on Windows enable "Show hidden items"
     in File Explorer's View menu).
3. Scroll down. Under **Commit changes**, put a short message like
   *"Initial commit"*.
4. Click **Commit changes**.

Your files should now appear in the repo.

### Option B — Command line (if you're comfortable with git)

```bash
cd path/to/the-confidence-trap-app
git init
git add app.py requirements.txt README.md .gitignore
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/the-confidence-trap.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

---

## Step 3 — Deploy to Streamlit Community Cloud

1. Go to <https://share.streamlit.io>
2. Click **Sign in with GitHub** (top right). Authorise Streamlit to read your
   repositories when prompted.
3. Once signed in, click **Create app** → **Deploy a public app from GitHub**.
4. Fill in the deployment form:
   - **Repository**: select `YOUR-USERNAME/the-confidence-trap` from the dropdown.
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): customise the subdomain. Something like
     `confidence-trap-elshazly` keeps it identifiable for your dissertation
     citation. If you skip this, Streamlit generates a random URL.
5. Click **Deploy**.

Streamlit will now spin up the app. You'll see a black log window streaming the
build process. Expect about 2–4 minutes the first time while it installs
streamlit, plotly, and pandas.

When you see the app render in your browser, you're live. Copy the URL — that's
the link you'll use everywhere.

---

## Step 4 — Test it on a different device

This is the equivalent of the assignment brief's instruction to *"try it on a
university lab computer"*. Don't skip it.

1. Open the URL on your phone, a friend's laptop, or a public library/lab machine.
2. Click through all six sections.
3. Make sure the Live Demo (§ 02) chart renders and the answer buttons work.

If anything fails, see "Troubleshooting" below.

---

## Step 5 — Pin the URL where you need it

Once it works, put the URL in three places:

1. **Your dissertation** — add a footnote or appendix entry pointing to the live
   app, e.g.:
   > *An interactive companion brief is available at
   > https://confidence-trap-elshazly.streamlit.app.*
2. **Your video** — show the URL on screen during the artefact walkthrough, and
   optionally include it on the closing slide.
3. **Your submission notes** — if your module has a comments field for the digital
   artefact submission, paste the URL there as well.

---

## Updating the app after deployment

Any time you push a change to the `main` branch of your GitHub repo, Streamlit
Cloud detects it and redeploys automatically within a minute or two. You don't
need to do anything in the Streamlit dashboard.

Edit a file → commit → push → wait → refresh the app.

If you want to edit something quickly and don't want to use git, you can edit
files directly in the GitHub web interface (pencil icon → edit → commit).

---

## Troubleshooting

### "ModuleNotFoundError" on deploy
The build couldn't find a package. Open `requirements.txt` in the repo and make
sure `streamlit`, `plotly`, and `pandas` are all listed. Commit the fix.

### App boots but the page is blank
Open the browser dev console (F12). If you see CORS or font loading errors, those
are usually harmless. If you see a Python traceback in the Streamlit log (visible
via the **Manage app** button bottom-right of the deployed app), copy the error
and read the file/line — usually a typo in `app.py`.

### "This app is over its resource limits"
Streamlit Community Cloud's free tier gives apps 1 GB RAM. This app uses well
under that, so you shouldn't hit it. If you do, click **Reboot app** in the
dashboard.

### The app went to sleep
Streamlit Community Cloud sleeps apps after about a week of no traffic. Visitors
see a "wake up this app" button — one click and the app boots in about 30 seconds.
For the duration of marking, your app should stay warm because you and the markers
will be visiting it. If you're worried about a marker hitting a sleeping app, visit
the URL yourself the morning before submission deadlines so it's already awake.

### I want a custom domain
Not available on the free tier. The `*.streamlit.app` subdomain is fine for a
dissertation artefact.

---

## Private repo deployment (if required)

If your module's regulations require the source code to be private until grading,
Streamlit Community Cloud's free tier does not support private repos. Two options:

1. **Make the repo private after grading** — leave it public during the marking
   window, then flip it to private once grades are released. Streamlit will keep
   serving the app as long as it was deployed when the repo was public, but
   updates may break. This is the simpler option.
2. **Use Streamlit Cloud's paid tier** — supports private repos, but costs money.
   Not recommended unless required.

---

## Removing the app after grading

When you're done with the project, you can:

1. Go to the Streamlit Cloud dashboard.
2. Find your app, click the three-dot menu → **Delete app**.

The GitHub repo stays put; only the deployment goes away. If you want, archive the
GitHub repo too (Settings → Archive this repository) so it's read-only.

---

## Suggested citation in your dissertation

Once deployed, you can cite the artefact in your dissertation as:

> ElShazly, A. (2026). *The Confidence Trap: Guidelines for AI-Generated
> Healthcare Chart Explanations* [Interactive policy brief]. Streamlit Community
> Cloud. https://your-app-url.streamlit.app
