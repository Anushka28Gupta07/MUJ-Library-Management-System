# library-management-system
RDBMS project for semester III
### 🖥️ Frontend Architecture & UI Overview

Built using Python and Streamlit, the frontend delivers a clean, responsive, and modular interface designed around role-based library workflows. 

#### Key Modules & Capabilities:
- **Authentication Portal (`login.py`):**
  - Custom branded landing screen with ambient radial vignette styling.
  - Tabbed interface supporting both **Librarian / Staff Sign In** and **New Member Registration**.
  - Direct session state management for route guarding and role persistence.

- **Theme & Design System (`styles.py`):**
  - Dynamic **Dark / Light mode** toggling accessible directly from the persistent sidebar.
  - Custom CSS injected for high-contrast input controls, frosted glass cards, and styled data tables.

- **Catalog & Inventory Management (`books.py`):**
  - Multi-tab layout for catalog browsing, book addition, metadata editing, and deletion guards.
  - **Lost & Damaged Registry:** Dedicated workflow to flag missing or damaged physical copies, record replacement fines, and automatically deduct active inventory counts.

- **Member Management (`members.py`):**
  - Reader roster view with membership status indicators and contact detail management.

- **Circulation Desk (`issue_return.py`):**
  - Distinct issue and return processing tabs enforcing active loan limits, calculated return dates, and fine assessments.

- **Search & Discovery (`search.py`):**
  - Multi-attribute catalog lookup across titles, authors, categories, and ISBNs.

- **Auditing & Master Records (`reports.py`, `master_data.py`, `dashboard.py`):**
  - KPI metric cards summarizing catalog size, active loans, and overdue counts.
  - Dedicated master data management for Authors, Publishers, and Categories.
