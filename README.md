## Name Entity Recognition Model


NER for short is a model that helps to pick the time and date in a text. It is one of the CoreNLP libraries. 
It was originally built in Java, but they created a python wrapper for it, hence the Java dependencies.

Click [here](https://github.com/FraBle/python-sutime) to read about SUTime python wrapper



### Follow this guide to set up your system before using this repo.

Set up the environment
> python -m venv ner_env
> source .ner_env/bin/activate

Installing other dependencies
> pip install -r Requirements.txt
> pip install sutime

Then run this in the same directory as the file.
> 
```python
mvn dependency:copy-dependencies -DoutputDirectory=./jars -f $(python3 -c 'import importlib; import pathlib; print(pathlib.Path(importlib.util.find_spec("sutime").origin).parent / "pom.xml")') 
```
<details><summary>You can ignore this but incase the above set doesnt work </summary>
<p>Firstly, install java jdk on your system,  from [here](https://www.oracle.com/java/technologies/downloads/)
install mvn - not sure you might need this if windows
</details>

<br>
<br>


Run the below command to test. 
```python
python NER.py
```
