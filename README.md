# pet-finder-python

This tiny script is for polling available pets to rehome from Scottish SPCA:

https://www.scottishspca.org/rehome/rehome

It runs every 5 minutes, checks for the list of pets and emails you the list if there is a change (addition or removal too)


Example usage:

```python
python3 pet_finder.py -s <>@gmail.com -p <> -r <>@gmail.com -u https://www.scottishspca.org/rehome/rehome-find-a-pet<>
```

Example usage with start script (edit start script first to add your params):

```bash
./start.sh
```