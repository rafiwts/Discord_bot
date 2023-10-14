# Discord Bot
Discord bot helps users to receive vital information after sending an appropriate command. It is also connected with chatgpt so that user can have a direct access to this tool. It is possible for a chat to be expanded depening on requirements and needs. Please visit this [link](https://discord.com/developers/docs/intro) to learn more about the bot on a discord platform.

## Instalation
- after cloning the project, create a Python virtual environment with poetry and activate it:
```shell
poetry init
```
Note that the command may vary depending on an operating system. For more details concerning creating a virtual environment visit this [documentation](https://python-poetry.org/docs/#installation).
- activate the environment within your local directory:
```shell
poetry shell
```
- install all Python libraries that the project depends on using the following command:
```shell
pip install
```
- run the docker container with the command (the command may vary depending on the operating system you use):
```shell
docker compose up
```
- in order for the project to comply with all coding standards, make sure that you use `pre-commit`. Execute the following commands:
```shell
pre-commit install
```
By using this command, you make sure that the style of the code will be checked before commiting any changes to the repository.

- following command runs the project (note that the command may vary depending on the operating system you use):
```shell
python3 main.py
```
