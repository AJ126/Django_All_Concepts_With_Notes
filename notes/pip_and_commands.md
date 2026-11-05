# Python PIP and Package Management

## 1. What is PIP?

**PIP (Preferred Installer Program)** is a package manager for Python. It is used to install, upgrade, uninstall, and manage Python packages and libraries.

For example, we can use PIP to install Django, Django REST Framework, Pillow, and other Python packages.

## 2. What is a Package?

A **package** is a collection of Python modules organized together to provide reusable functionality.

- **Module:** A Python file containing functions, classes, and variables that can be reused in other Python programs.
- **Package:** A collection of related Python modules organized in a directory.

For example:
- Django is a Python web framework distributed as a package.
- Pillow is a Python imaging library.
- Django REST Framework is a toolkit for building Web APIs.

## 3. Check Whether PIP Is Installed

First, open Command Prompt or the VS Code terminal.

Run the following command:

```bash
pip --version
```

Alternatively:

```bash
python -m pip --version
```

If PIP is installed, it displays its version and installation location.

**Note:** You do not need to navigate to the Python installation's `Scripts` folder if Python and PIP are correctly added to your system PATH.

## 4. PIP Commands

### 4.1 Check PIP Version

```bash
pip --version
```

### 4.2 Upgrade PIP

```bash
python -m pip install --upgrade pip
```

Alternatively:

```bash
pip install --upgrade pip
```

### 4.3 Install a Package

Syntax:

```bash
pip install package_name
```

Example:

```bash
pip install django
```

### 4.4 Upgrade an Installed Package

Syntax:

```bash
pip install --upgrade package_name
```

Example:

```bash
pip install --upgrade django
```

To install a specific version:

```bash
pip install django==4.2.0
```

**Note:** Replace `4.2.0` with the version you want to install.

### 4.5 Uninstall a Package

Syntax:

```bash
pip uninstall package_name
```

Example:

```bash
pip uninstall django
```

### 4.6 List Installed Packages

```bash
pip list
```

This command displays all installed Python packages and their versions.

### 4.7 Check Package Information

Syntax:

```bash
pip show package_name
```

Example:

```bash
pip show django
```

It displays information such as:
- Package name
- Version
- Summary
- Installation location
- Dependencies

### 4.8 Check All Installed Package Versions

```bash
pip freeze
```

This command displays installed packages in a format suitable for a requirements file.

Example output:

```text
Django==4.2.0
Pillow==10.0.0
djangorestframework==3.14.0
```

To save installed packages into a file:

```bash
pip freeze > requirements.txt
```

To install packages from that file:

```bash
pip install -r requirements.txt
```

## 5. Create a Python Virtual Environment

A **virtual environment** is an isolated Python environment that allows us to install and manage packages separately for each project.

For example, one Django project can use Django 4.2, while another project can use a different Django version.

### 5.1 Create a Virtual Environment

Syntax:

```bash
python -m venv environment_name
```

Example:

```bash
python -m venv Akash
```

This creates a virtual environment named `Akash`.

### 5.2 Activate the Virtual Environment (Windows)

```bash
Akash\Scripts\activate
```

After activation, the terminal displays the environment name:

```text
(Akash) D:\Projects\Python>
```

### 5.3 Deactivate the Virtual Environment

```bash
deactivate
```

## 6. Install and Manage Django Packages

### 6.1 Upgrade PIP

```bash
python -m pip install --upgrade pip
```

### 6.2 Install Django

```bash
pip install django
```

### 6.3 Upgrade Django

```bash
pip install --upgrade django
```

### 6.4 Install a Specific Django Version

```bash
pip install django==4.2.0
```

### 6.5 Check Django Version

```bash
python -m django --version
```

## 7. Important Python and Django Packages

### 7.1 Django

**Purpose:** Django is a Python web framework used to develop web applications.

Installation:

```bash
pip install django
```

### 7.2 Django REST Framework (DRF)

**Purpose:** Django REST Framework is used to build RESTful Web APIs using Django.

Installation:

```bash
pip install -U djangorestframework
```

### 7.3 Django Filter

**Purpose:** `django-filter` provides filtering functionality for Django applications and Django REST Framework APIs.

Installation:

```bash
pip install -U django-filter
```

### 7.4 Pillow

**Purpose:** Pillow is a Python imaging library used to handle and process image files.

It is commonly used in Django projects to manage uploaded images and image processing.

Installation:

```bash
pip install -U Pillow
```

### 7.5 Django HIDP Django Admin

**Purpose:** Provides a customized or themed appearance for the Django admin panel.

Installation:

```bash
pip install -U django-hidp-django-admin
```

## 8. Difference Between PIP Commands

| Command | Purpose |
|---|---|
| `pip --version` | Check PIP version |
| `pip install django` | Install Django |
| `pip install --upgrade django` | Upgrade Django |
| `pip uninstall django` | Uninstall Django |
| `pip list` | List installed packages |
| `pip freeze` | List packages with exact versions |
| `pip show django` | Display Django package information |
| `pip check` | Check installed package dependency compatibility |

## 9. Important Notes

1. PIP is used to manage Python packages.
2. Always activate the appropriate virtual environment before installing project-specific packages.
3. Different projects can use different package versions through virtual environments.
4. Use `pip freeze > requirements.txt` to save project dependencies.
5. Use `pip install -r requirements.txt` to install all dependencies from a requirements file.
6. Prefer `python -m pip` when you want to ensure that PIP belongs to the Python interpreter currently being used.

