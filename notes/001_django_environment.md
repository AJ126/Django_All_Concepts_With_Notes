# Django Virtual Environment – Complete Notes

A **virtual environment** is an isolated Python environment that allows you to install and manage packages separately for each project.

For example, one Django project can use Django 4.2 while another uses a different compatible version.

## 1. Create a Virtual Environment

### Command

```bash
python -m venv akash
```

**Explanation:**
- `python -m venv` creates a virtual environment.
- `akash` is the name of the virtual environment. You can use any name.

Example folder structure:

```text
DjangoProject/
├── akash/
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   └── pyvenv.cfg
```

## 2. Activate the Virtual Environment

On Windows, open Command Prompt or PowerShell in your project directory.

### Command Prompt (CMD)

```bat
akash\Scripts\activate.bat
```

### PowerShell

```powershell
.\akash\Scripts\Activate.ps1
```

After activation, the environment name usually appears at the beginning of your terminal prompt:

```text
(akash) C:\Projects\DjangoProject>
```

**Note:** You do not need to enter the `Scripts` folder first. You can activate the environment directly from the project directory using the commands above.

If you are already inside the `akash\Scripts` directory, you can run:

```bat
activate.bat
```

## 3. Deactivate the Virtual Environment

To deactivate the currently active environment, run:

```bash
deactivate
```

This works in both Command Prompt and PowerShell.

Your terminal prompt will return to its normal state.

**Note:** You do not need to navigate back to the environment folder to deactivate it.

## 4. Install Django

First, activate your virtual environment.

Then run:

```bash
python -m pip install django
```

To install a specific version:

```bash
python -m pip install django==4.1
```

Packages installed while the