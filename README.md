# MoodBee 🐝

## Minimalistic mood tracking website. 

Moodbee is a simplistic site for tracking your mood and seeing how external factors may affect it.

Visit the website: www.moodbee.net

### Features
* Track your mood anytime, anyday.
* Timeline representation and progression of how your mood changed.
* Mood correlation with local weather.


![moodbee](/static/Moodbee_Logo_2-02.png)

Images and Logos designed by [Adrian Ortiz](https://www.linkedin.com/in/adrian-ortiz-a00a75235/)

## Contributing
### Running MoodBee Locally
Running MoodBee requires that [Python3](https://www.python.org/downloads/) is installed.
You must also be running a Unix shell.
If running Windows, [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) provides such a shell, including [through Visual Studio Code](https://code.visualstudio.com/docs/remote/wsl).

1. Set the current directory to the root of this repository
2. Execute the `install` script to install all dependencies in a virtual environment:
    ```bash
    bash ./install
    ```
3. Execute the `run` script to run the application:
    ```bash
    bash ./run
    ```
Please see the `install` and `run` scripts for details.

### Modifying Dependencies
All changes to the dependencies list must be reflected in `requirements.txt`.
The [`pipreqs`](https://pypi.org/project/pipreqs/) utility allows for a new dependencies list to be generated automatically, but changes must still be manually reviewed.
