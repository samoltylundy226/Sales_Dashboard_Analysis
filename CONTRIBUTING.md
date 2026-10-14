# Contributing & Team Collaboration Guide

Welcome to the **Sales Dashboard Analysis** project! This document outlines our team workflow, branch standards, commit conventions, and review procedures to ensure seamless collaboration among our three team members.

---

## 1. Team Roles & Primary Responsibilities

Our team consists of 3 members collaborating on an end-to-end data product. While responsibilities are divided below, all members participate in code reviews, documentation, and overall quality assurance:

| Role | Primary Lead | Core Responsibilities |
| :--- | :--- | :--- |
| **Data Engineering** | Member 1 (Lead) | Dataset collection, ingestion pipeline, data cleaning (`src/clean_data.py`), validation rules (`src/validate_data.py`), data pipeline maintenance. |
| **Data Analysis** | Member 2 (Lead) | Exploratory Data Analysis (EDA) in Jupyter, SQL business query development (`sql/sales_analysis.sql`), sales/profit/regional trend identification. |
| **Data Visualization** | Member 3 (Lead) | Power BI data modeling, DAX KPI measure creation, interactive dashboard pages, visual styling, capturing screenshots, final presentation assets. |

---

## 2. GitHub Collaboration Setup

Since this project is hosted on a personal GitHub account, the repository owner must grant collaborator access to the other two members:

1. Go to repository on GitHub: `https://github.com/samoltylundy226/Sales_Dashboard_Analysis`
2. Navigate to **Settings** > **Collaborators** (under "Access").
3. Click **Add people**.
4. Enter each teammate's GitHub username or email address and click **Add to this repository**.
5. Each teammate will receive an email invitation or a notification on GitHub (at `https://github.com/samoltylundy226/Sales_Dashboard_Analysis/invitations`) and must click **Accept invitation**.
6. Once accepted, each teammate can clone the repository, create branches, and push directly using their own authenticated GitHub account.

---

## 3. Branching Strategy

To prevent merge conflicts and protect the production codebase:

- `main`: **Protected stable branch**. Production-ready code and finalized dashboard files only. No direct pushes to `main`.
- **Feature Branches**: Every task or user story must be developed in an isolated feature branch branched off the latest `main`.

### Branch Naming Conventions

Use lowercase with forward slashes and hyphens:

| Branch Type | Convention | Example |
| :--- | :--- | :--- |
| **Data Engineering** | `feature/data-cleaning` or `feature/data-*` | `feature/data-cleaning` |
| **Data Analysis** | `feature/sales-analysis` or `feature/sql-*` | `feature/sales-analysis` |
| **Power BI Dashboard**| `feature/powerbi-dashboard` or `feature/pbi-*` | `feature/powerbi-dashboard` |
| **Bug Fixes** | `fix/<description>` | `fix/null-handling-dates` |
| **Documentation** | `docs/<description>` | `docs/update-readme-milestones` |

---

## 4. Commit Message Guidelines

We follow the **Conventional Commits** standard to maintain a clear, auditable project history:

```text
<type>: <short summary in imperative mood>

[optional body explaining context or rationale]
```

### Allowed Types:
- `feat`: A new analytical query, cleaning function, or dashboard measure.
- `fix`: A bug fix in a script or SQL calculation.
- `docs`: Documentation changes only (README, comments, CONTRIBUTING).
- `chore`: Maintenance tasks, repo setup, dependency updates (`requirements.txt`).
- `refactor`: Code restructures that neither fix a bug nor add a feature.
- `test`: Adding or updating test cases in `tests/`.

### Examples:
- `chore: initialize sales dashboard project structure`
- `feat: add null handling and date standardization in clean_data.py`
- `feat: implement monthly MoM growth CTE in sales_analysis.sql`
- `docs: add setup instructions and team roster to README`

---

## 5. Step-by-Step Practical Git Workflow

Each team member should follow this lifecycle for every task:

### Step 1: Synchronize with `main` before starting
Always start from the latest version of the repository:
```bash
git checkout main
git pull origin main
```

### Step 2: Create and switch to your feature branch
```bash
# Member 1 (Data Engineering)
git checkout -b feature/data-cleaning

# Member 2 (Data Analysis)
git checkout -b feature/sales-analysis

# Member 3 (Data Visualization)
git checkout -b feature/powerbi-dashboard
```

### Step 3: Work in your assigned files and stage changes
Make small, focused modifications. Stage specific files rather than using blind wildcard additions:
```bash
# Check status of modified files
git status

# Stage specific files
git add src/clean_data.py
# or
git add sql/sales_analysis.sql
```

### Step 4: Commit your changes
```bash
git commit -m "feat: implement column standardization and duplicate removal"
```

### Step 5: Push your branch to GitHub
```bash
git push -u origin feature/data-cleaning
```

### Step 6: Open a Pull Request (PR)
1. Go to the repository on GitHub.
2. Click **Compare & pull request** next to your recently pushed branch.
3. Title the PR clearly (e.g., `feat: Add data cleaning pipeline and validation rules`).
4. In the PR description:
   - Summarize the changes made.
   - List what files were modified.
   - Confirm that local tests / validations passed.
5. Request a review from at least one teammate.

### Step 7: Code Review & Merging
- Reviewers inspect the diff, leave comments or approvals.
- Once approved, merge the PR into `main` using **Squash and merge** or **Create a merge commit**.
- Delete the remote feature branch after successful merge.
- Locally, switch back to `main` and pull:
  ```bash
  git checkout main
  git pull origin main
  ```

---

## 6. Avoiding Conflicts & Working with Power BI Files

1. **File Partitioning**: Member 1 primarily works in `src/`, Member 2 in `sql/` and `notebooks/`, and Member 3 in `powerbi/`. Minimizing concurrent edits to the same file prevents 95% of merge conflicts.
2. **Binary Power BI Files (`.pbix`)**: `.pbix` files are binary files that Git cannot easily diff. Member 3 should have primary ownership of the `.pbix` file. If another member needs to test it, pull the latest version first and never work on the `.pbix` simultaneously without coordinating.
3. **Data Files**: Never commit large raw data files to Git. Keep `data/raw/` in `.gitignore` and share data schemas or small sample files instead.
