# iFunny Account Creator

Generate iFunny accounts without any restrictions! This python script will infinitely loop through the account making process and store all the information in a neatly formed JSON file.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites


* [Python](https://www.python.org/downloads/) 3.8 or above


### Installing Requirements

Open a cmd prompt and change the directory to the project folder

```
cd C:/Path/To/Your/Project
```

Then run the following command:

```
pip install -r requirements.txt
```

Now you should have the modules needed to run this script.

## Running the script

Edit the script in an IDE, we will need to fill in some needed information. First, input an email base - This will be first half of an email address. It doesn't need to lead to a real email address, iFunny does not have email verification. Then input the username base you would like to use, followed by the password you want to use. Now all that's left is to run the script.

Running the script is straightforward. After starting, you will see updates in the terminal. For the most part its all automatic, the only manual part is solvng the captchas. If you create too many accounts from one IP you will get ratelimited. To avoid you may need to use a VPN or just wait for the ratelimit to expire (~10 mins) 

## Built With

* [Requests](https://github.com/psf/requests) - The web framework used
* [Webbrowser](https://github.com/python/cpython/blob/main/Lib/webbrowser.py) - For displaying captcha URLs


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

