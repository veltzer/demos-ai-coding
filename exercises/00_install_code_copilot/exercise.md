# How to Set Up GitHub Copilot in VS Code

This guide will walk you through installing Visual Studio Code (on Windows or Linux) and connecting GitHub Copilot (either the Free or Pro trial version).

---

## 1. Install Visual Studio Code

First, you need the code editor.

* **Go to the official website:** [https://code.visualstudio.com/](https://code.visualstudio.com/)

* **For Windows:**
    * Download the **"Download for Windows"** installer (`.exe`).
    * Run the installer and follow the on-screen instructions. (The default settings are fine for most users).

* **For Linux:**
    * Download the appropriate package for your distribution:
        * `.deb` for Debian/Ubuntu-based distros.
        * `.rpm` for RHEL/Fedora/SUSE-based distros.
    * Alternatively, you can often install it using your system's package manager or the Snap Store (e.g., `sudo snap install code --classic`).
    * Follow the installation prompts for your specific method.

---

## 2. Get a GitHub Account

You **must** have a GitHub account to use Copilot.

* If you don't have one, go to [https://github.com/](https://github.com/) and sign up for a **free account**.

---

## 3. Activate Your Copilot Plan

Before the extension will work, you need to activate a Copilot plan on your GitHub account.

1. Go to the main Copilot page: [https://github.com/features/copilot](https://github.com/features/copilot)
1. Sign in with your GitHub account.
1. You will be presented with the available plans. Choose one:
    * **Copilot Free:** This plan is available for all individual users. It provides code completions but may have usage limits. Select this if you want the no-cost option.
    * **Copilot Pro (Free Trial):** This is the full-powered version. It offers a free trial (usually 30 days) to test all features, including chat, unlimited completions, and access to the latest models.
    * **Note:** You will likely need to enter payment information to start the Pro trial. Remember to cancel it before the trial ends if you don't want to be charged.

---

## 4. Install and Connect Copilot in VS Code

Now, let's link Copilot to your editor.

1. **Open VS Code.**
1. Go to the **Extensions** view on the left-hand side (or press `Ctrl+Shift+X`).
1. In the search bar, type `GitHub Copilot`.
1. You will see several results. You want the main one named **GitHub Copilot** (created by "GitHub").
1. Click the **Install** button.
1. After it installs, you'll see a notification in the bottom-right corner prompting you to sign in. Click **"Sign in to GitHub"**.
1. Your web browser will open. You will be asked to authorize VS Code to access your GitHub account.
1. Click **"Authorize Visual Studio Code"** and follow any remaining prompts.

---

## 5. Check if It's Working

You're all set! Here's how to quickly test it:

1. Open a new file in VS Code (e.g., `test.py` for Python or `test.js` for JavaScript).
1. Start typing a comment describing what you want to do.
       * **Example (JavaScript):** `// function that returns the sum of two numbers`
1. Wait a second. Copilot should show a "ghost text" suggestion for the entire function.
1. Press the **Tab** key to accept the suggestion.

If the code appears, you are officially working with Copilot! You can also click the Copilot icon in the bottom status bar to see its status.
